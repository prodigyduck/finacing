"""Tests for Holding entity"""
import pytest
from decimal import Decimal
from src.domain.entities.holding import Holding


def test_holding_creation_valid():
    """유효한 종목 생성"""
    holding = Holding(symbol="삼성전자")
    assert holding.symbol == "삼성전자"


def test_holding_creation_with_quantity():
    """수량 포함 종목 생성"""
    holding = Holding(symbol="삼성전자", quantity=10)
    assert holding.symbol == "삼성전자"
    assert holding.quantity == 10


def test_holding_creation_with_prices():
    """가격 포함 종목 생성"""
    holding = Holding(
        symbol="삼성전자",
        purchase_price=Decimal("80000"),
        current_price=Decimal("85000")
    )
    assert holding.symbol == "삼성전자"
    assert holding.purchase_price == Decimal("80000")
    assert holding.current_price == Decimal("85000")


def test_holding_creation_invalid_empty_symbol():
    """빈 종목명으로 생성 실패"""
    with pytest.raises(ValueError, match="종목명은 비어있을 수 없습니다"):
        Holding(symbol="")


def test_holding_creation_invalid_whitespace_symbol():
    """공백만 있는 종목명으로 생성 실패"""
    with pytest.raises(ValueError, match="종목명은 비어있을 수 없습니다"):
        Holding(symbol="   ")


def test_holding_immutability():
    """Holding 엔티티 불변성 확인"""
    holding = Holding(symbol="삼성전자")
    with pytest.raises(AttributeError):
        holding.symbol = "NAVER"
