from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import (
    NotificationSerializer,
    MarkNotificationReadSerializer,
    MarkAllNotificationsReadSerializer
)
from .paginations import NotificationPagination

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)

        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)

        return queryset


class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        notification = get_object_or_404(Notification, id=id)

        if notification.recipient != user:
            return Response(
                {"detail": "You are not authorized to mark this notification as read", "code": "403"},
                status=status.HTTP_403_FORBIDDEN
            )

        notification.is_read = True
        notification.save()

        serializer = MarkNotificationReadSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAllNotificationsAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)

        serializer = MarkAllNotificationsReadSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)