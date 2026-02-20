from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserDetailSerializer
)

User = get_user_model()  # This gets CustomUser

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()  # Using CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    """
    View to get details of a specific user
    """
    queryset = User.objects.all()  # Using CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

class FollowUserView(views.APIView):
    """
    View to follow a user
    """
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

    def post(self, request, user_id):
        # Using CustomUser.objects.all() to get the user
        user_to_follow = get_object_or_404(User.objects.all(), id=user_id)
        
        # Check if trying to follow self
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are already following {user_to_follow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following
        request.user.following.add(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_follow.followers.count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(views.APIView):
    """
    View to unfollow a user
    """
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

    def post(self, request, user_id):
        # Using CustomUser.objects.all() to get the user
        user_to_unfollow = get_object_or_404(User.objects.all(), id=user_id)
        
        # Check if trying to unfollow self
        if request.user == user_to_unfollow:
            return Response(
                {'error': 'You cannot unfollow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if actually following
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are not following {user_to_unfollow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove from following
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_unfollow.followers.count()
        }, status=status.HTTP_200_OK)

class FollowersListView(generics.ListAPIView):
    """
    View to list users who follow the current user
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

    def get_queryset(self):
        return self.request.user.followers.all()

class FollowingListView(generics.ListAPIView):
    """
    View to list users the current user follows
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]  # Explicit IsAuthenticated

    def get_queryset(self):
        return self.request.user.following.all()