from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


class UserRegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
