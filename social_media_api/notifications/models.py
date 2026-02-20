# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Notification(models.Model):
    """
    Notification model for tracking user interactions
    Uses GenericForeignKey to link to different types of objects (posts, comments, etc.)
    """
    # Types of notifications
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    verb = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES
    )
    
    # For GenericForeignKey to target object (post, comment, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    target = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.verb} for {self.recipient.username}"