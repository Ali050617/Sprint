from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UserProfile
from django.contrib.auth.tokens import default_token_generator


# REGISTER
class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user


# VERIFY-EMAIL
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        token = attrs.get('token')
        try:
            user = User.objects.get(email_token=token)
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "Недействительный или просроченный токен."})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_verified = True
        user.is_active = True
        user.email_token = None
        user.save()
        return user


# REFRESH-TOKEN
class RefreshTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "is_active": self.user.is_active,
            "is_staff": self.user.is_staff,
            "is_verified": self.user.is_verified,
            "date_joined": self.user.date_joined.isoformat(),
            "role": self.user.role,
        }

        response_data = {
            "access": data['access'],
            "refresh": data['refresh'],
            "user": user_data
        }
        return response_data


# PASSWORD-RESET
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value


# PASSWORD-RESET-CONFIRM
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, attrs):
        self._validate_password(attrs)
        self._validate_token(attrs['token'])
        return attrs

    def _validate_password(self, attrs):
        password, password_confirm = attrs['password'], attrs['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError("Пароль и подтверждение пароля не совпадают.")

        if len(password) < 8 or not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Пароль должен быть не менее 8 символов и содержать хотя бы одну букву.")

    def _validate_token(self, token):
        user = self._get_user_by_token(token)
        if not user:
            raise serializers.ValidationError("Токен недействителен или истёк срок его действия.")

    def _get_user_by_token(self, token):
        for user in User.objects.all():
            if default_token_generator.check_token(user, token):
                return user
        return None


# USER DATA
class UserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField(read_only=True)


# USER PROFILE
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'bio',
            'image',
            'followers_count',
            'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()