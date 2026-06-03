# Tasks: Account-Based Portfolio Tracking

**Input**: Design documents from `/specs/002-account-based-portfolio/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD approach - tests written first for each component (Red-Green-Refactor)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Backend: `src/` at repository root
- Frontend: `frontend/src/`
- Tests: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project already initialized - just verification and preparation

- [ ] T001 Verify Python 3.11+ and Node.js 20+ environment
- [ ] T002 Verify existing project structure matches plan.md
- [ ] T003 [P] Verify backend dependencies (FastAPI, pydantic, pytest, pytest-cov) installed
- [ ] T004 [P] Verify frontend dependencies (Vue.js 3, TypeScript, ECharts, Vuetify, Vitest) installed
- [ ] T005 [P] Run existing unit tests to ensure baseline health

**Checkpoint**: Environment ready - foundational implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain entities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Entities (Required by ALL stories)

- [ ] T006 [P] [US1] Write failing tests for Account entity in tests/unit/domain/test_account.py (TDD: Red)
- [ ] T007 [P] [US1] Write failing tests for Holding entity in tests/unit/domain/test_holding.py (TDD: Red)
- [ ] T008 [P] [US1] Write failing tests for AccountRecord entity in tests/unit/domain/test_account_record.py (TDD: Red)
- [ ] T009 [P] [US1] Write failing tests for PortfolioSnapshot entity in tests/unit/domain/test_portfolio_snapshot.py (TDD: Red)
- [ ] T010 [US1] Implement Account entity in src/domain/entities/account.py (TDD: Green)
- [ ] T011 [US1] Implement Holding entity in src/domain/entities/holding.py (TDD: Green)
- [ ] T012 [US1] Implement AccountRecord entity in src/domain/entities/account_record.py (TDD: Green)
- [ ] T013 [US1] Implement PortfolioSnapshot entity in src/domain/entities/portfolio_snapshot.py (TDD: Green)
- [ ] T014 [US1] Refactor domain entities for type hints and validation (TDD: Refactor)
- [ ] T015 [US1] Run mypy, black, ruff on domain entities

### Parser Chain Infrastructure

- [ ] T016 [P] [US1] Write failing tests for ParserChain base class in tests/unit/infrastructure/test_parser_chain.py
- [ ] T017 [P] [US1] Write failing tests for LegacyParser adapter in tests/unit/infrastructure/test_legacy_parser.py
- [ ] T018 [US1] Implement ParserChain in src/infrastructure/parsers/parser_chain.py
- [ ] T019 [US1] Implement LegacyParser adapter in src/infrastructure/parsers/legacy_parser.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 계좌별 포트폴리오 기록 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 계좌별로 자산 현황과 보유 종목을 기록하고 파싱할 수 있음

**Independent Test**: 계좌별 마크다운 파일을 작성하고 파서가 이를 정확히 읽어 계좌별 총액과 종목 리스트를 추출하는 단위 테스트로 검증

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL)

- [ ] T020 [P] [US1] Write failing contract test for /api/v1/history accounts field in tests/unit/test_api_contracts.py
- [ ] T021 [P] [US1] Write failing parser test for account-based format in tests/unit/infrastructure/test_account_parser.py
- [ ] T022 [P] [US1] Write failing parser test for legacy format compatibility in tests/unit/infrastructure/test_account_parser.py
- [ ] T023 [P] [US1] Write failing use case test for AnalyzeAccounts in tests/unit/application/test_analyze_accounts.py
- [ ] T024 [P] [US1] Write failing E2E test for account data display in tests/e2e/test_account_dashboard.spec.ts

### Implementation for User Story 1

#### Infrastructure Layer

- [ ] T025 [US1] Implement AccountParser for account-based format in src/infrastructure/parsers/account_parser.py (depends on T021 passing)
- [ ] T026 [US1] Update ObsidianParser to work with ParserChain in src/infrastructure/parsers/obsidian_parser.py
- [ ] T027 [US1] Add error handling for malformed account data in src/infrastructure/parsers/account_parser.py

#### Application Layer

- [ ] T028 [US1] Implement AnalyzeAccounts use case in src/application/use_cases/analyze_accounts.py (depends on T023 passing)
- [ ] T029 [US1] Add allocation calculation logic to AnalyzeAccounts in src/application/use_cases/analyze_accounts.py
- [ ] T030 [US1] Add comparison metrics (best/worst performer) in src/application/use_cases/analyze_accounts.py

#### Presentation Layer

- [ ] T031 [US1] Extend /api/v1/history endpoint with accounts field in src/presentation/app.py (depends on T020 passing)
- [ ] T032 [US1] Add account filter query parameter to /api/v1/history in src/presentation/app.py
- [ ] T033 [US1] Add error responses for invalid account names in src/presentation/app.py

#### Frontend Layer

- [ ] T034 [P] [US1] Create AccountCard.vue component in frontend/src/components/AccountCard.vue
- [ ] T035 [P] [US1] Create HoldingsList.vue component in frontend/src/components/HoldingsList.vue
- [ ] T036 [US1] Update history Pinia store with accounts data in frontend/src/stores/history.ts
- [ ] T037 [US1] Update Dashboard.vue to display account cards in frontend/src/views/Dashboard.vue

#### Testing & Validation

- [ ] T038 [US1] Run unit tests for US1 and verify 100% pass rate
- [ ] T039 [US1] Run E2E test for account dashboard and verify passing
- [ ] T040 [US1] Test with real Obsidian file in both legacy and account-based formats
- [ ] T041 [US1] Verify API response matches contracts/api-contracts.md

**Checkpoint**: User Story 1 complete - 계좌별 포트폴리오 기록 and 계좌별 차트 시각화 (Priority: P2)

**Goal**: 사용자가 각 계좌의 가치 추이를 시간에 따라 시각화하고 계좌별 차트를 볼 수 있음

**Independent Test**: E2E 테스트로 계좌별 데이터를 포함하는 테스트 파일을 사용하여 대시보드에 계좌별 차트가 렌더링되고 올바른 데이터를 표시하는지 확인

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL)

- [ ] T042 [P] [US2] Write failing E2E test for account chart rendering in tests/e2e/test_account_charts.spec.ts
- [ ] T043 [P] [US2] Write failing component test for AccountChart.vue in frontend/src/components/__tests__/AccountChart.spec.ts
- [ ] T044 [P] [US2] Write failing E2E test for account filter interaction in tests/e2e/test_account_charts.spec.ts

### Implementation for User Story 2

#### Frontend Components

- [ ] T045 [US2] Implement AccountChart.vue component with ECharts in frontend/src/components/AccountChart.vue (depends on T043 passing)
- [ ] T046 [US2] Add account selector dropdown to AccountChart in frontend/src/components/AccountChart.vue
- [ ] T047 [US2] Implement chart filtering by account in frontend/src/components/AccountChart.vue (depends on T044 passing)
- [ ] T048 [US2] Add Toss-style chart styling (minimal noise, clear legends) in frontend/src/components/AccountChart.vue
- [ ] T049 [US2] Make AccountChart responsive for mobile/desktop in frontend/src/components/AccountChart.vue

#### Application Layer

- [ ] T050 [US2] Extend AnalyzeHistory to support account-level projections in src/application/use_cases/analyze_history.py
- [ ] T051 [US2] Add account projection calculation to AnalyzeHistory in src/application/use_cases/analyze_history.py

#### Presentation Layer

- [ ] T052 [US2] Update /api/v1/history to include account projections in src/presentation/app.py

#### Integration

- [ ] T053 [US2] Update Dashboard.vue to display account charts in frontend/src/views/Dashboard.vue
- [ ] T054 [US2] Wire account selector to chart filtering in frontend/src/views/Dashboard.vue

#### Testing & Validation

- [ ] T055 [US2] Run E2E tests for US2 and verify passing
- [ ] T056 [US2] Test chart rendering performance (< 500ms target)
- [ ] T057 [US2] Verify chart interactivity (zoom, legend toggle, account filter)

**Checkpoint**: User Story 2 complete - 계좌별 차트 시각화 and 계좌간 비교 및 분석 (Priority: P3)

**Goal**: 사용자가 계좌간 성과를 비교하고 배분 비율을 파악하며 드릴다운으로 종목 상세를 볼 수 있음

**Independent Test**: 단위 테스트로 배분 비율 계산 로직을 검증하고 E2E 테스트로 드릴다운 인터랙션을 확인

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL)

- [ ] T058 [P] [US3] Write failing unit test for allocation calculation in tests/unit/application/test_analyze_accounts.py
- [ ] T059 [P] [US3] Write failing unit test for performance comparison in tests/unit/application/test_compare_accounts.py
- [ ] T060 [P] [US3] Write failing E2E test for drill-down interaction in tests/e2e/test_account_drilldown.spec.ts

### Implementation for User Story 3

#### Application Layer

- [ ] T061 [US3] Implement CompareAccounts use case in src/application/use_cases/compare_accounts.py (depends on T059 passing)
- [ ] T062 [US3] Add allocation percentage calculation in CompareAccounts in src/application/use_cases/compare_accounts.py (depends on T058 passing)
- [ ] T063 [US3] Add performance ranking logic in CompareAccounts in src/application/use_cases/compare_accounts.py
- [ ] T064 [US3] Add trend analysis (up/down/flat) in CompareAccounts in src/application/use_cases/compare_accounts.py

#### Presentation Layer

- [ ] T065 [US3] Update /api/v1/history to include comparison data in src/presentation/app.py
- [ ] T066 [US3] Add comparison endpoint /api/v1/comparison in src/presentation/app.py (optional)

#### Frontend Components

- [ ] T067 [P] [US3] Create ComparisonTable.vue component in frontend/src/components/ComparisonTable.vue
- [ ] T068 [P] [US3] Create AllocationChart.vue component in frontend/src/components/AllocationChart.vue
- [ ] T069 [US3] Implement drill-down interaction in AccountCard.vue (depends on T060 passing)
- [ ] T070 [US3] Update Dashboard.vue to display comparison section in frontend/src/views/Dashboard.vue

#### Testing & Validation

- [ ] T071 [US3] Run unit tests for US3 and verify passing
- [ ] T072 [US3] Run E2E tests for drill-down and verify passing
- [ ] T073 [US3] Test comparison data accuracy with sample accounts

**Checkpoint**: User Story 3 complete - 계좌간 비교 및 분석 working

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Documentation

- [ ] T074 [P] Update CLAUDE.md with new domain entities structure
- [ ] T075 [P] Update README.md with account-based format examples
- [ ] T076 [P] Create migration guide from legacy to account-based format in docs/migration.md

### Code Quality

- [ ] T077 Run mypy on all src/ and fix any type issues
- [ ] T078 Run black formatter on all src/ and tests/
- [ ] T079 Run ruff linter and fix all warnings
- [ ] T080 [P] Add additional edge case tests in tests/unit/domain/test_portfolio_snapshot.py

### Performance

- [ ] T081 Benchmark parser performance with 12,000 records (target: < 1s)
- [ ] T082 Benchmark API response time (target: < 200ms)
- [ ] T083 Optimize chart rendering if needed (target: < 500ms)

### E2E Validation

- [ ] T084 Run full E2E test suite and verify all scenarios pass
- [ ] T085 Test with real Obsidian file containing multiple accounts
- [ ] T086 Test with mixed legacy and account-based data

### Security & Data Integrity

- [ ] T087 Verify Obsidian data remains read-only (no writes from app)
- [ ] T088 Test error handling for malformed account data
- [ ] T089 Test error handling for missing or invalid account names

### Final Verification

- [ ] T090 Run quickstart.md validation to ensure guide is accurate
- [ ] T091 Verify all constitution gates still pass (Clean Architecture, TDD, Toss-style UI, Performance)
- [ ] T092 Check test coverage meets targets (Domain: 100%, Application: 95%+, Infrastructure: 90%+)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - NO dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational + US1 completion (charts need account data structure)
- **User Story 3 (Phase 5)**: Depends on Foundational + US1 completion (comparison needs account data)
- **Polish (Phase 6)**: Depends on US1, US2, US3 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - **MVP cutoff point**
- **User Story 2 (P2)**: Depends on US1 completion (needs account data from US1)
- **User Story 3 (P3)**: Depends on US1 completion (needs account data from US1)

**Note**: US2 and US3 can proceed in parallel after US1 completes

### Within Each User Story

**TDD Workflow (Mandatory)**:
1. Write failing test (Red)
2. Run test and verify failure
3. Implement minimum code to pass (Green)
4. Refactor if needed (Refactor)
5. Move to next task

**Execution Order Within Story**:
- All tests written first (T020-T024 for US1)
- Tests run and verified failing
- Implementation begins (Infrastructure → Application → Presentation → Frontend)
- Story validated independently before next story

### Parallel Opportunities

**Within Foundational Phase (Phase 2)**:
```bash
# Can run in parallel after Setup complete:
T006: Account entity tests
T007: Holding entity tests
T008: AccountRecord entity tests
T009: PortfolioSnapshot entity tests

# After entities pass:
T010: Account implementation
T011: Holding implementation
T012: AccountRecord implementation
T013: PortfolioSnapshot implementation
```

**Within User Story 1 (Phase 3)**:
```bash
# Tests first (all parallel):
T020: API contract test
T021: Parser test (account-based)
T022: Parser test (legacy)
T023: Use case test
T024: E2E test

# Frontend components (parallel):
T034: AccountCard.vue
T035: HoldingsList.vue
```

**After US1 Complete**:
```bash
# US2 and US3 can proceed in parallel:
US2 (Phase 4): Account charts and visualization
US3 (Phase 5): Comparison and analysis
```

---

## Parallel Example: User Story 1 Tests (TDD Red Phase)

```bash
# Launch all tests for User Story 1 together - they all should FAIL:
Task: "Write failing contract test for /api/v1/history accounts field"
Task: "Write failing parser test for account-based format"
Task: "Write failing parser test for legacy format compatibility"
Task: "Write failing use case test for AnalyzeAccounts"
Task: "Write failing E2E test for account data display"

# Verify all tests fail (Red phase complete)
# Now proceed with implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T019) - **CRITICAL**
3. Complete Phase 3: User Story 1 (T020-T041)
4. **STOP and VALIDATE**: Test US1 independently
5. Deploy/demo if ready

**MVP delivers**: 계좌별 포트폴리오 기록 - users can record and view account-specific portfolio data

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **Deploy/Demo (MVP!)**
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Polish → Final release

### Parallel Team Strategy

With multiple developers after US1 MVP:

1. Team completes Setup + Foundational together
2. Team completes US1 together
3. **After US1 complete**:
   - Developer A: User Story 2 (charts)
   - Developer B: User Story 3 (comparison)
4. Integrate US2 + US3

---

## Test Coverage Targets

| Layer | Target | Notes |
|-------|--------|-------|
| Domain (entities) | 100% | Critical business logic |
| Application (use cases) | 95%+ | Core application logic |
| Infrastructure (parsers) | 90%+ | Parsing logic |
| Presentation (API) | 80%+ | Endpoint integration |
| Frontend (components) | 70%+ | UI components |
| E2E | Critical paths | User journeys only |

---

## Notes

- **[P]** tasks = different files, no dependencies on incomplete tasks
- **[Story]** label maps task to specific user story (US1, US2, US3)
- **TDD is MANDATORY**: Tests MUST be written first and verified failing before implementation
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- After each implementation task, run relevant tests to verify Green phase
- After story complete, run full test suite to verify no regressions
