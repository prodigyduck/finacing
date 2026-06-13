# Tasks: Performance & Stability

**Input**: Design documents from `/specs/008-performance-stability/`

**Tests**: Test tasks included

**Organization**: Tasks grouped by user story

---

## Phase 1: Setup

- [ ] T001 Create services directory structure in frontend/src/services/

---

## Phase 2: Foundational

- [ ] T002 [P] Create cache utility in frontend/src/utils/cache.ts with localStorage wrapper
- [ ] T003 [P] Create API state types in frontend/src/types/api.ts (ApiCallState, CacheEntry, RealtimeConfig)

---

## Phase 3: User Story 1 - 스켈레톤 UI와 데이터 로딩 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 페이지 로드 시 0.5초 이내에 스켈레톤 UI를 확인하고 lazy loading으로 초기 로딩 최적화

**Independent Test**: 대시보드를 열고 0.5초 이내에 스켈레톤이 표시되며 스크롤 시 나머지 데이터가 로드되는지 확인

### Tests for US1

- [ ] T004 [P] [US1] Unit test for SkeletonLoader component in frontend/tests/unit/components/SkeletonLoader.spec.ts
- [ ] T005 [US1] E2E test for loading performance in frontend/tests/e2e/performance-stability.spec.ts (measure 0.5s skeleton, 2s total)

### Implementation for US1

- [ ] T006 [P] [US1] Create SkeletonLoader.vue component in frontend/src/components/SkeletonLoader.vue with loading animation
- [ ] T007 [US1] Create useApiCall.ts composable in frontend/src/composables/useApiCall.ts with loading state
- [ ] T008 [US1] Implement lazy loading for 1+ year data in frontend/src/composables/useApiCall.ts
- [ ] T009 [US1] Integrate SkeletonLoader into Dashboard.vue in frontend/src/views/Dashboard.vue
- [ ] T010 [US1] Add loading spinner/progress indicator in SkeletonLoader.vue

---

## Phase 4: User Story 2 - 에러 처리와 Retry 로직 (Priority: P2)

**Goal**: 사용자가 API 실패 시 적절한 에러 메시지와 재시도 옵션을 확인하고 최대 3회 재시도가 자동으로 실행됨

**Independent Test**: API를 강제로 실패시키고 에러 메시지와 재시도 버튼이 표시되며 3회 재시도 후 캐시 데이터가 표시되는지 확인

### Tests for US2

- [ ] T011 [P] [US2] Unit test for useApiCall retry logic in frontend/tests/unit/composables/useApiCall.spec.ts
- [ ] T012 [US2] E2E test for error handling and retry in frontend/tests/e2e/performance-stability.spec.ts

### Implementation for US2

- [ ] T013 [P] [US2] Create ErrorMessage.vue component in frontend/src/components/ErrorMessage.vue with retry button
- [ ] T014 [US2] Add Axios interceptor for retry with exponential backoff in frontend/src/composables/useApiCall.ts (1s, 2s, 4s)
- [ ] T015 [US2] Implement 3-retry limit and fallback to cache in useApiCall.ts
- [ ] T016 [US2] Integrate ErrorMessage into Dashboard.vue in frontend/src/views/Dashboard.vue

---

## Phase 5: User Story 3 - 오프라인 모드와 캐시 (Priority: P3)

**Goal**: 사용자가 오프라인 상태에서 캐시된 데이터를 확인하고 오프라인 인디케이터를 보며 연결 복구 시 자동 갱신됨

**Independent Test**: 오프라인 모드에서 대시보드를 열고 캐시 데이터와 오프라인 인디케이터가 표시되며 연결 복구 시 최신 데이터가 자동 로드되는지 확인

### Tests for US3

- [ ] T017 [P] [US3] Unit test for useCache composable in frontend/tests/unit/composables/useCache.spec.ts
- [ ] T018 [US3] E2E test for offline mode in frontend/tests/e2e/performance-stability.spec.ts

### Implementation for US3

- [ ] T019 [P] [US3] Create useCache.ts composable in frontend/src/composables/useCache.ts with localStorage/IndexedDB
- [ ] T020 [P] [US3] Create OfflineIndicator.vue component in frontend/src/components/OfflineIndicator.vue
- [ ] T021 [US3] Set 24-hour TTL for cache entries in useCache.ts
- [ ] T022 [US3] Add online/offline event listeners in useCache.ts
- [ ] T023 [US3] Integrate OfflineIndicator into Dashboard.vue in frontend/src/views/Dashboard.vue

---

## Phase 6: User Story 4 - 실시간 데이터 갱신 (Priority: P4)

**Goal**: 사용자가 WebSocket/Polling으로 실시간 데이터 갱신을 지원받고 변경 부분이 하이라이트됨

**Independent Test**: 대시보드를 보고 있을 때 새로운 데이터가 도착하면 자동 갱신되며 변경 부분이 하이라이트되는지 확인

### Tests for US4

- [ ] T024 [P] [US4] Unit test for useRealtime composable in frontend/tests/unit/composables/useRealtime.spec.ts
- [ ] T025 [US4] E2E test for realtime updates in frontend/tests/e2e/performance-stability.spec.ts

### Implementation for US4

- [ ] T026 [P] [US4] Create useRealtime.ts composable in frontend/src/composables/useRealtime.ts with WebSocket/Polling
- [ ] T027 [US4] Create WebSocket service in frontend/src/services/websocket.ts
- [ ] T028 [US4] Implement 5-second interval for Polling fallback in useRealtime.ts
- [ ] T029 [US4] Add highlight animation for changed data in AccountCard.vue in frontend/src/components/AccountCard.vue
- [ ] T030 [US4] Handle disconnect with auto-reconnect in useRealtime.ts

---

## Phase 7: Polish

- [ ] T031 [P] Set API timeout to 30s in frontend/src/composables/useApiCall.ts
- [ ] T032 [P] Add ARIA labels for accessibility
- [ ] T033 [P] Run all tests and ensure coverage
- [ ] T034 Performance optimization - measure cache hit rate
- [ ] T035 Update documentation in specs/008-performance-stability/implementation-summary.md

---

## Summary

- **Total Task Count**: 35 tasks
- **Tasks per User Story**: US1: 7 tasks, US2: 6 tasks, US3: 7 tasks, US4: 7 tasks
- **Parallel Opportunities**: 18 tasks marked [P]
- **MVP Scope**: Phase 1-3 (US1 only) = 10 tasks
