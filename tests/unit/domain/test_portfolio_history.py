import pytest
from datetime import date
from decimal import Decimal

from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory


def _record(month: int, day: int, amount: float) -> InvestmentRecord:
    return InvestmentRecord(date=date(2026, month, day), amount_억=Decimal(str(amount)))


class TestPortfolioHistory:
    def test_empty_history(self):
        h = PortfolioHistory()
        assert h.latest() is None
        assert h.earliest() is None
        assert h.total_change() is None
        assert h.period_return_rate() is None
        assert len(h) == 0

    def test_records_sorted_by_date(self):
        h = PortfolioHistory(records=[_record(2, 1, 4.5), _record(1, 1, 4.0)])
        assert h.records[0].date == date(2026, 1, 1)
        assert h.records[1].date == date(2026, 2, 1)

    def test_latest_and_earliest(self):
        h = PortfolioHistory(records=[_record(1, 1, 4.0), _record(2, 1, 4.5), _record(3, 1, 5.0)])
        assert h.latest() == _record(3, 1, 5.0)
        assert h.earliest() == _record(1, 1, 4.0)

    def test_total_change(self):
        h = PortfolioHistory(records=[_record(1, 1, 4.0), _record(2, 1, 4.5)])
        assert h.total_change() == Decimal("0.5")

    def test_total_change_negative(self):
        h = PortfolioHistory(records=[_record(1, 1, 5.0), _record(2, 1, 4.0)])
        assert h.total_change() == Decimal("-1.0")

    def test_period_return_rate(self):
        h = PortfolioHistory(records=[_record(1, 1, 4.0), _record(2, 1, 4.5)])
        assert h.period_return_rate() == pytest.approx(12.5)

    def test_period_return_rate_zero_base(self):
        h = PortfolioHistory(records=[_record(1, 1, 0.0), _record(2, 1, 4.0)])
        assert h.period_return_rate() is None

    def test_records_in_range(self):
        h = PortfolioHistory(records=[
            _record(1, 1, 4.0),
            _record(1, 15, 4.2),
            _record(2, 1, 4.5),
            _record(3, 1, 5.0),
        ])
        result = h.records_in_range(date(2026, 1, 10), date(2026, 2, 1))
        assert len(result) == 2
        assert result[0].date == date(2026, 1, 15)
        assert result[1].date == date(2026, 2, 1)

    def test_len(self):
        h = PortfolioHistory(records=[_record(1, 1, 4.0), _record(2, 1, 4.5)])
        assert len(h) == 2
