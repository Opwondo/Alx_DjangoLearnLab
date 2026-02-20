# posts/urls.py - Add feed URL
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# The router will automatically generate URLs for our viewsets
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),  # Add feed endpoint

    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
    path('<int:pk>/likes/', PostViewSet.as_view({'get': 'likes_list'}), name='post-likes'),
    path('feed/', FeedView.as_view(), name='feed'),
]