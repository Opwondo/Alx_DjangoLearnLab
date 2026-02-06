from rest_framework import serializers
from django.utils.timezone import now
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes custom validation for publication_year.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']  # Auto-generated, not editable
    
    def validate_publication_year(self, value):
        """
        Custom validation: Ensure publication_year is not in the future.
        """
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        # Additional validation: year should be reasonable (e.g., after 1400)
        if value < 1400:
            raise serializers.ValidationError(
                "Publication year should be after 1400."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes nested BookSerializer to show author's books.
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
        # Check if name is not empty after stripping whitespace
        if not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        
        # Check if name contains only letters and spaces
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "Author name should contain only letters and spaces."
            )
        
        return value.strip()


# Additional serializer for creating books with nested author data
class BookWithAuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Book with nested Author data.
    Useful when creating a book and its author in one request.
    """
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
