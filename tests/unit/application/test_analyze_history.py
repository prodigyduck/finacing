from datetime import date
from decimal import Decimal

from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory
from src.application.use_cases.analyze_history import AnalyzeHistory


def _record(month: int, day: int, amount: float) -> InvestmentRecord:
    return InvestmentRecord(date=date(2026, month, day), amount_억=Decimal(str(amount)))


class TestAnalyzeHistory:
    def test_execute_empty(self):
        result = AnalyzeHistory().execute(PortfolioHistory())
        assert result["record_count"] == 0
        assert result["latest"] is None

    def test_execute_with_data(self):
        history = PortfolioHistory(records=[_record(1, 1, 4.0), _record(2, 1, 4.5)])
        result = AnalyzeHistory().execute(history)
        assert result["record_count"] == 2
        assert result["latest"]["amount"] == 4.5
        assert result["earliest"]["amount"] == 4.0
        assert result["total_change"] == 0.5
        assert result["return_rate"] == 12.5
        assert len(result["records"]) == 2
