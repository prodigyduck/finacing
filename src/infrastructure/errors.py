class RateLimitError(Exception):
    """Raised when an upstream agent or service returns a 429 rate limit."""


class QuotaExceededError(Exception):
    """Raised when an upstream agent or service indicates quota exhaustion."""
