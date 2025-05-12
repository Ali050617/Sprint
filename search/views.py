from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from posts.models import Post
from comments.models import Comment
from user_profile.models import UserProfile
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer, SearchCommentSerializer
from user_profile.serializers import UserProfileSerializer
from .paginations import SearchPagination
import logging

logger = logging.getLogger(__name__)

class SearchView(generics.GenericAPIView):
    pagination_class = SearchPagination

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        search_type = request.query_params.get('type', 'all').lower()

        if not query:
            return Response({
                "posts": {"count": 0, "next": None, "previous": None, "results": []},
                "comments": {"count": 0, "next": None, "previous": None, "results": []},
                "users": {"count": 0, "next": None, "previous": None, "results": []}
            }, status=status.HTTP_200_OK)

        valid_types = ['post', 'comment', 'user', 'all']
        if search_type not in valid_types:
            search_type = 'all'

        response_data = {
            "posts": {"count": 0, "next": None, "previous": None, "results": []},
            "comments": {"count": 0, "next": None, "previous": None, "results": []},
            "users": {"count": 0, "next": None, "previous": None, "results": []}
        }

        # Search posts
        if search_type in ['post', 'all']:
            posts_queryset = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                is_active=True
            )
            posts_paginator = self.pagination_class()
            posts_page = posts_paginator.paginate_queryset(posts_queryset, request)
            posts_serializer = PostSerializer(posts_page, many=True)
            response_data["posts"] = {
                "count": posts_paginator.page.paginator.count,
                "next": posts_paginator.get_next_link(),
                "previous": posts_paginator.get_previous_link(),
                "results": posts_serializer.data
            }
            logger.info(f"Found {posts_queryset.count()} posts for query '{query}'")

        # Search comments
        if search_type in ['comment', 'all']:
            comments_queryset = Comment.objects.filter(
                Q(content__icontains=query) | Q(post__title__icontains=query) | Q(author__username__icontains=query),
                is_active=True
            ).select_related('post', 'author')
            comments_paginator = self.pagination_class()
            comments_page = comments_paginator.paginate_queryset(comments_queryset, request)
            # Use simplified comment serializer for search
            comments_serializer = SearchCommentSerializer(comments_page, many=True)
            response_data["comments"] = {
                "count": comments_paginator.page.paginator.count,
                "next": comments_paginator.get_next_link(),
                "previous": comments_paginator.get_previous_link(),
                "results": comments_serializer.data
            }
            logger.info(f"Found {comments_queryset.count()} comments for query '{query}'")

        # Search users
        if search_type in ['user', 'all']:
            users_queryset = UserProfile.objects.filter(
                Q(user__username__icontains=query) | Q(bio__icontains=query) | Q(user__email__icontains=query)
            ).select_related('user')
            users_paginator = self.pagination_class()
            users_page = users_paginator.paginate_queryset(users_queryset, request)
            users_serializer = UserProfileSerializer(users_page, many=True)
            response_data["users"] = {
                "count": users_paginator.page.paginator.count,
                "next": users_paginator.get_next_link(),
                "previous": users_paginator.get_previous_link(),
                "results": users_serializer.data
            }
            logger.info(f"Found {users_queryset.count()} users for query '{query}'")

        return Response(response_data, status=status.HTTP_200_OK)