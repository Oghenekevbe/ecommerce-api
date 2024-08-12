"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    
    # 3rd party apps
    'rest_framework',
    'dj_rest_auth',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    'dj_rest_auth.registration',
    'drf_yasg',

    # apps
    "store",
    "storeAdmin",
    "storeSellers",
    "users",
    "paymentapp",
]

SITE_ID = 1

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = (
    # "django.contrib.auth.backends.ModelBackend",
    'users.email_backend.EmailAuthenticationBackend', #for django admin
    'allauth.account.auth_backends.AuthenticationBackend', #for other email authentication
)

# Allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Options: 'none', 'optional', 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Use email for authentication

# REST framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ]
}

# Simple JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
}

# REST Auth settings
REST_AUTH = {
    'LOGIN_SERIALIZER': 'users.serializers.LoginSerializer', 
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
    'TOKEN_MODEL': None,  # Disable default token model
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,  # Controls whether the JWT token is accessible via JavaScript
}

# Email settings
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Paystack settings
PAYSTACK_KEY = config("PAYSTACK_KEY")

# PayPal settings
PAYPAL_Client_ID = config('PAYPAL_Client_ID')
PAYPAL_SECRET_KEY = config('PAYPAL_SECRET_KEY')

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "core.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# Uncomment and configure the following for PostgreSQL
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': config('PGDATABASE'),
#     'USER': config('PGUSER'),
#     'PASSWORD': config('PGPASSWORD'),
#     'HOST': config('PGHOST'),
#     'PORT': config('PGPORT', 5432),
#     'OPTIONS': {
#       'sslmode': 'require',
#     },
#   },
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AWS S3 settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'obawebdev'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3boto3Storage'

# Email and password reset redirect URLs
EMAIL_CONFIRM_REDIRECT_BASE_URL = "http://localhost:8000/email/confirm/"
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = "http://localhost:8000/password-reset/confirm/"
