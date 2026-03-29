"""
InvestmentAsset Entity

개별 투자 자산을 나타내는 Entity입니다.
"""

from decimal import Decimal
from dataclasses import dataclass

from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


@dataclass
class InvestmentAsset:
    """투자 자산 Entity"""

    name: str
    asset_type: AssetType
    quantity: int
    unit_price: Money

    def __post_init__(self):
        """생성 후 유효성 검사"""
        if not self.name or self.name.strip() == "":
            raise ValueError("자산 이름은 비어있을 수 없습니다")
        if self.quantity < 0:
            raise ValueError("수량은 0 이상이어야 합니다")

    def total_value(self) -> Money:
        """
        총 가치 계산

        Returns:
            수량 × 단가
        """
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        """문자열 표현"""
        if self.asset_type == AssetType.CASH:
            return f"{self.name}: {self.total_value()}"
        return f"{self.name} ({self.asset_type.display_name()}): {self.quantity}주 × {self.unit_price} = {self.total_value()}"
