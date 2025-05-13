from tokenize import TokenError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, UserProfile
from .paginations import FollowersListPagination, FollowingListPagination
from .tokens import send_password_reset_email, reset_password_confirm
from .utils import reset_password_confirm
from .serializers import (
    RegisterSerializer,
    RefreshTokenSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    UserDataSerializer,
    UserProfileSerializer, VerifyEmailSerializer,

)


# REGISTER
class UserRegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# VERIFY EMAIL
class EmailVerificationView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Email успешно подтвержден."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN
class UserLoginView(TokenObtainPairView):
    serializer_class = RefreshTokenSerializer


# LOGOUT
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
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
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=serializer.validated_data['email'])
        send_password_reset_email(user)
        return Response({"detail": "Токен для сброса пароля отправлен на электронную почту."}, status=status.HTTP_200_OK)


# RESET PASSWORD CONFIRM
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = reset_password_confirm(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
