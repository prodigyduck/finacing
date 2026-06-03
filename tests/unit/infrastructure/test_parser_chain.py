"""Tests for ParserChain base class"""
import pytest
from src.infrastructure.parsers.parser_chain import ParserChain


class DummyParser:
    """더미 파서 for testing"""
    def __init__(self, can_parse_result=False):
        self.can_parse_result = can_parse_result
        self.parse_called = False

    def can_parse(self, text: str) -> bool:
        return self.can_parse_result

    def parse(self, text: str, year: int):
        self.parse_called = True
        return {"result": "dummy"}


def test_parser_chain_selects_first_matching_parser():
    """첫 번째 매칭 파서를 선택"""
    parser1 = DummyParser(can_parse_result=False)
    parser2 = DummyParser(can_parse_result=True)
    parser3 = DummyParser(can_parse_result=True)

    chain = ParserChain([parser1, parser2, parser3])
    result = chain.parse("test text", 2026)

    assert parser2.parse_called
    assert not parser3.parse_called


def test_parser_chain_raises_error_if_no_parser_matches():
    """매칭하는 파서가 없으면 에러"""
    parser1 = DummyParser(can_parse_result=False)
    parser2 = DummyParser(can_parse_result=False)

    chain = ParserChain([parser1, parser2])

    with pytest.raises(ValueError, match="No parser can handle this format"):
        chain.parse("test text", 2026)


def test_parser_chain_empty_list():
    """빈 파서 리스트"""
    chain = ParserChain([])

    with pytest.raises(ValueError, match="No parser can handle this format"):
        chain.parse("test text", 2026)


def test_parser_chain_stops_at_first_match():
    """첫 번째 매칭에서 중지"""
    parser1 = DummyParser(can_parse_result=True)
    parser2 = DummyParser(can_parse_result=True)

    chain = ParserChain([parser1, parser2])
    chain.parse("test text", 2026)

    assert parser1.parse_called
    assert not parser2.parse_called
