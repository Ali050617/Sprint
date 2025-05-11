from django.urls import path
from .views import (PostCommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView,
    CommentLikeView, CommentUnlikeView,)

urlpatterns = [
    path('posts/<int:post_id>/comments/', PostCommentListCreateAPIView.as_view()),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('comments/<int:pk>/like/', CommentLikeView.as_view()),
    path('comments/<int:pk>/unlike/', CommentUnlikeView.as_view()),
]
