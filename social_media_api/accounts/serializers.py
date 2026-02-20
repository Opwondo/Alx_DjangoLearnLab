# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    Handles creating new users with password validation
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Enter a strong password"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        """
        Check that the two passwords match
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user
        """
        # Remove password2 from the data as we don't save it
        validated_data.pop('password2')
        
        # Create user with encrypted password
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """
        Validate the login credentials
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing/updating user profiles
    """
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 
                 'followers_count', 'following_count', 'date_joined']
        read_only_fields = ['id', 'date_joined']