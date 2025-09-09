# Media Management Bot - Makefile
# This Makefile provides convenient commands for development and deployment

.PHONY: help setup install validate clean test run docker-build docker-up docker-down docker-logs monitor

# Default target
help:
	@echo "Media Management Bot - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup          - Interactive setup (creates directories, .env file)"
	@echo "  install        - Install Python dependencies"
	@echo "  validate       - Validate configuration"
	@echo ""
	@echo "Development:"
	@echo "  run            - Run the bot locally"
	@echo "  test           - Run tests"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-up      - Start all services with Docker Compose"
	@echo "  docker-down    - Stop all Docker services"
	@echo "  docker-logs    - View Docker logs"
	@echo "  docker-shell   - Open shell in bot container"
	@echo ""
	@echo "MongoDB Database:"
	@echo "  db-setup       - Setup MongoDB interactively"
	@echo "  db-init        - Initialize MongoDB database"
	@echo "  db-test        - Test MongoDB connection"
	@echo "  db-reset       - Reset MongoDB database (WARNING: destroys data)"
	@echo ""
	@echo "Monitoring:"
	@echo "  monitor        - Start monitoring stack (Prometheus + Grafana)"
	@echo "  monitor-down   - Stop monitoring stack"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          - Clean temporary files and caches"
	@echo "  backup         - Backup database and media files"
	@echo "  logs           - View bot logs"

# Setup and Installation
setup:
	@echo "🚀 Setting up Media Management Bot..."
	python3 scripts/setup.py

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

validate:
	@echo "🔍 Validating configuration..."
	python3 scripts/validate_config.py

# Development
run:
	@echo "🤖 Starting bot..."
	python3 bot.py

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "🎨 Formatting code..."
	black . --line-length=100
	isort . --profile black

# Docker commands
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose down

docker-logs:
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f

docker-shell:
	@echo "🐚 Opening shell in bot container..."
	docker-compose exec bot /bin/bash

# MongoDB Database commands
db-setup:
	@echo "🍃 Setting up MongoDB..."
	python3 scripts/setup_mongodb.py

db-init:
	@echo "🗄️  Initializing MongoDB database..."
	python3 -c "from config.mongodb import initialize_mongodb; initialize_mongodb()"

db-test:
	@echo "🔍 Testing MongoDB connection..."
	python3 -c "from config.mongodb import test_mongodb_connection; import json; print(json.dumps(test_mongodb_connection(), indent=2))"

db-reset:
	@echo "⚠️  WARNING: This will destroy all MongoDB data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "🗑️  Dropping all collections..."
	python3 -c "from config.mongodb import mongodb_manager; mongodb_manager.connect(); [mongodb_manager.database.drop_collection(c) for c in mongodb_manager.database.list_collection_names()]; print('All collections dropped')"

# Monitoring
monitor:
	@echo "📊 Starting monitoring stack..."
	docker-compose --profile monitoring up -d

monitor-down:
	@echo "📊 Stopping monitoring stack..."
	docker-compose --profile monitoring down

# Maintenance
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf data/temp/*

backup:
	@echo "💾 Creating backup..."
	mkdir -p backups
	tar -czf backups/backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data/ logs/ .env

logs:
	@echo "📋 Viewing bot logs..."
	tail -f logs/bot.log

# Development environment
dev-setup: setup install validate
	@echo "✅ Development environment ready!"

# Production deployment
prod-deploy: validate docker-build docker-up
	@echo "🚀 Production deployment complete!"

# Quick start for new users
quickstart:
	@echo "🚀 Quick Start Setup"
	@echo "==================="
	@make setup
	@make install
	@make validate
	@echo ""
	@echo "✅ Setup complete! Next steps:"
	@echo "1. Review your .env file"
	@echo "2. Run 'make run' to start the bot"
	@echo "3. Or run 'make docker-up' for Docker deployment"

# Health check
health:
	@echo "🏥 Health Check"
	@echo "==============="
	@python3 -c "import sys; print(f'Python: {sys.version}')"
	@docker --version 2>/dev/null || echo "Docker: Not installed"
	@docker-compose --version 2>/dev/null || echo "Docker Compose: Not installed"
	@python3 scripts/validate_config.py

# Update dependencies
update-deps:
	@echo "📦 Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip freeze > requirements.txt
