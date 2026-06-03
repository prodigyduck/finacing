# Implementation Plan: Account-Based Portfolio Tracking

**Branch**: `003-account-based-portfolio` | **Date**: 2026-06-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-account-based-portfolio/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

포트폴리오 시스템을 단일 총액 기록에서 계좌별 다중 계좌 지원으로 확장합니다. 각 계좌는 계좌명, 총액, 보유 종목 리스트를 포함하며, 시스템은 레거시 총액 형식과 새 계좌별 형식을 모두 파싱할 수 있어야 합니다. 사용자 인터페이스는 계좌별 차트, 통합 대시보드, 드릴다운 종목 상세, 계좌간 비교 및 배분 비율 분석을 제공합니다.

**Technical Approach**: Clean Architecture를 유지하며 Domain 엔티티에 계좌 관련 구조를 추가하고, Infrastructure 레이어의 파서를 하이브리드 형식을 지원하도록 확장합니다. TDD 방식으로 Domain 엔티티와 Application 유스케이스에 대한 단위 테스트를 먼저 작성합니다.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript/JavaScript (ES2022+)

**Primary Dependencies**:
- Backend: FastAPI, pydantic, pytest, pytest-cov
- Frontend: Vue.js 3, TypeScript, ECharts, Vuetify, Vite, Vitest

**Storage**: Obsidian markdown files (local, read-only)

**Testing**:
- Backend: pytest (unit tests), pytest-playwright (E2E)
- Frontend: Vitest (unit tests), Playwright (E2E)

**Target Platform**: Local web application (Backend: http://localhost:8000, Frontend: http://localhost:5180)

**Project Type**: Web service (FastAPI + Vue.js SPA)

**Performance Goals**:
- 데이터 파싱: 100 계좌 × 10년 데이터 (~12,000 레코드)를 1초 이내 처리
- 차트 렌더링: 500ms 이내에 계좌별 차트 표시
- API 응답: /api/v1/history는 200ms 이내 응답

**Constraints**:
- Obsidian 데이터는 읽기 전용, 수정 불가
- Clean Architecture 의존성 준수 (Infrastructure → Application → Domain)
- 기존 파서와의 호환성 유지
- 마이그레이션 도구는 선택사항

**Scale/Scope**:
- 최대 10개 계좌 지원
- 10년 이상의 시계열 데이터
- 계좌당 최대 50개 보유 종목

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality (Clean Architecture)

**Status**: ✅ PASS

**Verification Plan**:
- Domain 엔티티 (Account, Holding, AccountRecord)는 프레임워크 독립적으로 설계
- Infrastructure (ObsidianParser)는 Domain 엔티티만 의존, 직접 구현 로직 포함하지 않음
- Application (AnalyzeHistory)는 Domain 엔티티와 인터페이스만 의존
- type hints, Black formatting, Ruff linting 적용

### II. Testing Standards (TDD & Coverage)

**Status**: ✅ PASS

**Verification Plan**:
- Domain 엔티티: 단위 테스트 100% 커버리지 (pytest)
- Application 유스케이스: 단위 테스트 95% 이상 커버리지
- Infrastructure 파서: 단위 테스트 (레거시+신규 형식)
- E2E 테스트: Playwright로 계좌별 차트 렌더링 및 인터랙션 검증
- TDD workflow: Red-Green-Refactor

### III. User Experience Consistency (Toss-Style)

**Status**: ✅ PASS

**Verification Plan**:
- 계좌 카드: 명확한 계좌명, 총액, 비중 퍼센트 표시
- 차트: 최소 노이즈, 명확한 범례, 인터랙티브 필터링
- 드릴다운: 일관된 인터랙션 (클릭 → 상세 펼침)
- 색상 팔레트: 토스 스타일 (기본, 차축, 차순 등)
- 반응형: 모바일/데스크톱 지원

### IV. Performance Requirements

**Status**: ✅ PASS

**Verification Plan**:
- 파싱 성능: 12,000 레코드 < 1초 (pytest-benchmark)
- API 응답: < 200ms (locust 또는 pytest-playwright)
- 차트 렌더링: < 500ms (Playwright timing)
- 데이터 최적화: 불필요한 계산 캐싱, 지연 로딩

**Overall Gate Status**: ✅ ALL PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/002-account-based-portfolio/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output (pending)
├── data-model.md        # Phase 1 output (pending)
├── quickstart.md        # Phase 1 output (pending)
├── contracts/           # Phase 1 output (pending)
│   └── api-contracts.md # API endpoint specifications
└── tasks.md             # Phase 2 output (pending - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
# Backend: Python (FastAPI, Clean Architecture)
src/
├── domain/
│   └── entities/
│       ├── investment_record.py    # 기존: 총액 레코드
│       ├── account.py              # NEW: 계좌 엔티티
│       ├── holding.py               # NEW: 보유 종목 엔티티
│       ├── account_record.py        # NEW: 계좌 기록 엔티티
│       └── portfolio_snapshot.py   # NEW: 포트폴리오 스냅샷
├── application/
│   └── use_cases/
│       ├── analyze_history.py      # 기존: 추세 분석 (확장 필요)
│       └── compare_accounts.py      # NEW: 계좌 비교 유스케이스
├── infrastructure/
│   └── parsers/
│       ├── obsidian_parser.py       # 기존: 레거시 파서 (확장 필요)
│       └── account_parser.py         # NEW: 계좌별 파서
├── presentation/
│   └── app.py                        # FastAPI (확장 필요: 계좌별 엔드포인트)
└── config/
    └── logging.py                    # 기존

# Frontend: Vue.js 3 + TypeScript
frontend/src/
├── api/
│   └── client.ts                     # Axios (확장 필요)
├── components/
│   ├── PortfolioChart.vue           # 기존: 전체 차트 (확장 필요)
│   ├── AccountCard.vue               # NEW: 계좌 카드
│   ├── AccountChart.vue              # NEW: 계좌별 차트
│   └── HoldingsList.vue              # NEW: 종목 리스트 (드릴다운)
├── stores/
│   └── history.ts                    # Pinia (확장 필요: 계좌 상태)
├── views/
│   └── Dashboard.vue                 # 기존: 대시보드 (확장 필요)
└── router/
    └── index.ts                      # 기존

# Tests
tests/
├── unit/
│   ├── domain/
│   │   ├── test_account.py           # NEW
│   │   ├── test_holding.py           # NEW
│   │   └── test_account_record.py    # NEW
│   ├── application/
│   │   ├── test_analyze_history.py   # 기존 (확장 필요)
│   │   └── test_compare_accounts.py  # NEW
│   └── infrastructure/
│       ├── test_obsidian_parser.py   # 기존 (확장 필요)
│       └── test_account_parser.py    # NEW
└── e2e/
    └── test_account_dashboard.spec.ts # NEW: Playwright E2E
```

**Structure Decision**: Option 2 (Web application) selected. The project has a clear frontend/backend separation:
- Backend (`src/`): Python 3.11+ with FastAPI, following Clean Architecture
- Frontend (`frontend/`): Vue.js 3 SPA with TypeScript, ECharts visualization
- Tests co-located with implementation for better discoverability
- Domain entities remain framework-agnostic (no FastAPI/Pydantic in domain layer)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All constitution gates passed | No violations to justify |

---

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **하이브리드 파싱 전략**: 기존 ObsidianParser를 어떻게 확장하여 레거시와 신규 형식을 모두 지원할 것인가?
   - 옵션 A: 단일 파서에 다중 형식 지원 로직 추가
   - 옵션 B: 별도 AccountParser와 레거시 호환 래퍼
   - 옵션 C: 파서 체인 (패턴 매칭 → 적절한 파서로 위임)

2. **계좌별 마크다운 형식 설계**: 인간 친화적이고 파싱 가능한 형식은 무엇인가?
   - 옵션 A: 헤더 기반 (## 계좌명 하위에 종목 리스트)
   - 옵션 B: 테이블 형식 (Markdown table)
   - 옵션 C: 리스트 기반 (- 계좌명: 금액 [종목1, 종목2])

3. **선형 회귀 예측 확장**: 기존 AnalyzeHistory를 계좌별로 어떻게 확장할 것인가?
   - 각 계좌에 대해 별도 예측 실행
   - 전체 예측과 계좌별 예측 모두 제공
   - 사용자가 계좌 선택 시 해당 계좌만 예측

4. **API 설계**: 계좌별 데이터를 어떻게 노출할 것인가?
   - 옵션 A: 기존 /api/v1/history 확장 (accounts 배열 추가)
   - 옵션 B: 별도 /api/v1/accounts 엔드포인트
   - 옵션 C: 하이브리드 (전체 + 선택적 계좌 필터)

### Research Output

See `research.md` (to be generated)

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` (to be generated)

### API Contracts

See `contracts/api-contracts.md` (to be generated)

### Quick Start Guide

See `quickstart.md` (to be generated)

---

## Phase 2: Implementation Tasks

Generated by `/speckit-tasks` command (not part of `/speckit-plan`)
