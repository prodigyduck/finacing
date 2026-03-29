"""
AnalyzePortfolio 유스케이스

포트폴리오를 분석하는 유스케이스입니다.
"""

from typing import Dict, Any

from src.domain.entities.portfolio import Portfolio
from src.domain.value_objects.asset_type import AssetType
from src.domain.value_objects.money import Money


class AnalyzePortfolio:
    """포트폴리오 분석 유스케이스"""

    def execute(self, portfolio: Portfolio) -> Dict[str, Any]:
        """
        포트폴리오 분석

        Args:
            portfolio: 분석할 포트폴리오

        Returns:
            분석 결과 딕셔너리
                - total_value: 총 자산 가치
                - asset_count: 자산 개수
                - allocation: 자산 유형별 배분 비율
        """
        total = portfolio.total_value()
        allocation = portfolio.allocation_by_type()

        return {
            "total_value": int(total.amount),
            "asset_count": len(portfolio.assets),
            "allocation": allocation,
        }
