
import os
from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Security
SECRET_KEY = config('SECRET_KEY')

# Timezone
TIME_ZONE = config('TIME_ZONE', default='Africa/Johannesburg')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# login and logout 
# settings.py

LOGIN_REDIRECT_URL = 'dashboard'  # Redirect to dashboard after successful login
LOGOUT_REDIRECT_URL = 'homepage'  # Redirect to home after logout

AUTH_USER_MODEL = 'auth.User'  # Use the default User model from django.contrib.auth


# Media location

MEDIA_URL = '/static/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'


LOGIN_URL = 'login'
# Timezone

USE_TZ = True  # This ensures that Django will use timezone-aware datetimes


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TurfAPP',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files in production
]

# HTTPS Settings
# SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security
# SECURE_SSL_REDIRECT = True      # Redirect HTTP to HTTPS
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'Turfloop.urls'

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

ASGI_APPLICATION = 'Turfloop.asgi.application'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# settings.py

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import os

# Define the static files directory inside the TurfAPP folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'TurfAPP', 'static'),  # Directory for static files inside TurfAPP
]

# Directory where Django will collect static files during 'collectstatic'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files directory



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
