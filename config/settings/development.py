from .base import *

DEBUG = True

DATABASES['default']['OPTIONS'] = {'sslmode': 'disable'}  # Local dev without SSL

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ['django.contrib.staticfiles']
