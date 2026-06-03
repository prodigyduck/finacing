"""ParserChain for coordinating multiple parsers"""
from typing import List, Protocol


class Parser(Protocol):
    """Parser 인터페이스"""
    def can_parse(self, text: str) -> bool:
        """이 파서가 텍스트를 파싱할 수 있는지 확인"""
        ...

    def parse(self, text: str, year: int):
        """텍스트를 파싱하여 결과 반환"""
        ...


class ParserChain:
    """파서 체인 - 여러 파서를 순차적으로 시도"""

    def __init__(self, parsers: List[Parser]):
        self.parsers = parsers

    def parse(self, text: str, year: int):
        """파서 체인을 통해 파싱 시도"""
        for parser in self.parsers:
            if parser.can_parse(text):
                return parser.parse(text, year)

        raise ValueError("No parser can handle this format")
