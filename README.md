# 판교동 버스 정류소 이용자 통계 분석 시스템

경기도 성남시 판교동의 버스 정류소별 이용자 수 통계를 수집, 분석, 시각화하는 웹 애플리케이션입니다.

## https://openapigits.gg.go.kr/api/rest/getRoadInfoList?serviceKey=인증키
## https://openapigits.gg.go.kr/api/jsp/openApi_info.jsp


## 📋 프로젝트 개요

### 목표
- 판교동 내 버스 정류소별 이용자 수 데이터 수집 및 저장
- 시간대별, 요일별, 월별 이용 패턴 분석
- 직관적인 대시보드를 통한 데이터 시각화
- 정류소별 이용률 비교 및 최적화 제안

### 핵심 기능
1. **데이터 수집**
   - 경기버스정보 Open API 연동
   - 정류소별 실시간 승하차 데이터
   - 시계열 데이터 DB 저장

2. **통계 분석**
   - 시간대별 이용자 수 분석
   - 요일별/계절별 패턴 분석
   - 정류소 인기도 랭킹
   - 노선별 이용 현황

3. **시각화 대시보드**
   - 실시간 정류소 현황 모니터링
   - 히트맵 및 차트 분석
   - 시계열 트렌드 그래프

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **Backend** | FastAPI, Python 3.13 |
| **Database** | SQLite (개발), PostgreSQL (프로덕션) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Chart.js |
| **Frontend** | HTML5, Vue.js 또는 React |
| **API** | 경기버스정보 Open API |
| **배포** | Docker, AWS/GCP |

## 📦 필요한 의존성

```
# 데이터 처리
pandas>=2.0.0
numpy>=1.24.0

# 시각화
plotly>=5.17.0
matplotlib>=3.7.0

# 데이터베이스
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# HTTP 요청
httpx>=0.27.0
requests>=2.31.0

# 스케줄링 (데이터 수집)
APScheduler>=3.10.0

# 환경 변수
python-dotenv>=1.0.0
```

## 📅 개발 단계

### Phase 1: 기초 설정 (1주)
- [x] 프로젝트 구조 설계
- [ ] 데이터베이스 스키마 설계
- [ ] API 명세 작성

### Phase 2: 백엔드 개발 (2주)
- [ ] 경기버스정보 API 연동
- [ ] 정류소/이용자 데이터 모델 구축
- [ ] CRUD API 엔드포인트 작성
- [ ] 데이터 수집 스케줄러 구현

### Phase 3: 데이터 분석 (1.5주)
- [ ] 통계 분석 모듈 개발
- [ ] 시간대별/요일별 분석 로직
- [ ] 이상 탐지 알고리즘

### Phase 4: 프론트엔드 (1.5주)
- [ ] 대시보드 UI 설계
- [ ] 차트 및 히트맵 구현
- [ ] 필터링 및 검색 기능

### Phase 5: 테스트 및 배포 (1주)
- [ ] 통합 테스트
- [ ] 성능 최적화
- [ ] Docker 컨테이너화
- [ ] 배포

## 🗂️ 프로젝트 구조

```
bus_searcher/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 메인 앱
│   ├── api/
│   │   ├── routes.py           # 노선 관련 API
│   │   ├── stops.py            # 정류소 관련 API
│   │   └── statistics.py       # 통계 분석 API
│   ├── models/
│   │   ├── bus_stop.py         # 정류소 데이터 모델
│   │   ├── ridership.py        # 이용자 수 데이터 모델
│   │   └── statistics.py       # 통계 모델
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py           # DB 설정
│   │   └── models.py           # SQLAlchemy 모델
│   ├── services/
│   │   ├── api_client.py       # 경기버스정보 API 클라이언트
│   │   ├── data_collector.py   # 데이터 수집 서비스
│   │   └── analyzer.py         # 통계 분석 서비스
│   └── utils/
│       └── scheduler.py        # 작업 스케줄러
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── test_models.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── statistics.html
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 🚀 설치 및 실행

### 필수 조건
- Python 3.13
- pip 또는 poetry

### 설치 방법

```bash
# 1. 저장소 클론
cd /Users/donghun2/workspace/bus_searcher

# 2. 가상환경 생성 (Python 3.13)
python3.13 -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install -e .
pip install -e ".[dev]"

# 4. 환경 변수 설정
cp .env.example .env

# 5. 데이터베이스 초기화
python -m app.database.init

# 6. 서버 실행
uvicorn app.main:app --reload
```

### 접속 방법
- API 문서: http://localhost:8000/docs
- 대시보드: http://localhost:8000/dashboard
- 통계: http://localhost:8000/statistics

## 📊 데이터 소스

### 경기버스정보 Open API
- **제공처**: 경기도청 공공데이터포털
- **엔드포인트**: https://www.api.bus.go.kr
- **인증**: API Key 필요
- **데이터**: 실시간 버스 위치, 정류소 정보, 도착 예정 시간

### 판교동 정류소 범위
- 위도: 37.3940 ~ 37.4050
- 경도: 127.1050 ~ 127.1200
- 대상 정류소: 약 45개

## 🔑 API 키 설정

```bash
# .env 파일에 추가
BUSINFO_API_KEY=your_api_key_here
DB_URL=sqlite:///./bus_statistics.db
SCHEDULER_ENABLED=true
DATA_COLLECTION_INTERVAL=300  # 5분마다 수집
```

## 📈 주요 분석 지표

1. **이용자 수 통계**
   - 정류소별 일일 이용자 수
   - 시간대별 피크 시간대
   - 요일별 패턴 (평일 vs 주말)

2. **정류소 성능**
   - 이용률 상위/하위 정류소
   - 월별 이용자 수 증감률
   - 노선별 이용 현황

3. **트렌드 분석**
   - 계절별 이용 패턴
   - 특정 이벤트의 영향 분석
   - 예측 모델

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app --cov-report=html

# 특정 테스트 파일 실행
pytest tests/test_api.py -v
```

## 🐳 Docker 배포

```bash
# 이미지 빌드
docker build -t bus-searcher:0.1.0 .

# 컨테이너 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## 📝 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/api/stops` | 모든 정류소 조회 |
| GET | `/api/stops/{stop_id}` | 특정 정류소 상세 조회 |
| GET | `/api/statistics/stops` | 정류소별 이용자 통계 |
| GET | `/api/statistics/hourly` | 시간대별 통계 |
| GET | `/api/statistics/daily` | 일일 통계 |
| GET | `/api/statistics/top-stops` | 상위 정류소 랭킹 |

## 🤝 기여 가이드

1. Feature 브랜치 생성: `git checkout -b feature/새기능`
2. 커밋: `git commit -am '기능 추가'`
3. 푸시: `git push origin feature/새기능`
4. Pull Request 생성

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 📞 문의

프로젝트 관련 질문사항은 Issues에서 등록해주세요.