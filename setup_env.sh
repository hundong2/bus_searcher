#!/bin/bash

# Python 3.13 가상환경 설정 스크립트
echo "현재 Python 버전 확인 중..."
python3 --version

echo "기존 가상환경 백업 중..."
if [ -d "venv" ]; then
    mv venv venv_backup_$(date +%Y%m%d_%H%M%S)
fi

echo "Python 3.13으로 새 가상환경 생성 중..."
# pyenv가 설치된 경우
if command -v pyenv &> /dev/null; then
    pyenv install 3.13.0
    pyenv local 3.13.0
    python3 -m venv venv
else
    # Homebrew Python 3.13 사용
    /opt/homebrew/bin/python3.13 -m venv venv
fi

echo "가상환경 활성화 및 패키지 설치..."
source venv/bin/activate
pip install --upgrade pip
pip install -e .

echo "설정 완료! 다음 명령어로 가상환경을 활성화하세요:"
echo "source venv/bin/activate"
