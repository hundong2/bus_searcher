"""SQLAlchemy 데이터베이스 모델."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BusStop(Base):
    """버스 정류소 모델."""
    __tablename__ = "bus_stops"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String, unique=True, index=True, nullable=False)
    station_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    bus_route_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BusRoute(Base):
    """버스 노선 모델."""
    __tablename__ = "bus_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String, unique=True, index=True, nullable=False)
    route_name = Column(String, nullable=False)
    route_type = Column(String, nullable=False)
    start_station = Column(String, nullable=False)
    end_station = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RidershipData(Base):
    """정류소별 이용자 데이터 모델."""
    __tablename__ = "ridership_data"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String, ForeignKey("bus_stops.station_id"), index=True)
    date = Column(String, index=True, nullable=False)  # YYYY-MM-DD
    hour = Column(Integer, nullable=True)  # 0-23
    passenger_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
