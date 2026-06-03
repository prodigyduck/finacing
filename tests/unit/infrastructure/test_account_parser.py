"""Tests for AccountParser for account-based format"""
import pytest
from datetime import date
from decimal import Decimal
from src.infrastructure.parsers.account_parser import AccountParser


def test_account_parser_can_parse_account_format():
    """계좌별 형식 인식"""
    parser = AccountParser()
    account_text = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오
"""
    assert parser.can_parse(account_text) is True


def test_account_parser_cannot_parse_legacy_format():
    """레거시 형식 거부"""
    parser = AccountParser()
    legacy_text = "1.01 5.20\n6.03 5.61\n"
    assert parser.can_parse(legacy_text) is False


def test_account_parser_parse_single_account():
    """단일 계좌 파싱"""
    parser = AccountParser()
    markdown = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오
"""
    snapshots = parser.parse(markdown, 2026)

    assert len(snapshots) == 1
    assert snapshots[0].date == date(2026, 6, 3)
    assert len(snapshots[0].accounts) == 1
    assert snapshots[0].accounts[0].account_name == "증권계좌"
    assert snapshots[0].accounts[0].total_amount_억 == Decimal("3.50")
    assert len(snapshots[0].accounts[0].holdings) == 3


def test_account_parser_parse_multiple_accounts():
    """다중 계좌 파싱"""
    parser = AccountParser()
    markdown = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER

### 계좌: ISA
총액: 2.00억
보유종목: KB국책주성
"""
    snapshots = parser.parse(markdown, 2026)

    assert len(snapshots) == 1
    assert len(snapshots[0].accounts) == 2
    assert snapshots[0].accounts[0].account_name == "증권계좌"
    assert snapshots[0].accounts[1].account_name == "ISA"


def test_account_parser_parse_account_without_holdings():
    """종목 없는 계좌 파싱"""
    parser = AccountParser()
    markdown = """## 2026-06-03

### 계좌: 현금
총액: 0.11억
보유종목:
"""
    snapshots = parser.parse(markdown, 2026)

    assert len(snapshots[0].accounts) == 1
    assert snapshots[0].accounts[0].account_name == "현금"
    assert len(snapshots[0].accounts[0].holdings) == 0


def test_account_parser_parse_multiple_dates():
    """여러 날짜 파싱"""
    parser = AccountParser()
    markdown = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억

## 2026-06-01

### 계좌: 증권계좌
총액: 3.45억
"""
    snapshots = parser.parse(markdown, 2026)

    assert len(snapshots) == 2
    assert snapshots[0].date == date(2026, 6, 3)
    assert snapshots[1].date == date(2026, 6, 1)
