import pytest
from pathlib import Path

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"


@pytest.fixture
def sample_investment_note_text():
    """샘플 투자 메모 텍스트 (Google Keep 형식)"""
    return """
주식 삼성전자 100주 85000원
주식 카카오 50주 65000원
현금 1000000원
ETF TIGER 200 30주 25000원
"""


@pytest.fixture
def parsed_assets():
    """파싱된 샘플 자산 데이터"""
    return [
        {"name": "삼성전자", "type": "주식", "quantity": 100, "unit_price": 85000},
        {"name": "카카오", "type": "주식", "quantity": 50, "unit_price": 65000},
        {"name": "현금", "type": "현금", "quantity": 1, "unit_price": 1000000},
        {"name": "TIGER 200", "type": "ETF", "quantity": 30, "unit_price": 25000},
    ]
