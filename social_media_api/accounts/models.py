# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User Model that extends Django's AbstractUser
    Think of this as adding extra fields to the default user
    """
    # Additional fields
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Tell us about yourself (max 500 characters)"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    
    # Self-referential many-to-many field for followers
    # symmetrical=False means if A follows B, B doesn't automatically follow A
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    
    def __str__(self):
        """This shows how the user appears in admin panel"""
        return self.username
    
    @property
    def followers_count(self):
        """Helper property to get number of followers"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Helper property to get number of users this user follows"""
        return self.following.count()