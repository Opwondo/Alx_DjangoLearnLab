# notifications/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer, NotificationMarkReadSerializer

class NotificationListView(generics.ListAPIView):
    """
    View to list notifications for the current user
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get query parameters for filtering
        show_read = self.request.query_params.get('show_read', 'false').lower() == 'true'
        notification_type = self.request.query_params.get('type', None)
        
        queryset = Notification.objects.filter(recipient=user)
        
        if not show_read:
            queryset = queryset.filter(is_read=False)
        
        if notification_type:
            queryset = queryset.filter(verb=notification_type)
        
        return queryset

class NotificationMarkReadView(generics.GenericAPIView):
    """
    View to mark notifications as read
    """
    serializer_class = NotificationMarkReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if serializer.validated_data.get('mark_all'):
            # Mark all notifications as read
            updated = Notification.objects.filter(
                recipient=user, is_read=False
            ).update(is_read=True)
            return Response({
                'message': f'Marked {updated} notifications as read'
            })
        
        else:
            # Mark specific notifications as read
            notification_ids = serializer.validated_data.get('notification_ids', [])
            updated = Notification.objects.filter(
                id__in=notification_ids, recipient=user
            ).update(is_read=True)
            return Response({
                'message': f'Marked {updated} notifications as read'
            })

class NotificationUnreadCountView(generics.GenericAPIView):
    """
    View to get unread notification count
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        return Response({'unread_count': count})