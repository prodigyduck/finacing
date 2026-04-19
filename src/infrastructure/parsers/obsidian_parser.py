import os
import re
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Optional

from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory


class ObsidianParser:
    def __init__(self, vault_path: Optional[str] = None, investment_file: str = "투자/투자.md"):
        if vault_path is None:
            vault_path = os.environ.get("OBSIDIAN_VAULT_PATH", os.path.expanduser("~/git/obsidian"))
        self.vault_path = Path(vault_path).expanduser()
        self.investment_file = investment_file

    def parse(self, year: Optional[int] = None) -> PortfolioHistory:
        filepath = self.vault_path / self.investment_file
        if not filepath.exists():
            raise FileNotFoundError(f"투자 파일을 찾을 수 없습니다: {filepath}")

        text = filepath.read_text(encoding="utf-8")
        records = self._parse_records(text, year)
        return PortfolioHistory(records=records, year=year or date.today().year)

    def _parse_records(self, text: str, year: Optional[int] = None) -> list[InvestmentRecord]:
        if year is None:
            year = date.today().year

        records: list[InvestmentRecord] = []
        pattern = re.compile(r"^(\d{1,2})\.(\d{1,2})\s+(\d+\.?\d*)\s*$")

        for line in text.splitlines():
            m = pattern.match(line.strip())
            if not m:
                continue
            month = int(m.group(1))
            day = int(m.group(2))
            amount = Decimal(m.group(3))
            try:
                d = date(year, month, day)
            except ValueError:
                continue
            records.append(InvestmentRecord(date=d, amount_억=amount))

        return records
