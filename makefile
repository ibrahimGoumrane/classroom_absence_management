# Makefile for Docker Compose management

# Default environment file
ENV_FILE=.env

# Docker Compose command
DC=docker-compose

# Services
WEB_SERVICE=web
DB_SERVICE=db

# Default target: up the docker containers
up:
	@echo "Starting Docker Compose services..."
	@$(DC) --env-file $(ENV_FILE) up --build -d

# Bring down the services
down:
	@echo "Stopping Docker Compose services..."
	@$(DC) down

# View logs from the web service
logs:
	@echo "Viewing logs from web service..."
	@$(DC) logs -f $(WEB_SERVICE)

# Run migrations after the containers are up
migrate:
	@echo "Running migrations..."
	@$(DC) exec $(WEB_SERVICE) python manage.py migrate

# Build Docker containers without starting them
build:
	@echo "Building Docker containers..."
	@$(DC) build

# Clean up containers, networks, and volumes
clean:
	@echo "Cleaning up Docker containers, networks, and volumes..."
	@$(DC) down --volumes --remove-orphans

# Create a superuser (useful for setting up Django admin)
createsuperuser:
	@echo "Creating Django superuser..."
	@$(DC) exec $(WEB_SERVICE) python manage.py createsuperuser

# Check if Docker Compose is running
status:
	@echo "Checking Docker Compose status..."
	@$(DC) ps

# Show Docker Compose configuration
config:
	@echo "Displaying Docker Compose configuration..."
	@$(DC) config
