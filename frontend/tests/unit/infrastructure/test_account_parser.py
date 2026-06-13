"""Unit tests for AccountParser"""
import pytest
from datetime import date
from decimal import Decimal

from src.infrastructure.parsers.account_parser import AccountParser
from src.domain.entities.portfolio_snapshot import PortfolioSnapshot
from src.domain.entities.account_record import AccountRecord


class TestAccountParser:
    """AccountParser 단위 테스트"""

    def test_can_parse_account_based_format(self):
        """계좌별 형식 감지 테스트"""
        parser = AccountParser()
        text = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오
"""
        assert parser.can_parse(text) is True

    def test_can_parse_legacy_format(self):
        """레거시 형식 감지 테스트"""
        parser = AccountParser()
        text = """1.13 4.40
1.14 4.43
1.15 4.45
"""
        assert parser.can_parse(text) is True

    def test_cannot_parse_invalid_format(self):
        """잘못된 형식 거부 테스트"""
        parser = AccountParser()
        text = "This is not investment data"
        assert parser.can_parse(text) is False

    def test_parse_account_based_format(self):
        """계좌별 형식 파싱 테스트"""
        parser = AccountParser()
        text = """## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오

### 계좌: ISA
총액: 2.11억
보유종목: KB국책주성, 미래에셋TDF

### 계좌: 현금
총액: 0.00억
보유종목:
"""
        snapshots = parser.parse(text, 2026)

        assert len(snapshots) == 1
        snapshot = snapshots[0]
        assert snapshot.date == date(2026, 6, 3)
        assert len(snapshot.accounts) == 3

        # 증권계좌 확인
        stock_account = next(acc for acc in snapshot.accounts if acc.account_name == "증권계좌")
        assert stock_account.total_amount_억 == Decimal("3.50")
        assert len(stock_account.holdings) == 3

        # ISA 확인
        isa_account = next(acc for acc in snapshot.accounts if acc.account_name == "ISA")
        assert isa_account.total_amount_억 == Decimal("2.11")
        assert len(isa_account.holdings) == 2

        # 현금 확인
        cash_account = next(acc for acc in snapshot.accounts if acc.account_name == "현금")
        assert cash_account.total_amount_억 == Decimal("0.00")
        assert len(cash_account.holdings) == 0

    def test_parse_legacy_format(self):
        """레거시 형식 파싱 테스트"""
        parser = AccountParser()
        text = """1.13 4.40
1.14 4.43
1.15 4.45
"""
        snapshots = parser.parse(text, 2026)

        assert len(snapshots) >= 3

        # 첫 번째 레코드 확인
        first = snapshots[0]
        assert first.date == date(2026, 1, 13)
        assert len(first.accounts) == 1
        assert first.accounts[0].account_name == "총계좌"
        assert first.accounts[0].total_amount_억 == Decimal("4.40")

    def test_parse_mixed_format(self):
        """혼합 형식 파싱 테스트 (레거시 + 계좌별)"""
        parser = AccountParser()
        text = """1.13 4.40
1.14 4.43

## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자
"""
        snapshots = parser.parse(text, 2026)

        # 레거시 데이터 + 계좌별 데이터 모두 파싱
        assert len(snapshots) >= 3

        # 계좌별 데이터 확인
        account_snapshot = next(s for s in snapshots if s.date == date(2026, 6, 3))
        assert len(account_snapshot.accounts) == 1
        assert account_snapshot.accounts[0].account_name == "증권계좌"

    def test_parse_raises_error_on_invalid_format(self):
        """잘못된 형식에서 ValueError 발생 테스트"""
        parser = AccountParser()
        text = "Not valid format"
        with pytest.raises(ValueError, match="계좌별 형식 또는 레거시 형식이 아닙니다"):
            parser.parse(text, 2026)

    def test_parse_multiple_dates(self):
        """여러 날짜 파싱 테스트"""
        parser = AccountParser()
        text = """## 2026-06-01

### 계좌: 증권계좌
총액: 3.00억
보유종목: 삼성전자

## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER
"""
        snapshots = parser.parse(text, 2026)

        assert len(snapshots) == 2
        assert snapshots[0].date == date(2026, 6, 1)
        assert snapshots[1].date == date(2026, 6, 3)
        assert snapshots[0].accounts[0].total_amount_억 == Decimal("3.00")
        assert snapshots[1].accounts[0].total_amount_억 == Decimal("3.50")
