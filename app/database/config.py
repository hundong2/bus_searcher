"""데이터베이스 설정."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 환경 변수에서 DB URL 가져오기
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./bus_statistics.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """데이터베이스 세션 생성."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
