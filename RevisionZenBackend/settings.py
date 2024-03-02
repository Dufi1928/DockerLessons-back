from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')



CORS_ALLOWED_ORIGINS = [
    "https://revisionzen.com",
    "https://revisionzen.fr",
    "https://localhost:*",
    "https://localhost:3000",
    "*"
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = [
    'https://revisionzen.com:433',
    'https://revisionzen.fr:433',
    'http://revisionzen.fr:80',
    'http://revisionzen.com:80',
    'http://localhost:3000',
    'https://revisionzen.com:5173',
    'http://revisionzen.com:5173',
    'https://revisionzen.fr:5173',
    'http://revisionzen.fr:5173',
]


INSTALLED_APPS = [
    'Authentification',
    'Cards',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

STATIC_URL = '/static/'

ASGI_APPLICATION = 'RevisionZenBackend.routing.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RevisionZenBackend.urls'

SSL_CERTIFICATE = "/etc/letsencrypt/live/mygameon.pro/fullchain.pem"
SSL_PRIVATE_KEY = "/etc/letsencrypt/live/mygameon.pro/privkey.pem"


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'default_db_name'),
        'USER': os.environ.get('DATABASE_USER', 'default_user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'default_password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'TEST': {
            'NAME': 'test_gameon',
        },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


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

LANGUAGE_CODE = 'en-us'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False
AUTH_USER_MODEL = 'Authentification.User'
SESSION_COOKIE_NAME = 'jwt'
CSRF_COOKIE_NAME = 'csrftoken'

CORS_ALLOW_CREDENTIALS = True


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    },
}
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


