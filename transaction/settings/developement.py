from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'transaction_db',
        'USER': 'izabella',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '7531'
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'