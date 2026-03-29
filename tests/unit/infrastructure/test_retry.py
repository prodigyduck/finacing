import pytest
import time

from src.infrastructure.retry import retry


def test_on_final_failure_hook_called_after_exhaustion():
    calls = []

    def on_final(e):
        calls.append(str(type(e).__name__))

    @retry(max_attempts=2, delay=0.01, backoff_factor=1.0, exceptions=(ValueError,), on_final_failure=on_final)
    def always_fail():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        always_fail()

    assert calls == ["ValueError"]


def test_retry_success_before_exhaustion_does_not_call_hook():
    calls = []

    def on_final(e):
        calls.append("called")

    state = {"count": 0}

    @retry(max_attempts=3, delay=0.01, backoff_factor=1.0, exceptions=(ValueError,), on_final_failure=on_final)
    def succeed_on_second():
        state["count"] += 1
        if state["count"] < 2:
            raise ValueError("first")
        return "ok"

    assert succeed_on_second() == "ok"
    assert calls == []
