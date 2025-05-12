from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from posts.models import Post
from comments.models import Comment
from user_profile.models import UserProfile
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from user_profile.serializers import UserProfileSerializer
from .paginations import SearchPagination
import logging

logger = logging.getLogger(__name__)

class SearchView(APIView):
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
            posts = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                is_active=True
            )
            logger.info(f"Found {posts.count()} posts for query '{query}'")

            post_paginator = SearchPagination()
            paginated_posts = post_paginator.paginate_queryset(posts, request)
            post_serializer = PostSerializer(paginated_posts, many=True)

            response_data['posts'] = {
                "count": post_paginator.page.paginator.count,
                "next": post_paginator.get_next_link(),
                "previous": post_paginator.get_previous_link(),
                "results": post_serializer.data
            }

        # Search comments
        if search_type in ['comment', 'all']:
            comments = Comment.objects.filter(
                Q(content__icontains=query) |
                Q(post__title__icontains=query) |
                Q(author__username__icontains=query),
                is_active=True
            )
            logger.info(f"Found {comments.count()} comments for query '{query}'")

            comment_paginator = SearchPagination()
            paginated_comments = comment_paginator.paginate_queryset(comments, request)
            comment_serializer = CommentSerializer(paginated_comments, many=True)

            response_data['comments'] = {
                "count": comment_paginator.page.paginator.count,
                "next": comment_paginator.get_next_link(),
                "previous": comment_paginator.get_previous_link(),
                "results": comment_serializer.data
            }

        # Search users
        if search_type in ['user', 'all']:
            user_profiles = UserProfile.objects.filter(
                Q(user__username__icontains=query) |
                Q(bio__icontains=query) |
                Q(user__email__icontains=query)
            )
            logger.info(f"Found {user_profiles.count()} users for query '{query}'")

            user_paginator = SearchPagination()
            paginated_users = user_paginator.paginate_queryset(user_profiles, request)
            user_serializer = UserProfileSerializer(paginated_users, many=True)

            response_data['users'] = {
                "count": user_paginator.page.paginator.count,
                "next": user_paginator.get_next_link(),
                "previous": user_paginator.get_previous_link(),
                "results": user_serializer.data
            }

        return Response(response_data, status=status.HTTP_200_OK)