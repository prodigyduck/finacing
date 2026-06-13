# Tasks: Interactive Features

**Input**: Design documents from `/specs/006-interactive-features/`

**Tests**: Test tasks included

**Organization**: Tasks grouped by user story

---

## Phase 1: Setup

- [ ] T001 Create router directory structure in frontend/src/router/

---

## Phase 2: Foundational

- [ ] T002 Setup ECharts interaction types in frontend/src/types/chart.ts (tooltip, legend, dataZoom)
- [ ] T003 [P] Install Vue Router dependency if not present in frontend/

---

## Phase 3: User Story 1 - 그래프 인터랙션 개선 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 그래프에서 향상된 툴팁, 레전드 클릭 show/hide, 줌 인/아웃을 사용

**Independent Test**: 계좌별 추이 그래프에서 데이터 포인트에 마우스 오버 시 툴팁 확인, 레전드 클릭으로 show/hide 확인, 마우스 휠로 줌 확인

### Tests for US1

- [ ] T004 [P] [US1] Unit test for useChartInteraction composable in frontend/tests/unit/composables/useChartInteraction.spec.ts
- [ ] T005 [US1] E2E test for chart tooltip, legend click, zoom in frontend/tests/e2e/interactive-features.spec.ts

### Implementation for US1

- [ ] T006 [US1] Create useChartInteraction.ts composable in frontend/src/composables/useChartInteraction.ts with tooltip, legend, zoom logic
- [ ] T007 [US1] Update AccountChart.vue to use enhanced tooltip in frontend/src/components/AccountChart.vue
- [ ] T008 [US1] Add legend click show/hide functionality in AccountChart.vue
- [ ] T009 [US1] Implement mouse wheel zoom with dataZoom in AccountChart.vue

---

## Phase 4: User Story 2 - 계좌 드릴다운 (Priority: P2)

**Goal**: 사용자가 계좌 카드를 클릭하여 보유 종목 상세와 종목별 변동 차트 확인

**Independent Test**: 계좌 카드를 클릭하고 모달이 열리며 보유 종목 리스트와 종목별 차트가 표시되는지 확인

### Tests for US2

- [ ] T010 [P] [US2] Unit test for AccountDetailModal component in frontend/tests/unit/components/AccountDetailModal.spec.ts
- [ ] T011 [US2] E2E test for drilldown flow in frontend/tests/e2e/interactive-features.spec.ts

### Implementation for US2

- [ ] T012 [P] [US2] Create HoldingChart.vue component in frontend/src/components/HoldingChart.vue for stock charts
- [ ] T013 [US2] Create AccountDetailModal.vue component in frontend/src/components/AccountDetailModal.vue
- [ ] T014 [US2] Add click handler to AccountCard.vue to open modal in frontend/src/components/AccountCard.vue
- [ ] T015 [US2] Integrate HoldingChart into AccountDetailModal in AccountDetailModal.vue
- [ ] T016 [US2] Add back button and close functionality in AccountDetailModal.vue

---

## Phase 5: User Story 3 - 계좌 비교 모드 (Priority: P3)

**Goal**: 사용자가 두 계좌를 선택하여 나란히 비교하고 기간별 before/after 확인

**Independent Test**: 비교 모드 버튼을 클릭하고 두 계좌를 선택하여 비교 그래프와 증감율이 표시되는지 확인

### Tests for US3

- [ ] T017 [P] [US3] Unit test for useAccountComparison composable in frontend/tests/unit/composables/useAccountComparison.spec.ts
- [ ] T018 [US3] E2E test for comparison mode in frontend/tests/e2e/interactive-features.spec.ts

### Implementation for US3

- [ ] T019 [US3] Create useAccountComparison.ts composable in frontend/src/composables/useAccountComparison.ts with comparison logic
- [ ] T020 [US3] Create CompareMode.vue component in frontend/src/components/CompareMode.vue with account selector
- [ ] T021 [US3] Add period selector for before/after in CompareMode.vue
- [ ] T022 [US3] Display side-by-side charts with difference calculation in CompareMode.vue
- [ ] T023 [US3] Handle same account selection error in CompareMode.vue

---

## Phase 6: Polish

- [ ] T024 [P] Update router routes in frontend/src/router/routes.ts for drilldown
- [ ] T025 [P] Add ARIA labels for accessibility
- [ ] T026 [P] Run all tests and ensure coverage
- [ ] T027 Performance optimization - debounce zoom events
- [ ] T028 Update documentation in specs/006-interactive-features/implementation-summary.md

---

## Summary

- **Total Task Count**: 28 tasks
- **Tasks per User Story**: US1: 6 tasks, US2: 7 tasks, US3: 7 tasks
- **Parallel Opportunities**: 15 tasks marked [P]
- **MVP Scope**: Phase 1-3 (US1 only) = 9 tasks
