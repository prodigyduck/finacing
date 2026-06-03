"""Tests for PortfolioSnapshot entity"""
import pytest
from datetime import date
from decimal import Decimal
from src.domain.entities.portfolio_snapshot import PortfolioSnapshot
from src.domain.entities.account_record import AccountRecord
from src.domain.entities.holding import Holding


def test_portfolio_snapshot_creation_valid():
    """유효한 포트폴리오 스냅샷 생성"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50"),
                holdings=(Holding(symbol="삼성전자"),)
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("2.00"),
                holdings=(Holding(symbol="KB국책주성"),)
            )
        )
    )
    assert snapshot.date == date(2026, 6, 3)
    assert len(snapshot.accounts) == 2


def test_portfolio_snapshot_empty_accounts_fails():
    """빈 계좌 리스트로 생성 실패"""
    with pytest.raises(ValueError, match="최소 하나의 계좌 기록이 필요합니다"):
        PortfolioSnapshot(
            date=date(2026, 6, 3),
            accounts=()
        )


def test_portfolio_snapshot_total_amount():
    """전체 총액 계산"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("2.00")
            )
        )
    )
    assert snapshot.total_amount == Decimal("5.50")


def test_portfolio_snapshot_account_names():
    """계좌명 리스트 (중복 제거)"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("2.00")
            )
        )
    )
    names = snapshot.account_names
    assert len(names) == 2
    assert "증권계좌" in names
    assert "ISA" in names


def test_portfolio_snapshot_get_account_record():
    """특정 계좌 기록 조회"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("2.00")
            )
        )
    )
    record = snapshot.get_account_record("증권계좌")
    assert record is not None
    assert record.account_name == "증권계좌"
    assert record.total_amount_억 == Decimal("3.50")


def test_portfolio_snapshot_get_account_record_not_found():
    """존재하지 않는 계좌 조회"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
        )
    )
    record = snapshot.get_account_record("없는계좌")
    assert record is None


def test_portfolio_snapshot_get_account_allocation():
    """계좌별 비중 계산"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("1.50")
            )
        )
    )
    # 3.50 / 5.00 = 0.7
    allocation = snapshot.get_account_allocation("증권계좌")
    assert allocation == Decimal("0.7")


def test_portfolio_snapshot_allocation_zero_total():
    """총액이 0일 때 비중 계산"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="빈계좌",
                total_amount_억=Decimal("0")
            ),
        )
    )
    allocation = snapshot.get_account_allocation("빈계좌")
    assert allocation is None


def test_portfolio_snapshot_all_holdings():
    """모든 계좌의 모든 보유 종목"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50"),
                holdings=(
                    Holding(symbol="삼성전자"),
                    Holding(symbol="NAVER")
                )
            ),
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="ISA",
                total_amount_억=Decimal("2.00"),
                holdings=(Holding(symbol="KB국책주성"),)
            )
        )
    )
    all_holdings = snapshot.all_holdings
    assert len(all_holdings) == 3


def test_portfolio_snapshot_immutability():
    """PortfolioSnapshot 엔티티 불변성 확인"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50")
            ),
        )
    )
    with pytest.raises(AttributeError):
        snapshot.accounts = ()
