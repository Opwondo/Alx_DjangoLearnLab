from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('secure-search/', views.secure_search, name='secure_search'),
    path('secure-contact/', views.secure_contact, name='secure_contact'),
    path('unsafe-example/', views.unsafe_search_example, name='unsafe_example'),
    path('example-form/', views.example_form_view, name='example_form'),     
    path('example-form', RedirectView.as_view(url='/bookshelf/example-form/', permanent=True)),
    # Redirects for URLs without trailing slashes
    path('secure-search', RedirectView.as_view(url='/bookshelf/secure-search/', permanent=True)),
    path('secure-contact', RedirectView.as_view(url='/bookshelf/secure-contact/', permanent=True)),

]