from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    # ========== COMMENT CLASS-BASED VIEWS - BEGIN ==========
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
    # ========== COMMENT CLASS-BASED VIEWS - END ==========
)

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Blog Post URLs
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # ========== COMMENT URLS - BEGIN ==========
    # Class-based comment URLs
    path('post/<int:post_id>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # Function-based comment URLs (retained for compatibility)
    path('post/<int:post_id>/comments/add/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    # ========== COMMENT URLS - END ==========
]
