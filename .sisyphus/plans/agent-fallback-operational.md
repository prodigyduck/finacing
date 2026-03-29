# Operational Plan: Agent Fallback (Sisyphus → Prometheus → Atlas)

## Purpose
Implement an automated agent fallback mechanism with circuit-breaking, structured logging, metrics, and full test coverage. Policy: immediate switch on rate-limit/quota detection, no exceptions for long-running tasks.

## Confirmed Decisions (from user)
1. **Test runner**: pytest with commands:
   - Unit: `pytest tests/unit -q`
   - Integration: `pytest tests/integration -q`
   - All: `pytest -q`
2. **CI provider**: GitHub Actions; new workflow allowed at `.github/workflows/ci.yml`.
3. **Orchestration layer**: Inject orchestrator into `FetchInvestmentData.execute` (application layer).
4. **Observability backend**: Prometheus (`prometheus_client`) for metrics.
5. **Fallback semantics**: Immediate switch on detection; no special handling for long-running tasks (same policy).
6. **Secrets/logging**: No secrets in logs; authentication via `.env`, do not log credentials.
7. **Exclusions**: None — all code in scope allowed.

## Architecture Overview

### Components
- **AgentOrchestrator**: Central service that tries agents in configured order, respects circuit-breaker health, emits metrics.
- **Retry decorator update**: Add optional `on_final_failure` hook for orchestrator consumption.
- **Exception types**: `RateLimitError`, `QuotaExceededError` (mapped from provider errors).
- **Config**: Feature flag `AGENT_FALLBACK_ENABLED`, chain `AGENT_CHAIN`, timeouts, retries.
- **Logging**: Structured logs to `.sisyphus/logs/agent-fallback.log` and app logger.
- **Metrics**: Prometheus metrics (`agent_attempts_total`, `agent_circuit_open_total`, etc.) via `/metrics`.

### Integration Points
- **Primary**: `FetchInvestmentData.execute` → calls `orchestrator.execute_with_fallback(lambda: repo.fetch_investment_notes(...))`
- **Detection**: `GKeepRepository._login` and `fetch_investment_notes` → map provider errors to `RateLimitError`/`QuotaExceededError`.
- **Hook**: `retry` decorator → call `on_final_failure` when retries exhausted.
- **Config**: `src/presentation/app.py` lifespan → read env, initialize orchestrator, inject into use case.

## Implementation Steps (TDD, atomic commits)

### Step 1: Add Exception Types
**File**: `src/infrastructure/errors.py` (new)
- Define:
  - `RateLimitError(Exception)`
  - `QuotaExceededError(Exception)`
- Reason: Distinguish fallback-triggering errors from transient network issues.

**Tests**: `tests/unit/infrastructure/test_errors.py` (new) — assert exception hierarchy and message handling.

**Commit**: `feat(infra): add RateLimitError/QuotaExceededError for fallback signaling`

---

### Step 2: Update Retry Decorator with Hook
**File**: `src/infrastructure/retry.py`
- Add optional parameter `on_final_failure: Callable | None = None` to `retry` decorator.
- After all retry attempts exhausted and before raising, call `on_final_failure` if provided.
- Maintain backward compatibility: if `on_final_failure` is `None`, behave as before.

**Tests**: `tests/unit/infrastructure/test_retry.py` — extend to test hook invocation on final failure and non-invocation on success.

**Commit**: `feat(retry): add optional on_final_failure hook for orchestrator integration`

---

### Step 3: Fix Bugs in GKeepRepository
**File**: `src/infrastructure/repositories/gkeep_repository.py`
- Remove duplicate/nested `def` in `fetch_investment_notes`.
- Add `logger = logging.getLogger(__name__)` at module top.
- Wrap gkeepapi calls in try/except; map HTTP 429 or provider-specific rate-limit errors to `RateLimitError` and re-raise.

**Tests**: Update `tests/unit/infrastructure/test_gkeep_repository.py` to assert `RateLimitError` raised on simulated 429.

**Commit**: `fix(gkeep): remove nested def, add logger, map 429 to RateLimitError`

---

### Step 4: Implement AgentOrchestrator
**File**: `src/application/services/agent_orchestrator.py` (new)

**API**:
```python
class AgentOrchestrator:
    def __init__(
        self,
        chain: list[str],
        logger: logging.Logger,
        metrics: prometheus_client.registry.CollectorRegistry | None = None,
        timeout_ms: int = 30000,
        cooldown_ms: int = 60000,
        failure_threshold: int = 2
    ): ...

    def execute_with_fallback(
        self,
        callable: Callable[..., T],
        *args: Any,
        **kwargs: Any
    ) -> T:
        """Try agents in chain; return first success or raise final error."""
```

**Behaviors**:
- Try each agent in order; return on first success.
- On `RateLimitError`/`QuotaExceededError`, log structured event and increment `agent_attempts_total{agent="...", outcome="fallback"}`.
- Circuit-breaker per agent: track consecutive failures; mark unhealthy if threshold reached; skip for `cooldown_ms`.
- On final failure after all agents, raise `AgentFallbackExhaustedError` with per-agent diagnostics.
- Emit metrics:
  - `agent_attempts_total{agent, outcome}` (outcome: success, fallback, error)
  - `agent_circuit_open_total{agent}`
  - `agent_latency_seconds{agent}` (histogram)

**Tests**: `tests/unit/application/test_agent_orchestrator.py` — mock agent callables; assert fallback, circuit-breaker, metrics.

**Commit**: `feat(orchestrator): add AgentOrchestrator with circuit-breaker and metrics`

---

### Step 5: Central Configuration & App Startup
**File**: `src/config/agent_config.py` (new)
- Parse environment variables:
  - `AGENT_FALLBACK_ENABLED` (bool, default `false`)
  - `AGENT_CHAIN` (list[str], default `["sisyphus"]`)
  - `AGENT_TIMEOUT_MS` (int, default `30000`)
  - `AGENT_RETRY_ATTEMPTS` (int, default `3`)
  - `AGENT_COOLDOWN_MS` (int, default `60000`)
  - `AGENT_FAILURE_THRESHOLD` (int, default `2`)

**File**: `src/presentation/app.py`
- In lifespan (`@contextmanager`):
  - Load config; if `AGENT_FALLBACK_ENABLED` is `true`, instantiate `AgentOrchestrator` with `AGENT_CHAIN`.
  - Register orchestrator to app state: `app.state.orchestrator`.
- Endpoint `/metrics`: expose Prometheus metrics (using `prometheus_client.make_asgi_app`).
- Log initialization: fallback enabled, chain, config values (no secrets).

**Commit**: `feat(config): add AGENT_* env parsing and orchestrator initialization in app lifespan`

---

### Step 6: Inject Orchestrator into FetchInvestmentData
**File**: `src/application/use_cases/fetch_investment_data.py`
- Modify `FetchInvestmentData.execute`:
  - If `orchestrator` is provided (via dependency injection), call:
    - `orchestrator.execute_with_fallback(lambda: repo.fetch_investment_notes(label))`
  - Else, call `repo.fetch_investment_notes(label)` directly (backward compatible).
- Modify `src/presentation/app.py.get_portfolio`:
  - Pass `app.state.orchestrator` to `FetchInvestmentData` if present.

**Tests**: `tests/unit/application/test_fetch_investment_data.py` — mock repo and orchestrator; assert orchestrator used when enabled.

**Commit**: `feat(usecase): inject orchestrator into FetchInvestmentData; support fallback via env flag`

---

### Step 7: Central Logging Configuration
**File**: `src/config/logging.py` (new)
- Configure structured logging:
  - Format: JSON or plain with timestamp, level, logger, message, context dict.
  - Handler 1: `StreamHandler` to stdout (FastAPI/Uvicorn).
  - Handler 2: `FileHandler` to `.sisyphus/logs/agent-fallback.log` (ensure directory exists).
- Import in `src/presentation/app.py` before FastAPI instantiation.

**File**: `.sisyphus/logs/.gitkeep` (new) — placeholder for log directory.

**Commit**: `feat(logging): add central logging config with file handler for fallback events`

---

### Step 8: Metrics Endpoint
**File**: `src/presentation/app.py`
- Add `/metrics` route using `prometheus_client.make_asgi_app`.
- Ensure metrics registry includes orchestrator metrics.

**Commit**: `feat(obs): expose /metrics endpoint for Prometheus scraping`

---

### Step 9: Integration Tests
**File**: `tests/integration/presentation/test_agent_fallback.py` (new)

**Tests** (all deterministic, no network):
- `test_http_path_fallback`: mock agent responses; primary returns 429, fallback returns success; assert 200 response and metrics.
- `test_timeout_fallback`: primary agent raises timeout (simulated), fallback used; assert correct metrics.
- `test_all_agents_fail`: both agents fail; assert 5xx response and structured error with per-agent diagnostics.
- `test_metrics_emitted`: after request, hit `/metrics`; grep for `agent_attempts_total{agent="prometheus",outcome="success"}`.

**Commands**:
```bash
pytest tests/integration/presentation/test_agent_fallback.py -q
```

**Commit**: `test(integration): add deterministic integration tests for agent fallback and metrics`

---

### Step 10: CI Workflow (GitHub Actions)
**File**: `.github/workflows/ci.yml` (new)

**Jobs**:
- `test-unit`: run `pytest tests/unit -q` with coverage.
- `test-integration`: run `pytest tests/integration -q`.
- `lint`: run `ruff check src tests` and `black --check src tests`.
- `metrics-smoke`: run `pytest tests/integration/test_agent_fallback.py::test_metrics_emitted -q` and verify `agent_attempts_total` present in `/metrics`.

**Example job**:
```yaml
name: orchestrator-integration
runs-on: ubuntu-latest
steps:
  - uses: actions/checkout@v4
  - run: pip install -e . && pip install pytest pytest-cov prometheus_client
  - run: pytest tests/integration -q
  - name: Collect logs
    if: failure()
    run: cat .sisyphus/logs/agent-fallback.log || echo "no logs yet"
```

**Commit**: `ci(ci.yml): add GitHub Actions workflow to run unit, integration, and metrics smoke tests`

---

## QA / Acceptance Criteria (Zero User Intervention)

### Unit Tests
```bash
# Orchestrator fallback on rate limit
pytest tests/unit/application/test_agent_orchestrator.py::test_fallback_on_rate_limit -q

# Circuit-breaker skips unhealthy agent
pytest tests/unit/application/test_agent_orchestrator.py::test_circuit_breaker -q

# Retry hook called on final failure
pytest tests/unit/infrastructure/test_retry.py::test_retry_final_failure_invokes_hook -q

# No secrets in logs
pytest tests/unit/infrastructure/test_no_secret_logging.py::test_no_secrets_in_logs -q
```

### Integration Tests
```bash
# HTTP path fallback (primary 429, fallback success)
pytest tests/integration/presentation/test_agent_fallback.py::test_http_path_fallback -q

# Timeout fallback
pytest tests/integration/presentation/test_agent_fallback.py::test_timeout_fallback -q

# All agents fail
pytest tests/integration/presentation/test_agent_fallback.py::test_all_agents_fail -q

# Metrics emitted
pytest tests/integration/presentation/test_agent_fallback.py::test_metrics_emitted -q
```

### Manual Verification (optional)
1. Start app: `AGENT_FALLBACK_ENABLED=true AGENT_CHAIN="sisyphus,prometheus" python -m src.presentation.app`
2. Hit `/api/v1/portfolio` and observe logs in `.sisyphus/logs/agent-fallback.log`.
3. Hit `/metrics`; ensure `agent_attempts_total` present.

---

## Risk Mitigations

| Risk | Mitigation |
|---|---|
| Flapping between agents (oscillation) | Per-agent circuit-breaker with cooldown (`AGENT_COOLDOWN_MS`); skip unhealthy agents. |
| Behavioral/regression (caller contract changes) | Keep response shape identical; add contract tests; run in CI. |
| Secret leakage in logs/metrics | Sanitize before logging; enforce no-secret policy via unit test. |
| Missing metrics/alerts | Explicit metrics + `/metrics` endpoint; CI smoke test checks for metric existence. |
| Incomplete test coverage/flaky tests | TDD: unit tests first, deterministic integration tests; avoid network delays in tests. |
| Rollout risk (no fallback) | Ship behind feature flag (`AGENT_FALLBACK_ENABLED=false` by default); canary promotion. |

---

## Rollout Plan

1. **Dev**: Feature flag off (`AGENT_FALLBACK_ENABLED=false`); run tests locally.
2. **Staging**: Enable feature flag with single agent (`AGENT_CHAIN="sisyphus"`); monitor logs/metrics.
3. **Canary**: Set `AGENT_CHAIN="sisyphus,prometheus"`; monitor fallback rates.
4. **Prod full**: Same config as canary; set up alerts on `agent_circuit_open_total`.

---

## Rollback Plan
- Disable feature flag: set `AGENT_FALLBACK_ENABLED=false` and redeploy.
- If orchestrator bug detected: remove orchestrator injection and revert to direct repository calls (backward compatible).

---

## Documentation Updates

- Update `AGENTS.md` to include fallback policy and orchestrator responsibilities.
- Update `docs/SECURITY.md` to note no-secrets policy for logs.
- Update `docs/RELIABILITY.md` to describe fallback behavior and monitoring.

---

## Next Steps (After Plan Approval)
1. Implement Steps 1–10 in order, committing each step.
2. Run unit tests after each step; integration tests after Step 9.
3. Merge PR with CI checks passing.
4. Monitor `/metrics` and logs in staging; adjust thresholds if needed.
5. Enable feature flag in prod with canary.

---

## Appendix: Example Config (.env)
```bash
# Agent fallback
AGENT_FALLBACK_ENABLED=true
AGENT_CHAIN=sisyphus,prometheus,atlas
AGENT_TIMEOUT_MS=30000
AGENT_RETRY_ATTEMPTS=3
AGENT_COOLDOWN_MS=60000
AGENT_FAILURE_THRESHOLD=2

# Logging
AGENT_FALLBACK_LOG_FILE=.sisyphus/logs/agent-fallback.log
```
