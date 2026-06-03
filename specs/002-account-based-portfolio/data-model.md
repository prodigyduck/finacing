# Data Model: Account-Based Portfolio Tracking

**Feature**: Account-Based Portfolio Tracking
**Date**: 2026-06-03
**Status**: Final

## Overview

포트폴리오 시스템을 단일 총액 기록에서 계좌별 다중 계좌 지원으로 확장합니다. 데이터 모델은 Clean Architecture를 준수하며 Domain 레이어에 정의됩니다.

## Entity Relationships

```
PortfolioSnapshot (1) ──> (N) AccountRecord
AccountRecord (1) ──> (0..N) Holding
AccountRecord (N) ──> (1) Account (static metadata)
```

## Domain Entities

### 1. Account (계좌)

**설명**: 투자 계좌의 정적 메타데이터

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class AccountType(Enum):
    """계좌 유형"""
    SECURITIES = "securities"  # 증권 계좌
    ISA = "isa"                # ISA (Individual Savings Account)
    IRA = "ira"                # IRA (Individual Retirement Account)
    PENSION = "pension"        # 연금 계좌
    CASH = "cash"              # 현성 계좌
    OTHER = "other"            # 기타

@dataclass(frozen=True)
class Account:
    """투자 계좌 엔티티"""
    name: str                              # 계좌명 (예: "증권계좌", "ISA")
    type: Optional[AccountType] = None      # 계좌 유형 (선택사항)
    description: Optional[str] = None      # 계좌 설명 (선택사항)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("계좌명은 비어있을 수 없습니다")
```

**검증 규칙**:
- `name`: 필수, 공백 제외 최소 1글자
- `type`: 선택사항, AccountType enum 값
- 중복 계좌명 허용 (사용자가 식별 가능한 한도 내에서)

---

### 2. Holding (보유 종목)

**설명**: 계좌가 보유한 개별 자산

```python
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class Holding:
    """보유 종목 엔티티"""
    symbol: str                              # 종목명 또는 심볼 (예: "삼성전자", "AAPL")
    quantity: Optional[int] = None           # 수량 (선택사항, 추후 확장)
    purchase_price: Optional[Decimal] = None # 매입가 (선택사항, 추후 확장)
    current_price: Optional[Decimal] = None # 현재가 (선택사항, 추후 확장)

    def __post_init__(self) -> None:
        if not self.symbol or not self.symbol.strip():
            raise ValueError("종목명은 비어있을 수 없습니다")
```

**검증 규칙**:
- `symbol`: 필수, 공백 제외 최소 1글자
- `quantity`: 양수 (제공되는 경우)
- `purchase_price`, `current_price`: 0 이상 (제공되는 경우)

**참고**: 현재 버전에서는 `symbol`만 필수이며, 수량과 가격은 추후 확장을 위해 선택사항입니다.

---

### 3. AccountRecord (계좌 기록)

**설명**: 특정 시점의 계좌 상태

```python
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Tuple

@dataclass(frozen=True)
class AccountRecord:
    """계좌 기록 엔티티 - 특정 날짜의 계좌 상태"""
    date: date                               # 기록 날짜
    account_name: str                        # 계좌명 (Account.name과 일치)
    total_amount_억: Decimal                  # 계좌 총액 (단위: 억 원)
    holdings: Tuple[Holding, ...] = ()       # 보유 종목 리스트 (불변)

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
```

**검증 규칙**:
- `date`: 유효한 날짜
- `account_name`: 필수, 공백 제외 최소 1글자
- `total_amount_억`: 0 이상
- `holdings`: 불변 튜플 (빈 튜플 허용)

---

### 4. PortfolioSnapshot (포트폴리오 스냅샷)

**설명**: 특정 날짜의 전체 포트폴리오 상태

```python
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Tuple, Optional

@dataclass(frozen=True)
class PortfolioSnapshot:
    """포트폴리오 스냅샷 엔티티 - 특정 날짜의 전체 상태"""
    date: date                               # 스냅샷 날짜
    accounts: Tuple[AccountRecord, ...]      # 모든 계좌 기록 (불변)

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
    def all_holdings(self) -> Tuple[Holding, ...]:
        """모든 계좌의 모든 보유 종목 (중복 포함)"""
        all_h = []
        for acc in self.accounts:
            all_h.extend(acc.holdings)
        return tuple(all_h)

    def get_account_record(self, account_name: str) -> Optional[AccountRecord]:
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
```

**검증 규칙**:
- `date`: 유효한 날짜
- `accounts`: 최소 1개 이상의 AccountRecord

---

## Legacy Entities (기존)

### InvestmentRecord (투자 기록)

```python
@dataclass(frozen=True)
class InvestmentRecord:
    date: date
    amount_억: Decimal
```

**상태**: 유지 보수 모드, 신규 AccountRecord로 대체 권장

### PortfolioHistory (포트폴리오 이력)

```python
@dataclass(frozen=True)
class PortfolioHistory:
    records: Tuple[InvestmentRecord, ...]
    year: int
```

**상태**: 유지 보수 모드, 신규 PortfolioSnapshot 기반으로 리팩토링 권장

---

## State Transitions

### AccountRecord 상태 전이

```
[새 기록 생성]
    ↓
[검증: 날짜, 계좌명, 금액, 종목]
    ↓
[저장: PortfolioSnapshot.accounts 튜플에 추가]
    ↓
[불변 상태: 수정 불가, 새로운 스냅샷 생성]
```

**중요**: 모든 엔티티는 불변(frozen=True)이므로 상태 수정은 불가능합니다. 변경이 필요한 경우 새로운 인스턴스를 생성해야 합니다.

---

## Validation Examples

### 유효한 AccountRecord

```python
from datetime import date
from decimal import Decimal

# 단일 계좌
record = AccountRecord(
    date=date(2026, 6, 3),
    account_name="증권계좌",
    total_amount_억=Decimal("3.50"),
    holdings=(
        Holding(symbol="삼성전자"),
        Holding(symbol="NAVER"),
        Holding(symbol="카카오"),
    )
)

# 현금 계좌 (종목 없음)
cash_record = AccountRecord(
    date=date(2026, 6, 3),
    account_name="현금",
    total_amount_억=Decimal("0.11"),
    holdings=()
)
```

### 유효한 PortfolioSnapshot

```python
# 다중 계좌 스냅샷
snapshot = PortfolioSnapshot(
    date=date(2026, 6, 3),
    accounts=(
        AccountRecord(
            date=date(2026, 6, 3),
            account_name="증권계좌",
            total_amount_억=Decimal("3.50"),
            holdings=(Holding(symbol="삼성전자"),)
        ),
        AccountRecord(
            date=date(2026, 6, 3),
            account_name="ISA",
            total_amount_억=Decimal("2.00"),
            holdings=(Holding(symbol="KB국책주성"),)
        ),
        AccountRecord(
            date=date(2026, 6, 3),
            account_name="IRA",
            total_amount_억=Decimal("0.11"),
            holdings=()
        )
    )
)

# 전체 총액: 3.50 + 2.00 + 0.11 = 5.61억
assert snapshot.total_amount == Decimal("5.61")
```

---

## Migration Strategy

### 레거시 → 신규 변환

```python
def migrate_investment_record_to_account_record(
    record: InvestmentRecord,
    default_account_name: str = "전체 포트폴리오"
) -> AccountRecord:
    """레거시 InvestmentRecord를 AccountRecord로 변환"""
    return AccountRecord(
        date=record.date,
        account_name=default_account_name,
        total_amount_억=record.amount_억,
        holdings=()
    )

def migrate_portfolio_history_to_snapshot(
    history: PortfolioHistory,
    default_account_name: str = "전체 포트폴리오"
) -> PortfolioSnapshot:
    """레거시 PortfolioHistory를 PortfolioSnapshot으로 변환"""
    # 각 날짜별로 하나의 AccountRecord 생성
    account_records = [
        AccountRecord(
            date=r.date,
            account_name=default_account_name,
            total_amount_억=r.amount_억,
            holdings=()
        )
        for r in history.records
    ]
    
    # 날짜별로 그룹화하여 PortfolioSnapshot 생성
    snapshots = []
    for date, records in group_by_date(account_records):
        snapshots.append(PortfolioSnapshot(date=date, accounts=tuple(records)))
    
    return snapshots
```

---

## Clean Architecture Compliance

### 의존성 방향

```
Presentation (app.py)
    ↓ depends on
Application (use_cases)
    ↓ depends on
Domain (entities) ← Infrastructure (parsers) depends on
```

**규칙**:
- Domain은 다른 레이어에 의존하지 않음
- Infrastructure는 Domain만 의존 (프레임워크 의존성 없음)
- Application은 Domain만 의존
- Presentation은 Application에 의존

**구현 시 주의사항**:
- `@dataclass(frozen=True)` 사용하여 불변성 보장
- type hints 필수 (mypy 통과)
- validation은 `__post_init__`에서 수행
- Decimal 사용하여 금전적 값 정확도 보장

---

## Testing Strategy

### 단위 테스트 커버리지 목표

- `Account`: 100%
- `Holding`: 100%
- `AccountRecord`: 100%
- `PortfolioSnapshot`: 100%

### 테스트 케이스 예시

```python
# test_account.py
def test_account_creation_valid():
    account = Account(name="증권계좌", type=AccountType.SECURITIES)
    assert account.name == "증권계좌"

def test_account_creation_invalid_empty_name():
    with pytest.raises(ValueError):
        Account(name="")

# test_portfolio_snapshot.py
def test_total_amount_calculation():
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(..., total_amount_억=Decimal("3.50")),
            AccountRecord(..., total_amount_억=Decimal("2.00")),
        )
    )
    assert snapshot.total_amount == Decimal("5.50")

def test_account_allocation():
    snapshot = PortfolioSnapshot(
        date=date(2026, 6, 3),
        accounts=(
            AccountRecord(..., total_amount_억=Decimal("3.50")),
            AccountRecord(..., total_amount_억=Decimal("1.50")),
        )
    )
    # 3.50 / 5.00 = 0.7
    assert snapshot.get_account_allocation("증권계좌") == Decimal("0.7")
```

---

## Appendix: Enum Definitions

```python
class AccountType(Enum):
    """계좌 유형 열거형"""
    SECURITIES = "securities"  # 증권 계좌
    ISA = "isa"                # ISA (Individual Savings Account)
    IRA = "ira"                # IRA (Individual Retirement Account)
    PENSION = "pension"        # 연금 계좌
    CASH = "cash"              # 현성 계좌
    OTHER = "other"            # 기타
```

---

**문서 버전**: 1.0
**마지막 수정**: 2026-06-03
**다음 단계**: API Contracts (`contracts/api-contracts.md`)
