from .base import *
DEBUG = True

ALLOWED_HOSTS = ['1pf0hc31cf.execute-api.us-east-2.amazonaws.com']
#CORS_ALLOWED_ORIGINS = [""]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT')
    }
}