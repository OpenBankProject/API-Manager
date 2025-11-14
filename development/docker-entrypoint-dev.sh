#!/bin/bash

# Development entrypoint script for API Manager
# This script sets up the development environment and starts the Django development server

set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
DB_USER=${POSTGRES_USER:-apimanager}
while ! pg_isready -h 127.0.0.1 -p 5434 -U "$DB_USER" -q; do
  echo "Database is unavailable - sleeping"
  sleep 2
done
echo "Database is ready!"

# Change to the Django project directory
cd /app/apimanager

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (for development convenience)
echo "Setting up development superuser..."
python manage.py shell -c "
import os
from django.contrib.auth.models import User
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
" || echo "Superuser setup skipped (error occurred)"

# Start the development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
