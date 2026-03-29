"""
IKeepRepository 포트

Google Keep 데이터 접근을 위한 인터페이스입니다.
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.investment_asset import InvestmentAsset


class IKeepRepository(ABC):
    """Google Keep 리포지토리 포트"""

    @abstractmethod
    def fetch_investment_notes(self, label: str) -> List[InvestmentAsset]:
        """
        Google Keep에서 지정된 라벨의 투자 메모를 가져와서 파싱합니다.

        Args:
            label: 검색할 라벨 이름 (예: "투자")

        Returns:
            파싱된 투자 자산 리스트
        """
        pass
