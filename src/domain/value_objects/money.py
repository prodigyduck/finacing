"""
Money Value Object

금액을 나타내는 불변 Value Object입니다.
통화와 금액을 포함하며, 금융 계산에 사용됩니다.
"""

from decimal import Decimal
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Money:
    """금액을 나타내는 Value Object"""

    amount: Decimal
    currency: str = "KRW"

    def __post_init__(self):
        """생성 후 유효성 검사"""
        if self.amount < Decimal("0"):
            raise ValueError("금액은 0 이상이어야 합니다")

    def formatted_amount(self) -> str:
        """포맷팅된 금액 문자열 반환 (천 단위 구분)"""
        # 천 단위 구분 추가
        formatted = "{:,}".format(self.amount)
        return formatted

    def __str__(self) -> str:
        """문자열 표현"""
        return f"{self.formatted_amount()} {self.currency}"

    def __add__(self, other: "Money") -> "Money":
        """Money 덧셈 (같은 통화만 가능)"""
        if self.currency != other.currency:
            raise ValueError("통화가 다릅니다")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, factor: Union[float, int]) -> "Money":
        """Money 곱셈"""
        if factor < 0:
            raise ValueError("곱하는 값은 0 이상이어야 합니다")
        return Money(amount=self.amount * Decimal(str(factor)), currency=self.currency)
