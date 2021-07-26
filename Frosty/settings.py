

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent




DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    'main',
    'materializecssform',
    'formtools',
    'django_user_agents',
    'Frosty',
    'tinymce',
    'multiselectfield',
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

ROOT_URLCONF = 'Frosty.urls'

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










WSGI_APPLICATION = 'Frosty.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',

    }
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


#MICROSOFT_AUTH_EXTRA_SCOPES = "email"
#MICROSOFT_AUTH_AUTHENTICATE_HOOK = "main.aad.store_token"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#MICROSOFT_AUTH_CLIENT_ID = '21ac534a-fb63-47e7-a2c1-ee1e98fddf0b'
#MICROSOFT_AUTH_CLIENT_SECRET = 'EV8N~fMI-A3~hCT3a2vOJTRM61Vr5.7Ngz'
#MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/Frosty/'
AUTHENTICATION_BACKENDS = [
        #"microsoft_auth.backends.MicrosoftAuthenticationBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]
