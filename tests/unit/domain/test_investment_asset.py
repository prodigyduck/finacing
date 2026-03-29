"""
InvestmentAsset Entity 테스트

개별 투자 자산을 나타내는 Entity입니다.
"""

import pytest
from decimal import Decimal
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class TestInvestmentAsset:
    """InvestmentAsset Entity 테스트"""

    def test_create_investment_asset(self):
        """투자 자산 생성"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )

        assert asset.name == "삼성전자"
        assert asset.asset_type == AssetType.STOCK
        assert asset.quantity == 100
        assert asset.unit_price.amount == Decimal("85000")

    def test_calculate_total_value(self):
        """총 가치 계산"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )

        total = asset.total_value()
        assert total.amount == Decimal("8500000")  # 100 * 85000
        assert total.currency == "KRW"

    def test_zero_quantity_asset(self):
        """수량이 0인 자산"""
        asset = InvestmentAsset(
            name="보유중 아님",
            asset_type=AssetType.STOCK,
            quantity=0,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        assert asset.total_value().amount == Decimal("0")

    def test_cash_asset(self):
        """현금 자산 (수량은 1)"""
        asset = InvestmentAsset(
            name="현금",
            asset_type=AssetType.CASH,
            quantity=1,
            unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
        )
        assert asset.total_value().amount == Decimal("1000000")

    def test_negative_quantity_raises_error(self):
        """음수 수량은 에러"""
        with pytest.raises(ValueError, match="수량은 0 이상이어야 합니다"):
            InvestmentAsset(
                name="삼성전자",
                asset_type=AssetType.STOCK,
                quantity=-10,
                unit_price=Money(amount=Decimal("85000"), currency="KRW"),
            )

    def test_empty_name_raises_error(self):
        """빈 이름은 에러"""
        with pytest.raises(ValueError, match="자산 이름은 비어있을 수 없습니다"):
            InvestmentAsset(
                name="",
                asset_type=AssetType.STOCK,
                quantity=100,
                unit_price=Money(amount=Decimal("85000"), currency="KRW"),
            )

    def test_asset_equality(self):
        """자산 동등성"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset3 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=200,  # 다른 수량
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )

        assert asset1 == asset2  # 모든 속성이 같으면 동일
        assert asset1 != asset3  # 수량이 다르면 다름

    def test_asset_string_representation(self):
        """자산 문자열 표현"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        assert "삼성전자" in str(asset)
        assert "100주" in str(asset)
