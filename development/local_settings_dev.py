import os

# Development settings for Docker environment

# Debug mode for development - force override
DEBUG = True
if os.getenv('DEBUG'):
    DEBUG = os.getenv('DEBUG').lower() in ('true', '1', 'yes', 'on')

# Secret key from environment or default for development
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# API Configuration
if os.getenv('API_HOST'):
    API_HOST = os.getenv('API_HOST')
else:
    API_HOST = 'http://127.0.0.1:8080'

if os.getenv('API_PORTAL'):
    API_PORTAL = os.getenv('API_PORTAL')
else:
    API_PORTAL = API_HOST

# OAuth Configuration
if os.getenv('OAUTH_CONSUMER_KEY'):
    OAUTH_CONSUMER_KEY = os.getenv('OAUTH_CONSUMER_KEY')
else:
    OAUTH_CONSUMER_KEY = "your-oauth-consumer-key"

if os.getenv('OAUTH_CONSUMER_SECRET'):
    OAUTH_CONSUMER_SECRET = os.getenv('OAUTH_CONSUMER_SECRET')
else:
    OAUTH_CONSUMER_SECRET = "your-oauth-consumer-secret"

# Callback URL for OAuth - use localhost for browser accessibility
if os.getenv('CALLBACK_BASE_URL'):
    CALLBACK_BASE_URL = os.getenv('CALLBACK_BASE_URL')
else:
    CALLBACK_BASE_URL = "http://localhost:8000"

# Allowed hosts
if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'web']

# CSRF and CORS settings for development
if os.getenv('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
else:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

if os.getenv('CORS_ORIGIN_WHITELIST'):
    CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST').split(',')

# Database configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Check if DATABASE_URL is provided (for PostgreSQL in Docker)
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Static files configuration for Docker
STATIC_ROOT = '/static-collected'

# Ensure DEBUG is properly set for static file serving
DEBUG = True

# Security settings for development (less restrictive)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Disable SSL redirect for development
SECURE_SSL_REDIRECT = False

# Session configuration for OAuth flow reliability
SESSION_COOKIE_AGE = 3600  # 1 hour instead of 5 minutes
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Use database sessions for reliability

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'obp': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'consumers': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'customers': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'metrics': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
