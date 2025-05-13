from tokenize import TokenError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, UserProfile
from .paginations import FollowersListPagination, FollowingListPagination
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    UserDataSerializer,
    UserProfileSerializer,

)


# REGISTER
class UserRegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# VERIFY EMAIL
pass

# LOGIN
class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# LOGOUT
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(        # send_email(user.email, user.email_token)
{
                'detail': "Refresh token is required"
            }, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({
                'detail': "Invalid token"
            }, status=401)

        return Response(status=204)

# RESET PASSWORD
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.get(email=email)
        user.generate_email_token()

        return Response({"detail": "Ссылка для сброса пароля отправлена на почту."})


# CONFIRM RESET PASSWORD
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email_token=token)
        except User.DoesNotExist:
            raise ValidationError({"detail": "Неверный токен."})

        user.set_password(password)
        user.email_token = None
        user.save()

        return Response({"detail": "Пароль успешно изменён."})


# USER
class UserDataView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user


# USER PROFILE
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserProfile, user=user)


# USER DETAIL
class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


# FOLLOWERS
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        if request.user.username == username:
            return Response({"detail": "Нельзя подписаться на самого себя."}, status=400)

        target_user = get_object_or_404(User, username=username)
        target_profile = get_object_or_404(UserProfile, user=target_user)
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if target_profile in user_profile.following.all():
            return Response({"detail": "Вы уже подписаны на этого пользователя."}, status=400)

        user_profile.following.add(target_profile)
        return Response(UserProfileSerializer(target_profile).data)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        if request.user.username == username:
            return Response({"detail": "Нельзя отписаться от самого себя."}, status=400)

        target_user = get_object_or_404(User, username=username)
        target_profile = get_object_or_404(UserProfile, user=target_user)
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if target_profile not in user_profile.following.all():
            return Response({"detail": "Вы не подписаны на этого пользователя."}, status=400)

        user_profile.following.remove(target_profile)
        return Response(UserProfileSerializer(target_profile).data)


class FollowersListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FollowersListPagination

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        return profile.followers.all()


class FollowingListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FollowingListPagination

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        return profile.following.all()
