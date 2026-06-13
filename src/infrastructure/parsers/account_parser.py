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
        # Account-based patterns
        self.account_pattern = re.compile(r'###\s*계좌:\s*(.+)$')
        self.amount_pattern = re.compile(r'총액:\s*(\d+\.?\d*)억$')
        self.holdings_pattern = re.compile(r'보유종목:\s*(.*)$')
        self.date_pattern = re.compile(r'##\s+(\d{4}-\d{2}-\d{2})$')

        # Legacy pattern (M.DD amount format)
        self.legacy_pattern = re.compile(r'^(\d+)\.(\d+)\s+(\d+\.?\d*)$')

        # Simple account format: "6.04 0.47 + 4.27 + 0.86" (삼성, 키움, 토스 순서)
        self.simple_account_pattern = re.compile(r'^(\d+)\.(\d+)\s+(.+)$')
        self.account_names = ['삼성', '키움', '토스']  # 고정 순서

    def can_parse(self, text: str) -> bool:
        """계좌별 형식 또는 레거시 형식인지 확인"""
        # Check each line for account header or legacy format
        for line in text.splitlines():
            line = line.strip()
            if (self.account_pattern.match(line) or
                self.legacy_pattern.match(line) or
                self.simple_account_pattern.match(line)):
                return True
        return False

    def parse(self, text: str, year: int) -> List[PortfolioSnapshot]:
        """마크다운 텍스트를 파싱하여 스냅샷 리스트 반환 (계좌별 + 레거시 혼합 지원)"""
        if not self.can_parse(text):
            raise ValueError("계좌별 형식 또는 레거시 형식이 아닙니다")

        snapshots = []
        lines = text.splitlines()

        current_date = None
        current_accounts = []
        current_account_data = {}
        current_year = year

        for line in lines:
            # 날짜 헤더 확인
            date_match = self.date_pattern.match(line)
            if date_match:
                new_date = self._parse_date(date_match.group(1))
                current_year = new_date.year

                # 같은 날짜가 이미 있으면 계좌만 추가 (새 스냅샷 생성 안 함)
                if current_date == new_date and current_accounts:
                    # 기존 계좌 데이터를 유지하고 새 계좌를 추가하기 위해 continue
                    # (아래 계좌 헤더 처리에서 추가됨)
                    pass
                elif current_date and current_accounts:
                    # 다른 날짜면 이전 스냅샷 저장
                    snapshots.append(PortfolioSnapshot(
                        date=current_date,
                        accounts=tuple(current_accounts)
                    ))
                    current_accounts = []

                current_date = new_date
                current_account_data = {}
                continue

            # 레거시 형식 확인 (M.DD amount) - 예: "1.13 4.40"
            legacy_match = self.legacy_pattern.match(line)
            if legacy_match and current_year:
                # 이전 스냅샷이 있으면 저장
                if current_date and current_accounts:
                    snapshots.append(PortfolioSnapshot(
                        date=current_date,
                        accounts=tuple(current_accounts)
                    ))

                month = int(legacy_match.group(1))
                day = int(legacy_match.group(2))
                amount = Decimal(legacy_match.group(3))

                current_date = date(current_year, month, day)
                current_accounts = []

                # 레거시 데이터는 "총계좌"로 통합
                current_accounts.append(AccountRecord(
                    date=current_date,
                    account_name="총계좌",
                    total_amount_억=amount,
                    holdings=()
                ))
                continue

            # 단순 계좌 형식 확인 (M.DD amount1 + amount2 + ...) - 예: "6.04 0.47 + 4.27 + 0.86"
            simple_match = self.simple_account_pattern.match(line)
            if simple_match and current_year:
                # 이전 스냅샷이 있으면 저장
                if current_date and current_accounts:
                    snapshots.append(PortfolioSnapshot(
                        date=current_date,
                        accounts=tuple(current_accounts)
                    ))

                month = int(simple_match.group(1))
                day = int(simple_match.group(2))
                amounts_str = simple_match.group(3).strip()

                # + 로 구분된 금액 파싱
                amounts = [Decimal(a.strip()) for a in amounts_str.split('+') if a.strip()]

                current_date = date(current_year, month, day)
                current_accounts = []

                # 고정 순서로 계좌 생성 (삼성, 키움, 토스)
                for i, account_name in enumerate(self.account_names):
                    if i < len(amounts):
                        current_accounts.append(AccountRecord(
                            date=current_date,
                            account_name=account_name,
                            total_amount_억=amounts[i],
                            holdings=()
                        ))
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
