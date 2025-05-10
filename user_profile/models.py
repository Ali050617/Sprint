from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User')
    ]

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    email_token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_email_token(self):
        self.email_token = get_random_string(length=32)
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(max_length=400)
    image = models.ImageField(upload_to='users-photos/')
    followers_count = models.PositiveIntegerField()
    following_count = models.PositiveIntegerField()

    def __str__(self):
        return f'Профиль пользователя {self.user.email}'

