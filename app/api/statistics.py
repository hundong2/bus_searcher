"""통계 분석 API 엔드포인트."""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.api_client import BusAPIClient
from app.models.ridership import WeeklyRidership, StopInfo, DailyRidership

router = APIRouter(prefix="/api/statistics", tags=["statistics"])

# API 클라이언트 인스턴스
api_client = BusAPIClient()


@router.get("/stops", response_model=List[StopInfo], summary="판교동 정류소 목록")
async def get_pangyeo_stops():
    """
    판교동의 모든 버스 정류소 조회
    
    - 판교동 좌표 범위 내의 정류소 정보 반환
    - 정류소 ID, 이름, 위치 정보 포함
    """
    lat_min = 37.3940
    lat_max = 37.4050
    lon_min = 127.1050
    lon_max = 127.1200
    
    stops = await api_client.get_stops_in_area(lat_min, lat_max, lon_min, lon_max)
    
    if not stops:
        raise HTTPException(status_code=404, detail="정류소 정보를 찾을 수 없습니다")
    
    return [
        StopInfo(
            stop_id=stop["stop_id"],
            stop_name=stop["stop_name"],
            latitude=stop["latitude"],
            longitude=stop["longitude"]
        )
        for stop in stops
    ]


@router.get("/weekly/{stop_id}", response_model=WeeklyRidership, summary="정류소 주간 이용자 통계")
async def get_weekly_ridership(stop_id: str):
    """
    특정 정류소의 최근 1주일 이용자 통계 조회
    
    - 일별 이용자 수 데이터
    - 주간 총 이용자 수
    - 일평균 이용자 수
    - 피크 시간대 정보
    """
    ridership = await api_client.get_stop_ridership(stop_id)
    
    if not ridership:
        raise HTTPException(status_code=404, detail="해당 정류소의 데이터를 찾을 수 없습니다")
    
    week_data = [
        DailyRidership(**data)
        for data in ridership.get("week_data", [])
    ]
    
    return WeeklyRidership(
        stop_id=stop_id,
        week_data=week_data,
        total_count=ridership.get("total_count", 0),
        average_daily=ridership.get("average_daily", 0)
    )


@router.get("/top-stops", response_model=List[WeeklyRidership], summary="상위 정류소 랭킹")
async def get_top_stops(limit: int = 5):
    """
    이용자 수가 많은 상위 정류소 조회
    
    - limit: 조회할 상위 정류소 개수 (기본값: 5)
    - 각 정류소의 주간 이용자 통계 반환
    """
    stops = await api_client.get_stops_in_area(37.3940, 37.4050, 127.1050, 127.1200)
    
    if not stops:
        raise HTTPException(status_code=404, detail="정류소 정보를 찾을 수 없습니다")
    
    # 각 정류소의 이용자 수 조회
    top_stops_data = []
    for stop in stops[:limit]:
        ridership = await api_client.get_stop_ridership(stop["stop_id"])
        if ridership:
            week_data = [
                DailyRidership(**data)
                for data in ridership.get("week_data", [])
            ]
            top_stops_data.append(WeeklyRidership(
                stop_id=stop["stop_id"],
                stop_name=stop["stop_name"],
                week_data=week_data,
                total_count=ridership.get("total_count", 0),
                average_daily=ridership.get("average_daily", 0)
            ))
    
    # 총 이용자 수로 정렬
    top_stops_data.sort(key=lambda x: x.total_count, reverse=True)
    
    return top_stops_data[:limit]


@router.get("/summary", summary="판교동 통계 요약")
async def get_summary():
    """
    판교동 전체 통계 요약
    
    - 전체 정류소 개수
    - 전체 주간 이용자 수
    - 가장 이용량이 많은 정류소
    - 평균 이용자 수
    """
    stops = await api_client.get_stops_in_area(37.3940, 37.4050, 127.1050, 127.1200)
    
    if not stops:
        raise HTTPException(status_code=404, detail="정류소 정보를 찾을 수 없습니다")
    
    total_ridership = 0
    max_ridership = 0
    top_stop_name = ""
    
    for stop in stops:
        ridership = await api_client.get_stop_ridership(stop["stop_id"])
        if ridership:
            count = ridership.get("total_count", 0)
            total_ridership += count
            if count > max_ridership:
                max_ridership = count
                top_stop_name = stop["stop_name"]
    
    return {
        "total_stops": len(stops),
        "total_weekly_ridership": total_ridership,
        "top_stop": {
            "name": top_stop_name,
            "weekly_count": max_ridership
        },
        "average_per_stop": total_ridership // len(stops) if stops else 0,
        "period": "Last 7 days"
    }
