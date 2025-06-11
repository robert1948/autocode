# --- File: cape_control_backend/settings.py ---
# Django project settings. Important configurations for database, CORS, and installed apps.

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file during local development.
# In production on Google Cloud Run, these variables will be set directly in the environment.
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Use an environment variable for the secret key, with a fallback for local testing.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-very-secret-and-long-key-for-local-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode should be False in production. Control with an environment variable.
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

# Allowed hosts for the Django application.
# Crucial for security in production.
# In production, this should include your Cloud Run URL and custom domain.
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Add the Cloud Run service URL here, e.g., 'your-cloud-run-service-url.run.app'
# Or 'your-custom-domain.com'
# Example: ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-service-name-hash-region.run.app', 'cape-control.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',          # Django REST Framework
    'djoser',                  # Djoser for authentication endpoints
    'corsheaders',             # Django CORS Headers for cross-origin requests
    'users',                   # Your custom users app
    'agents',                  # Your custom agents app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS middleware must be very high, preferably before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cape_control_backend.urls'

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

WSGI_APPLICATION = 'cape_control_backend.wsgi.application'

# Database
# Use PostgreSQL with Cloud SQL.
# Environment variables will configure this in production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cape_control_db'),
        'USER': os.getenv('DB_USER', 'your_local_db_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_local_db_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'), # Use Cloud SQL IP/connection name in production
        'PORT': os.getenv('DB_PORT', '5432'),
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
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # For collectstatic

# This is important for WhiteNoise to correctly serve static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication', # For simple token-based auth
        'rest_framework.authentication.SessionAuthentication', # For browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Allow read for anyone, write for authenticated
    ),
}

# Djoser settings for user authentication
DJOSER = {
    'USER_ID_FIELD': 'username', # Or 'email' if you prefer email as primary ID
    'LOGIN_FIELD': 'email', # Users log in with email
    'SEND_ACTIVATION_EMAIL': False, # For simplicity in MVP
    'USERNAME_REGEX': r'^[\w.@+-]+$',
    'PASSWORD_REGEX': r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', # At least 8 characters, one letter, one number
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}

# CORS Headers settings
# Allow your React frontend (e.g., http://localhost:3000, your Cloud Run frontend URL) to access the backend.
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
# Add the Cloud Run frontend URL and custom domain here.
# Example: CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'https://your-frontend-service-url.run.app', 'https://cape-control.com']
CORS_ALLOW_CREDENTIALS = True # Important for sending cookies/auth tokens

