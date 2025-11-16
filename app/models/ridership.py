"""이용자 통계 데이터 모델."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DailyRidership(BaseModel):
    """일일 이용자 통계."""
    date: str
    stop_id: str
    passenger_count: int
    peak_hour: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15",
                "stop_id": "22000001",
                "passenger_count": 250,
                "peak_hour": 8
            }
        }


class WeeklyRidership(BaseModel):
    """주간 이용자 통계."""
    stop_id: str
    stop_name: Optional[str] = None
    week_data: List[DailyRidership]
    total_count: int
    average_daily: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "stop_id": "22000001",
                "stop_name": "판교역 1번출구",
                "week_data": [
                    {
                        "date": "2024-01-15",
                        "stop_id": "22000001",
                        "passenger_count": 250,
                        "peak_hour": 8
                    }
                ],
                "total_count": 1750,
                "average_daily": 250
            }
        }


class StopInfo(BaseModel):
    """정류소 정보."""
    stop_id: str
    stop_name: str
    latitude: float
    longitude: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "stop_id": "22000001",
                "stop_name": "판교역 1번출구",
                "latitude": 37.3950,
                "longitude": 127.1100
            }
        }
