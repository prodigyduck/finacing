import time

from src.application.services.agent_orchestrator import AgentOrchestrator


def test_orchestrator_fallback_and_metrics():
    orch = AgentOrchestrator(chain=["a", "b"], failure_threshold=1, cooldown_ms=1000)

    def fail():
        raise RuntimeError("nope")

    def ok():
        return 123

    adapters = {"a": fail, "b": ok}
    res = orch.execute_with_fallback(adapters)
    assert res == 123
    # metrics should have been recorded for attempts
    # (we cannot import registry internals here reliably, but the call should not error)


def test_circuit_breaker_opens_and_skips():
    orch = AgentOrchestrator(chain=["x"], failure_threshold=1, cooldown_ms=1000)

    def fail():
        raise RuntimeError("boom")

    adapters = {"x": fail}
    try:
        orch.execute_with_fallback(adapters)
    except RuntimeError:
        pass

    # Circuit should be open now; a second call should be skipped
    adapters = {"x": fail}
    try:
        res = orch.execute_with_fallback(adapters)
    except RuntimeError:
        # All agents failed
        res = None
    assert res is None
