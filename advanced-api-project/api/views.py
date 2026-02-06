from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ===============================
# LIST VIEW – GET all books
# Accessible to everyone
# ===============================
class BookListView(generics.ListAPIView):
    """
    Handles retrieving all Book records.
    Publicly accessible (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ===============================
# DETAIL VIEW – GET single book
# Accessible to everyone
# ===============================
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single Book by ID.
    Publicly accessible (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ===============================
# CREATE VIEW – POST new book
# Authenticated users only
# ===============================
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ===============================
# UPDATE VIEW – PUT/PATCH book
# Authenticated users only
# ===============================
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ===============================
# DELETE VIEW – DELETE book
# Authenticated users only
# ===============================
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
