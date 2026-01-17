from atexit import register
from django.urls import path
from .views import CustomLoginView, CustomLogoutView, list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),  
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]