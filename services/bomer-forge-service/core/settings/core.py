from pathlib import Path
import os
from google.oauth2 import service_account

from core.constants import (
    DJANGO_ALLOWED_HOSTS,
    DJANGO_CSRF_COOKIE_SAMESITE,
    DJANGO_CSRF_COOKIE_SECURE,
    DJANGO_CSRF_HEADER_NAME,
    DJANGO_CSRF_TRUSTED_ORIGINS,
    DJANGO_CSRF_USE_SESSIONS,
    DJANGO_SESSION_COOKIE_SAMESITE,
    DJANGO_SESSION_COOKIE_SECURE,
    DJANGO_SECRET_KEY,
    DJANGO_STATIC_ROOT,
)


__all__ = (
    "ALLOWED_HOSTS",
    "AUTHENTICATION_BACKENDS",
    "BASE_DIR",
    "CSRF_COOKIE_SAMESITE",
    "CSRF_COOKIE_SECURE",
    # "CSRF_HEADER_NAME",
    "CSRF_TRUSTED_ORIGINS",
    "CSRF_USE_SESSIONS",
    "DATABASES",
    "DEBUG",
    "DEFAULT_AUTO_FIELD",
    "INSTALLED_APPS",
    "LANGUAGE_CODE",
    "MIDDLEWARE",
    "ROOT_URLCONF",
    "SECRET_KEY",
    "SESSION_COOKIE_SAMESITE",
    "SESSION_COOKIE_SECURE",
    "STATIC_ROOT",
    "STATIC_URL",
    # "STORAGES",
    "TEMPLATES",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "WSGI_APPLICATION",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS


SESSION_COOKIE_SAMESITE = DJANGO_SESSION_COOKIE_SAMESITE
SESSION_COOKIE_SECURE = DJANGO_SESSION_COOKIE_SECURE

CSRF_COOKIE_SAMESITE = DJANGO_CSRF_COOKIE_SAMESITE
CSRF_COOKIE_SECURE = DJANGO_CSRF_COOKIE_SECURE
# CSRF_HEADER_NAME = DJANGO_CSRF_HEADER_NAME
CSRF_TRUSTED_ORIGINS = DJANGO_CSRF_TRUSTED_ORIGINS
CSRF_USE_SESSIONS = DJANGO_CSRF_USE_SESSIONS


# Google Cloud Storage Settings
GS_BUCKET_NAME = "bomer-forge-service-bucket"

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, "secrets/bomer-ai-5903df29fa96.json")
)

GS_PROJECT_ID = "bomer-ai"

# Configure Django to use GCS for file storage
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

# Optional settings
GS_FILE_OVERWRITE = False  # Don't overwrite existing files
GS_DEFAULT_ACL = "publicRead"  # Make files publicly readable
GS_LOCATION = "media"  # Prefix for uploaded files

# Storages
STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE,
        "OPTIONS": {
            "bucket_name": GS_BUCKET_NAME,
            "project_id": GS_PROJECT_ID,
            "credentials": GS_CREDENTIALS,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "celery_worker",
    "django_celery_results",
    "configurable_variables",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "ai",
    "studies",
    "draft_building_designs",
    "building_components",
    "materials",
    "projects",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django",
        "USER": "service_app_user",
        "PASSWORD": "service_app_user",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = DJANGO_STATIC_ROOT
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
