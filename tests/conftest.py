from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Optional

import pytest

from src.domain.entities.investment_record import InvestmentRecord
from src.domain.entities.portfolio_history import PortfolioHistory
from src.infrastructure.parsers.obsidian_parser import ObsidianParser

SAMPLE_MARKDOWN = """\
---
aliases:
  - 투자
tags:
---

1.13 4.40
1.20 4.50
2.01 4.60
2.15 4.75
3.01 4.80
3.15 5.00
"""


def _record(month: int, day: int, amount: float) -> InvestmentRecord:
    return InvestmentRecord(date=date(2026, month, day), amount_억=Decimal(str(amount)))


@pytest.fixture
def sample_history() -> PortfolioHistory:
    return PortfolioHistory(
        records=[
            _record(1, 13, 4.40),
            _record(1, 20, 4.50),
            _record(2, 1, 4.60),
            _record(2, 15, 4.75),
            _record(3, 1, 4.80),
            _record(3, 15, 5.00),
        ],
        year=2026,
    )


@pytest.fixture
def sample_md_text() -> str:
    return SAMPLE_MARKDOWN


class FakeObsidianParser(ObsidianParser):
    """File-free parser that returns canned data for API tests."""

    def __init__(
        self,
        history: PortfolioHistory | None = None,
        raw_data: dict | None = None,
        pull_output: str = "Already up to date.",
        commit_hash: str = "abc1234",
    ):
        # Skip parent __init__ to avoid path validation for test fixtures
        self.vault_path = Path("/tmp/fake-obsidian")
        self.investment_file = "투자/투자.md"
        self._history = history
        self._raw_data = raw_data
        self._pull_output = pull_output
        self._commit_hash = commit_hash
        self.pull_called = 0
        self.parse_called = 0
        self.read_raw_called = 0
        self.write_raw_called = 0
        self.commit_called = 0
        self.last_written: dict | None = None

    def pull(self) -> str:
        self.pull_called += 1
        return self._pull_output

    def parse(self, year: int | None = None) -> PortfolioHistory:
        self.parse_called += 1
        if self._history is None:
            raise FileNotFoundError("fake: no data")
        return self._history

    def read_raw(self, year: int | None = None) -> dict:
        self.read_raw_called += 1
        if self._raw_data is None:
            raise FileNotFoundError("fake: no data")
        return self._raw_data

    def write_raw(self, year: int, frontmatter: str, records: list[dict]) -> None:
        self.write_raw_called += 1
        self.last_written = {"year": year, "frontmatter": frontmatter, "records": records}

    def commit(self, message: str) -> str | None:
        self.commit_called += 1
        return self._commit_hash


@pytest.fixture
def fake_parser(sample_history: PortfolioHistory) -> FakeObsidianParser:
    return FakeObsidianParser(history=sample_history)


@pytest.fixture
def fake_parser_with_raw(sample_history: PortfolioHistory) -> FakeObsidianParser:
    return FakeObsidianParser(
        history=sample_history,
        raw_data={
            "year": 2026,
            "frontmatter": "---\ntags:\n---\n",
            "records": [
                {"month": 1, "day": 13, "amount": "4.40"},
                {"month": 1, "day": 20, "amount": "4.50"},
            ],
        },
    )
