"""경기버스정보 API 클라이언트."""

import httpx
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class BusAPIClient:
    """경기버스정보 Open API 클라이언트."""
    
    def __init__(self):
        self.api_key = os.getenv("BUSINFO_API_KEY", "test_key")
        self.base_url = os.getenv("BUSINFO_API_BASE_URL", "https://www.api.bus.go.kr")
        self.timeout = 10.0
    
    async def get_stops_in_area(self, lat_min: float, lat_max: float, 
                                lon_min: float, lon_max: float) -> List[Dict[str, Any]]:
        """특정 지역의 정류소 목록 조회."""
        try:
            # 실제 API 호출 (테스트용 목데이터 반환)
            stops = await self._fetch_mock_stops()
            return stops
        except Exception as e:
            print(f"API 오류: {str(e)}")
            return []
    
    async def get_stop_ridership(self, stop_id: str) -> Dict[str, Any]:
        """정류소의 이용자 수 정보 조회."""
        try:
            ridership_data = await self._fetch_mock_ridership(stop_id)
            return ridership_data
        except Exception as e:
            print(f"API 오류: {str(e)}")
            return {}
    
    async def _fetch_mock_stops(self) -> List[Dict[str, Any]]:
        """목데이터: 판교동 정류소 목록."""
        return [
            {
                "stop_id": "22000001",
                "stop_name": "판교역 1번출구",
                "latitude": 37.3950,
                "longitude": 127.1100,
            },
            {
                "stop_id": "22000002",
                "stop_name": "판교역 2번출구",
                "latitude": 37.3951,
                "longitude": 127.1101,
            },
            {
                "stop_id": "22000003",
                "stop_name": "삼성전자 남문",
                "latitude": 37.3975,
                "longitude": 127.1125,
            },
            {
                "stop_id": "22000004",
                "stop_name": "판교 테크원",
                "latitude": 37.4000,
                "longitude": 127.1150,
            },
        ]
    
    async def _fetch_mock_ridership(self, stop_id: str) -> Dict[str, Any]:
        """목데이터: 정류소별 이용자 수."""
        import random
        from datetime import datetime, timedelta
        
        # 최근 7일 데이터 생성
        ridership_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_count = random.randint(100, 500)
            ridership_data.append({
                "date": date,
                "stop_id": stop_id,
                "passenger_count": daily_count,
                "peak_hour": random.randint(7, 9),
            })
        
        return {
            "stop_id": stop_id,
            "week_data": ridership_data,
            "total_count": sum(d["passenger_count"] for d in ridership_data),
            "average_daily": sum(d["passenger_count"] for d in ridership_data) // 7,
        }
