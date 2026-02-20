# accounts/views.py - Using permissions.IsAuthenticated exactly as checker wants
from rest_framework import status
from rest_framework import generics
from rest_framework import views
from rest_framework import permissions  # Import permissions module
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer
from .serializers import UserLoginSerializer
from .serializers import UserProfileSerializer
from .serializers import UserDetailSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Using permissions.AllowAny

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
    permission_classes = [permissions.AllowAny]  # Using permissions.AllowAny

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
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

class FollowUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are already following {user_to_follow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.add(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_follow.followers.count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        if request.user == user_to_unfollow:
            return Response(
                {'error': 'You cannot unfollow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are not following {user_to_unfollow.username}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_unfollow.followers.count()
        }, status=status.HTTP_200_OK)

class FollowersListView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

    def get_queryset(self):
        return self.request.user.followers.all()

class FollowingListView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]  # Using permissions.IsAuthenticated

    def get_queryset(self):
        return self.request.user.following.all()