from .settings import *

DEBUG = False

ALLOWED_HOSTS =[]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'transaction_app_final',
        'USER': 'lilit1',
        'PASSWORD': '123456789',
        'HOST': '127.0.0.1',
        # 'PORT': '5432',
    }
}
