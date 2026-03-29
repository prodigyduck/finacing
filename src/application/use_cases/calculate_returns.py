"""
CalculateReturns 유스케이스

수익률을 계산하는 유스케이스입니다.
"""

from typing import Dict, Any

from src.domain.entities.portfolio import Portfolio
from src.domain.entities.investment_asset import InvestmentAsset
from src.domain.value_objects.money import Money


class CalculateReturns:
    """수익률 계산 유스케이스"""

    def execute(
        self, portfolio: Portfolio, asset_name: str, avg_buy_price: Money
    ) -> Dict[str, Any]:
        """
        수익률 계산

        Args:
            portfolio: 포트폴리오
            asset_name: 자산 이름
            avg_buy_price: 평단가

        Returns:
            수익률 정보 딕셔너리
                - current_price: 현재가
                - avg_buy_price: 평단가
                - profit_amount: 수익/손실 금액
                - return_rate: 수익률 (%)
                - status: 상태 (profit/loss/break_even)

        Raises:
            ValueError: 자산을 찾을 수 없을 때
        """
        # 자산 찾기
        asset = None
        for a in portfolio.assets:
            if a.name == asset_name:
                asset = a
                break

        if asset is None:
            raise ValueError(f"자산을 찾을 수 없습니다: {asset_name}")

        current_price = asset.unit_price.amount
        avg_price = avg_buy_price.amount

        # 수익/손실 계산
        profit_amount = (current_price - avg_price) * asset.quantity

        # 수익률 계산
        return_rate = float((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0.0

        # 상태 결정
        if return_rate > 0:
            status = "profit"
        elif return_rate < 0:
            status = "loss"
        else:
            status = "break_even"

        return {
            "current_price": int(current_price),
            "avg_buy_price": int(avg_price),
            "profit_amount": int(profit_amount),
            "return_rate": round(return_rate, 2),
            "status": status,
        }
