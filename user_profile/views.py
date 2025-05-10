from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


class UserRegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyEmailView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            raise ValidationError({"detail": "Token is required."})

        try:
            user = User.objects.get(email_token=token)
            user.is_verified = True
            user.save()
            return Response({"detail": "Email verified successfully."})
        except User.DoesNotExist:
            raise ValidationError({"detail": "Invalid token."})