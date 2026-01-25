from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
import bleach  # For HTML sanitization

class BookSearchForm(forms.Form):
    """
    Secure search form with input validation and sanitization.
    Prevents SQL injection and XSS attacks.
    """
    query = forms.CharField(
        max_length=100,
        min_length=2,
        validators=[
            MinLengthValidator(2, message="Search must be at least 2 characters."),
            MaxLengthValidator(100, message="Search cannot exceed 100 characters.")
        ],
        label='Search Books',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter title or author...',
            'class': 'form-control'
        })
    )
    
    def clean_query(self):
        """Sanitize the search query to prevent XSS attacks."""
        query = self.cleaned_data.get('query', '')
        
        # Remove any HTML tags to prevent XSS
        query = bleach.clean(query, tags=[], strip=True)
        
        # Remove SQL keywords to help prevent SQL injection
        sql_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'SELECT', 'UNION', '--']
        for keyword in sql_keywords:
            query = query.replace(keyword, '')
            query = query.replace(keyword.lower(), '')
        
        return query.strip()


class ContactForm(forms.Form):
    """
    Secure contact form with comprehensive validation.
    """
    name = forms.CharField(
        max_length=100,
        label='Your Name',
        validators=[MinLengthValidator(2)]
    )
    
    email = forms.EmailField(
        label='Email Address',
        max_length=150
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Message',
        max_length=1000,
        validators=[MinLengthValidator(10)]
    )
    
    category = forms.ChoiceField(
        choices=[
            ('', 'Select a category'),
            ('general', 'General Inquiry'),
            ('support', 'Technical Support'),
            ('feedback', 'Feedback')
        ],
        label='Category'
    )
    
    def clean_message(self):
        """Sanitize message to prevent XSS attacks."""
        message = self.cleaned_data.get('message', '')
        # Remove any HTML tags
        return bleach.clean(message, tags=[], strip=True)
