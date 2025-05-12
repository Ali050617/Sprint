from rest_framework import serializers
from user_profile.serializers import UserDataSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserDataSerializer(read_only=True)
    actor = UserDataSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'is_read', 'created_at'
        ]
        read_only_fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'created_at'
        ]


class MarkNotificationReadSerializer(serializers.ModelSerializer):
    recipient = UserDataSerializer(read_only=True)
    actor = UserDataSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'is_read', 'created_at'
        ]
        read_only_fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'created_at'
        ]


class MarkAllNotificationsReadSerializer(serializers.Serializer):
    detail = serializers.CharField(default="All notifications marked as read")\

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'is_read', 'created_at'
        ]
        read_only_fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'created_at'
        ]