from rest_framework import serializers
from comments.models import Comment
from posts.models import Post
from user_profile.serializers import UserDataSerializer

class MidSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at',
                  'updated_at', 'is_active', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class SearchCommentSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    post = MidSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at',
                  'updated_at', 'is_active', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()