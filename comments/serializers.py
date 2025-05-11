from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post
from .models import Comment

class UserSerializer(serializers.ModelSerializer):
    is_verified = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff',
                  'date_joined', 'is_verified', 'role']

    def get_is_verified(self, obj):
        return True

    def get_role(self, obj):
        return 'admin' if obj.is_staff else 'user'


class PostAuthorSerializer(UserSerializer):
    pass

class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at',
                  'updated_at', 'is_active', 'likes_count', 'comments_count']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at',
                  'updated_at', 'is_active', 'likes_count']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='author', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'created_at']


class CommentUnlikeSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()