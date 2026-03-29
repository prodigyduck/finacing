"""
Portfolio Entity 테스트

전체 포트폴리오를 나타내는 Entity입니다.
"""

import pytest
from decimal import Decimal
from src.domain.entities.portfolio import Portfolio
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class TestPortfolio:
    """Portfolio Entity 테스트"""

    def test_create_empty_portfolio(self):
        """빈 포트폴리오 생성"""
        portfolio = Portfolio(assets=[])
        assert len(portfolio.assets) == 0

    def test_create_portfolio_with_assets(self):
        """자산으로 포트폴리오 생성"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="현금",
            asset_type=AssetType.CASH,
            quantity=1,
            unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
        )

        portfolio = Portfolio(assets=[asset1, asset2])
        assert len(portfolio.assets) == 2

    def test_calculate_total_value(self):
        """총 자산 계산"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="현금",
            asset_type=AssetType.CASH,
            quantity=1,
            unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
        )

        portfolio = Portfolio(assets=[asset1, asset2])
        total = portfolio.total_value()

        # 100 * 85000 + 1000000 = 9500000
        assert total.amount == Decimal("9500000")
        assert total.currency == "KRW"

    def test_calculate_asset_allocation_by_type(self):
        """자산 유형별 배분 비율 계산"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("50000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="현금",
            asset_type=AssetType.CASH,
            quantity=1,
            unit_price=Money(amount=Decimal("5000000"), currency="KRW"),
        )

        portfolio = Portfolio(assets=[asset1, asset2])
        allocation = portfolio.allocation_by_type()

        # 주식: 5000000 / 10000000 = 50%
        assert allocation[AssetType.STOCK] == 0.5
        # 현금: 5000000 / 10000000 = 50%
        assert allocation[AssetType.CASH] == 0.5

    def test_add_asset(self):
        """자산 추가"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[])
        portfolio.add_asset(asset)

        assert len(portfolio.assets) == 1
        assert portfolio.assets[0] == asset

    def test_remove_asset_by_name(self):
        """자산 제거"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="카카오",
            asset_type=AssetType.STOCK,
            quantity=50,
            unit_price=Money(amount=Decimal("65000"), currency="KRW"),
        )

        portfolio = Portfolio(assets=[asset1, asset2])
        portfolio.remove_asset("카카오")

        assert len(portfolio.assets) == 1
        assert portfolio.assets[0].name == "삼성전자"

    def test_remove_nonexistent_asset_raises_error(self):
        """존재하지 않는 자산 제거 시 에러"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])

        with pytest.raises(ValueError, match="자산을 찾을 수 없습니다"):
            portfolio.remove_asset("카카오")

    def test_get_assets_by_type(self):
        """자산 유형별 필터링"""
        asset1 = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        asset2 = InvestmentAsset(
            name="TIGER 200",
            asset_type=AssetType.ETF,
            quantity=30,
            unit_price=Money(amount=Decimal("25000"), currency="KRW"),
        )
        asset3 = InvestmentAsset(
            name="카카오",
            asset_type=AssetType.STOCK,
            quantity=50,
            unit_price=Money(amount=Decimal("65000"), currency="KRW"),
        )

        portfolio = Portfolio(assets=[asset1, asset2, asset3])
        stocks = portfolio.get_assets_by_type(AssetType.STOCK)

        assert len(stocks) == 2
        assert all(asset.asset_type == AssetType.STOCK for asset in stocks)

    def test_portfolio_string_representation(self):
        """포트폴리오 문자열 표현"""
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])

        portfolio_str = str(portfolio)
        assert "포트폴리오" in portfolio_str
        assert "8,500,000 KRW" in portfolio_str
