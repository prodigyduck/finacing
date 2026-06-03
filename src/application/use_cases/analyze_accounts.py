"""AnalyzeAccounts use case for analyzing account data"""
from typing import Dict, Any, List
from decimal import Decimal

from src.domain.entities.portfolio_snapshot import PortfolioSnapshot


class AnalyzeAccounts:
    """계좌별 분석 유스케이스"""

    def execute(self, snapshot: PortfolioSnapshot) -> Dict[str, Any]:
        """스냅샷을 분석하여 계좌별 데이터와 비교 정보 반환"""
        accounts_data = []

        for account_record in snapshot.accounts:
            allocation = snapshot.get_account_allocation(account_record.account_name)
            accounts_data.append({
                "name": account_record.account_name,
                "latest_amount": float(account_record.total_amount_억),
                "allocation": float(allocation) if allocation else 0.0,
                "holdings": [
                    {"symbol": holding.symbol}
                    for holding in account_record.holdings
                ]
            })

        # 비교 데이터 생성
        comparison = self._create_comparison(accounts_data, snapshot)

        return {
            "accounts": accounts_data,
            "comparison": comparison
        }

    def _create_comparison(self, accounts_data: List[Dict], snapshot: PortfolioSnapshot) -> Dict[str, Any]:
        """비교 데이터 생성"""
        if not accounts_data:
            return {
                "best_performer": None,
                "worst_performer": None,
                "allocation_table": []
            }

        # 비중 기준 최우수/최저 성과 계좌
        sorted_by_allocation = sorted(accounts_data, key=lambda a: a["allocation"])
        worst = sorted_by_allocation[0]["name"]
        best = sorted_by_allocation[-1]["name"]

        # 배분 비율 표
        allocation_table = [
            {
                "account": acc["name"],
                "amount": acc["latest_amount"],
                "percentage": acc["allocation"] * 100
            }
            for acc in accounts_data
        ]

        return {
            "best_performer": best,
            "worst_performer": worst,
            "allocation_table": allocation_table
        }
