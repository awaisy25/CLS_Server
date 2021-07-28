from .base import *

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_DEV_NAME'),
        'USER': env('DB_DEV_USER'),
        'PASSWORD': env('DB_DEV_PASSWORD'),
        'HOST': env('DB_DEV_HOST'),
        'PORT': env('DB_DEV_PORT')
    }
}
