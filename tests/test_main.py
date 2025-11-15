"""Tests for main FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to Bus Searcher API"
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_routes():
    """Test getting all routes."""
    response = client.get("/routes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "route_number" in data[0]
    assert "origin" in data[0]
    assert "destination" in data[0]


def test_get_routes_filtered_by_origin():
    """Test getting routes filtered by origin."""
    response = client.get("/routes?origin=Downtown")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(route["origin"] == "Downtown" for route in data)


def test_get_routes_filtered_by_destination():
    """Test getting routes filtered by destination."""
    response = client.get("/routes?destination=Airport")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(route["destination"] == "Airport" for route in data)


def test_get_route_by_id():
    """Test getting a specific route by ID."""
    response = client.get("/routes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "route_number" in data
    assert "stops" in data


def test_get_route_not_found():
    """Test getting a non-existent route."""
    response = client.get("/routes/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_get_stops():
    """Test getting all stops."""
    response = client.get("/stops")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "location" in data[0]


def test_get_stops_filtered_by_name():
    """Test getting stops filtered by name."""
    response = client.get("/stops?name=Downtown")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("Downtown" in stop["name"] for stop in data)


def test_get_stop_by_id():
    """Test getting a specific stop by ID."""
    response = client.get("/stops/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


def test_get_stop_not_found():
    """Test getting a non-existent stop."""
    response = client.get("/stops/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_search_routes():
    """Test search functionality."""
    response = client.get("/search?query=Downtown")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert "count" in data
    assert data["query"] == "Downtown"
    assert isinstance(data["results"], list)


def test_search_routes_by_route_number():
    """Test search by route number."""
    response = client.get("/search?query=101")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert any(route["route_number"] == "101" for route in data["results"])
