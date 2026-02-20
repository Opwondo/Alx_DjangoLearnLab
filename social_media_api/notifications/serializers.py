# notifications/serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from posts.models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    actor_username = serializers.ReadOnlyField(source='actor.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    target_type = serializers.SerializerMethodField()
    target_summary = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username', 'actor', 'actor_username',
            'verb', 'target_type', 'target_summary', 'created_at', 'is_read'
        ]
        read_only_fields = ['id', 'created_at']

    def get_target_type(self, obj):
        """
        Get the type of the target object (post, comment, etc.)
        """
        if obj.target:
            return obj.target.__class__.__name__.lower()
        return None

    def get_target_summary(self, obj):
        """
        Get a summary of the target object
        """
        if obj.target:
            if isinstance(obj.target, Post):
                return obj.target.title[:50]
            elif isinstance(obj.target, Comment):
                return obj.target.content[:50]
        return None

class NotificationMarkReadSerializer(serializers.Serializer):
    """
    Serializer for marking notifications as read
    """
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    mark_all = serializers.BooleanField(default=False)

    def validate(self, data):
        if not data.get('mark_all') and not data.get('notification_ids'):
            raise serializers.ValidationError(
                "Either provide notification_ids or set mark_all=True"
            )
        return data