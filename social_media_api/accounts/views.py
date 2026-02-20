# accounts/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """
    API endpoint for user login
    POST /api/login/
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]  # Anyone can login

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile
    GET /api/profile/ - View profile
    PUT/PATCH /api/profile/ - Update profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Only logged in users can access

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user