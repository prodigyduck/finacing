import pytest

from types import SimpleNamespace

import src.infrastructure.repositories.gkeep_repository as gkr
from src.infrastructure.errors import RateLimitError


class DummyAuthException(Exception):
    def __init__(self, status_code=None):
        self.status_code = status_code


def test_fetch_investment_notes_maps_429_to_ratelimit(monkeypatch):
    # Arrange: create repo and simulate login raising gkeep exception with status_code 429
    repo = gkr.GKeepRepository("e@example.com", "pw")

    class FakeGKeep:
        def __init__(self):
            pass

    def fake_login():
        # Simulate gkeepapi.exception.GKeepException with status_code 429
        exc = DummyAuthException()
        exc.status_code = 429
        raise exc

    monkeypatch.setattr(repo, "_login", fake_login)

    with pytest.raises(RateLimitError):
        repo.fetch_investment_notes("투자")
