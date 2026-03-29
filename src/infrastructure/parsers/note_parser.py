"""
NoteParser

Google Keep 노트 텍스트를 파싱하여 투자 자산으로 변환하는 파서입니다.
"""

import re
from decimal import Decimal
from typing import List, Optional

from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class NoteParser:
    """Google Keep 노트 파서"""

    # 정규식 패턴
    # 자산 유형 (주식, ETF, 채권, 현금) + 자산명 + 수량 + 금액
    PATTERN = re.compile(
        r"""
        (주식|ETF|채권|현금)?\s*   # 자산 유형 (선택)
        (.+?)\s+                  # 자산명 (비탐욕적 매칭)
        (\d+(?:개|주)?)\s+       # 수량 (개/주 단위 선택)
        ([\d,]+)원              # 금액
        """,
        re.VERBOSE,
    )

    # 간단한 패턴 (자산명 + 수량 + 금액)
    SIMPLE_PATTERN = re.compile(
        r"""
        (.+?)\s+                  # 자산명
        (\d+(?:개|주)?)\s+       # 수량
        ([\d,]+)원?             # 금액 (선택적)
        """,
        re.VERBOSE,
    )

    # 현금 패턴 (현금만 있는 경우)
    CASH_PATTERN = re.compile(
        r"""
        (현금|CASH)\s+           # 현금 키워드
        ([\d,]+)원              # 금액
        """,
        re.VERBOSE,
    )

    # 순서 변경 패턴 (자산명 + 타입 + 수량 + 금액)
    REVERSED_PATTERN = re.compile(
        r"""
        (.+?)\s+                # 자산명
        (주식|ETF|채권|현금)\s+  # 자산 유형
        (\d+(?:개|주)?)\s+     # 수량
        ([\d,]+)원?            # 금액 (선택적)
        """,
        re.VERBOSE,
    )

    def parse_line(self, line: str) -> Optional[InvestmentAsset]:
        """
        한 줄 파싱

        Args:
            line: 파싱할 텍스트 줄

        Returns:
            InvestmentAsset 또는 None (파싱 실패 시)
        """
        line = line.strip()

        if not line:
            return None

        # 현금 패턴 우선 체크 (수량 없는 형식)
        match = self.CASH_PATTERN.match(line)
        if match:
            quantity = 1
            price_str = match.group(2).replace(",", "")
            unit_price = Money(amount=Decimal(price_str), currency="KRW")
            return InvestmentAsset(
                name="현금", asset_type=AssetType.CASH, quantity=quantity, unit_price=unit_price
            )

        # 주요 패턴 시도 (타입 + 자산명)
        match = self.PATTERN.match(line)
        if match and match.group(1):
            return self._create_asset_from_match(match, full=True)

        # 순서 변경 패턴 시도 (자산명 + 타입)
        match = self.REVERSED_PATTERN.match(line)
        if match:
            return self._create_asset_from_match(match, full=True, reversed=True)

        # 간단한 패턴 시도 (타입 없음)
        match = self.SIMPLE_PATTERN.match(line)
        if match:
            return self._create_asset_from_match(match, full=False)

        return None

    def parse_text(self, text: str) -> List[InvestmentAsset]:
        """
        여러 줄 파싱

        Args:
            text: 파싱할 텍스트

        Returns:
            InvestmentAsset 리스트
        """
        assets = []
        lines = text.strip().split("\n")

        for line in lines:
            asset = self.parse_line(line)
            if asset:
                assets.append(asset)

        return assets

    def _create_asset_from_match(
        self, match, full: bool = True, reversed: bool = False
    ) -> InvestmentAsset:
        """
        정규식 매치로부터 자산 생성

        Args:
            match: 정규식 매치 객체
            full: 전체 패턴 여부 (자산 유형 포함)
            reversed: 순서 변경 패턴 여부

        Returns:
            InvestmentAsset
        """
        if reversed:
            # 순서 변경 패턴: 자산명 + 타입 + 수량 + 금액
            name = match.group(1).strip()
            asset_type_str = match.group(2)
            quantity = int(re.sub(r"[개주]", "", match.group(3)))
            price_str = match.group(4).replace(",", "") if match.group(4) else "0"

            if "주식" in asset_type_str:
                asset_type = AssetType.STOCK
            elif "ETF" in asset_type_str:
                asset_type = AssetType.ETF
            elif "채권" in asset_type_str:
                asset_type = AssetType.BOND
            elif "현금" in asset_type_str:
                asset_type = AssetType.CASH
            else:
                asset_type = AssetType.OTHER
        elif full:
            # 전체 패턴: 자산 유형이 포함됨
            asset_type_str = match.group(1)
            name = match.group(2).strip()
            quantity = int(re.sub(r"[개주]", "", match.group(3)))
            price_str = match.group(4).replace(",", "")

            # 자산 유형 결정
            if "주식" in asset_type_str:
                asset_type = AssetType.STOCK
            elif "ETF" in asset_type_str:
                asset_type = AssetType.ETF
            elif "채권" in asset_type_str:
                asset_type = AssetType.BOND
            elif "현금" in asset_type_str:
                asset_type = AssetType.CASH
            else:
                asset_type = AssetType.OTHER
        else:
            # 간단한 패턴: 자산 유형 결정 필요
            name = match.group(1).strip()
            quantity = int(re.sub(r"[개주]", "", match.group(2)))
            price_str = match.group(3).replace(",", "") if match.group(3) else "0"

            # 자산명에서 유형 추론
            if "ETF" in name or "TIGER" in name or "KODEX" in name:
                asset_type = AssetType.ETF
            elif "현금" in name:
                asset_type = AssetType.CASH
            elif "채권" in name or "국채" in name:
                asset_type = AssetType.BOND
            elif "주식" in name:
                asset_type = AssetType.STOCK
            else:
                asset_type = AssetType.OTHER

        unit_price = Money(amount=Decimal(price_str), currency="KRW")

        return InvestmentAsset(
            name=name, asset_type=asset_type, quantity=quantity, unit_price=unit_price
        )
