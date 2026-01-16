# Thalos Prime - Makefile
# Development automation tasks

.PHONY: help install install-dev test test-unit test-integration coverage lint format type-check clean docker-build docker-run

help:
	@echo "Thalos Prime - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make coverage       - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run linters (flake8, pylint)"
	@echo "  make format         - Format code (black, isort)"
	@echo "  make type-check     - Run type checker (mypy)"
	@echo "  make check-all      - Run all quality checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove build artifacts and caches"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v -m unit

test-integration:
	pytest tests/integration/ -v -m integration

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

lint:
	@echo "Running flake8..."
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	@echo "Running pylint..."
	pylint src/ --max-line-length=100 --disable=C0103,C0114,C0115,C0116,R0903,R0913

format:
	@echo "Running black..."
	black src/ tests/ --line-length=100
	@echo "Running isort..."
	isort src/ tests/ --profile black --line-length=100

type-check:
	mypy src/ --ignore-missing-imports

check-all: lint type-check test
	@echo "All checks passed!"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	@echo "Cleanup complete!"

docker-build:
	docker build -t thalos-prime:latest .

docker-run:
	docker run -p 8000:8000 thalos-prime:latest

# Development server
dev-web:
	python src/interfaces/web/web_server.py

dev-cli:
	python src/main.py

# Database setup (if needed)
db-init:
	@echo "Initializing database..."
	mkdir -p data
	@echo "Database directory created"

# Quick validation
validate: format lint type-check test
	@echo "Validation complete - all checks passed!"
