"""Tests for legacy format compatibility with parser chain"""
import pytest
from src.infrastructure.parsers.parser_chain import ParserChain
from src.infrastructure.parsers.legacy_parser import LegacyParser
from src.infrastructure.parsers.account_parser import AccountParser


def test_parser_chain_handles_legacy_format():
    """파서 체인이 레거시 형식 처리"""
    chain = ParserChain([AccountParser(), LegacyParser()])
    legacy_text = "1.01 5.20\n6.03 5.61\n"

    snapshots = chain.parse(legacy_text, 2026)

    assert len(snapshots) == 2
    # LegacyParser는 '전체 포트폴리오' 계좌 생성
    assert snapshots[0].accounts[0].account_name == "전체 포트폴리오"


def test_parser_chain_handles_account_format():
    """파서 체인이 계좌별 형식 처리"""
    chain = ParserChain([AccountParser(), LegacyParser()])
    account_text = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
"""

    snapshots = chain.parse(account_text, 2026)

    assert len(snapshots) == 1
    assert snapshots[0].accounts[0].account_name == "증권계좌"


def test_parser_chain_priority():
    """파서 우선순위 (AccountParser 먼저)"""
    chain = ParserChain([AccountParser(), LegacyParser()])

    # AccountParser가 계좌 형식을 먼저 처리
    account_text = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
"""
    snapshots = chain.parse(account_text, 2026)

    # '전체 포트폴리오'가 아니라 '증권계좌'여야 함
    assert snapshots[0].accounts[0].account_name == "증권계좌"
