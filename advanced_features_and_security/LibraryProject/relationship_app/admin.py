from django.contrib import admin
from .models import UserProfile

# Register your models here.
from .models import Author  # import your model

# Register the model with the admin site
admin.site.register(Author)
admin.site.register(UserProfile)
