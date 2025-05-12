from rest_framework import serializers
from user_profile.serializers import UserDataSerializer
from comments.models import Comment
from posts.serializers import PostSerializer


class SearchCommentSerializer(serializers.ModelSerializer):
    author = UserDataSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at',
                  'updated_at', 'is_active', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()