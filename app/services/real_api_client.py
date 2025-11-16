"""경기도공공데이터 포털 실제 API 클라이언트."""

import httpx
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)


class RealBusAPIClient:
    """경기도공공데이터 포털 Open API 클라이언트."""
    
    def __init__(self):
        self.api_key = os.getenv("BUSINFO_API_KEY", "")
        # 경기버스정보 API 엔드포인트
        self.base_url = "http://openapi.gbis.go.kr/ws/rest"
        self.timeout = 30.0
    
    async def get_stops_in_area(self, lat_min: float, lat_max: float, 
                                lon_min: float, lon_max: float) -> List[Dict[str, Any]]:
        """
        특정 지역의 정류소 목록 조회.
        
        경기버스정보 API의 정류소검색 엔드포인트 사용.
        """
        try:
            stops = []
            
            # 판교동 지역을 그리드로 나누어 조회
            lat_step = (lat_max - lat_min) / 2
            lon_step = (lon_max - lon_min) / 2
            
            for lat in [lat_min, lat_min + lat_step]:
                for lon in [lon_min, lon_min + lon_step]:
                    region_stops = await self._search_stops_by_coordinate(
                        lat, lon
                    )
                    stops.extend(region_stops)
            
            # 중복 제거
            unique_stops = {stop["stationId"]: stop for stop in stops}
            return list(unique_stops.values())
            
        except Exception as e:
            logger.error(f"정류소 조회 오류: {str(e)}")
            return []
    
    async def _search_stops_by_coordinate(self, latitude: float, 
                                         longitude: float) -> List[Dict[str, Any]]:
        """
        좌표 기반 정류소 검색.
        
        API 엔드포인트: /stationinfo/getStationByPolyline
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "apiKey": self.api_key,
                    "lat": latitude,
                    "lon": longitude,
                    "radius": 1000  # 반경 1km
                }
                
                response = await client.get(
                    f"{self.base_url}/stationinfo/getStationByPolyline",
                    params=params
                )
                
                if response.status_code == 200:
                    return self._parse_stop_response(response.text)
                else:
                    logger.warning(f"API 응답 오류: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"좌표 기반 검색 오류: {str(e)}")
            return []
    
    async def get_stop_info(self, station_id: str) -> Dict[str, Any]:
        """
        특정 정류소의 상세 정보 조회.
        
        API 엔드포인트: /stationinfo/getStationWithBusLisInfo
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "apiKey": self.api_key,
                    "stationId": station_id
                }
                
                response = await client.get(
                    f"{self.base_url}/stationinfo/getStationWithBusLisInfo",
                    params=params
                )
                
                if response.status_code == 200:
                    return self._parse_stop_info_response(response.text)
                else:
                    logger.warning(f"정류소 정보 조회 실패: {station_id}")
                    return {}
                    
        except Exception as e:
            logger.error(f"정류소 정보 조회 오류: {str(e)}")
            return {}
    
    async def get_route_info(self, route_id: str) -> Dict[str, Any]:
        """
        특정 노선의 상세 정보 조회.
        
        API 엔드포인트: /routeinfo/getRouteWithStationList
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "apiKey": self.api_key,
                    "routeId": route_id
                }
                
                response = await client.get(
                    f"{self.base_url}/routeinfo/getRouteWithStationList",
                    params=params
                )
                
                if response.status_code == 200:
                    return self._parse_route_response(response.text)
                else:
                    return {}
                    
        except Exception as e:
            logger.error(f"노선 정보 조회 오류: {str(e)}")
            return {}
    
    def _parse_stop_response(self, xml_response: str) -> List[Dict[str, Any]]:
        """XML 응답을 파싱하여 정류소 목록 반환."""
        stops = []
        try:
            root = ET.fromstring(xml_response)
            
            for item in root.findall(".//busStationList"):
                stop = {
                    "stationId": item.findtext("stationId", ""),
                    "stationName": item.findtext("stationName", ""),
                    "latitude": float(item.findtext("latitude", 0)),
                    "longitude": float(item.findtext("longitude", 0)),
                    "busRouteCount": int(item.findtext("busRouteCount", 0))
                }
                if stop["stationId"]:
                    stops.append(stop)
                    
        except Exception as e:
            logger.error(f"XML 파싱 오류: {str(e)}")
        
        return stops
    
    def _parse_stop_info_response(self, xml_response: str) -> Dict[str, Any]:
        """정류소 상세 정보 XML 파싱."""
        try:
            root = ET.fromstring(xml_response)
            
            station_info = {
                "stationId": root.findtext(".//stationId", ""),
                "stationName": root.findtext(".//stationName", ""),
                "latitude": float(root.findtext(".//latitude", 0)),
                "longitude": float(root.findtext(".//longitude", 0)),
            }
            
            # 운행 노선 정보
            routes = []
            for route in root.findall(".//busRouteList"):
                routes.append({
                    "routeId": route.findtext("routeId", ""),
                    "routeName": route.findtext("routeName", ""),
                    "routeType": route.findtext("routeTypeCd", ""),
                })
            station_info["routes"] = routes
            
            return station_info
            
        except Exception as e:
            logger.error(f"정류소 정보 파싱 오류: {str(e)}")
            return {}
    
    def _parse_route_response(self, xml_response: str) -> Dict[str, Any]:
        """노선 정보 XML 파싱."""
        try:
            root = ET.fromstring(xml_response)
            
            route_info = {
                "routeId": root.findtext(".//routeId", ""),
                "routeName": root.findtext(".//routeName", ""),
                "routeTypeCd": root.findtext(".//routeTypeCd", ""),
                "startStationName": root.findtext(".//startStationName", ""),
                "endStationName": root.findtext(".//endStationName", ""),
            }
            
            # 경유 정류소 목록
            stations = []
            for station in root.findall(".//stationList"):
                stations.append({
                    "stationId": station.findtext("stationId", ""),
                    "stationName": station.findtext("stationName", ""),
                    "sequence": int(station.findtext("sequence", 0)),
                })
            route_info["stations"] = stations
            
            return route_info
            
        except Exception as e:
            logger.error(f"노선 정보 파싱 오류: {str(e)}")
            return {}
