from django.shortcuts import render

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    Provides a GET method handler.
    """
    queryset = Book.objects.all()  # Get all books from database
    serializer_class = BookSerializer  # Use our BookSerializer
