"""AccountParser for parsing account-based markdown format"""
import re
from datetime import date
from decimal import Decimal
from typing import List

from src.domain.entities.account_record import AccountRecord
from src.domain.entities.portfolio_snapshot import PortfolioSnapshot
from src.domain.entities.holding import Holding


class AccountParser:
    """계좌별 파서 (신규 형식: ### 계좌: {이름})"""

    def __init__(self):
        self.account_pattern = re.compile(r'^###\s*계좌:\s*(.+)$')
        self.amount_pattern = re.compile(r'^총액:\s*(\d+\.?\d*)억$')
        self.holdings_pattern = re.compile(r'^보유종목:\s*(.*)$')
        self.date_pattern = re.compile(r'^##\s+(\d{4}-\d{2}-\d{2})$')

    def can_parse(self, text: str) -> bool:
        """계좌별 형식인지 확인 (### 계좌: 헤더 존재)"""
        return bool(self.account_pattern.search(text))

    def parse(self, text: str, year: int) -> List[PortfolioSnapshot]:
        """마크다운 텍스트를 파싱하여 스냅샷 리스트 반환"""
        if not self.can_parse(text):
            raise ValueError("계좌별 형식이 아닙니다")

        snapshots = []
        lines = text.splitlines()

        current_date = None
        current_accounts = []
        current_account_data = {}

        for line in lines:
            # 날짜 헤더 확인
            date_match = self.date_pattern.match(line)
            if date_match:
                # 이전 날짜의 스냅샷 저장
                if current_date and current_accounts:
                    snapshots.append(PortfolioSnapshot(
                        date=current_date,
                        accounts=tuple(current_accounts)
                    ))
                current_date = self._parse_date(date_match.group(1))
                current_accounts = []
                current_account_data = {}
                continue

            # 계좌 헤더 확인
            account_match = self.account_pattern.match(line)
            if account_match:
                # 이전 계좌 데이터가 있으면 AccountRecord 생성
                if current_account_data:
                    current_accounts.append(self._create_account_record(current_date, current_account_data))
                current_account_data = {"name": account_match.group(1).strip()}
                continue

            # 총액 확인
            amount_match = self.amount_pattern.match(line)
            if amount_match and current_account_data:
                current_account_data["amount"] = Decimal(amount_match.group(1))
                continue

            # 보유종목 확인
            holdings_match = self.holdings_pattern.match(line)
            if holdings_match and current_account_data:
                holdings_str = holdings_match.group(1).strip()
                if holdings_str:
                    holdings = tuple(
                        Holding(symbol=name.strip())
                        for name in holdings_str.split(",")
                        if name.strip()
                    )
                else:
                    holdings = ()
                current_account_data["holdings"] = holdings

                # AccountRecord 생성 (보유종목 라인이 계좌 블록의 끝)
                current_accounts.append(self._create_account_record(current_date, current_account_data))
                current_account_data = {}

        # 마지막 스냅샷 추가
        if current_date and current_accounts:
            snapshots.append(PortfolioSnapshot(
                date=current_date,
                accounts=tuple(current_accounts)
            ))

        return snapshots

    def _create_account_record(self, snapshot_date: date, data: dict) -> AccountRecord:
        """AccountRecord 생성"""
        return AccountRecord(
            date=snapshot_date,
            account_name=data["name"],
            total_amount_억=data.get("amount", Decimal("0")),
            holdings=data.get("holdings", ())
        )

    def _parse_date(self, date_str: str) -> date:
        """날짜 문자열 파싱 (YYYY-MM-DD)"""
        year, month, day = map(int, date_str.split("-"))
        return date(year, month, day)
