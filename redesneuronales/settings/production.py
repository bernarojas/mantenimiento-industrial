from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mantenimiento-industrial.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3fecf4d7oqiuj',
        'USER': 'upktwgkhagfmia',
        'PASSWORD': 'e14490ee5d2749a6cf6586efdb09e87f677aeb4691faccf971daf11ce2d74d31',
        'HOST':'ec2-34-230-198-12.compute-1.amazonaws.com',
        'DATABASE_PORT':'5432',
   }
}