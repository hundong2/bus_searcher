"""Main FastAPI application for bus searcher."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Bus Searcher API",
    description="API for searching and managing bus routes",
    version="0.1.0"
)


class BusRoute(BaseModel):
    """Bus route model."""
    id: int
    route_number: str
    origin: str
    destination: str
    stops: List[str]


class BusStop(BaseModel):
    """Bus stop model."""
    id: int
    name: str
    location: str


# Sample data for demonstration
bus_routes = [
    {
        "id": 1,
        "route_number": "101",
        "origin": "Downtown",
        "destination": "Airport",
        "stops": ["Downtown", "Main Street", "Park Avenue", "Airport"]
    },
    {
        "id": 2,
        "route_number": "202",
        "origin": "University",
        "destination": "Mall",
        "stops": ["University", "Library", "Shopping District", "Mall"]
    }
]

bus_stops = [
    {"id": 1, "name": "Downtown", "location": "City Center"},
    {"id": 2, "name": "Main Street", "location": "Business District"},
    {"id": 3, "name": "Park Avenue", "location": "Residential Area"},
    {"id": 4, "name": "Airport", "location": "International Airport"}
]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Bus Searcher API",
        "version": "0.1.0",
        "endpoints": {
            "routes": "/routes",
            "stops": "/stops",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/routes", response_model=List[BusRoute])
async def get_routes(origin: Optional[str] = None, destination: Optional[str] = None):
    """Get all bus routes, optionally filtered by origin and destination."""
    filtered_routes = bus_routes
    
    if origin:
        filtered_routes = [r for r in filtered_routes if r["origin"].lower() == origin.lower()]
    
    if destination:
        filtered_routes = [r for r in filtered_routes if r["destination"].lower() == destination.lower()]
    
    return filtered_routes


@app.get("/routes/{route_id}", response_model=BusRoute)
async def get_route(route_id: int):
    """Get a specific bus route by ID."""
    for route in bus_routes:
        if route["id"] == route_id:
            return route
    raise HTTPException(status_code=404, detail="Route not found")


@app.get("/stops", response_model=List[BusStop])
async def get_stops(name: Optional[str] = None):
    """Get all bus stops, optionally filtered by name."""
    filtered_stops = bus_stops
    
    if name:
        filtered_stops = [s for s in filtered_stops if name.lower() in s["name"].lower()]
    
    return filtered_stops


@app.get("/stops/{stop_id}", response_model=BusStop)
async def get_stop(stop_id: int):
    """Get a specific bus stop by ID."""
    for stop in bus_stops:
        if stop["id"] == stop_id:
            return stop
    raise HTTPException(status_code=404, detail="Stop not found")


@app.get("/search")
async def search_routes(query: str):
    """Search for routes by any field."""
    results = []
    query_lower = query.lower()
    
    for route in bus_routes:
        if (query_lower in route["route_number"].lower() or
            query_lower in route["origin"].lower() or
            query_lower in route["destination"].lower() or
            any(query_lower in stop.lower() for stop in route["stops"])):
            results.append(route)
    
    return {"query": query, "results": results, "count": len(results)}
