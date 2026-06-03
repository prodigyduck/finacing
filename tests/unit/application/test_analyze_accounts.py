"""Tests for AnalyzeAccounts use case"""
import pytest
from datetime import date
from decimal import Decimal
from src.application.use_cases.analyze_accounts import AnalyzeAccounts
from src.domain.entities.portfolio_snapshot import PortfolioSnapshot
from src.domain.entities.account_record import AccountRecord
from src.domain.entities.holding import Holding


def test_analyze_accounts_execute():
    """AnalyzeAccounts 실행 테스트"""
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

    use_case = AnalyzeAccounts()
    result = use_case.execute(snapshot)

    assert "accounts" in result
    assert len(result["accounts"]) == 2
    assert "comparison" in result


def test_analyze_accounts_account_data_structure():
    """계좌 데이터 구조 확인"""
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(
                date=date(2026, 6, 3),
                account_name="증권계좌",
                total_amount_억=Decimal("3.50"),
                holdings=(Holding(symbol="삼성전자"),)
            ),
        )
    )

    use_case = AnalyzeAccounts()
    result = use_case.execute(snapshot)

    account = result["accounts"][0]
    assert account["name"] == "증권계좌"
    assert account["latest_amount"] == 3.50
    assert "allocation" in account
    assert "holdings" in account


def test_analyze_accounts_comparison_data():
    """비교 데이터 확인"""
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

    use_case = AnalyzeAccounts()
    result = use_case.execute(snapshot)

    comparison = result["comparison"]
    assert "best_performer" in comparison
    assert "worst_performer" in comparison
    assert "allocation_table" in comparison
    assert len(comparison["allocation_table"]) == 2


def test_analyze_accounts_allocation_calculation():
    """비중 계산 확인 (3.50 + 2.00 = 5.50, 3.50/5.50 = 0.636...)"""
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

    use_case = AnalyzeAccounts()
    result = use_case.execute(snapshot)

    # 3.50 / 5.50 ≈ 0.636
    account = next(a for a in result["accounts"] if a["name"] == "증권계좌")
    assert abs(account["allocation"] - 0.636) < 0.01
