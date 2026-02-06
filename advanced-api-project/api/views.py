from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    Retrieves all Book records and supports:
    - Filtering
    - Searching
    - Ordering
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Correct filter backends (NO "filters." prefix)
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Filtering fields
    filterset_fields = [
        'title',
        'publication_year',
        'author',
    ]

    # Search fields
    search_fields = [
        'title',
        'author__name',
    ]

    # Ordering fields
    ordering_fields = [
        'title',
        'publication_year',
    ]

    ordering = ['title']


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
