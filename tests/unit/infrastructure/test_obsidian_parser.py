from decimal import Decimal

import pytest

from src.infrastructure.parsers.obsidian_parser import ObsidianParser


class TestObsidianParser:
    def test_parse_records_from_text(self):
        text = """---
aliases:
  - 투자
tags:
---

1.13 4.4
1.14 4.43
1.15 4.45
2.1 4.50
"""
        parser = ObsidianParser()
        records = parser._parse_records(text, year=2026)
        assert len(records) == 4
        assert records[0].amount_억 == Decimal("4.4")
        assert records[0].date.month == 1
        assert records[0].date.day == 13
        assert records[-1].amount_억 == Decimal("4.50")

    def test_ignores_non_data_lines(self):
        text = """---
tags:
---

1.13 4.4
some random text
1.14 4.43
"""
        parser = ObsidianParser()
        records = parser._parse_records(text, year=2026)
        assert len(records) == 2

    def test_ignores_empty_lines(self):
        text = """1.13 4.4

1.14 4.43


"""
        parser = ObsidianParser()
        records = parser._parse_records(text, year=2026)
        assert len(records) == 2

    def test_invalid_date_skipped(self):
        text = """2.30 4.4
1.13 4.4
"""
        parser = ObsidianParser()
        records = parser._parse_records(text, year=2026)
        assert len(records) == 1
        assert records[0].date.month == 1

    def test_file_not_found(self):
        with pytest.raises(ValueError, match="Invalid vault path"):
            ObsidianParser(vault_path="/nonexistent/path")
