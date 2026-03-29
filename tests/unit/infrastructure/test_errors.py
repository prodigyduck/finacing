import pytest

from src.infrastructure.errors import RateLimitError, QuotaExceededError


def test_rate_limit_error_is_exception():
    with pytest.raises(RateLimitError):
        raise RateLimitError("too many requests")


def test_quota_exceeded_error_is_exception():
    with pytest.raises(QuotaExceededError):
        raise QuotaExceededError("quota exceeded")
