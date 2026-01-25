"""
Django settings for LibraryProject project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Keep as True for development

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'bookshelf',
    'relationship_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# HTTPS & SECURITY SETTINGS
# ============================================

# ============================================
# STEP 1: HTTPS SUPPORT CONFIGURATION
# ============================================
# SECURE_SSL_REDIRECT: Set to True to redirect all non-HTTPS requests to HTTPS.
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS

# SECURE_HSTS_SECONDS: Set to 31536000 (1 year) to instruct browsers to only
# access the site via HTTPS for the specified time.
SECURE_HSTS_SECONDS = 31536000  # 1 year

# SECURE_HSTS_INCLUDE_SUBDOMAINS: Set to True to include all subdomains
# in the HSTS policy.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD: Set to True to allow preloading in HSTS preload lists.
SECURE_HSTS_PRELOAD = True

# ============================================
# STEP 2: SECURE COOKIES CONFIGURATION
# ============================================
# SESSION_COOKIE_SECURE: Set to True to ensure session cookies are only
# transmitted over HTTPS connections.
SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE: Set to True to ensure CSRF cookies are only
# transmitted over HTTPS connections.
CSRF_COOKIE_SECURE = True

# Additional cookie security
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF cookie SameSite attribute
SESSION_COOKIE_SAMESITE = 'Lax'  # Session cookie SameSite attribute

# ============================================
# STEP 3: SECURE HEADERS CONFIGURATION
# ============================================
# X_FRAME_OPTIONS: Set to "DENY" to prevent your site from being framed
# and protect against clickjacking attacks.
X_FRAME_OPTIONS = 'DENY'

# SECURE_CONTENT_TYPE_NOSNIFF: Set to True to prevent browsers from
# MIME-sniffing a response away from the declared content-type.
SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_BROWSER_XSS_FILTER: Set to True to enable the browser's
# XSS filtering and help prevent cross-site scripting attacks.
SECURE_BROWSER_XSS_FILTER = True

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'

# ============================================
# DEVELOPMENT OVERRIDES
# ============================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# For development/testing, override HTTPS settings
# Remove or comment this section in production
if DEBUG:
    # Disable HTTPS redirect for development
    SECURE_SSL_REDIRECT = False
    
    # Disable secure cookies for development
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    
    # Disable HSTS for development
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# Password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
