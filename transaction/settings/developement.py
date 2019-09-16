from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'transaction_app',
        'USER': 'lilit',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        # 'PORT': '5432',
    }
}
