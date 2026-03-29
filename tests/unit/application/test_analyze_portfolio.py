"""
AnalyzePortfolio 유스케이스 테스트

포트폴리오를 분석하는 유스케이스입니다.
"""

import pytest
from decimal import Decimal
from src.application.use_cases.analyze_portfolio import AnalyzePortfolio
from src.application.use_cases.fetch_investment_data import FetchInvestmentData
from src.application.ports.keep_repository import IKeepRepository
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.entities.portfolio import Portfolio
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money
from unittest.mock import Mock


class TestAnalyzePortfolio:
    """AnalyzePortfolio 유스케이스 테스트"""

    def test_analyze_portfolio_summary(self):
        """포트폴리오 요약 분석"""
        # Given
        mock_repo = Mock(spec=IKeepRepository)
        assets = [
            InvestmentAsset(
                name="삼성전자",
                asset_type=AssetType.STOCK,
                quantity=100,
                unit_price=Money(amount=Decimal("50000"), currency="KRW"),
            ),
            InvestmentAsset(
                name="현금",
                asset_type=AssetType.CASH,
                quantity=1,
                unit_price=Money(amount=Decimal("5000000"), currency="KRW"),
            ),
        ]
        mock_repo.fetch_investment_notes.return_value = assets

        fetch_use_case = FetchInvestmentData(repository=mock_repo)
        analyze_use_case = AnalyzePortfolio()

        # When
        portfolio = Portfolio(assets=fetch_use_case.execute(label="투자"))
        result = analyze_use_case.execute(portfolio)

        # Then
        assert result["total_value"] == 10000000
        assert result["asset_count"] == 2
        assert result["allocation"][AssetType.STOCK] == 0.5
        assert result["allocation"][AssetType.CASH] == 0.5

    def test_analyze_empty_portfolio(self):
        """빈 포트폴리오 분석"""
        # Given
        portfolio = Portfolio(assets=[])
        analyze_use_case = AnalyzePortfolio()

        # When
        result = analyze_use_case.execute(portfolio)

        # Then
        assert result["total_value"] == 0
        assert result["asset_count"] == 0
        assert result["allocation"] == {}

    def test_analyze_single_asset_portfolio(self):
        """단일 자산 포트폴리오 분석"""
        # Given
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])
        analyze_use_case = AnalyzePortfolio()

        # When
        result = analyze_use_case.execute(portfolio)

        # Then
        assert result["total_value"] == 8500000
        assert result["asset_count"] == 1
        assert result["allocation"][AssetType.STOCK] == 1.0

    def test_analyze_multiple_asset_types(self):
        """다양한 자산 유형 분석"""
        # Given
        assets = [
            InvestmentAsset(
                name="삼성전자",
                asset_type=AssetType.STOCK,
                quantity=100,
                unit_price=Money(amount=Decimal("30000"), currency="KRW"),
            ),
            InvestmentAsset(
                name="TIGER 200",
                asset_type=AssetType.ETF,
                quantity=30,
                unit_price=Money(amount=Decimal("20000"), currency="KRW"),
            ),
            InvestmentAsset(
                name="현금",
                asset_type=AssetType.CASH,
                quantity=1,
                unit_price=Money(amount=Decimal("4000000"), currency="KRW"),
            ),
        ]
        portfolio = Portfolio(assets=assets)
        analyze_use_case = AnalyzePortfolio()

        # When
        result = analyze_use_case.execute(portfolio)

        # Then
        # 주식: 3000000 / 10000000 = 30%
        # ETF: 600000 / 10000000 = 6%
        # 현금: 4000000 / 10000000 = 40%
        # 나머지 24%는 미분류 (OTHER)
        assert result["total_value"] == 7600000  # 3000000 + 600000 + 4000000
        assert result["asset_count"] == 3
        assert pytest.approx(result["allocation"][AssetType.STOCK], 0.01) == 0.3947
        assert pytest.approx(result["allocation"][AssetType.ETF], 0.01) == 0.0789
        assert pytest.approx(result["allocation"][AssetType.CASH], 0.01) == 0.5263
