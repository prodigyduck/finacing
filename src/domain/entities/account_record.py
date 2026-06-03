"""AccountRecord entity for account state at a specific point in time"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.holding import Holding


@dataclass(frozen=True)
class AccountRecord:
    """계좌 기록 엔티티 - 특정 날짜의 계좌 상태"""
    date: date
    account_name: str
    total_amount_억: Decimal
    holdings: Tuple["Holding", ...] = ()

    def __post_init__(self) -> None:
        if self.total_amount_억 < Decimal("0"):
            raise ValueError("계좌 총액은 0 이상이어야 합니다")
        if not self.account_name or not self.account_name.strip():
            raise ValueError("계좌명은 비어있을 수 없습니다")

    @property
    def holding_symbols(self) -> Tuple[str, ...]:
        """보유 종목명 리스트"""
        return tuple(h.symbol for h in self.holdings)

    @property
    def holding_count(self) -> int:
        """보유 종목 수"""
        return len(self.holdings)
