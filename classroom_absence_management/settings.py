"""
Django settings for classroom_absence_management project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import os
from datetime import timedelta
from celery.schedules import crontab

# Load environment variables from .env file
env = environ.Env()
# Specify the path to .env in the project root (one level up from settings.py)
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'training')

MEDIA_URL = 'training/'

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Celery Beat Configuration
CELERY_BEAT_SCHEDULE = {
    'encode-missing-faces-every-saturday': {
        'task': 'apps.studentimages.tasks.encode_new_images_task',
        'schedule': crontab(hour=23, minute=59, day_of_week=6),  # Every Saturday at 11:59 PM
    },
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP for real emails
EMAIL_HOST = 'smtp.gmail.com'  # Example: Gmail SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str('MY_EMAIL_ADDRESS')  # Your Gmail address
EMAIL_HOST_PASSWORD = env.str('MY_EMAIL_APP_PASSWORD')  # App-specific password (not regular password)
DEFAULT_FROM_EMAIL = 'Classroom Face Reco'  # The name that will appear in the email

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'rest_framework.authtoken',  # Token authentication
    'apps.users',
    'apps.students',
    'apps.teachers',
    'apps.subjects',
    'apps.attendance',
    'apps.classes',
    'apps.studentimages',
    'django_extensions',  # Django Extensions
    'django_celery_beat',
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

ROOT_URLCONF = 'classroom_absence_management.urls'

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

WSGI_APPLICATION = 'classroom_absence_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('DB_NAME', default='classroom_db'),
        'USER': env.str('DB_USER', default='admin'),
        'PASSWORD': env.str('DB_PASSWORD', default='root'),
        'HOST': env.str('DB_HOST', default='db'),  # or 'db' if in Docker
        'PORT': env.int('DB_PORT', default=3307),  # Make sure this matches the port you're using
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'apps.users.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'apps.users.exception.custom_exception_handler',
}


# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
#     'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
# }
