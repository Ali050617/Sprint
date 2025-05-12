from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer, PostLikeSerializer, PostUnlikeSerializer
from notifications.utils import create_notification


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response({"detail": "Post not found", "code": "404"}, status=status.HTTP_404_NOT_FOUND)
        post.likes_count += 1
        post.save()

        # Create notification for post like
        if post.author != request.user:
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_type='post',
                target_id=post.id
            )

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUnlikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUnlikeSerializer
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