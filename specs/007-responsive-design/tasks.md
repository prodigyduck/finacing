# Tasks: Responsive Design

**Input**: Design documents from `/specs/007-responsive-design/`

**Tests**: Test tasks included

**Organization**: Tasks grouped by user story

---

## Phase 1: Setup

- [ ] T001 Create breakpoints SCSS file in frontend/src/styles/breakpoints.scss

---

## Phase 2: Foundational

- [ ] T002 [P] Define breakpoint variables in breakpoints.scss (mobile: 375px, tablet: 768px, desktop: 1920px)
- [ ] T003 [P] Create useBreakpoints.ts composable in frontend/src/composables/useBreakpoints.ts

---

## Phase 3: User Story 1 - 모바일 최적화 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 모바일(375px)에서 계좌 카드가 세로로 배치되고 그래프 높이가 조절된 것을 확인

**Independent Test**: 모바일 기기(또는 브라우저 모바일 모드)에서 대시보드를 열고 카드가 세로 배치되며 그래프 높이가 200-250px인지 확인

### Tests for US1

- [ ] T004 [P] [US1] Unit test for useBreakpoints in frontend/tests/unit/composables/useBreakpoints.spec.ts
- [ ] T005 [US1] E2E test for mobile layout in frontend/tests/e2e/responsive-design.spec.ts

### Implementation for US1

- [ ] T006 [US1] Add mobile media query in toss-theme.scss in frontend/src/styles/toss-theme.scss (@media max-width: 768px)
- [ ] T007 [US1] Update AccountCard.vue for vertical layout in mobile in frontend/src/components/AccountCard.vue
- [ ] T008 [US1] Adjust chart height for mobile in AccountChart.vue in frontend/src/components/AccountChart.vue (200-250px)
- [ ] T009 [US1] Update font sizes for mobile in frontend/src/styles/toss-theme.scss (12-14px)

---

## Phase 4: User Story 2 - 태블릿/데스크톱 레이아웃 (Priority: P2)

**Goal**: 사용자가 태블릿(2단)과 데스크톱(3단)에서 그리드 레이아웃과 사이드바를 확인

**Independent Test**: 태블릿과 데스크톱에서 대시보드를 열고 각각 2단/3단 그리드와 사이드바가 표시되는지 확인

### Tests for US2

- [ ] T010 [P] [US2] Unit test for ResponsiveGrid.vue in frontend/tests/unit/components/ResponsiveGrid.spec.ts
- [ ] T011 [US2] E2E test for tablet/desktop layout in frontend/tests/e2e/responsive-design.spec.ts

### Implementation for US2

- [ ] T012 [P] [US2] Create ResponsiveGrid.vue component in frontend/src/components/ResponsiveGrid.vue with CSS Grid
- [ ] T013 [P] [US2] Create Sidebar.vue component in frontend/src/components/Sidebar.vue with account list
- [ ] T014 [US2] Integrate ResponsiveGrid into DashboardLayout.vue in frontend/src/components/DashboardLayout.vue
- [ ] T015 [US2] Add tablet media query for 2-column grid in frontend/src/styles/toss-theme.scss (@media min-width: 768px)
- [ ] T016 [US2] Add desktop media query for 3-column grid and sidebar in frontend/src/styles/toss-theme.scss (@media min-width: 1920px)

---

## Phase 5: User Story 3 - 반응형 폰트와 간격 (Priority: P3)

**Goal**: 사용자가 어떤 기기에서든 폰트 크기와 요소 간 간격이 화면 크기에 맞게 조절된 것을 확인

**Independent Test**: 모바일/태블릿/데스크톱에서 각각 폰트 크기(12-14px, 14-16px, 16-18px)와 간격이 조절되는지 확인

### Tests for US3

- [ ] T017 [US3] E2E test for responsive font and spacing in frontend/tests/e2e/responsive-design.spec.ts

### Implementation for US3

- [ ] T018 [US3] Add responsive font sizes with clamp() in frontend/src/styles/toss-theme.scss
- [ ] T019 [US3] Add responsive spacing with calc() in frontend/src/styles/toss-theme.scss
- [ ] T020 [US3] Test font rendering across breakpoints in frontend/

---

## Phase 6: Polish

- [ ] T021 [P] Add landscape orientation support in frontend/src/styles/toss-theme.scss
- [ ] T022 [P] Add min-width warning for <320px screens
- [ ] T023 [P] Run all tests and ensure coverage
- [ ] T024 Performance optimization - CSS containment for layout thrashing
- [ ] T025 Update documentation in specs/007-responsive-design/implementation-summary.md

---

## Summary

- **Total Task Count**: 25 tasks
- **Tasks per User Story**: US1: 6 tasks, US2: 7 tasks, US3: 4 tasks
- **Parallel Opportunities**: 13 tasks marked [P]
- **MVP Scope**: Phase 1-3 (US1 only) = 9 tasks
