import time
import pytest

from src.application.services.agent_orchestrator import AgentOrchestrator


def test_orchestrator_success_uses_first_available():
    calls = {"sisyphus": lambda: "a", "prometheus": lambda: "b"}
    orch = AgentOrchestrator(chain=["sisyphus", "prometheus"], timeout_ms=1000)

    assert orch.execute_with_fallback(calls) == "a"


def test_orchestrator_fallbacks_on_failure_and_records_metrics():
    def fail():
        raise ValueError("boom")

    calls = {"sisyphus": fail, "prometheus": lambda: "ok"}
    orch = AgentOrchestrator(chain=["sisyphus", "prometheus"], timeout_ms=1000)

    res = orch.execute_with_fallback(calls)
    assert res == "ok"


def test_circuit_opens_after_threshold_and_skips_agent():
    def fail():
        raise RuntimeError("x")

    calls = {"a": fail, "b": lambda: "ok"}
    orch = AgentOrchestrator(chain=["a", "b"], failure_threshold=2, cooldown_ms=100)

    # first failure
    with pytest.raises(RuntimeError):
        orch.execute_with_fallback({"a": fail})

    # second failure should open circuit
    with pytest.raises(RuntimeError):
        orch.execute_with_fallback({"a": fail})

    # now circuit open, calling with both agents should skip 'a' and succeed on 'b'
    res = orch.execute_with_fallback(calls)
    assert res == "ok"
