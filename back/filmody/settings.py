"""
Django settings for filmody project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from http.client import BAD_GATEWAY
from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ymvwkbpp-2e2bcs#ne0a9fj7kwe#@uij=#p1xxl989iu)5rbuh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'movies',
    'accounts',
    'playlists',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'drf_spectacular',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]

ROOT_URLCONF = 'filmody.urls'

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

WSGI_APPLICATION = 'filmody.wsgi.application'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # 페이지네이션 설정
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    # Authentication(인증)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # permission(허가)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'accounts.User'

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

# env 파일 로드
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')  # .env 파일 읽기

# API Keys
KOBIS_API_KEY = env('KOBIS_API_KEY')
KMDB_API_KEY = env('KMDB_API_KEY')
YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 이미지 저장 경로
MEDIA_URL = '/media/'  # 클라이언트가 이미지를 접근할 때 사용할 URL 경로
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 실제 파일이 저장될 디렉터리


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth 설정
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증 비활성화
ACCOUNT_EMAIL_REQUIRED = True  # 이메일 필수

# 별도의 view를 작성하지 않고 dj_rest_auth의 기본 기능을 커스텀 serializer와 함께 사용
REST_AUTH = {
  'REGISTER_SERIALIZER': 'accounts.serializers.SignUpSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.ProfileUpdateSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',
}


# 세션 설정
SESSION_COOKIE_NAME = 'sessionid'  # 기본값이지만 명시적으로 설정
SESSION_COOKIE_SAMESITE = 'Lax'    # 개발 환경에서는 Lax
SESSION_COOKIE_SECURE = False      # 개발 환경에서는 False (HTTPS 아닐때)
SESSION_COOKIE_HTTPONLY = True     
SESSION_COOKIE_DOMAIN = None       # 로컬 개발 환경에서는 None


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# 파일 업로드 최대 크기 설정
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# 개발 환경
BASE_URL = 'http://127.0.0.1:8000'