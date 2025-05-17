from rest_framework import serializers
from posts.models import Post
from user_profile.serializers import UserDataSerializer
from .models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_verified = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff',
                  'date_joined', 'is_verified', 'role']
        ref_name = "CommentUserSerializer"

    def get_is_verified(self, obj):
        return True

    def get_role(self, obj):
        return 'admin' if obj.is_staff else 'user'


class PostSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at',
                  'updated_at', 'is_active', 'likes_count', 'comments_count', ]
        ref_name = "CommentPostSerializer"

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at',
                  'updated_at', 'is_active', 'likes_count']
        read_only_fields = ['author', 'post', 'created_at', 'updated_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at']


class CommentUnlikeSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

