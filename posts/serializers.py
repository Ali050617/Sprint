from rest_framework import serializers
from django.contrib.auth.models import User

from user_profile.serializers import UserDataSerializer
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff',
                  'is_verified', 'date_joined', 'role']

    def get_role(self, obj):
        if obj.is_superuser:
            return "admin"
        elif obj.is_staff:
            return "staff"
        return "user"

    def get_is_verified(self, obj):
        return hasattr(obj, 'profile') and obj.profile.is_verified


class PostSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at',
                  'updated_at', 'is_active', 'likes_count', 'comments_count']
        read_only_fields = ['author', 'created_at', 'updated_at',
                            'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='author', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'created_at']

class PostUnlikeSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()












