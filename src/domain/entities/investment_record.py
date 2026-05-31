from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class InvestmentRecord:
    date: date
    amount_억: Decimal

    def __post_init__(self) -> None:
        if self.amount_억 < Decimal("0"):
            raise ValueError("금액은 0 이상이어야 합니다")
