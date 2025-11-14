#!/bin/bash

# API Manager Development Environment Setup Script
# This script sets up the Docker development environment for API Manager

set -e

echo "🚀 API Manager Development Environment Setup"
echo "============================================="
echo ""
echo "ℹ️  Running from: $(pwd)"
echo "ℹ️  This script should be run from the development/ directory"
echo ""

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ../logs

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and set your OAuth credentials:"
    echo "   - OAUTH_CONSUMER_KEY"
    echo "   - OAUTH_CONSUMER_SECRET"
    echo ""
    read -p "Do you want to edit .env now? (y/n): " edit_env
    if [ "$edit_env" = "y" ] || [ "$edit_env" = "Y" ]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ .env file already exists"
fi

# Check if OAuth credentials are set
source .env
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run this script from the development directory."
    exit 1
fi

# Check database password security
if [ "$POSTGRES_PASSWORD" = "CHANGE_THIS_PASSWORD" ] || [ -z "$POSTGRES_PASSWORD" ]; then
    echo "🔒 SECURITY WARNING: Database password not properly set!"
    echo "   Please update POSTGRES_PASSWORD in .env file with a secure password"
    echo "   The default password 'CHANGE_THIS_PASSWORD' should not be used"
    echo ""
else
    echo "✅ Database password configured"
fi

if [ "$OAUTH_CONSUMER_KEY" = "your-oauth-consumer-key" ] || [ "$OAUTH_CONSUMER_SECRET" = "your-oauth-consumer-secret" ] || [ -z "$OAUTH_CONSUMER_KEY" ] || [ -z "$OAUTH_CONSUMER_SECRET" ]; then
    echo "⚠️  WARNING: OAuth credentials not properly set!"
    echo "   Please update OAUTH_CONSUMER_KEY and OAUTH_CONSUMER_SECRET in .env file"
    echo "   You can get these from your OBP API instance"
    echo ""
else
    echo "✅ OAuth credentials configured"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"

    # Display service information
    echo ""
    echo "📊 Service Status:"
    docker-compose ps

    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Open http://localhost:8000 in your browser"
    echo "   2. Login with admin/admin123 for admin access"
    echo "   3. Check logs: docker-compose logs -f web"
    echo "   4. Stop services: docker-compose down"
    echo ""
    echo "🔧 Development commands (run from development/ directory):"
    echo "   - View logs: docker-compose logs api-manager-web"
    echo "   - Access shell: docker-compose exec api-manager-web bash"
    echo "   - Django shell: docker-compose exec api-manager-web bash -c 'cd apimanager && python manage.py shell'"
    echo "   - Database shell: docker-compose exec api-manager-db psql -U \${POSTGRES_USER:-apimanager} -d \${POSTGRES_DB:-apimanager}"
    echo ""

    # Test if the application is responding
    if curl -s -I http://localhost:8000 | grep -q "HTTP/1.1"; then
        echo "✅ Application is responding at http://localhost:8000"
    else
        echo "⚠️  Application might not be fully ready yet. Wait a moment and try accessing http://localhost:8000"
    fi

else
    echo "❌ Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi
