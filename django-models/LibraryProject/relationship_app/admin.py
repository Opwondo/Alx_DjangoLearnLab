from django.contrib import admin

# Register your models here.
from .models import Author  # import your model

# Register the model with the admin site
admin.site.register(Author)
