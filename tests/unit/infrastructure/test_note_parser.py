"""
NoteParser 테스트

Google Keep 노트 텍스트를 파싱하여 투자 자산으로 변환하는 파서입니다.
"""

import pytest
from decimal import Decimal
from src.infrastructure.parsers.note_parser import NoteParser
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class TestNoteParser:
    """NoteParser 테스트"""

    def test_parse_stock_asset(self):
        """주식 자산 파싱"""
        # Given
        text = "주식 삼성전자 100주 85000원"
        parser = NoteParser()

        # When
        result = parser.parse_line(text)

        # Then
        assert result.name == "삼성전자"
        assert result.asset_type == AssetType.STOCK
        assert result.quantity == 100
        assert result.unit_price.amount == Decimal("85000")

    def test_parse_etf_asset(self):
        """ETF 자산 파싱"""
        # Given
        text = "ETF TIGER 200 30주 25000원"
        parser = NoteParser()

        # When
        result = parser.parse_line(text)

        # Then
        assert result.name == "TIGER 200"
        assert result.asset_type == AssetType.ETF
        assert result.quantity == 30
        assert result.unit_price.amount == Decimal("25000")

    def test_parse_bond_asset(self):
        """채권 자산 파싱"""
        # Given
        text = "채권 국채 10년물 5개 1000000원"
        parser = NoteParser()

        # When
        result = parser.parse_line(text)

        # Then
        assert result.name == "국채 10년물"
        assert result.asset_type == AssetType.BOND
        assert result.quantity == 5
        assert result.unit_price.amount == Decimal("1000000")

    def test_parse_cash_asset(self):
        """현금 자산 파싱"""
        # Given
        text = "현금 1000000원"
        parser = NoteParser()

        # When
        result = parser.parse_line(text)

        # Then
        assert result.name == "현금"
        assert result.asset_type == AssetType.CASH
        assert result.quantity == 1
        assert result.unit_price.amount == Decimal("1000000")

    def test_parse_multiple_lines(self):
        """여러 줄 파싱"""
        # Given
        text = """
        주식 삼성전자 100주 85000원
        주식 카카오 50주 65000원
        현금 1000000원
        ETF TIGER 200 30주 25000원
        """
        parser = NoteParser()

        # When
        results = parser.parse_text(text)

        # Then
        assert len(results) == 4
        assert results[0].name == "삼성전자"
        assert results[1].name == "카카오"
        assert results[2].name == "현금"
        assert results[3].name == "TIGER 200"

    def test_parse_with_different_formats(self):
        """다양한 형식 파싱"""
        # Given
        test_cases = [
            "주식 삼성전자 100 85000",  # '원' 없이
            "삼성전자 주식 100주 85000원",  # 순서 바뀜
            "삼성전자 100주 85000원",  # 타입 없음 (기본값 OTHER)
        ]
        parser = NoteParser()

        # When/Then
        for text in test_cases:
            result = parser.parse_line(text)
            assert result is not None

    def test_parse_invalid_line(self):
        """유효하지 않은 줄 파싱"""
        # Given
        invalid_lines = [
            "",
            "   ",  # 공백만
            "유효하지 않은 텍스트",
        ]
        parser = NoteParser()

        # When/Then
        for text in invalid_lines:
            result = parser.parse_line(text)
            assert result is None

    def test_parse_with_comma_in_amount(self):
        """콤마가 포함된 금액 파싱"""
        # Given
        text = "주식 삼성전자 100주 85,000원"
        parser = NoteParser()

        # When
        result = parser.parse_line(text)

        # Then
        assert result.unit_price.amount == Decimal("85000")

    def test_parse_multiline_note_with_empty_lines(self):
        """빈 줄이 있는 다중 라인 파싱"""
        # Given
        text = """
        주식 삼성전자 100주 85000원

        현금 1000000원

        """
        parser = NoteParser()

        # When
        results = parser.parse_text(text)

        # Then
        assert len(results) == 2
        assert results[0].name == "삼성전자"
        assert results[1].name == "현금"
