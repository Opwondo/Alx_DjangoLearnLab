from rest_framework import serializers
from .models import Author, Book
from datetime import date


# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book data and validates that
    publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication year
        is not greater than the current year.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author data and dynamically includes
    all related books using a nested serializer.
    """

    # Nested serializer to show all books by this author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
