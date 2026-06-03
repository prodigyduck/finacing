# Research: Account-Based Portfolio Tracking

**Feature**: Account-Based Portfolio Tracking
**Date**: 2026-06-03
**Status**: Complete

## Research Tasks

### 1. 하이브리드 파싱 전략

**Decision**: **옵션 C - 파서 체인 (패턴 매칭 → 적절한 파서로 위임)**

**Rationale**:
- **유연성**: 새 형식이 추가될 때마다 파서를 체인에 추가하기만 하면 됨
- **단일 책임**: 각 파서는 자신의 형식만 처리
- **테스트 가능성**: 각 파서를 독립적으로 테스트 가능
- **확장성**: 추후 다른 형식(JSON, CSV 등)이 추가되어도 대응 가능

**구현 방안**:
```python
class ParserChain:
    def __init__(self, parsers: List[BaseParser]):
        self.parsers = parsers
    
    def parse(self, text: str, year: int) -> PortfolioSnapshot:
        for parser in self.parsers:
            if parser.can_parse(text):
                return parser.parse(text, year)
        raise ValueError("No parser can handle this format")

class LegacyParser(BaseParser):
    """기존 M.DD 금액 형식"""
    def can_parse(self, text: str) -> bool:
        return bool(re.search(r'^\d{1,2}\.\d{1,2}\s+\d+\.?\d*$', text, multiline=True))

class AccountParser(BaseParser):
    """새 계좌별 형식"""
    def can_parse(self, text: str) -> bool:
        return '## 계좌:' in text or '### 계좌:' in text
```

**Alternatives Considered**:
- **옵션 A (단일 파서)**: 단일 클래스에 모든 로직 → 복잡해짓고 테스트 어려움
- **옵션 B (별도 파서 + 래퍼)**: 래퍼가 파서 선택 로직을 가짐 → 파서 체인과 유사하지만 덜 유연함

---

### 2. 계좌별 마크다운 형식 설계

**Decision**: **옵션 A - 헤더 기반 (## 계좌명 하위에 종목 리스트)**

**Rationale**:
- **인간 친화적**: Obsidian에서 헤더를 폴드/펼침으로 계좌별 정리 가능
- **파싱 용이**: 헤더 레벨로 계좌 구분 명확
- **확장성**: 계좌 메타데이터(계좌 유형 등)를 헤더 속성으로 추가 가능
- **시각적 구조**: 계좌별로 명확하게 시각적으로 분리

**형식 예시**:
```markdown
---
key: value
---

## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오

### 계좌: ISA
총액: 2.00억
보유종목: KB국책주식, 미래에셋TDF

### 계좌: IRA
총액: 0.11억
보유종목: (없음)

## 2026-06-01

### 계좌: 증권계좌
총액: 3.45억
보유종목: 삼성전자, NAVER
```

**파싱 로직**:
1. `### 계좌: {계좌명}` 헤더로 계좌 시작 감지
2. 다음 `###` 또는 `##` 헤더까지를 해당 계좌 블록으로 처리
3. `총액:` 라인에서 금액 추출
4. `보유종목:` 라인에서 쉼표로 구분된 종목 리스트 추출

**Alternatives Considered**:
- **옵션 B (테이블 형식)**: 테이블이 모바일에서 깨질 수 있음, 편집이 덜 편리함
- **옵션 C (리스트 기반)**: 한 줄에 모든 정보 → 가독성 낮음, 계좌별로 분리가 덜 명확함

---

### 3. 선형 회귀 예측 확장

**Decision**: **각 계좌에 대해 별도 예측 실행 + 전체 예측 모두 제공**

**Rationale**:
- **사용자 가치**: 계좌별 성과 파악 + 전체 포트폴리오 예측 모두 가능
- **일관성**: 기존 AnalyzeHistory 로직 재사용
- **성능**: 계좌 수는 최대 10개 → 계산 부하 미미

**구현 방안**:
```python
class AnalyzeAccounts:
    def execute(self, snapshot: PortfolioSnapshot) -> Dict[str, Any]:
        accounts = snapshot.accounts
        results = {
            "total": self._analyze_total(accounts),
            "accounts": [self._analyze_account(acc) for acc in accounts],
            "comparison": self._compare_accounts(accounts),
        }
        return results
    
    def _analyze_account(self, account: Account) -> Dict:
        # 기존 _linear_regression 로직 재사용
        records = account.history
        reg = _linear_regression(records)
        # ... projections 계산
```

**Alternatives Considered**:
- **전체 예측만**: 사용자가 계좌별 성과 파악 불가 → 핵심 요구사항 충족 실패
- **선택적 예측**: 사용자가 계좌를 선택해야 예측 → 추가 인터랙션 필요

---

### 4. API 설계

**Decision**: **옵션 A - 기존 /api/v1/history 확장 (accounts 배열 추가)**

**Rationale**:
- **호환성**: 기존 클라이언트가 계좌 데이터 없이도 작동 가능
- **단일 엔드포인트**: 데이터 요청을 한 곳에서 처리
- **선택적 필터**: 쿼리 파라미터로 계좌 필터링 가능

**API 설계**:
```typescript
// 기존 형식 (호환성 유지)
GET /api/v1/history?year=2026
{
  "records": [...],           // 전체 합계 시계열
  "latest": {...},
  "earliest": {...},
  "total_change": 1.23,
  "return_rate": 0.45,
  "projections": [...],
  "accounts": [               // NEW: 계좌별 데이터
    {
      "name": "증권계좌",
      "latest_amount": 3.50,
      "records": [...],       // 계좌별 시계열
      "projections": [...],   // 계좌별 예측
      "holdings": [...],      // 최신 종목 리스트
      "allocation": 0.62      // 전체 대비 비중
    },
    ...
  ],
  "comparison": {             // NEW: 계좌간 비교
    "best_performer": "증권계좌",
    "worst_performer": "IRA",
    "allocation_table": [...]
  }
}

// 계좌 필터 (선택사항)
GET /api/v1/history?year=2026&account=증권계좌
{
  // 위와 동일하지만 accounts 배열에 해당 계좌만 포함
}
```

**Alternatives Considered**:
- **옵션 B (/api/v1/accounts 별도)**: 추가 엔드포인트 → 클라이언트가 두 번 호출해야 함
- **옵션 C (하이브리드)**: /api/v1/history와 /api/v1/accounts 모두 → 중복 복잡도

---

## 기술적 고려사항

### Domain 엔티티 설계

**새로운 엔티티**:
```python
@dataclass(frozen=True)
class Account:
    name: str
    type: Optional[AccountType] = None  # 증권, ISA, IRA 등
    total_amount_억: Decimal

@dataclass(frozen=True)
class Holding:
    symbol: str  # 종목명 (예: "삼성전자")
    quantity: Optional[int] = None      # 수량 (선택사항, 추후 확장)
    purchase_price: Optional[Decimal] = None  # 매입가 (선택사항)

@dataclass(frozen=True)
class AccountRecord:
    date: date
    account_name: str
    total_amount_억: Decimal
    holdings: Tuple[Holding, ...] = ()  # 불변 튜플

@dataclass(frozen=True)
class PortfolioSnapshot:
    date: date
    accounts: Tuple[AccountRecord, ...]
    
    @property
    def total_amount(self) -> Decimal:
        return sum(r.total_amount_억 for r in self.accounts)
```

### 마이그레이션 전략

**자동 마이그레이션 도구** (선택사항):
```python
def migrate_legacy_to_accounts(
    legacy_records: List[InvestmentRecord],
    default_account_name: str = "전체 포트폴리오"
) -> List[AccountRecord]:
    """레거시 데이터를 계좌별 형식으로 변환"""
    return [
        AccountRecord(
            date=r.date,
            account_name=default_account_name,
            total_amount_억=r.amount_억,
            holdings=()
        )
        for r in legacy_records
    ]
```

### 성능 최적화

1. **파싱**: 12,000 레코드 < 1초
   - 정규식 미리 컴파일
   - 한 번의 파일 읽기로 모든 레코드 처리

2. **API 응답**: < 200ms
   - 계좌별 예측 병렬 계산 (concurrent.futures)
   - 불필요한 필드는 선택적 노출

3. **차트 렌더링**: < 500ms
   - ECharts lazy loading
   - 계좌 선택 시만 해당 차트 렌더링

---

## 결론

모든 연구 과제가 해결되었으며, 다음과 같은 결론을 도출했습니다:

1. **파싱**: 파서 체인 패턴으로 레거시 + 신규 형식 모두 지원
2. **데이터 형식**: 헤더 기반의 인간 친화적 마크다운 형식
3. **예측**: 계좌별 선형 회귀 + 전체 예측 모두 제공
4. **API**: 기존 엔드포인트 확장으로 호환성 유지

이제 Phase 1(데이터 모델, 컨트랙트)로 진행할 수 있습니다.
