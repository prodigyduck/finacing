"""PortfolioSnapshot entity for portfolio state at a specific point in time"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.account_record import AccountRecord


@dataclass(frozen=True)
class PortfolioSnapshot:
    """포트폴리오 스냅샷 엔티티 - 특정 날짜의 전체 상태"""
    date: date
    accounts: Tuple["AccountRecord", ...]

    def __post_init__(self) -> None:
        if not self.accounts:
            raise ValueError("최소 하나의 계좌 기록이 필요합니다")

    @property
    def total_amount(self) -> Decimal:
        """전체 포트폴리오 총액 (모든 계좌 합계)"""
        return sum(r.total_amount_억 for r in self.accounts)

    @property
    def account_names(self) -> Tuple[str, ...]:
        """계좌명 리스트 (중복 제거)"""
        return sorted(set(r.account_name for r in self.accounts))

    @property
    def all_holdings(self) -> Tuple:
        """모든 계좌의 모든 보유 종목 (중복 포함)"""
        from src.domain.entities.holding import Holding
        all_h = []
        for acc in self.accounts:
            all_h.extend(acc.holdings)
        return tuple(all_h)

    def get_account_record(self, account_name: str) -> Optional["AccountRecord"]:
        """특정 계좌의 기록 반환"""
        for acc in self.accounts:
            if acc.account_name == account_name:
                return acc
        return None

    def get_account_allocation(self, account_name: str) -> Optional[Decimal]:
        """특정 계좌의 전체 대비 비중 (0~1)"""
        record = self.get_account_record(account_name)
        if not record or self.total_amount == 0:
            return None
        return record.total_amount_억 / self.total_amount
