from src.infrastructure.errors import RateLimitError, QuotaExceededError


def test_rate_limit_error_is_exception():
    e = RateLimitError("ratelimited")
    assert isinstance(e, Exception)
    assert str(e) == "ratelimited"


def test_quota_exceeded_error_is_exception():
    e = QuotaExceededError("quota")
    assert isinstance(e, Exception)
    assert str(e) == "quota"
