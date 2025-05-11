from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer, CommentUnlikeSerializer, CommentLikeSerializer


class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, is_active=True)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentLikeSerializer

    def post(self, request, *args, **kwargs):
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post.likes_count += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentUnlikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentUnlikeSerializer
    def post(self, request, pk):
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            error_data = {
                "detail": "Post not found",
                "code": "404"
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        if post.likes_count > 0:
            post.likes_count -= 1
            post.save()
            return Response({"detail": "Successfully unliked", "code": "200"}, status=status.HTTP_200_OK)
        else:
            error_data = {
                "detail": "Likes count is already 0",
                "code": "400"
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)