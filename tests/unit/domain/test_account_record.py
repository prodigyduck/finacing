"""Tests for AccountRecord entity"""
import pytest
from datetime import date
from decimal import Decimal
from src.domain.entities.account_record import AccountRecord
from src.domain.entities.holding import Holding


def test_account_record_creation_valid():
    """유효한 계좌 기록 생성"""
    record = AccountRecord(
        date=date(2026, 6, 3),
        account_name="증권계좌",
        total_amount_억=Decimal("3.50"),
        holdings=(Holding(symbol="삼성전자"),)
    )
    assert record.date == date(2026, 6, 3)
    assert record.account_name == "증권계좌"
    assert record.total_amount_억 == Decimal("3.50")
    assert len(record.holdings) == 1


def test_account_record_without_holdings():
    """종목 없는 계좌 기록 생성"""
    record = AccountRecord(
        date=date(2026, 6, 3),
        account_name="현금",
        total_amount_억=Decimal("0.11")
    )
    assert record.holdings == ()
    assert record.holding_count == 0


def test_account_record_negative_amount_fails():
    """음수 금액으로 생성 실패"""
    with pytest.raises(ValueError, match="계좌 총액은 0 이상이어야 합니다"):
        AccountRecord(
            date=date(2026, 6, 3),
            account_name="증권계좌",
            total_amount_억=Decimal("-1.0")
        )


def test_account_record_invalid_empty_name():
    """빈 계좌명으로 생성 실패"""
    with pytest.raises(ValueError, match="계좌명은 비어있을 수 없습니다"):
        AccountRecord(
            date=date(2026, 6, 3),
            account_name="",
            total_amount_억=Decimal("3.50")
        )


def test_account_record_holding_symbols_property():
    """holding_symbols 속성 테스트"""
    record = AccountRecord(
        date=date(2026, 6, 3),
        account_name="증권계좌",
        total_amount_억=Decimal("3.50"),
        holdings=(
            Holding(symbol="삼성전자"),
            Holding(symbol="NAVER"),
            Holding(symbol="카카오")
        )
    )
    symbols = record.holding_symbols
    assert len(symbols) == 3
    assert "삼성전자" in symbols
    assert "NAVER" in symbols
    assert "카카오" in symbols


def test_account_record_holding_count_property():
    """holding_count 속성 테스트"""
    record = AccountRecord(
        date=date(2026, 6, 3),
        account_name="증권계좌",
        total_amount_억=Decimal("3.50"),
        holdings=(
            Holding(symbol="삼성전자"),
            Holding(symbol="NAVER")
        )
    )
    assert record.holding_count == 2


def test_account_record_immutability():
    """AccountRecord 엔티티 불변성 확인"""
    record = AccountRecord(
        date=date(2026, 6, 3),
        account_name="증권계좌",
        total_amount_억=Decimal("3.50")
    )
    with pytest.raises(AttributeError):
        record.total_amount_억 = Decimal("5.00")
