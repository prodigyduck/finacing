# Tasks: Toss-Style UI/UX Enhancement

**Input**: Design documents from `/specs/004-toss-style-ui/`

**Prerequisites**: plan.md, spec.md

**Tests**: Test tasks included (Constitution requires TDD)

**Organization**: Tasks grouped by user story for independent implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`
- **Tests**: `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory structure for styles and components per implementation plan
- [ ] T002 [P] Install SCSS dependencies for theme support in frontend/
- [ ] T003 [P] Configure Vite for SCSS processing in frontend/vite.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story

⚠️ CRITICAL: No user story work can begin until this phase is complete

- [ ] T004 Create global theme variables in frontend/src/styles/variables.scss (colors, spacing, border-radius, shadows)
- [ ] T005 [P] Create Toss theme base file in frontend/src/styles/toss-theme.scss with color palette and design tokens
- [ ] T006 [P] Setup theme composition in frontend/src/main.ts to import global styles

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 계좌 카드 시각적 개선 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 둥근 모서리(16px), 그림자 효과, 18px Bold 폰트의 계좌 카드를 확인하고 배분 비율을 원형 프로그레스로 볼 수 있음

**Independent Test**: 대시보드를 열고 계좌 카드가 둥근 모서리, 그림자, 굵은 폰트로 표시되며 원형 프로그레스가 배분 비율을 시각화하는지 확인

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T007 [P] [US1] Unit test for AccountCard.vue props in frontend/tests/unit/components/AccountCard.spec.ts
- [ ] T008 [P] [US1] Unit test for CircularProgress.vue in frontend/tests/unit/components/CircularProgress.spec.ts
- [ ] T009 [US1] E2E test for account card visual style in frontend/tests/e2e/toss-style-ui.spec.ts (rounded corners, shadow, font)

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create CircularProgress.vue component in frontend/src/components/CircularProgress.vue with SVG circle and percentage display
- [ ] T011 [P] [US1] Create AccountCard.vue component in frontend/src/components/AccountCard.vue with rounded corners (16px), shadow, and 18px Bold font for account name
- [ ] T012 [US1] Integrate CircularProgress into AccountCard for allocation visualization
- [ ] T013 [US1] Apply card styles from toss-theme.scss to AccountCard.vue

**Checkpoint**: User Story 1 complete - account cards have Toss-style visual design

---

## Phase 4: User Story 2 - 색상 팔레트 통합 (Priority: P2)

**Goal**: 사용자가 전체 페이지에서 토스 스타일 색상 팔레트(차축 #00BFFF, 차순 #FF6B6B, 기본 #F5F5F5)가 일관되게 적용된 것을 확인하고 증감이 색상으로 구분되는 것을 확인

**Independent Test**: 대시보드 전체를 스캔하고 모든 UI 요소에 토스 색상이 일관되게 적용되었으며 증감이 빨간색/파란색으로 구분되는지 확인

### Tests for User Story 2

- [ ] T014 [P] [US2] Unit test for color theme application in frontend/tests/unit/styles/toss-theme.spec.ts
- [ ] T015 [US2] E2E test for color consistency across components in frontend/tests/e2e/toss-style-ui.spec.ts

### Implementation for User Story 2

- [ ] T016 [P] [US2] Apply Toss color palette to AccountChart.vue in frontend/src/components/AccountChart.vue (series colors, legend)
- [ ] T017 [P] [US2] Apply Toss color palette to AllocationChart.vue in frontend/src/components/AllocationChart.vue (pie chart colors)
- [ ] T018 [P] [US2] Apply Toss color palette to ComparisonTable.vue in frontend/src/components/ComparisonTable.vue (table styling)
- [ ] T019 [US2] Add increase/decrease color indicators (red #FF6B6B, blue #4A90E2) to account cards in frontend/src/components/AccountCard.vue
- [ ] T020 [US2] Update global Vuetify theme config in frontend/src/plugins/vuetify.ts with Toss colors

**Checkpoint**: User Story 2 complete - Toss color palette applied consistently

---

## Phase 5: User Story 3 - 레이아웃 최적화 (Priority: P3)

**Goal**: 사용자가 상단에 계좌 카드가 가로로 배치되고 하단에 그래프가 크게 표시되며 간격(padding 24px)이 충분한 것을 확인

**Independent Test**: 대시보드를 열고 상단에 계좌 카드가 가로 배치되어 있고 하단에 그래프가 크게 표시되며 요소 간 24px padding이 있는지 확인

### Tests for User Story 3

- [ ] T021 [US3] E2E test for responsive layout in frontend/tests/e2e/toss-style-ui.spec.ts (card positioning, chart sizing, spacing)

### Implementation for User Story 3

- [ ] T022 [US3] Create DashboardLayout.vue component in frontend/src/components/DashboardLayout.vue with horizontal card grid and bottom chart area
- [ ] T023 [US3] Apply 24px padding between sections in DashboardLayout.vue
- [ ] T024 [US3] Update Dashboard.vue to use DashboardLayout and arrange cards horizontally in frontend/src/views/Dashboard.vue
- [ ] T025 [US3] Adjust chart height for larger display in frontend/src/components/AccountChart.vue
- [ ] T026 [US3] Add mobile responsive styles (vertical card layout) in frontend/src/styles/toss-theme.scss with @media query

**Checkpoint**: User Story 3 complete - layout optimized with proper spacing and responsiveness

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 [P] Update component props TypeScript interfaces in frontend/src/components/ for type safety
- [ ] T028 [P] Add accessibility attributes (ARIA labels) to account cards and charts
- [ ] T029 [P] Code cleanup and remove unused styles in frontend/src/styles/
- [ ] T030 [P] Run all tests and ensure coverage above 80% in frontend/
- [ ] T031 [P] Visual regression testing with Playwright screenshots in frontend/tests/e2e/
- [ ] T032 Performance optimization - measure chart render time in frontend/
- [ ] T033 Update CLAUDE.md with Toss-style design decisions in memory/
- [ ] T034 Run pre-commit checks (black, ruff, mypy for backend; npm test for frontend)
- [ ] T035 Create summary documentation in specs/004-toss-style-ui/implementation-summary.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Integrates with US1 components but independently testable
- **User Story 3 (P3)**: Can start after Foundational - Integrates with US1/US2 components but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Component creation before integration
- Core implementation before styling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for AccountCard.vue props in frontend/tests/unit/components/AccountCard.spec.ts"
Task: "Unit test for CircularProgress.vue in frontend/tests/unit/components/CircularProgress.spec.ts"

# Launch all components for User Story 1 together:
Task: "Create CircularProgress.vue component in frontend/src/components/CircularProgress.vue"
Task: "Create AccountCard.vue component in frontend/src/components/AccountCard.vue"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (E2E test)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Toss-style cards!)
3. Add User Story 2 → Test independently → Deploy/Demo (Toss colors everywhere!)
4. Add User Story 3 → Test independently → Deploy/Demo (Complete Toss-style layout!)
5. Each story adds visual polish without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Account Cards)
   - Developer B: User Story 2 (Color Palette)
   - Developer C: User Story 3 (Layout)
3. Stories complete and integrate independently

---

## Summary

- **Total Task Count**: 35 tasks
- **Tasks per User Story**:
  - US1 (P1): 7 tasks (3 tests, 4 implementation)
  - US2 (P2): 6 tasks (2 tests, 4 implementation)
  - US3 (P3): 5 tasks (1 test, 4 implementation)
- **Parallel Opportunities**: 20 tasks marked [P] can run in parallel
- **Independent Test Criteria**: Each story has E2E test for independent validation
- **Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 13 tasks for Toss-style cards MVP
- **Format Validation**: All tasks follow checklist format (checkbox, ID, labels, file paths) ✅

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
