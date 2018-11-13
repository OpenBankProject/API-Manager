import os.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Used internally by Django, can be anything of your choice
SECRET_KEY = '<random string>'
# API hostname, e.g. https://api.openbankproject.com
API_HOST = '<hostname>'
# Consumer key + secret to authenticate the _app_ against the API
OAUTH_CONSUMER_KEY = '<key>'
OAUTH_CONSUMER_SECRET = '<secret>'
# Database filename, default is `../db.sqlite3` relative to this file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', '..', 'db.sqlite3'),
    }
}
STATIC_ROOT = '/static'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
