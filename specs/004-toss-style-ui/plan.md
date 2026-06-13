# Implementation Plan: Toss-Style UI/UX Enhancement

**Branch**: `004-toss-style-ui` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-toss-style-ui/spec.md`

## Summary

대시보드 UI/UX를 토스 스타일로 개선한다. 카드 디자인(둥근 모서리 16px, 그림자 효과), 색상 팔레트(차축 #00BFFF, 차순 #FF6B6B, 기본 #F5F5F5), 레이아웃(계좌 카드 상단 가로 배치, 그래프 하단 크게, padding 24px)을 적용한다. 기존 Vue.js 3 + ECharts 기반 프론트엔드를 수정하며, 백엔드는 변경 없이 기존 API를 그대로 사용한다.

## Technical Context

**Language/Version**: TypeScript/JavaScript (ES2022+), Python 3.11+ (기존 백엔드 유지)

**Primary Dependencies**: Vue.js 3, ECharts, Vuetify, Vite, Vitest

**Storage**: Obsidian markdown files (local, read-only) - 기존 데이터 소스 유지

**Testing**: Vitest (unit), Playwright (E2E)

**Target Platform**: Local web application (Backend: http://localhost:8000, Frontend: http://localhost:5180)

**Project Type**: Web service (FastAPI + Vue.js SPA)

**Performance Goals**: 차트 렌더링 500ms 이내, 페이지 로드 1초 이내

**Constraints**: Obsidian 데이터는 읽기 전용, 기존 Clean Architecture 유지, 백엔드 API 변경 없음

**Scale/Scope**: 최대 10개 계좌, 모바일(375px) ~ 데스크톱(1920px+) 지원

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality (Clean Architecture)

**Status**: ✅ PASS

**Verification**: 이 feature는 프론트엔드 UI 컴포넌트만 수정하며, 백엔드 Clean Architecture는 영향받지 않음. Vue.js 컴포넌트는 기존 패턴을 따르며, TypeScript 타입 안전성을 유지함.

### II. Testing Standards (TDD & Coverage)

**Status**: ✅ PASS

**Verification**: 새로운 UI 컴포넌트에 대해 Vitest 단위 테스트와 Playwright E2E 테스트를 작성함. 기존 AccountChart.vue, AllocationChart.vue 등의 테스트를 업데이트함.

### III. User Experience Consistency (Toss-Style)

**Status**: ✅ PASS (본 feature의 주 목적)

**Verification**: 토스 스타일 디자인 가이드(색상, 간격, 폰트)를 따르며, 반응형과 접근성을 보장함.

### IV. Performance Requirements (Responsive & Efficient)

**Status**: ✅ PASS

**Verification**: 기존 차트 렌더링 성능을 유지하며, 추가 CSS/스타일링은 브라우저 네이티브 최적화에 의존함. Lazy evaluation 불필요.

**Overall Gate Status**: ✅ ALL PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/004-toss-style-ui/
├── plan.md              # This file
├── research.md          # Phase 0 output (토스 디자인 가이드 연구)
├── data-model.md        # Phase 1 output (UI 엔티티)
├── quickstart.md        # Phase 1 output (개발 시작 가이드)
├── contracts/           # Phase 1 output (UI 컴포넌트 인터페이스)
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── AccountChart.vue         # 수정: 색상 팔레트, 레이아웃
│   │   ├── AllocationChart.vue     # 수정: 색상 팔레트
│   │   ├── ComparisonTable.vue     # 수정: 색상 팔레트
│   │   ├── AccountCard.vue         # 신규: 계좌 카드 (둥근 모서리, 그림자)
│   │   ├── CircularProgress.vue    # 신규: 배분 비율 원형 프로그레스
│   │   └── DashboardLayout.vue     # 신규: 레이아웃 컴포넌트
│   ├── styles/
│   │   ├── toss-theme.scss         # 신규: 토스 스타일 테마
│   │   └── variables.scss          # 수정: 색상 변수 (차축, 차순, 기본)
│   └── views/
│       └── Dashboard.vue            # 수정: 레이아웃 적용
└── tests/
    ├── unit/
    │   ├── components/
    │   │   ├── AccountCard.spec.ts
    │   │   └── CircularProgress.spec.ts
    │   └── styles/
    │       └── toss-theme.spec.ts
    └── e2e/
        └── toss-style-ui.spec.ts    # Playwright E2E 테스트

# 백엔드는 변경 없음
src/ (기존 그대로)
```

**Structure Decision**: Web application (frontend + backend) - 프론트엔드만 수정

## Complexity Tracking

> **필요 없음** - Constitution Gate 모두 통과

---

## Phase 0: Research & Decisions

### Research Tasks

1. **토스 디자인 가이드 연구**: 토스의 공식 디자인 시스템(색상, 간격, 폰트, 둥근 모서리, 그림자)을 문서화
2. **Vue.js 3 + Vuetify 스타일링 방법**: 전역 테마 적용, CSS 변수, scoped 스타일 비교
3. **ECharts 색상 팔레트 설정**: 차트 시리즈 색상, 테마 옵션, 커스텀 색상 적용 방법
4. **반응형 레이아웃 패턴**: CSS Grid, Flexbox, 미디어 쿼리를 활용한 카드 배치
5. **원형 프로그레스 구현**: ECharts Gauge 차트 또는 SVG 기반 구현 선택

### Research Output (research.md)

**Decision: 토스 디자인 가이드 채택**

- **색상 팔레트**:
  - 차축 (Primary): #00BFFF (Deep Sky Blue)
  - 차순 (Secondary): #FF6B6B (Coral Red)
  - 기본 (Neutral): #F5F5F5 (Light Gray), #333333 (Dark Gray)
  - 증감: 증가 #FF6B6B, 감소 #4A90E2 (Blue)
- **간격 (Spacing)**: 8px 기준 그리드 (8px, 16px, 24px, 32px)
- **둥근 모서리 (Border Radius)**: 8px (작은 요소), 16px (카드), 24px (모달)
- **그림자 (Box Shadow)**: `0 2px 8px rgba(0, 0, 0, 0.1)` (기본), `0 4px 16px rgba(0, 0, 0, 0.15)` (호버)
- **폰트 (Typography)**: 14px (기본), 16px (중요), 18px Bold (제목), 12px (캡션)

**Decision: 전역 테마 + CSS 변수 방식**

- Vuetify 3의 전역 테마 설정을 사용하여 기본 색상과 간격을 정의
- CSS 변수(`--toss-primary`, `--toss-spacing`, 등)를 사용하여 컴포넌트 간 일관성 보장
- Scoped 스타일은 컴포넌트별 특수 사항에만 사용

**Decision: ECharts 커스텀 색상**

- ECharts `color` 옵션에 토스 색상 팔레트 배열을 전달
- 차트 시리즈별로 명시적 색상을 지정하여 일관성 보장

**Decision: CSS Grid + Flexbox 레이아웃**

- 계좌 카드: CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`)로 반응형 배치
- 모바일: 미디어 쿼리 (`@media (max-width: 768px)`)로 세로 배치
- 그래프 영역: Flexbox `flex: 1`으로 하단 확보

**Decision: SVG 기반 원형 프로그레스**

- ECharts Gauge 차트를 사용하여 원형 프로그레스 구현
- 배분 비율 0% ~ 100% 범위, 색상 그라데이션 지원

---

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**UI 엔티티** (백엔드와 독립적):

```typescript
interface AccountCardProps {
  accountName: string;        // 계좌명 (최대 20자, 초과 시 말줄임표)
  totalAmount: number;        // 총액 (억 단위)
  allocation: number;         // 배분 비율 (0 ~ 100%)
  changeAmount?: number;      // 증감액 (선택, 전일 대비)
  changeType?: 'increase' | 'decrease' | 'neutral';  // 증감 유형
}

interface CircularProgressProps {
  value: number;              // 0 ~ 100
  size?: number;             // 기본 80px
  color?: string;            // 기본 --toss-primary
  thickness?: number;        // 기본 8px
}

interface TossTheme {
  colors: {
    primary: string;         // #00BFFF
    secondary: string;       // #FF6B6B
    neutral: string;         // #F5F5F5
    increase: string;        // #FF6B6B
    decrease: string;        // #4A90E2
  };
  spacing: {
    xs: string;              // 8px
    sm: string;              // 16px
    md: string;              // 24px
    lg: string;              // 32px
  };
  borderRadius: {
    sm: string;              // 8px
    md: string;              // 16px
    lg: string;              // 24px
  };
  shadows: {
    default: string;        // 0 2px 8px rgba(0, 0, 0, 0.1)
    hover: string;          // 0 4px 16px rgba(0, 0, 0, 0.15)
  };
}
```

### Component Contracts (contracts/)

**AccountCard.vue**:

```typescript
interface Props {
  account: AccountCardProps;
}

interface Emits {
  (e: 'click', accountName: string): void;
}

// Template:
// - CSS class: `.account-card` (둥근 모서리 16px, 그림자)
// - 계좌명: 18px Bold
// - 총액: 16px Regular
// - 배분 비율: CircularProgress 컴포넌트
// - 증감: 색상과 아이콘 (🔺/🔻)
```

**CircularProgress.vue**:

```typescript
interface Props {
  value: number;             // 0 ~ 100
  size?: number;            // 기본 80px
  color?: string;           // 기본 --toss-primary
  thickness?: number;       // 기본 8px
}

// Template:
// - SVG circle 요소로 원형 프로그레스 구현
// - stroke-dasharray로 진행률 표시
// - 중앙에 텍스트로 백분율 표시
```

**DashboardLayout.vue**:

```typescript
interface Props {
  accounts: AccountCardProps[];
  chartData: ChartData;
}

// Template:
// - 상단: 계좌 카드 Grid (가로 배치, padding 24px)
// - 하단: 차트 영역 (flex: 1)
```

### Quickstart (quickstart.md)

**개발 시작 가이드**:

1. **의존성 설치**: 기존 패키지 유지 (Vue.js 3, Vuetify, ECharts)
2. **테마 파일 생성**: `frontend/src/styles/toss-theme.scss` 작성
3. **컴포넌트 생성 순서**:
   - `CircularProgress.vue` → 단위 테스트
   - `AccountCard.vue` → 단위 테스트
   - `DashboardLayout.vue` → E2E 테스트
4. **기존 컴포넌트 수정**:
   - `AccountChart.vue`: 색상 팔레트 적용
   - `AllocationChart.vue`: 색상 팔레트 적용
   - `Dashboard.vue`: 레이아웃 적용
5. **테스트 실행**:
   - 단위 테스트: `npm test`
   - E2E 테스트: `npm run test:e2e`

---

## Agent Context Update

CLAUDE.md의 plan reference를 업데이트해야 함 (이미 002-account-based-portfolio로 설정됨, 004-toss-style-ui로 변경 필요 시)

---

## Constitution Check (Re-evaluated Post-Design)

*GATE: Must pass before Phase 2 (tasks)*

### I. Code Quality (Clean Architecture)

**Status**: ✅ PASS

**Verification**: 프론트엔드 UI 컴포넌트만 수정, 백엔드는 영향 없음. TypeScript 타입 안전성 유지.

### II. Testing Standards (TDD & Coverage)

**Status**: ✅ PASS

**Verification**: 각 UI 컴포넌트에 Vitest 단위 테스트 작성, Playwright E2E 테스트로 전체 사용자 흐름 검증.

### III. User Experience Consistency (Toss-Style)

**Status**: ✅ PASS

**Verification**: 토스 디자인 가이드를 문서화하고 모든 컴포넌트에 적용. 색상, 간격, 폰트가 일관적임.

### IV. Performance Requirements (Responsive & Efficient)

**Status**: ✅ PASS

**Verification**: CSS/SVG 기반 구현으로 네이티브 성능 활용. 차트 렌더링 기존 500ms 유지 목표.

**Overall Gate Status**: ✅ ALL PASSED - Proceed to Phase 2 (/speckit-tasks)
