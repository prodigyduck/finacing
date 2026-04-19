import pytest
from datetime import date
from decimal import Decimal

from src.domain.entities.investment_record import InvestmentRecord


class TestInvestmentRecord:
    def test_create_record(self):
        r = InvestmentRecord(date=date(2026, 1, 13), amount_억=Decimal("4.4"))
        assert r.date == date(2026, 1, 13)
        assert r.amount_억 == Decimal("4.4")

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            InvestmentRecord(date=date(2026, 1, 13), amount_억=Decimal("-1"))

    def test_zero_amount_ok(self):
        r = InvestmentRecord(date=date(2026, 1, 13), amount_억=Decimal("0"))
        assert r.amount_억 == Decimal("0")

    def test_frozen(self):
        r = InvestmentRecord(date=date(2026, 1, 13), amount_억=Decimal("4.4"))
        with pytest.raises(AttributeError):
            r.amount_억 = Decimal("5.0")
