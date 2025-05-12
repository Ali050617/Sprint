from django.urls import path
from .views import (
    NotificationListView,
    MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView
)

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:id>/mark-as-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-as-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
]