"""
Base Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import environ

from django.core.management.utils import get_random_secret_key

root = environ.Path(__file__) - 3  # Get root of the project
env = environ.Env()
environ.Env.read_env()  # Reading .env file.

BASE_DIR = root()

# Quick-start development settings - unsuitable for production
# TODO: See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = env.str('SECRET_KEY', default=get_random_secret_key())

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Site id for using in sitemap
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'taggit',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
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

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': env.db('DATABASE_URL')}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = env.str('STATIC_URL', default='/static/')

# EMAIL SETTINGS

# SMTP-host
EMAIL_HOST = env.str('EMAIL_HOST', default='localhost')

# SMTP-port
EMAIL_PORT = env.int('EMAIL_PORT', default=25)

# Login for access to SMTP-server
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

EMAIL_BACKEND = env.str('EMAIL_BACKEND',
                        default='django.core.mail.backends.smtp.EmailBackend')
