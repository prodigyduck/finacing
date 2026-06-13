# Tasks: Data Change Highlight

**Input**: Design documents from `/specs/005-data-change-highlight/`

**Tests**: Test tasks included

**Organization**: Tasks grouped by user story

---

## Phase 1: Setup

- [ ] T001 Create composables directory structure in frontend/src/composables/
- [ ] T002 [P] Create utils directory in frontend/src/utils/

---

## Phase 2: Foundational

- [ ] T003 Create date helper utilities in frontend/src/utils/dateHelpers.ts (last business day, week/month aggregation)
- [ ] T004 [P] Setup change calculation types in frontend/src/types/change.ts

---

## Phase 3: User Story 1 - 전일 대비 증감 표시 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 각 계좌의 전일 대비 증감을 🔺🔻 아이콘과 색상으로 확인

**Independent Test**: 대시보드를 열고 각 계좌 카드에 증감(🔺+0.1억 또는 🔻-0.05억)가 색상과 함께 표시되는지 확인

### Tests for US1

- [ ] T005 [P] [US1] Unit test for useChangeCalculation composable in frontend/tests/unit/composables/useChangeCalculation.spec.ts
- [ ] T006 [US1] E2E test for change indicator display in frontend/tests/e2e/data-change-highlight.spec.ts

### Implementation for US1

- [ ] T007 [US1] Create useChangeCalculation.ts composable in frontend/src/composables/useChangeCalculation.ts with previous day comparison logic
- [ ] T008 [US1] Create ChangeIndicator.vue component in frontend/src/components/ChangeIndicator.vue with icon (🔺🔻) and color (red/blue)
- [ ] T009 [US1] Integrate ChangeIndicator into AccountCard.vue in frontend/src/components/AccountCard.vue
- [ ] T010 [US1] Handle first day edge case (display "-" or "데이터 없음") in useChangeCalculation.ts

---

## Phase 4: User Story 2 - 기간 선택 기능 (Priority: P2)

**Goal**: 사용자가 일별/주별/월별 탭을 선택하여 원하는 기간의 데이터 확인

**Independent Test**: 기간 탭을 선택하고 그래프가 해당 기간에 맞게 표시되는지 확인

### Tests for US2

- [ ] T011 [P] [US2] Unit test for usePeriodFilter composable in frontend/tests/unit/composables/usePeriodFilter.spec.ts
- [ ] T012 [US2] E2E test for period switching in frontend/tests/e2e/data-change-highlight.spec.ts

### Implementation for US2

- [ ] T013 [US2] Create usePeriodFilter.ts composable in frontend/src/composables/usePeriodFilter.ts with daily/weekly/monthly aggregation
- [ ] T014 [US2] Create PeriodSelector.vue component in frontend/src/components/PeriodSelector.vue with tab UI
- [ ] T015 [US2] Integrate PeriodSelector into Dashboard.vue in frontend/src/views/Dashboard.vue
- [ ] T016 [US2] Update AccountChart to use filtered data from usePeriodFilter in frontend/src/components/AccountChart.vue
- [ ] T017 [US2] Handle empty period case (display "해당 기간 데이터 없음") in usePeriodFilter.ts

---

## Phase 5: User Story 3 - 요약 정보 상단 표시 (Priority: P3)

**Goal**: 사용자가 상단에 총 자산과 전일 대비 변화를 요약된 것을 확인

**Independent Test**: 대시보드 최상단을 보고 "총 자산: 5.57억 (전일 대비 🔺 +0.03억)"가 표시되는지 확인

### Tests for US3

- [ ] T018 [US3] E2E test for summary bar display and click interaction in frontend/tests/e2e/data-change-highlight.spec.ts

### Implementation for US3

- [ ] T019 [US3] Create SummaryBar.vue component in frontend/src/components/SummaryBar.vue with total assets and change display
- [ ] T020 [US3] Add click-to-scroll functionality in SummaryBar.vue
- [ ] T021 [US3] Integrate SummaryBar into Dashboard.vue at top of page in frontend/src/views/Dashboard.vue
- [ ] T022 [US3] Calculate total assets and change across all accounts in SummaryBar.vue

---

## Phase 6: Polish

- [ ] T023 [P] Update TypeScript interfaces in frontend/src/types/
- [ ] T024 [P] Add ARIA labels for accessibility
- [ ] T025 [P] Run all tests and ensure coverage
- [ ] T026 Performance optimization - memoize change calculations
- [ ] T027 Update documentation in specs/005-data-change-highlight/implementation-summary.md

---

## Summary

- **Total Task Count**: 27 tasks
- **Tasks per User Story**: US1: 6 tasks, US2: 7 tasks, US3: 5 tasks
- **Parallel Opportunities**: 13 tasks marked [P]
- **MVP Scope**: Phase 1-3 (US1 only) = 10 tasks
