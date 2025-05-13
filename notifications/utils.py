from .models import Notification


def create_notification(recipient, actor=None, verb=None, target_type=None, target_id=None):
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_type=target_type,
        target_id=target_id
    )


def get_unread_notification_count(user):
    return Notification.objects.filter(recipient=user, is_read=False).count()