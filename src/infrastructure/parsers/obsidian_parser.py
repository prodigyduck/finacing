import calendar
import os
import re
import subprocess
import logging
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Optional

from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory

logger = logging.getLogger(__name__)

_PATTERN = re.compile(r"^(\d{1,2})\.(\d{1,2})\s+(\d+\.?\d*)\s*$")


class ObsidianParser:
    def __init__(self, vault_path: Optional[str] = None, investment_file: str = "투자/투자.md"):
        if vault_path is None:
            vault_path = os.environ.get("OBSIDIAN_VAULT_PATH", os.path.expanduser("~/git/obsidian"))
        self.vault_path = Path(vault_path).expanduser()
        self.investment_file = investment_file

    def pull(self) -> str:
        """git pull on the Obsidian vault to get latest changes."""
        try:
            result = subprocess.run(
                ["git", "pull", "--ff-only"],
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout.strip()
            logger.info(f"Obsidian git pull: {output}")
            return output
        except Exception as e:
            logger.warning(f"Obsidian git pull failed: {e}")
            return str(e)

    def parse(self, year: Optional[int] = None) -> PortfolioHistory:
        filepath = self.vault_path / self.investment_file
        if not filepath.exists():
            raise FileNotFoundError(f"투자 파일을 찾을 수 없습니다: {filepath}")

        text = filepath.read_text(encoding="utf-8")
        records = self._parse_records(text, year)
        return PortfolioHistory(records=records, year=year or date.today().year)

    def read_raw(self, year: Optional[int] = None) -> dict:
        """Read raw investment data as structured records with preserved frontmatter."""
        filepath = self.vault_path / self.investment_file
        if not filepath.exists():
            raise FileNotFoundError(f"투자 파일을 찾을 수 없습니다: {filepath}")

        if year is None:
            year = date.today().year

        text = filepath.read_text(encoding="utf-8")
        frontmatter, body = self._split_frontmatter(text)

        records: list[dict] = []
        for line in body.splitlines():
            m = _PATTERN.match(line.strip())
            if not m:
                continue
            month = int(m.group(1))
            day = int(m.group(2))
            try:
                date(year, month, day)
            except ValueError:
                continue
            records.append({"month": month, "day": day, "amount": m.group(3)})

        return {"year": year, "frontmatter": frontmatter, "records": records}

    def write_raw(self, year: int, frontmatter: str, records: list[dict]) -> None:
        """Write structured records back to the markdown file."""
        validated: list[tuple[int, int, str]] = []
        for r in records:
            month = r["month"]
            day = r["day"]
            amount_str = str(r["amount"])
            amount = Decimal(amount_str)
            if amount < 0:
                raise ValueError(f"금액은 0 이상이어야 합니다: {amount_str}")
            max_day = calendar.monthrange(year, month)[1]
            if not 1 <= day <= max_day:
                raise ValueError(f"잘못된 날짜: {month}.{day} (최대 {max_day}일)")
            validated.append((month, day, amount_str))

        validated.sort(key=lambda x: (x[0], x[1]))

        lines: list[str] = []
        if frontmatter.strip():
            lines.append(frontmatter.rstrip())
            lines.append("")
        for month, day, amount in validated:
            lines.append(f"{month}.{day} {amount}")

        filepath = self.vault_path / self.investment_file
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
        logger.info(f"Wrote {len(validated)} records to {filepath}")

    def commit(self, message: str) -> Optional[str]:
        """Git add + commit the investment file in the vault. Returns short hash or None."""
        try:
            subprocess.run(
                ["git", "add", self.investment_file],
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                timeout=10,
            )
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.warning(f"Git commit failed: {result.stderr.strip()}")
                return None
            # Extract short hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                timeout=5,
            )
            return hash_result.stdout.strip() or None
        except Exception as e:
            logger.warning(f"Git commit failed: {e}")
            return None

    def _split_frontmatter(self, text: str) -> tuple[str, str]:
        """Split text into (frontmatter_block, body)."""
        if not text.startswith("---"):
            return "", text
        end = text.find("---", 3)
        if end == -1:
            return "", text
        return text[: end + 3], text[end + 3 :].lstrip("\n")

    def _parse_records(self, text: str, year: Optional[int] = None) -> list[InvestmentRecord]:
        if year is None:
            year = date.today().year

        records: list[InvestmentRecord] = []
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
            records.append(InvestmentRecord(date=d, amount_억=amount))

        return records
