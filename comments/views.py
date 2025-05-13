from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer, CommentUnlikeSerializer, CommentLikeSerializer
from notifications.utils import create_notification

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
    queryset = Comment.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found", "code": "404"}, status=status.HTTP_404_NOT_FOUND)
        if request.user in comment.likes.all():
            return Response({"detail": "You already liked this comment", "code": "400"},
                            status=status.HTTP_400_BAD_REQUEST)
        comment.likes.add(request.user)
        comment.likes_count = comment.likes.count()
        comment.save()

        if comment.author != request.user:
            create_notification(
                recipient=comment.author,
                actor=request.user,
                verb='liked',
                target_type='comment',
                target_id=comment.id
            )
        serializer = CommentLikeSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentUnlikeView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUnlikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found", "code": "404"}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in comment.likes.all():
            return Response({
                "detail": "You haven't liked this comment yet",
                "code": "400"
            }, status=status.HTTP_400_BAD_REQUEST)

        comment.likes.remove(request.user)
        comment.likes_count = comment.likes.count()
        comment.save()

        return Response({"detail": "Successfully unliked", "code": "200"}, status=status.HTTP_200_OK)

