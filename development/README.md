# API Manager Development Environment

This folder contains Docker development setup for the Open Bank Project API Manager.

## Quick Start

```bash
# 1. Navigate to development directory
cd development

# 2. Copy environment template
cp .env.example .env

# 3. Run the setup script
./dev-setup.sh

# 4. Access the application
open http://localhost:8000
```

## What's Included

- **docker-compose.yml** - Orchestrates web and database services
- **Dockerfile.dev** - Development-optimized container image
- **local_settings_dev.py** - Django development settings
- **docker-entrypoint-dev.sh** - Container startup script
- **.env.example** - Environment variables template

## Services

- **api-manager-web** - Django application (port 8000)
- **api-manager-db** - PostgreSQL database (port 5434)

## Features

✅ Hot code reloading - changes reflect immediately  
✅ PostgreSQL database with persistent storage  
✅ Static files properly served  
✅ Automatic database migrations  
✅ Development superuser (admin/admin123)  
✅ OAuth integration with OBP API  

## Development Commands

```bash
# View logs
docker-compose logs api-manager-web

# Access container shell
docker-compose exec api-manager-web bash

# Django management commands
docker-compose exec api-manager-web bash -c 'cd apimanager && python manage.py shell'

# Database shell
docker-compose exec api-manager-db psql -U ${POSTGRES_USER:-apimanager} -d ${POSTGRES_DB:-apimanager}

# Stop services
docker-compose down
```

## Configuration

The setup uses environment variables defined in `.env`:

- `OAUTH_CONSUMER_KEY` - OAuth consumer key from OBP API
- `OAUTH_CONSUMER_SECRET` - OAuth consumer secret from OBP API  
- `API_HOST` - OBP API server URL (default: http://host.docker.internal:8080)
- `POSTGRES_PASSWORD` - Database password (IMPORTANT: Change from default!)
- `POSTGRES_USER` - Database username (default: apimanager)
- `POSTGRES_DB` - Database name (default: apimanager)

### 🔒 Security Note

**IMPORTANT**: The default database password is `CHANGE_THIS_PASSWORD` and must be changed before deployment. Set a strong password in your `.env` file:

```bash
POSTGRES_PASSWORD=your_secure_password_here
```

## Testing OAuth Integration

1. **First, set a secure database password** in your `.env` file
2. Ensure OBP API is running on http://127.0.0.1:8080/ (accessible as host.docker.internal:8080 from containers)
3. Start the development environment
4. Navigate to http://localhost:8000
5. Click "Proceed to authentication server" to test OAuth flow

## Troubleshooting

- **Port conflicts**: Database uses port 5434 to avoid conflicts
- **OAuth errors**: Verify OAUTH_CONSUMER_KEY and OAUTH_CONSUMER_SECRET in .env
- **Database connection errors**: Ensure POSTGRES_PASSWORD is set in .env and matches between services
- **Connection refused to OBP API**: The setup uses `host.docker.internal:8080` to reach the host machine's OBP API from containers
- **Static files missing**: Restart containers with `docker-compose down && docker-compose up -d`

## Docker Networking

The development setup uses `host.docker.internal:8080` to allow containers to access the OBP API running on the host machine at `127.0.0.1:8080`. This is automatically configured in the docker-compose.yml file.

This development environment provides hot reloading and mirrors the production setup while remaining developer-friendly.