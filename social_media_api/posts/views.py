# posts/views.py
from numpy import generic
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        # Check if the object has 'author' attribute (for both Post and Comment)
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts
    Provides list, create, retrieve, update, partial_update, destroy actions
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']  # Allow searching by title or content
    filterset_fields = ['author']  # Allow filtering by author

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a post
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        """
        Custom action to handle comments on a specific post
        GET: List all comments for this post
        POST: Create a new comment on this post
        """
        post = self.get_object()
        
        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments
    Provides list, create, retrieve, update, partial_update, destroy actions
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a comment
        Note: post must be provided in the request data
        """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Optionally filter comments by post
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

class FeedView(generic.ListAPIView):
    """
    View to get posts from users that the current user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Fix the permission class:
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get posts from users that the current user follows
        """
        user = self.request.user
        # Get users that the current user follows
        following_users = user.following.all()
        # Return posts from followed users, ordered by creation date (newest first)
        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')