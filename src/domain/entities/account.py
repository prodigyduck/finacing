"""Account entity for investment accounts"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AccountType(Enum):
    """계좌 유형"""
    SECURITIES = "securities"  # 증권 계좌
    ISA = "isa"                # ISA (Individual Savings Account)
    IRA = "ira"                # IRA (Individual Retirement Account)
    PENSION = "pension"        # 연금 계좌
    CASH = "cash"              # 현금 계좌
    OTHER = "other"            # 기타


@dataclass(frozen=True)
class Account:
    """투자 계좌 엔티티"""
    name: str
    type: Optional[AccountType] = None
    description: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("계좌명은 비어있을 수 없습니다")
