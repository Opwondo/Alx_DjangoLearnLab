from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from blog.models import Post, Comment
# ========== TAGGING FUNCTIONALITY - BEGIN ==========
from taggit.forms import TagWidget
# ========== TAGGING FUNCTIONALITY - END ==========

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError("This email is already registered.")
        return email

# ========== POST FORM WITH TAGGING - BEGIN ==========
class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter post title'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write your post content here...',
        'rows': 10
    }))
    # ========== USING TAGWIDGET - BEGIN ==========
    tags = forms.CharField(
        required=False, 
        help_text="Separate tags with commas",
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., python, django, tutorial)'
        })
    )
    # ========== USING TAGWIDGET - END ==========

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        # ========== EXPLICIT WIDGETS DICTIONARY - BEGIN ==========
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
        # ========== EXPLICIT WIDGETS DICTIONARY - END ==========
# ========== POST FORM WITH TAGGING - END ==========

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write your comment here...',
        'rows': 3
    }))

    class Meta:
        model = Comment
        fields = ['content']
        # ========== COMMENT FORM WIDGETS - BEGIN ==========
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3
            }),
        }
        # ========== COMMENT FORM WIDGETS - END ==========

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) == 0:
            raise ValidationError("Comment cannot be empty.")
        return content
