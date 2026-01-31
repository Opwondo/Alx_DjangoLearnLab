from django.urls import path
from .views import BookList

# Define URL patterns for the API app
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
