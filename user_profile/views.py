from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer


class RegisterViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
