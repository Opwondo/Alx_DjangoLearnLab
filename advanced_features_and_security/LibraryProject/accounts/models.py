# accounts/models.py
# COMMENT OUT or REMOVE the CustomUser class

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# KEEP the manager if needed elsewhere, but REMOVE CustomUser class
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)

# REMOVE or COMMENT OUT this entire CustomUser class
# class CustomUser(AbstractUser):
#     date_of_birth = models.DateField(null=True, blank=True)
#     profile_photo = models.ImageField(
#         upload_to="profile_photos/",
#         null=True,
#         blank=True
#     )
# 
#     objects = CustomUserManager()
# 
#     def __str__(self):
#         return self.username