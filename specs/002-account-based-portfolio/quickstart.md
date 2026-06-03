# Quick Start Guide: Account-Based Portfolio Tracking

**Feature**: Account-Based Portfolio Tracking
**Date**: 2026-06-03
**Status**: Phase 1 - Complete

---

## Overview

이 가이드는 계좌별 포트폴리오 추적 기능을 빠르게 시작하고 테스트하는 방법을 설명합니다. 데이터 형식, API 사용, 그리고 개발 환경 설정을 다룹니다.

---

## Prerequisites

### Required Tools

- **Python 3.11+**: 백엔드 개발
- **Node.js 20+**: 프론트엔드 개발
- **Obsidian**: 데이터 입력 (선택사항)

### Project Setup

```bash
# 프로젝트 클론
git clone <repo-url>
cd financing

# 백엔드 설정
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 프론트엔드 설정
cd frontend
npm install
cd ..
```

---

## Data Format

### Option 1: Legacy Format (단일 총액)

기존 형식은 여전히 지원됩니다:

```markdown
## 2026.06.03
5.61

## 2026.05.27
5.58
```

### Option 2: Account-Based Format (계좌별)

새로운 계좌별 형식:

```markdown
## 2026-06-03

### 계좌: 증권계좌
총액: 3.50억
보유종목: 삼성전자, NAVER, 카카오

### 계좌: ISA
총액: 2.00억
보유종목: KB국책주성, 미래에셋TDF

### 계좌: IRA
총액: 0.11억
보유종목: 

## 2026-06-01

### 계좌: 증권계좌
총액: 3.45억
보유종목: 삼성전자, NAVER
```

### 파싱 규칙

1. **날짜 형식**: `## YYYY-MM-DD` 또는 `## M.DD`
2. **계좌 헤더**: `### 계좌: {계좌명}`
3. **총액**: `총액: {X.XX}억` (억 단위)
4. **종목**: `보유종목: 종목1, 종목2, ...` (쉼표로 구분)
5. **종목 없음**: `보유종목:` 뒤에 공백 또는 생략

---

## Running the Application

### 1. Start Backend

```bash
# 터미널 1
source .venv/bin/activate
python -m src.presentation.app
```

백엔드가 `http://localhost:8000`에서 실행됩니다.

### 2. Start Frontend

```bash
# 터미널 2
cd frontend
npm run dev
```

프론트엔드가 `http://localhost:5180`에서 실행됩니다.

### 3. Open Dashboard

브라우저에서 `http://localhost:5180`을 엽니다.

---

## API Usage

### 1. Get Full Portfolio

```bash
curl http://localhost:8000/api/v1/history?year=2026
```

**응답**:
```json
{
  "records": [...],
  "latest": {"date": "2026-06-03", "amount": 5.61},
  "accounts": [
    {
      "name": "증권계좌",
      "latest_amount": 3.50,
      "allocation": 0.624,
      "holdings": [
        {"name": "삼성전자", "quantity": null, "value": null}
      ]
    }
  ],
  "comparison": {
    "best_performer": {"name": "ISA", "return_rate": 0.35}
  }
}
```

### 2. Filter by Account

```bash
curl "http://localhost:8000/api/v1/history?year=2026&account=증권계좌"
```

**응답**:
```json
{
  "account": "증권계좌",
  "records": [...],
  "latest": {"date": "2026-06-03", "amount": 3.50},
  "holdings": [...]
}
```

---

## Development Workflow

### TDD Cycle

```bash
# 1. 테스트 작성 (빨간)
vim tests/unit/domain/test_account.py

# 2. 테스트 실행 (빨간 - 실패)
pytest tests/unit/domain/test_account.py -v

# 3. 코드 구현 (초록)
vim src/domain/entities/account.py

# 4. 테스트 실행 (초록 - 성공)
pytest tests/unit/domain/test_account.py -v

# 5. 리팩토링
black src tests
ruff check src tests
```

### Running Tests

```bash
# 단위 테스트
pytest tests/unit/ -v

# E2E 테스트 (서버 실행 중)
pytest tests/e2e/ -v

# 커버리지
pytest tests/unit/ --cov=src --cov-report=html
```

---

## File Structure

### Adding New Domain Entities

```python
# src/domain/entities/account.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Account:
    name: str
    type: Optional[AccountType] = None
    
    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("계좌명은 비어있을 수 없습니다")
```

### Adding Tests

```python
# tests/unit/domain/test_account.py
import pytest
from src.domain.entities.account import Account

def test_account_creation():
    account = Account(name="증권계좌")
    assert account.name == "증권계좌"

def test_account_invalid_name():
    with pytest.raises(ValueError):
        Account(name="")
```

---

## Quick Examples

### Example 1: Create Test Data

테스트용 Obsidian 파일 생성:

```bash
# 테스트 데이터 파일
cat > test_investment.md << 'EOF'
## 2026-06-03

### 계좌: 테스트계좌
총액: 5.00억
보유종목: 삼성전자, NAVER

## 2026-06-01

### 계좌: 테스트계좌
총액: 4.50억
보유종목: 삼성전자
EOF
```

### Example 2: Test API with Python

```python
# test_api.py
import requests

response = requests.get("http://localhost:8000/api/v1/history?year=2026")
data = response.json()

print(f"전체 합계: {data['latest']['amount']}억")
print(f"계좌 수: {len(data['accounts'])}")
for acc in data['accounts']:
    print(f"  - {acc['name']}: {acc['latest_amount']}억 ({acc['allocation']*100:.1f}%)")
```

### Example 3: Test with Vue Component

```vue
<!-- frontend/src/components/AccountCard.vue -->
<script setup lang="ts">
import { computed } from 'vue'

interface Account {
  name: string
  latest_amount: number
  allocation: number
}

const props = defineProps<{
  account: Account
}>()

const allocationPercent = computed(() => 
  (props.account.allocation * 100).toFixed(1)
)
</script>

<template>
  <div class="account-card">
    <h3>{{ account.name }}</h3>
    <p>{{ account.latest_amount }}억</p>
    <p>{{ allocationPercent }}%</p>
  </div>
</template>
```

---

## Troubleshooting

### Common Issues

#### 1. 파싱 오류

**문제**: 데이터가 파싱되지 않음

**해결**:
```bash
# 데이터 형식 확인
cat ~/git/obsidian/투자/투자.md | head -20

# 파서 디버깅
python -c "
from src.infrastructure.parsers.obsidian_parser import ObsidianParser
with open('~/git/obsidian/투자/투자.md') as f:
    print(ObsidianParser().parse(f.read(), 2026))
"
```

#### 2. API 응답 없음

**문제**: `curl http://localhost:8000/api/v1/history`가 응답하지 않음

**해결**:
```bash
# 백엔드 실행 중인지 확인
curl http://localhost:8000/health

# 백엔드 로그 확인
tail -f logs/app.log
```

#### 3. 프론트엔드 차트 렌더링 오류

**문제**: 차트가 표시되지 않음

**해결**:
```bash
# 브라우저 콘솔 확인
# API 응답 데이터 확인

# 네트워크 탭에서 API 호출 확인
# 응답 형식이 api-contracts.md와 일치하는지 확인
```

---

## Next Steps

1. **Phase 2**: 구현 작업 시작 (`/speckit-tasks`)
2. **테스트 작성**: TDD 방식으로 Domain 엔티티부터 시작
3. **파서 구현**: 하이브리드 파서로 레거시+신규 형식 지원
4. **UI 개발**: 계좌별 차트와 필터링 구현

---

## Resources

- **Spec**: [spec.md](spec.md)
- **Plan**: [plan.md](plan.md)
- **Research**: [research.md](research.md)
- **Data Model**: [data-model.md](data-model.md)
- **API Contracts**: [contracts/api-contracts.md](contracts/api-contracts.md)

---

**문서 버전**: 1.0
**마지막 수정**: 2026-06-03
**준비 상태**: Phase 2 구현 준비 완료
