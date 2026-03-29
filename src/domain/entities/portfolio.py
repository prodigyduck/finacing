"""
Portfolio Entity

Represents the entire portfolio as an Entity.
"""

from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Dict

from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


@dataclass
class Portfolio:
    """Portfolio Entity"""

    assets: List[InvestmentAsset] = field(default_factory=list)

    def total_value(self) -> Money:
        """
        Calculate total asset value

        Returns:
            Total value of all assets
        """
        if not self.assets:
            return Money(amount=Decimal("0"), currency="KRW")

        total = Decimal("0")
        currency = self.assets[0].unit_price.currency

        for asset in self.assets:
            total += asset.total_value().amount

        return Money(amount=total, currency=currency)

    def allocation_by_type(self) -> Dict[AssetType, float]:
        """
        Calculate allocation ratio by asset type

        Returns:
            Allocation ratio by asset type (0.0 ~ 1.0)
        """
        if not self.assets:
            return {}

        allocation: Dict[AssetType, float] = {}
        total = self.total_value().amount

        for asset in self.assets:
            asset_value = asset.total_value().amount
            ratio = float(asset_value / total) if total > 0 else 0.0

            if asset.asset_type in allocation:
                allocation[asset.asset_type] += ratio
            else:
                allocation[asset.asset_type] = ratio

        return allocation

    def add_asset(self, asset: InvestmentAsset) -> None:
        """
        Add asset to portfolio

        Args:
            asset: Asset to add
        """
        self.assets.append(asset)

    def remove_asset(self, name: str) -> None:
        """
        Remove asset from portfolio

        Args:
            name: Name of asset to remove

        Raises:
            ValueError: When asset cannot be found
        """
        for i, asset in enumerate(self.assets):
            if asset.name == name:
                self.assets.pop(i)
                return

        raise ValueError(f"자산을 찾을 수 없습니다: {name}")

    def get_assets_by_type(self, asset_type: AssetType) -> List[InvestmentAsset]:
        """
        Filter assets by type

        Args:
            asset_type: Asset type to filter by

        Returns:
            List of assets of the specified type
        """
        return [asset for asset in self.assets if asset.asset_type == asset_type]

    def __str__(self) -> str:
        """String representation"""
        total = self.total_value()
        return f"포트폴리오 ({len(self.assets)} 자산): 총 {total}"
