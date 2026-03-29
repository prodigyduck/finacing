"""프레젠테이션 레이어 테스트용 fixture"""

import pytest
from decimal import Decimal

from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money
from src.domain.entities.portfolio import Portfolio


@pytest.fixture
def sample_stock_asset():
    """샘플 주식 자산"""
    return InvestmentAsset(
        name="삼성전자",
        asset_type=AssetType.STOCK,
        quantity=100,
        unit_price=Money(amount=Decimal("85000"), currency="KRW"),
    )


@pytest.fixture
def sample_etf_asset():
    """샘플 ETF 자산"""
    return InvestmentAsset(
        name="TIGER 200",
        asset_type=AssetType.ETF,
        quantity=30,
        unit_price=Money(amount=Decimal("25000"), currency="KRW"),
    )


@pytest.fixture
def sample_cash_asset():
    """샘플 현금 자산"""
    return InvestmentAsset(
        name="현금",
        asset_type=AssetType.CASH,
        quantity=1,
        unit_price=Money(amount=Decimal("1000000"), currency="KRW"),
    )


@pytest.fixture
def sample_portfolio(sample_stock_asset, sample_etf_asset, sample_cash_asset):
    """샘플 포트폴리오"""
    return Portfolio(assets=[sample_stock_asset, sample_etf_asset, sample_cash_asset])


@pytest.fixture
def empty_portfolio():
    """빈 포트폴리오"""
    return Portfolio(assets=[])
