# Tasks: Investment Dashboard Core

**Input**: Design documents from `/specs/001-investment-dashboard-core/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Initialize Python virtual environment and dependencies
- [X] T003 [P] Configure linting and formatting (Black, Ruff, Mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement Obsidian data parsing interface in src/infrastructure/parsers/obsidian_parser.py
- [ ] T005 Implement basic FastAPI app structure in src/presentation/app.py
- [ ] T006 Implement Domain Entities (InvestmentRecord, PortfolioHistory) in src/domain/entities/

---

## Phase 3: User Story 1 - View Portfolio History (Priority: P1) 🎯 MVP

**Goal**: Visualize investment data from local Obsidian markdown files.

**Independent Test**: Provide a valid `투자.md` file, call the API, verify the parsed records match the file content.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Create InvestmentRecord model in src/domain/entities/investment_record.py
- [ ] T008 [US1] Implement ObsidianParser logic in src/infrastructure/parsers/obsidian_parser.py
- [ ] T009 [US1] Implement AnalyzeHistory use case for data retrieval in src/application/use_cases/analyze_history.py
- [ ] T010 [US1] Create REST API endpoint to retrieve history in src/presentation/app.py
- [ ] T011 [US1] Implement frontend API service in frontend/src/api/
- [ ] T012 [US1] Build PortfolioChart component in frontend/src/components/PortfolioChart.vue

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Analyze Trends and Projections (Priority: P2)

**Goal**: Understand future portfolio value based on historical trends using linear regression.

**Independent Test**: Use historical data points to verify the linear regression output for 3, 6, and 12-month projections.

### Implementation for User Story 2

- [ ] T013 [P] [US2] Extend AnalyzeHistory use case for trend analysis in src/application/use_cases/analyze_history.py
- [ ] T014 [US2] Implement linear regression logic in src/application/use_cases/analyze_history.py
- [ ] T015 [US2] Update REST API endpoint to include projections in src/presentation/app.py
- [ ] T016 [US2] Update frontend PortfolioChart to display trend/projection lines in frontend/src/components/PortfolioChart.vue
- [ ] T017 [US2] Implement X-axis label formatting (daily/weekly/monthly) in frontend/src/components/PortfolioChart.vue

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T018 [P] Add unit tests for AnalyzeHistory logic in tests/unit/
- [ ] T019 [P] Add E2E tests for dashboard flows in tests/e2e/
- [ ] T020 Code cleanup and refactoring
- [ ] T021 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Can start after User Story 1
