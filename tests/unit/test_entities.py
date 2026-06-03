from decimal import Decimal
from datetime import date
import pytest
from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory

def test_investment_record_creation():
    record = InvestmentRecord(date=date(2026, 5, 31), amount_억=Decimal("5.0"))
    assert record.date == date(2026, 5, 31)
    assert record.amount_억 == Decimal("5.0")

def test_portfolio_history_creation():
    records = [
        InvestmentRecord(date=date(2026, 1, 1), amount_억=Decimal("4.0")),
        InvestmentRecord(date=date(2026, 2, 1), amount_억=Decimal("4.1"))
    ]
    history = PortfolioHistory(records=records)
    assert len(history.records) == 2
    assert history.records[0].amount_억 == Decimal("4.0")
