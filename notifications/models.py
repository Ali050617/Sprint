from django.db import models
from django.conf import settings


class Notification(models.Model):
    TARGET_TYPE_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('profile', 'Profile'),
    ]

    VERB_CHOICES = [
        ('liked', 'Liked'),
        ('commented', 'Commented'),
        ('followed', 'Followed'),
        ('mentioned', 'Mentioned'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_created',
        null=True,
        blank=True
    )

    verb = models.CharField(max_length=50, choices=VERB_CHOICES)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.PositiveIntegerField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
        ]

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target_type} to {self.recipient}"