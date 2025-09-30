.PHONY: help install clean test lint format ingest api bot full docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies with Poetry"
	@echo "  clean        - Clean cache and temporary files"
	@echo "  test         - Run test suite"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black and isort"
	@echo "  ingest       - Index seed data"
	@echo "  api          - Start API server"
	@echo "  bot          - Start Telegram bot"
	@echo "  full         - Complete setup and run (ingest + api + bot)"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-up    - Start with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose services"

# Development setup
install:
	poetry install

clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf .coverage
	rm -rf htmlcov/

# Code quality
test:
	poetry run pytest src/tests/ -v

lint:
	poetry run ruff check src/
	poetry run black --check src/

format:
	poetry run black src/
	poetry run isort src/
	poetry run ruff check --fix src/

# Application commands
ingest:
	python run.py ingest

api:
	python run.py api

bot:
	python run.py bot

full:
	python run.py full

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

# Production helpers
check-env:
	@test -f .env || (echo "❌ .env file not found. Copy .env.example to .env and configure it." && exit 1)
	@echo "✅ Environment file found"

validate: check-env lint test
	@echo "✅ All validations passed"

# Install development hooks
install-hooks:
	poetry run pre-commit install

# Database management
reset-db:
	rm -f admissions.db
	rm -rf src/rag/index/*
	@echo "🗑️  Database and index cleared"