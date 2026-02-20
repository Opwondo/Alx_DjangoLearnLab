# notifications/urls.py
from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationUnreadCountView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('mark-read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('unread-count/', NotificationUnreadCountView.as_view(), name='notification-unread-count'),
]