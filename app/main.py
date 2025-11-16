"""Main FastAPI application for bus searcher."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.api import statistics, real_statistics
from app.database import models
from app.database.config import engine
import logging
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bus Searcher API",
    description="API for searching and managing bus routes in Pangyo-dong, Seongnam",
    version="0.1.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(statistics.router)
app.include_router(real_statistics.router)


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
        "message": "Welcome to Bus Searcher API - Pangyo-dong Statistics",
        "version": "0.1.0",
        "endpoints": {
            "mock_data": {
                "stops": "/api/statistics/stops",
                "weekly_ridership": "/api/statistics/weekly/{stop_id}",
            },
            "real_api": {
                "fetch_stops": "/api/real/fetch-stops",
                "saved_stops": "/api/real/stops",
                "stop_detail": "/api/real/stops/{stop_id}/info",
                "route_detail": "/api/real/routes/{route_id}/info",
            },
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
