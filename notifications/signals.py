import re
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from user_profile.models import User, UserProfile
from .models import Notification

User = get_user_model()

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.author,
            verb='commented',
            target_type='post',
            target_id=instance.post.id
        )

@receiver(post_save, sender=Comment)
def create_mention_notification(sender, instance, created, **kwargs):
    if created:
        # Find all @username mentions in the comment content
        mentions = re.findall(r'@(\w+)', instance.content)
        for username in mentions:
            try:
                mentioned_user = User.objects.get(username=username)
                if mentioned_user != instance.author and mentioned_user != instance.post.author:
                    Notification.objects.create(
                        recipient=mentioned_user,
                        actor=instance.author,
                        verb='mentioned',
                        target_type='comment',
                        target_id=instance.id
                    )
            except User.DoesNotExist:
                continue  # Skip invalid usernames

@receiver(m2m_changed, sender=Comment.likes.through)
def create_comment_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and pk_set:
        user_id = list(pk_set)[0]
        user = User.objects.get(id=user_id)

        if instance.author != user:
            Notification.objects.create(
                recipient=instance.author,
                actor=user,
                verb='liked',
                target_type='comment',
                target_id=instance.id
            )

@receiver(m2m_changed, sender=UserProfile.followers.through)
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and pk_set:
        for profile_id in pk_set:
            follower_profile = UserProfile.objects.get(id=profile_id)
            Notification.objects.create(
                recipient=instance.user,
                actor=follower_profile.user,
                verb='followed',
                target_type='profile',
                target_id=instance.id
            )