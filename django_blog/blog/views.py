from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'blog/base.html', {'title': 'Home'})

def posts(request):
    return HttpResponse("Blog Posts Page - Coming Soon")

def login_view(request):
    return HttpResponse("Login Page - Coming Soon")

def register(request):
    return HttpResponse("Register Page - Coming Soon")
