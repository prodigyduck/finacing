"""LegacyParser for adapting existing ObsidianParser to new architecture"""
import re
from datetime import date
from decimal import Decimal
from typing import List

from src.domain.entities.account_record import AccountRecord
from src.domain.entities.portfolio_snapshot import PortfolioSnapshot


_PATTERN = re.compile(r"^(\d{1,2})\.(\d{1,2})\s+(\d+\.?\d*)\s*$")


class LegacyParser:
    """레거시 파서 - 기존 총액 형식 지원"""

    def can_parse(self, text: str) -> bool:
        """레거시 형식인지 확인 (M.DD 금액 형식)"""
        return bool(_PATTERN.search(text, multiline=True))

    def parse(self, text: str, year: int) -> List[PortfolioSnapshot]:
        """레거시 형식을 '전체 포트폴리오' 계좌로 변환"""
        snapshots = []

        for line in text.splitlines():
            m = _PATTERN.match(line.strip())
            if not m:
                continue

            month = int(m.group(1))
            day = int(m.group(2))
            amount = Decimal(m.group(3))

            try:
                d = date(year, month, day)
            except ValueError:
                continue

            # '전체 포트폴리오' 계좌로 AccountRecord 생성
            account_record = AccountRecord(
                date=d,
                account_name="전체 포트폴리오",
                total_amount_억=amount,
                holdings=()
            )

            snapshots.append(PortfolioSnapshot(
                date=d,
                accounts=(account_record,)
            ))

        return snapshots
