from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import render
    
from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Custom permission
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        # For Book model, we don't have an owner field yet, so using admin only
        return request.user.is_staff

# Simple list view - Now requires authentication
class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    Requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require auth

# Full CRUD ViewSet with different permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Book model.
    Different permissions for different actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom permission classes
    permission_classes = [permissions.IsAuthenticated]
    
    # Override permission classes for specific actions
    def get_permissions(self):
        """
        Override permissions based on action.
        - List/Retrieve: Any authenticated user
        - Create/Update/Delete: Only admin users
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:  # create, update, partial_update, destroy
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class CustomAuthToken(ObtainAuthToken):
    """
    Custom token view that returns token along with user info.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })
