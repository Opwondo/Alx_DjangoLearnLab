from rest_framework import serializers
from django.utils.timezone import now
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer serializes all fields of the Book model.
    
    Custom validation:
    - Ensures publication_year is not in the future
    - Ensures publication_year is reasonable (after 1400)
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        Ensures the publication year is not in the future.
        """
        current_year = now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Additional validation: year should be reasonable
        if value < 1400:
            raise serializers.ValidationError(
                "Publication year should be after 1400."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer includes:
    - The name field
    - A nested BookSerializer to serialize the related books dynamically
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """
        Custom validation for author name.
        """
        if not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        return value.strip()
