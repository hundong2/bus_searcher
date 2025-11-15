# Bus Searcher API

A FastAPI-based REST API for searching and managing bus routes and stops.

## Features

- 🚌 Search bus routes by origin, destination, or route number
- 🚏 Browse bus stops and their locations
- 🔍 Full-text search across all route information
- 📚 Interactive API documentation (Swagger UI)
- 🐳 Docker support for easy deployment
- ✅ Comprehensive test coverage

## Requirements

- Python 3.8 or higher
- pip

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/hundong2/bus_searcher.git
cd bus_searcher
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Development Installation

Install with development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Option 3: Build and Install as Package

```bash
pip install build
python -m build
pip install dist/bus_searcher-0.1.0-py3-none-any.whl
```

## Running the Application

### Local Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker

Build and run with Docker:
```bash
docker build -t bus-searcher .
docker run -p 8000:8000 bus-searcher
```

Or use Docker Compose:
```bash
docker-compose up
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## API Endpoints

### General
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Routes
- `GET /routes` - Get all bus routes (supports filtering by origin and destination)
- `GET /routes/{route_id}` - Get a specific route by ID

### Stops
- `GET /stops` - Get all bus stops (supports filtering by name)
- `GET /stops/{stop_id}` - Get a specific stop by ID

### Search
- `GET /search?query={query}` - Search for routes by any field

## Example API Calls

```bash
# Get all routes
curl http://localhost:8000/routes

# Get routes from Downtown
curl http://localhost:8000/routes?origin=Downtown

# Get a specific route
curl http://localhost:8000/routes/1

# Search for routes containing "Airport"
curl http://localhost:8000/search?query=Airport

# Get all bus stops
curl http://localhost:8000/stops

# Health check
curl http://localhost:8000/health
```

## Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

Run specific test file:
```bash
pytest tests/test_main.py
```

## Building the Package

To build the package for distribution:

```bash
pip install build
python -m build
```

This will create distribution files in the `dist/` directory:
- `bus_searcher-0.1.0-py3-none-any.whl` (wheel format)
- `bus_searcher-0.1.0.tar.gz` (source distribution)

## Project Structure

```
bus_searcher/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application and endpoints
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Test suite
├── .gitignore
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── LICENSE
├── pyproject.toml       # Package configuration
├── README.md
├── requirements.txt     # Production dependencies
└── requirements-dev.txt # Development dependencies
```

## Development

### Code Style

The project follows PEP 8 style guidelines. Format your code before committing.

### Adding New Routes

1. Add your endpoint in `app/main.py`
2. Add corresponding tests in `tests/test_main.py`
3. Run tests to ensure everything works
4. Update this README if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.