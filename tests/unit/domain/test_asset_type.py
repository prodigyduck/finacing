"""
AssetType Enum 테스트

자산 유형을 나타내는 Enum입니다.
"""

import pytest
from src.domain.value_objects.asset_type import AssetType


class TestAssetType:
    """AssetType Enum 테스트"""

    def test_stock_exists(self):
        """주식 타입 존재"""
        assert AssetType.STOCK is not None

    def test_etf_exists(self):
        """ETF 타입 존재"""
        assert AssetType.ETF is not None

    def test_bond_exists(self):
        """채권 타입 존재"""
        assert AssetType.BOND is not None

    def test_cash_exists(self):
        """현금 타입 존재"""
        assert AssetType.CASH is not None

    def test_other_exists(self):
        """기타 타입 존재"""
        assert AssetType.OTHER is not None

    def test_asset_type_from_korean_stock(self):
        """'주식'으로부터 AssetType.STOCK 변환"""
        assert AssetType.from_string("주식") == AssetType.STOCK
        assert AssetType.from_string("STOCK") == AssetType.STOCK
        assert AssetType.from_string("stock") == AssetType.STOCK

    def test_asset_type_from_korean_etf(self):
        """'ETF'로부터 AssetType.ETF 변환"""
        assert AssetType.from_string("ETF") == AssetType.ETF
        assert AssetType.from_string("etf") == AssetType.ETF

    def test_asset_type_from_korean_bond(self):
        """'채권'으로부터 AssetType.BOND 변환"""
        assert AssetType.from_string("채권") == AssetType.BOND
        assert AssetType.from_string("BOND") == AssetType.BOND

    def test_asset_type_from_korean_cash(self):
        """'현금'으로부터 AssetType.CASH 변환"""
        assert AssetType.from_string("현금") == AssetType.CASH
        assert AssetType.from_string("CASH") == AssetType.CASH

    def test_asset_type_from_other_string(self):
        """알 수 없는 문자열은 OTHER로 변환"""
        assert AssetType.from_string("암호화폐") == AssetType.OTHER
        assert AssetType.from_string("부동산") == AssetType.OTHER

    def test_asset_type_display_name(self):
        """한국어 표시 이름"""
        assert AssetType.STOCK.display_name() == "주식"
        assert AssetType.ETF.display_name() == "ETF"
        assert AssetType.BOND.display_name() == "채권"
        assert AssetType.CASH.display_name() == "현금"
        assert AssetType.OTHER.display_name() == "기타"
