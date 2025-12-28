.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs

help:
	@echo "Studium Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make dev          - Set up development environment"
	@echo ""
	@echo "Development:"
	@echo "  make run          - Run the API server"
	@echo "  make worker       - Run Celery worker"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black and ruff"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start all services with Docker Compose"
	@echo "  make docker-down  - Stop all services"
	@echo "  make docker-logs  - Show Docker logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove build artifacts and cache files"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

dev:
	cp -n .env.example .env || true
	@echo "Development environment set up. Edit .env with your configuration."

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	celery -A app.celery_worker.celery_app worker --loglevel=info

test:
	pytest -v --cov=app --cov-report=term-missing

lint:
	ruff check app tests
	mypy app

format:
	black app tests
	ruff check --fix app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ .coverage htmlcov/

docker-build:
	docker compose build

docker-up:
	docker compose up -d
	@echo ""
	@echo "Services started:"
	@echo "  API:            http://localhost:8000"
	@echo "  API Docs:       http://localhost:8000/docs"
	@echo "  MinIO Console:  http://localhost:9001"
	@echo "  Flower:         http://localhost:5555"

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-clean:
	docker compose down -v
	docker system prune -f
