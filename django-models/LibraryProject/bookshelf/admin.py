
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to show
    list_filter = ('author', 'publication_year')            # Filters on the sidebar
    search_fields = ('title', 'author')                     # Search bar for title & author
