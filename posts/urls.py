from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, PostLikeView, PostUnlikeView


urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='like_post'),
    path('posts/<int:pk>/unlike/', PostUnlikeView.as_view(), name='post-unlike'),
]