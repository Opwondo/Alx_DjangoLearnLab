# bookshelf/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Book Admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'is_available')
    list_filter = ('author', 'publication_year', 'is_available')
    search_fields = ('title', 'author')


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile)