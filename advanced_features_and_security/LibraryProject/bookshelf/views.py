from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from pexpect import EOF
from .models import Book
from .forms import ExampleForm

import bleach
from django.db.models import Q
from .forms import BookSearchForm, ContactForm

# View to list books - requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# View to create a new book - requires can_create permission
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            is_available=True
        )
        messages.success(request, 'Book created successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

# View to edit a book - requires can_edit permission
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

# View to delete a book - requires can_delete permission
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# View for book detail - requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Secure search view - Demonstrates safe SQL handling
def secure_search(request):
    """
    Secure search implementation that:
    1. Uses Django ORM to prevent SQL injection
    2. Validates and sanitizes user input
    3. Escapes output in templates
    """
    results = []
    query = ''
    form = BookSearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        
        # SAFE: Using Django ORM with parameterized queries
        # This prevents SQL injection automatically
        results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )[:50]  # Limit results to prevent DoS
        
        # Log the search (safely)
        print(f"Safe search for: {query}")
    
    context = {
        'form': form,
        'results': results,
        'query': query,
    }
    return render(request, 'bookshelf/secure_search.html', context)


# Secure contact form view
def secure_contact(request):
    """
    Secure contact form implementation with:
    1. CSRF protection (automatic with Django forms)
    2. Input validation
    3. Output sanitization
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (all data is validated and sanitized)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            category = form.cleaned_data['category']
            
            # SECURE: All user input has been validated and sanitized
            # No SQL injection risk because we're not building raw SQL
            # No XSS risk because HTML has been stripped
            
            # Example: Save to database safely
            # ContactMessage.objects.create(
            #     name=name,
            #     email=email,
            #     message=message,
            #     category=category
            # )
            
            messages.success(
                request, 
                f'Thank you for your {category} message, {name}!'
            )
            return redirect('book_list')
    else:
        form = ContactForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})


# Example of UNSAFE code (for educational purposes - DO NOT USE)
def unsafe_search_example(request):
    """
    UNSAFE EXAMPLE - Demonstrates what NOT to do.
    This is vulnerable to SQL injection attacks.
    """
    if 'q' in request.GET:
        query = request.GET['q']
        
        #  UNSAFE: String concatenation in raw SQL - VULNERABLE TO SQL INJECTION
        # Never do this in production!
        unsafe_sql = f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'"
        
        #  UNSAFE: Executing raw SQL without parameterization
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(unsafe_sql)  # SQL INJECTION VULNERABILITY
            results = cursor.fetchall()
        
        return render(request, 'bookshelf/unsafe_example.html', {
            'results': results,
            'query': query
        })
    
    return render(request, 'bookshelf/unsafe_example.html')


# Example form view using ExampleForm
def example_form_view(request):
    """
    View demonstrating secure form handling with ExampleForm.
    Shows proper validation, sanitization, and CSRF protection.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # All data has been validated and sanitized
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            age = form.cleaned_data['age']
            
            # SECURE: Process the data (no SQL injection or XSS risk)
            messages.success(
                request,
                f'Thank you {name}! Your form has been submitted securely. Age: {age}'
            )
            return redirect('book_list')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})
