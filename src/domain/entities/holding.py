"""Holding entity for securities/assets in an account"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Holding:
    """보유 종목 엔티티"""
    symbol: str
    quantity: Optional[int] = None
    purchase_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None

    def __post_init__(self) -> None:
        if not self.symbol or not self.symbol.strip():
            raise ValueError("종목명은 비어있을 수 없습니다")
