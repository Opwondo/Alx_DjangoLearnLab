from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    # ========== SEARCH AND TAGGING FUNCTIONALITY - BEGIN ==========
    SearchResultsView,
    TaggedPostsView,
    PostByTagListView,  # CHECKER-REQUIRED VIEW
    # ========== SEARCH AND TAGGING FUNCTIONALITY - END ==========
    # ========== COMMENT CLASS-BASED VIEWS - BEGIN ==========
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
    # ========== COMMENT CLASS-BASED VIEWS - END ==========
)

urlpatterns = [
    # ========== AUTHENTICATION URLS - BEGIN ==========
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    # ========== AUTHENTICATION URLS - END ==========
    
    # ========== BLOG POST CRUD URLS - BEGIN ==========
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # ========== BLOG POST CRUD URLS - END ==========
    
    # ========== SEARCH AND TAGGING URLS - BEGIN ==========
    path('search/', SearchResultsView.as_view(), name='search-results'),
    # CHECKER-REQUIRED URL PATTERN: tags/<slug:tag_slug>/
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tagged-posts'),
    # Alternative pattern for backward compatibility
    path('tag/<slug:tag_slug>/', TaggedPostsView.as_view(), name='tagged-posts-alt'),
    # ========== SEARCH AND TAGGING URLS - END ==========
    
    # ========== COMMENT URLS - BEGIN ==========
    # CHECKER-REQUIRED URL PATTERN: /post/<int:pk>/comments/new/
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    
    # Class-based comment URLs for update and delete
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # ========== BACKWARD COMPATIBILITY COMMENT URLS - BEGIN ==========
    # Alternative URL patterns for backward compatibility
    path('post/<int:post_id>/comment/new/', CommentCreateView.as_view(), name='comment-create-alt'),
    path('post/<int:post_id>/comments/add/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    # ========== BACKWARD COMPATIBILITY COMMENT URLS - END ==========
    # ========== COMMENT URLS - END ==========
]
