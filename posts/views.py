from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from .models import Post, PostLike
from .serializers import PostSerializer, PostLikeSerializer, PostUnlikeSerializer


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


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Пост не найден.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if PostLike.objects.filter(post=post, user=user).exists():
            return Response({'detail': 'Вы уже поставили лайк.'}, status=status.HTTP_400_BAD_REQUEST)

        like = PostLike.objects.create(post=post, user=user)

        post.likes.add(user)
        post.likes_count = post.likes.count()
        post.save()

        serializer = PostLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostUnlikeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUnlikeSerializer

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            error_data = {
                "detail": "Post not found",
                "code": "404"
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            post_like = PostLike.objects.get(post=post, user=user)
        except PostLike.DoesNotExist:
            error_data = {
                "detail": "Not liked yet",
                "code": "400"
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        post_like.delete()
        post.likes_count = post.likes.count()  # обновляем количество лайков
        post.save()

        return Response({
            "detail": "Successfully unliked",
            "code": "200"
        }, status=status.HTTP_200_OK)