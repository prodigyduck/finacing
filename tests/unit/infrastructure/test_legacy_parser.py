"""Tests for LegacyParser adapter"""
import pytest
from src.infrastructure.parsers.legacy_parser import LegacyParser


def test_legacy_parser_can_parse_legacy_format():
    """레거시 형식 인식"""
    parser = LegacyParser()
    legacy_text = "1.01 5.20\n6.03 5.61\n"
    assert parser.can_parse(legacy_text) is True


def test_legacy_parser_cannot_parse_account_format():
    """계좌별 형식 거부"""
    parser = LegacyParser()
    account_text = "## 2026-06-03\n\n### 계좌: 증권계좌\n총액: 3.50억\n"
    assert parser.can_parse(account_text) is False


def test_legacy_parser_parse_creates_default_account():
    """레거시 데이터를 '전체 포트폴리오' 계좌로 변환"""
    parser = LegacyParser()
    legacy_text = "1.01 5.20\n6.03 5.61\n"

    from datetime import date
    snapshots = parser.parse(legacy_text, 2026)

    assert len(snapshots) == 2
    assert snapshots[0].accounts[0].account_name == "전체 포트폴리오"
    assert snapshots[0].accounts[0].total_amount_억 == 5.20


def test_legacy_parser_empty_text():
    """빈 텍스트 처리"""
    parser = LegacyParser()
    snapshots = parser.parse("", 2026)
    assert len(snapshots) == 0
