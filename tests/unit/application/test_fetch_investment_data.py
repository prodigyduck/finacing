"""
FetchInvestmentData 유스케이스 테스트

Google Keep에서 투자 데이터를 가져오는 유스케이스입니다.
"""

import pytest
from unittest.mock import Mock
from src.application.use_cases.fetch_investment_data import FetchInvestmentData
from src.application.ports.keep_repository import IKeepRepository
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money
from decimal import Decimal


class TestFetchInvestmentData:
    """FetchInvestmentData 유스케이스 테스트"""

    def test_fetch_investment_data_successfully(self):
        """투자 데이터 성공적으로 가져오기"""
        # Given
        mock_repo = Mock(spec=IKeepRepository)
        expected_assets = [
            InvestmentAsset(
                name="삼성전자",
                asset_type=AssetType.STOCK,
                quantity=100,
                unit_price=Money(amount=Decimal("85000"), currency="KRW"),
            ),
            InvestmentAsset(
                name="현금",
                asset_type=AssetType.CASH,
                quantity=1,
                unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
            ),
        ]
        mock_repo.fetch_investment_notes.return_value = expected_assets

        use_case = FetchInvestmentData(repository=mock_repo)

        # When
        result = use_case.execute(label="투자")

        # Then
        assert len(result) == 2
        assert result[0].name == "삼성전자"
        mock_repo.fetch_investment_notes.assert_called_once_with("투자")

    def test_fetch_with_empty_label(self):
        """빈 라벨로 가져오기"""
        # Given
        mock_repo = Mock(spec=IKeepRepository)
        mock_repo.fetch_investment_notes.return_value = []

        use_case = FetchInvestmentData(repository=mock_repo)

        # When
        result = use_case.execute(label="")

        # Then
        assert len(result) == 0
        mock_repo.fetch_investment_notes.assert_called_once_with("")

    def test_fetch_with_custom_label(self):
        """사용자 정의 라벨로 가져오기"""
        # Given
        mock_repo = Mock(spec=IKeepRepository)
        expected_assets = [
            InvestmentAsset(
                name="TIGER 200",
                asset_type=AssetType.ETF,
                quantity=30,
                unit_price=Money(amount=Decimal("25000"), currency="KRW"),
            ),
        ]
        mock_repo.fetch_investment_notes.return_value = expected_assets

        use_case = FetchInvestmentData(repository=mock_repo)

        # When
        result = use_case.execute(label="ETF 모음")

        # Then
        assert len(result) == 1
        assert result[0].asset_type == AssetType.ETF
        mock_repo.fetch_investment_notes.assert_called_once_with("ETF 모음")

    def test_execute_uses_orchestrator_when_present(self):
        mock_repo = Mock(spec=IKeepRepository)
        expected_assets = []
        mock_repo.fetch_investment_notes.return_value = expected_assets

        class DummyOrch:
            def __init__(self):
                self.called = False

            def execute_with_fallback(self, callables):
                self.called = True
                # Simulate calling the repo callable
                if callable(callables):
                    return callables()
                # mapping style
                for v in callables.values():
                    return v()

        orch = DummyOrch()
        use_case = FetchInvestmentData(repository=mock_repo, orchestrator=orch)

        res = use_case.execute(label="투자")
        assert orch.called is True
        assert res == expected_assets
