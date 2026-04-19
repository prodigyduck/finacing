from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from src.domain.entities.investment_record import InvestmentRecord


@dataclass
class PortfolioHistory:
    records: List[InvestmentRecord] = field(default_factory=list)
    year: int = 0

    def __post_init__(self) -> None:
        self.records.sort(key=lambda r: r.date)

    def latest(self) -> Optional[InvestmentRecord]:
        if not self.records:
            return None
        return self.records[-1]

    def earliest(self) -> Optional[InvestmentRecord]:
        if not self.records:
            return None
        return self.records[0]

    def total_change(self) -> Optional[Decimal]:
        first = self.earliest()
        last = self.latest()
        if not first or not last:
            return None
        return last.amount_억 - first.amount_억

    def period_return_rate(self) -> Optional[float]:
        first = self.earliest()
        if not first or first.amount_억 == 0:
            return None
        change = self.total_change()
        if change is None:
            return None
        return float(change / first.amount_억 * 100)

    def records_in_range(self, start: date, end: date) -> List[InvestmentRecord]:
        return [r for r in self.records if start <= r.date <= end]

    def __len__(self) -> int:
        return len(self.records)
