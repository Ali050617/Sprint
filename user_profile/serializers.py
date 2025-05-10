from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from .models import User


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
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)

        user.set_password(password)
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        token['is_verified'] = user.is_verified
        token['date_joined'] = user.date_joined
        token['role'] = user.role

        return token

