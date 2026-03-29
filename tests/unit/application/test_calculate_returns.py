"""
CalculateReturns 유스케이스 테스트

수익률을 계산하는 유스케이스입니다.
"""

import pytest
from decimal import Decimal
from src.application.use_cases.calculate_returns import CalculateReturns
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.entities.portfolio import Portfolio
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class TestCalculateReturns:
    """CalculateReturns 유스케이스 테스트"""

    def test_calculate_return_with_profit(self):
        """수익 있는 경우 수익률 계산"""
        # Given
        asset = InvestmentAsset(
            name="삼성전자",
            asset_type=AssetType.STOCK,
            quantity=100,
            unit_price=Money(amount=Decimal("85000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])

        # 평단가: 80000, 현재가: 85000
        calculate_use_case = CalculateReturns()

        # When
        result = calculate_use_case.execute(
            portfolio=portfolio,
            asset_name="삼성전자",
            avg_buy_price=Money(amount=Decimal("80000"), currency="KRW"),
        )

        # Then
        # 수익: (85000 - 80000) / 80000 * 100 = 6.25%
        assert result["current_price"] == 85000
        assert result["avg_buy_price"] == 80000
        assert result["profit_amount"] == 500000
        assert pytest.approx(result["return_rate"], 0.01) == 6.25
        assert result["status"] == "profit"

    def test_calculate_return_with_loss(self):
        """손실 있는 경우 수익률 계산"""
        # Given
        asset = InvestmentAsset(
            name="카카오",
            asset_type=AssetType.STOCK,
            quantity=50,
            unit_price=Money(amount=Decimal("60000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])

        # 평단가: 70000, 현재가: 60000
        calculate_use_case = CalculateReturns()

        # When
        result = calculate_use_case.execute(
            portfolio=portfolio,
            asset_name="카카오",
            avg_buy_price=Money(amount=Decimal("70000"), currency="KRW"),
        )

        # Then
        # 손실: (60000 - 70000) / 70000 * 100 = -14.29%
        assert result["current_price"] == 60000
        assert result["avg_buy_price"] == 70000
        assert result["profit_amount"] == -500000
        assert pytest.approx(result["return_rate"], 0.01) == -14.29
        assert result["status"] == "loss"

    def test_calculate_return_break_even(self):
        """손익분기 (수익률 0%)"""
        # Given
        asset = InvestmentAsset(
            name="현금",
            asset_type=AssetType.CASH,
            quantity=1,
            unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
        )
        portfolio = Portfolio(assets=[asset])

        calculate_use_case = CalculateReturns()

        # When
        result = calculate_use_case.execute(
            portfolio=portfolio,
            asset_name="현금",
            avg_buy_price=Money(amount=Decimal("1000000"), currency="KRW"),
        )

        # Then
        assert result["current_price"] == 1000000
        assert result["avg_buy_price"] == 1000000
        assert result["profit_amount"] == 0
        assert result["return_rate"] == 0.0
        assert result["status"] == "break_even"

    def test_calculate_return_asset_not_found(self):
        """존재하지 않는 자산 수익률 계산"""
        # Given
        portfolio = Portfolio(assets=[])
        calculate_use_case = CalculateReturns()

        # When/Then
        with pytest.raises(ValueError, match="자산을 찾을 수 없습니다"):
            calculate_use_case.execute(
                portfolio=portfolio,
                asset_name="삼성전자",
                avg_buy_price=Money(amount=Decimal("80000"), currency="KRW"),
            )
