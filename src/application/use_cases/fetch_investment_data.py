"""
FetchInvestmentData 유스케이스

Google Keep에서 투자 데이터를 가져오는 유스케이스입니다.
"""

from typing import List, Optional

from src.application.ports.keep_repository import IKeepRepository
from src.domain.entities.investment_asset import InvestmentAsset
from src.application.services.agent_orchestrator import AgentOrchestrator


class FetchInvestmentData:
    """투자 데이터 가져오기 유스케이스"""

    def __init__(self, repository: IKeepRepository, orchestrator: Optional[AgentOrchestrator] = None):
        """
        생성자

        Args:
            repository: Google Keep 리포지토리
        """
        self._repository = repository
        self._orchestrator = orchestrator

    def execute(self, label: str = "투자") -> List[InvestmentAsset]:
        """
        투자 데이터 가져오기

        Args:
            label: 검색할 라벨 이름 (기본값: "투자")

        Returns:
            파싱된 투자 자산 리스트
        """
        if self._orchestrator is not None:
            # Provide a callable per agent name - infrastructure adapters should be wired in presentation
            def repo_call():
                return self._repository.fetch_investment_notes(label)

            # For backward compatibility we attempt using a single 'sisyphus' agent if orchestrator has chain
            agent_name = getattr(self._orchestrator, "chain", ["sisyphus"])[0]
            return self._orchestrator.execute_with_fallback({agent_name: repo_call})

        return self._repository.fetch_investment_notes(label)
