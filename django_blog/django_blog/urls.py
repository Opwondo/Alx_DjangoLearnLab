from django.contrib import admin
from django.urls import include, path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('', include('blog.urls')),
    
]
