from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from src.domain.entities.portfolio_history import PortfolioHistory


class ParserPort:
    """Input port for parser operations (Interface)."""

    def pull(self) -> str:
        """Pull latest data from remote."""
        raise NotImplementedError

    def parse(self, year: Optional[int] = None) -> PortfolioHistory:
        """Parse investment data from source."""
        raise NotImplementedError


def _linear_regression(records: List) -> Optional[Tuple[float, float]]:
    """Return (slope_per_day, intercept) via least-squares on day offsets."""
    if len(records) < 2:
        return None
    base = records[0].date
    xs = [(r.date - base).days for r in records]
    ys = [float(r.amount_억) for r in records]
    n = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xy = sum(x * y for x, y in zip(xs, ys))
    sum_x2 = sum(x * x for x in xs)
    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        return None
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


class AnalyzeHistory:
    def __init__(self, parser: Optional[ParserPort] = None):
        """Initialize with optional parser dependency.

        If parser is provided, execute() will call parser.parse() first.
        Otherwise, execute() expects a PortfolioHistory argument.
        """
        self.parser = parser

    def execute(self, history: Optional[PortfolioHistory] = None, year: Optional[int] = None) -> Dict[str, Any]:
        """Execute analysis.

        If parser was provided during init, history can be None and will be fetched.
        Otherwise, history must be provided.
        """
        if self.parser and history is None:
            history = self.parser.parse(year=year)
        elif history is None:
            raise ValueError("Either provide parser during init or pass history argument")
        latest = history.latest()
        earliest = history.earliest()

        if not latest or not earliest:
            return {
                "records": [],
                "latest": None,
                "earliest": None,
                "total_change": None,
                "return_rate": None,
                "record_count": 0,
                "projections": [],
            }

        reg = _linear_regression(history.records)
        projections = []
        if reg:
            slope, intercept = reg
            base = history.records[0].date
            for months in (3, 6, 12):
                target = latest.date + timedelta(days=months * 30)
                day_offset = (target - base).days
                projected = intercept + slope * day_offset
                projections.append({
                    "months": months,
                    "date": target.isoformat(),
                    "amount": round(projected, 2),
                })

        return {
            "records": [
                {"date": r.date.isoformat(), "amount": float(r.amount_억)}
                for r in history.records
            ],
            "latest": {"date": latest.date.isoformat(), "amount": float(latest.amount_억)},
            "earliest": {"date": earliest.date.isoformat(), "amount": float(earliest.amount_억)},
            "total_change": float(history.total_change() or 0),
            "return_rate": history.period_return_rate(),
            "record_count": len(history),
            "projections": projections,
        }
