.PHONY: help install install-dev run test build clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make run          - Run the FastAPI application"
	@echo "  make test         - Run tests"
	@echo "  make build        - Build the Python package"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

build:
	pip install build
	python -m build

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +

docker-build:
	docker build -t bus-searcher .

docker-run:
	docker run -p 8000:8000 bus-searcher
