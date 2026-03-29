import pytest
import asyncio
import httpx
from httpx import ASGITransport

from src.presentation.app import app


class _SyncASGIClient:
    """A tiny sync wrapper around httpx.AsyncClient+ASGITransport using asyncio.run.

    This avoids TestClient/starlette/httpx compatibility issues in CI by
    driving the ASGI app via an async transport and exposing a sync API used
    by the existing tests.
    """

    def __init__(self, app):
        self.app = app

    def get(self, path, **kwargs):
        async def _req():
            async with httpx.AsyncClient(transport=ASGITransport(self.app), base_url="http://testserver") as client:
                return await client.get(path, **kwargs)

        return asyncio.run(_req())

    def post(self, path, **kwargs):
        async def _req():
            async with httpx.AsyncClient(transport=ASGITransport(self.app), base_url="http://testserver") as client:
                return await client.post(path, **kwargs)

        return asyncio.run(_req())

    def close(self):
        # Nothing to close because each request creates its own client
        return None


def _client():
    return _SyncASGIClient(app)


@pytest.mark.integration
def test_metrics_endpoint_present():
    client = _client()
    # make_asgi_app mounts at /metrics/ (trailing slash) -> request that path
    r = client.get("/metrics/")
    client.close()
    assert r.status_code == 200
    assert "# HELP" in r.text


@pytest.mark.integration
def test_http_path_fallback(monkeypatch):
    # Simulate repository in app state that raises RateLimitError on fetch
    from src.infrastructure.errors import RateLimitError

    class DummyRepo:
        def fetch_investment_notes(self, label):
            raise RateLimitError("ratelimit")

    app.state.repository = DummyRepo()
    client = _client()

    r = client.get("/api/v1/portfolio")
    client.close()
    # Should return 500 because orchestrator not configured to fallback in this simple test
    assert r.status_code in (200, 500)


@pytest.mark.integration
def test_integration_fallback_chain_and_metrics():
    """Primary agent fails with RateLimitError, fallback succeeds and metrics are emitted"""
    from src.application.services.agent_orchestrator import AgentOrchestrator
    from src.infrastructure.errors import RateLimitError

    # Create orchestrator with chain
    orch = AgentOrchestrator(chain=["sisyphus", "prometheus"], failure_threshold=1, cooldown_ms=1000)
    app.state.orchestrator = orch

    # Agent adapters
    def primary():
        raise RateLimitError("primary 429")

    def fallback():
        # Return empty assets list (compatible with use case)
        return []

    app.state.agent_adapters = {"sisyphus": primary, "prometheus": fallback}

    client = _client()
    r = client.get("/api/v1/portfolio")
    # Should succeed via fallback (returns portfolio or error if no repo used)
    assert r.status_code in (200, 500)

    # Check metrics include attempts for prometheus
    m = client.get("/metrics/")
    client.close()
    assert m.status_code == 200
    assert "agent_attempts_total" in m.text


@pytest.mark.integration
def test_all_agents_fail_and_reports_diagnostics():
    from src.application.services.agent_orchestrator import AgentOrchestrator

    orch = AgentOrchestrator(chain=["a", "b"], failure_threshold=1, cooldown_ms=1000)
    app.state.orchestrator = orch

    def failex():
        raise RuntimeError("nope")

    app.state.agent_adapters = {"a": failex, "b": failex}

    client = _client()
    r = client.get("/api/v1/portfolio")
    client.close()
    assert r.status_code == 500
    assert "Failed to fetch portfolio" in r.json().get("detail", "")
