"""실제 API 데이터를 사용하는 통계 분석 API."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.services.real_api_client import RealBusAPIClient
from app.database.models import BusStop, BusRoute, RidershipData
from app.database.config import get_db
from app.models.ridership import StopInfo, WeeklyRidership, DailyRidership
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/real", tags=["real-statistics"])
api_client = RealBusAPIClient()


@router.get("/fetch-stops", summary="판교동 정류소 데이터 수집")
async def fetch_pangyeo_stops(db: Session = Depends(get_db)):
    """
    경기도공공데이터 포털에서 판교동 정류소 정보를 조회하고 DB에 저장.
    
    - 좌표 범위: 37.3940~37.4050, 127.1050~127.1200
    - 결과를 데이터베이스에 저장
    """
    try:
        stops = await api_client.get_stops_in_area(
            lat_min=37.3940,
            lat_max=37.4050,
            lon_min=127.1050,
            lon_max=127.1200
        )
        
        if not stops:
            raise HTTPException(
                status_code=404,
                detail="정류소 정보를 조회할 수 없습니다. API 키를 확인하세요."
            )
        
        # 데이터베이스에 저장
        saved_count = 0
        for stop in stops:
            existing = db.query(BusStop).filter(
                BusStop.station_id == stop["stationId"]
            ).first()
            
            if existing:
                existing.station_name = stop["stationName"]
                existing.latitude = stop["latitude"]
                existing.longitude = stop["longitude"]
                existing.bus_route_count = stop.get("busRouteCount", 0)
                existing.updated_at = datetime.utcnow()
            else:
                new_stop = BusStop(
                    station_id=stop["stationId"],
                    station_name=stop["stationName"],
                    latitude=stop["latitude"],
                    longitude=stop["longitude"],
                    bus_route_count=stop.get("busRouteCount", 0)
                )
                db.add(new_stop)
            
            saved_count += 1
        
        db.commit()
        
        return {
            "message": "정류소 데이터 수집 완료",
            "total_stops": len(stops),
            "saved_stops": saved_count,
            "stops": [
                StopInfo(
                    stop_id=stop["stationId"],
                    stop_name=stop["stationName"],
                    latitude=stop["latitude"],
                    longitude=stop["longitude"]
                )
                for stop in stops
            ]
        }
        
    except Exception as e:
        logger.error(f"정류소 데이터 수집 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stops/{stop_id}/info", summary="정류소 상세 정보 조회")
async def get_stop_detail(stop_id: str):
    """
    특정 정류소의 상세 정보를 API에서 조회.
    
    - 정류소명, 위치, 운행 노선 정보 포함
    """
    try:
        stop_info = await api_client.get_stop_info(stop_id)
        
        if not stop_info:
            raise HTTPException(
                status_code=404,
                detail=f"정류소 정보를 찾을 수 없습니다: {stop_id}"
            )
        
        return stop_info
        
    except Exception as e:
        logger.error(f"정류소 상세 정보 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routes/{route_id}/info", summary="노선 상세 정보 조회")
async def get_route_detail(route_id: str):
    """
    특정 노선의 상세 정보를 API에서 조회.
    
    - 노선명, 운행 구간, 경유 정류소 정보 포함
    """
    try:
        route_info = await api_client.get_route_info(route_id)
        
        if not route_info:
            raise HTTPException(
                status_code=404,
                detail=f"노선 정보를 찾을 수 없습니다: {route_id}"
            )
        
        return route_info
        
    except Exception as e:
        logger.error(f"노선 상세 정보 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stops", response_model=List[StopInfo], summary="DB에 저장된 정류소 목록")
async def get_saved_stops(db: Session = Depends(get_db)):
    """
    데이터베이스에 저장된 판교동 정류소 목록 조회.
    
    /fetch-stops 엔드포인트로 먼저 데이터를 수집해야 합니다.
    """
    stops = db.query(BusStop).all()
    
    if not stops:
        raise HTTPException(
            status_code=404,
            detail="저장된 정류소 정보가 없습니다. /fetch-stops 엔드포인트를 먼저 호출하세요."
        )
    
    return [
        StopInfo(
            stop_id=stop.station_id,
            stop_name=stop.station_name,
            latitude=stop.latitude,
            longitude=stop.longitude
        )
        for stop in stops
    ]
