from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['djangoproyecto.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3q0cp201l89jc',
        'USER': 'gkohbjnrdqaxzp',
        'PASSWORD': 'a2c81e1bf5fae38e2757e28c6d356810b25a8ec6439cf7f17375cee140e02b10',
        'HOST':'ec2-34-197-25-109.compute-1.amazonaws.com',
        'DATABASE_PORT':'5432',
   }
}