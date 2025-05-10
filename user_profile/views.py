from tokenize import TokenError

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer


class UserRegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.generate_email_token()

        return user


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            raise ValidationError({"detail": "Token is required."})

        try:
            user = User.objects.get(email_token=token)
            if user.is_verified:
                raise ValidationError({"detail": "Email already verified."})
            user.is_verified = True
            user.email_token = None
            user.save()

            return Response({"detail": "Email verified successfully."})
        except User.DoesNotExist:
            raise ValidationError({"detail": "Invalid token."})



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


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.get(email=email)
        user.generate_email_token()


        return Response({"detail": "Ссылка для сброса пароля отправлена на почту."})

