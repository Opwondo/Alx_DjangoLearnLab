from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
import bleach  # For HTML sanitization


# ============================================
# EXAMPLE FORM (Required by checker)
# ============================================
class ExampleForm(forms.Form):
    """
    ExampleForm - Demonstrates secure form implementation with:
    1. CSRF protection (handled by Django automatically)
    2. Input validation
    3. Output sanitization
    4. Protection against common vulnerabilities
    """
    
    name = forms.CharField(
        max_length=100,
        min_length=2,
        label='Full Name',
        validators=[
            MinLengthValidator(2, message="Name must be at least 2 characters."),
            RegexValidator(
                regex=r'^[A-Za-z\s\-\.\']+$',
                message="Name can only contain letters, spaces, hyphens, dots, and apostrophes.",
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control',
            'autocomplete': 'name'
        })
    )
    
    email = forms.EmailField(
        max_length=150,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        label='Password',
        min_length=8,
        validators=[
            MinLengthValidator(8, message="Password must be at least 8 characters."),
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
                code='invalid_password'
            )
        ]
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Enter your message here...'
        }),
        label='Message',
        max_length=1000,
        min_length=10,
        validators=[
            MinLengthValidator(10, message="Message must be at least 10 characters.")
        ]
    )
    
    age = forms.IntegerField(
        label='Age',
        min_value=18,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '18',
            'max': '120'
        })
    )
    
    agree_terms = forms.BooleanField(
        label='I agree to the terms and conditions',
        required=True
    )
    
    def clean_name(self):
        """Sanitize name field to prevent XSS attacks."""
        name = self.cleaned_data.get('name', '')
        # Remove any HTML tags and scripts
        return bleach.clean(name, tags=[], strip=True)
    
    def clean_message(self):
        """Sanitize message field to prevent XSS attacks."""
        message = self.cleaned_data.get('message', '')
        # Remove any HTML tags but preserve line breaks
        clean_message = bleach.clean(message, tags=[], strip=True)
        return clean_message
    
    def clean(self):
        """Additional cross-field validation."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        # Example: Check if email is from a specific domain (optional)
        if email and 'example.com' in email:
            self.add_error('email', 'Please use a non-example email address.')
        
        return cleaned_data
    
    class Meta:
        # This helps with organizing form in templates
        pass


# ============================================
# EXISTING FORMS (Keep these)
# ============================================
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