# Reliability

## Overview

This document outlines reliability practices, patterns, and strategies for the Financing project. Reliability is crucial for a financial dashboard as users depend on accurate, available data for investment decisions.

## Reliability Principles

1. **Fault Tolerance:** Gracefully handle failures without crashing
2. **Redundancy:** Critical components have backups or fallbacks
3. **Monitoring:** Track system health and performance
4. **Recovery:** Quick recovery from failures with minimal data loss
5. **Testing:** Comprehensive testing prevents failures in production

---

## Error Handling Strategies

### 1. Try-Catch with Graceful Degradation

Wrap potentially failing operations in try-except blocks with fallback behavior.

```python
# ✅ Good: Graceful degradation
def fetch_investment_data(label: str) -> List[InvestmentAsset]:
    try:
        notes = keep.find(labels=[label])
        return [parse_note(note) for note in notes]
    except gkeepapi.APIException:
        st.warning("Failed to fetch live data. Using cached data.")
        return load_cached_data()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

# ❌ Bad: No error handling
def fetch_investment_data(label: str) -> List[InvestmentAsset]:
    notes = keep.find(labels=[label])  # May crash
    return [parse_note(note) for note in notes]
```

### 2. Retry Logic

Implement retry logic for transient failures (network issues, API rate limits).

```python
# ✅ Good: Retry with exponential backoff
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """Decorator for retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def fetch_with_retry(label: str) -> List[InvestmentAsset]:
    return keep.find(labels=[label])
```

### 3. Timeout Handling

Set timeouts for network operations to prevent hanging.

```python
# ✅ Good: Timeout handling
import signal

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

def fetch_with_timeout(label: str, timeout_seconds=30):
    """Fetch data with timeout"""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        result = keep.find(labels=[label])
        signal.alarm(0)  # Disable alarm
        return result
    except TimeoutError:
        st.error("Operation timed out. Please try again.")
        return []
```

---

## Data Validation

### Input Validation

Validate all user inputs before processing.

```python
# ✅ Good: Input validation
def validate_label(label: str) -> str:
    """Validate Google Keep label"""
    if not label or not label.strip():
        raise ValueError("Label cannot be empty")
    if len(label) > 100:
        raise ValueError("Label too long (max 100 characters)")
    if not label.isprintable():
        raise ValueError("Label contains invalid characters")
    return label.strip()

# Usage
try:
    validated_label = validate_label(user_input)
    assets = fetch_investment_data(validated_label)
except ValueError as e:
    st.error(f"Invalid input: {e}")
```

### Data Integrity Checks

Validate parsed investment data.

```python
# ✅ Good: Data integrity checks
def validate_asset(asset: InvestmentAsset) -> InvestmentAsset:
    """Validate investment asset data"""
    if not asset.name or not asset.name.strip():
        raise ValueError("Asset name cannot be empty")
    if asset.quantity <= 0:
        raise ValueError(f"Quantity must be positive: {asset.quantity}")
    if asset.unit_price.amount < 0:
        raise ValueError(f"Price cannot be negative: {asset.unit_price}")
    return asset

# Usage in parser
def parse_note(note_text: str) -> InvestmentAsset:
    asset = InvestmentAsset(...)
    return validate_asset(asset)
```

---

## Caching Strategies

### 1. Application-Level Caching

Cache frequently accessed data to reduce API calls.

```python
# ✅ Good: Application caching
from functools import lru_cache
import time

class DataCache:
    def __init__(self, ttl_seconds=300):
        self._cache = {}
        self._ttl = ttl_seconds

    def get(self, key):
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key, value):
        self._cache[key] = (value, time.time())

# Usage
cache = DataCache(ttl_seconds=300)  # 5 minute cache

def get_investment_data(label: str):
    cached = cache.get(label)
    if cached:
        return cached

    data = fetch_from_api(label)
    cache.set(label, data)
    return data
```

### 2. Streamlit Caching

Use Streamlit's built-in caching for expensive operations.

```python
# ✅ Good: Streamlit caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_expensive_data(label: str) -> List[InvestmentAsset]:
    """Fetch data with caching"""
    time.sleep(2)  # Simulate expensive operation
    return fetch_from_api(label)
```

---

## Monitoring & Logging

### Structured Logging

Use structured logging for better debugging and monitoring.

```python
# ✅ Good: Structured logging
import logging
import json

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for better parsing"""
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Fetching investment data", extra={"label": "투자", "attempt": 1})
```

### Error Tracking

Track errors for monitoring and debugging.

```python
# ✅ Good: Error tracking
class ErrorTracker:
    def __init__(self):
        self._errors = []

    def track_error(self, error: Exception, context: dict):
        """Track error with context"""
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self._errors.append(error_info)
        logger.error(f"Error tracked: {error_info}")

    def get_recent_errors(self, limit=10):
        """Get recent errors"""
        return self._errors[-limit:]

# Usage
tracker = ErrorTracker()
try:
    fetch_investment_data()
except Exception as e:
    tracker.track_error(e, context={"label": "투자"})
    st.error("Failed to fetch data. Error has been logged.")
```

### Performance Monitoring

Track performance metrics to identify bottlenecks.

```python
# ✅ Good: Performance monitoring
import time
from contextlib import contextmanager

@contextmanager
def performance_tracker(operation_name: str):
    """Track performance of operations"""
    start_time = time.time()
    try:
        yield
    finally:
        elapsed_time = time.time() - start_time
        logger.info(
            f"Operation completed",
            extra={
                "operation": operation_name,
                "duration_seconds": elapsed_time,
            }
        )

# Usage
with performance_tracker("fetch_investment_data"):
    assets = fetch_investment_data("투자")
```

---

## Backup & Recovery

### Data Backup

Regularly backup critical data.

```python
# ✅ Good: Data backup
import json
import os
from datetime import datetime

def backup_investment_data(assets: List[InvestmentAsset], backup_dir="backups"):
    """Backup investment data to file"""
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"investment_data_{timestamp}.json")

    data = [asset.to_dict() for asset in assets]
    with open(backup_file, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Backup created: {backup_file}")

# Scheduled backup
def scheduled_backup():
    """Run scheduled backup"""
    assets = fetch_investment_data("투자")
    backup_investment_data(assets)
```

### Data Recovery

Restore from backup when needed.

```python
# ✅ Good: Data recovery
def restore_from_backup(backup_file: str) -> List[InvestmentAsset]:
    """Restore investment data from backup"""
    with open(backup_file, "r") as f:
        data = json.load(f)

    assets = [InvestmentAsset.from_dict(asset_data) for asset_data in data]
    logger.info(f"Restored {len(assets)} assets from {backup_file}")
    return assets

# Usage
if st.button("Restore from Backup"):
    backup_file = st.file_uploader("Select backup file")
    if backup_file:
        assets = restore_from_backup(backup_file)
        st.success(f"Restored {len(assets)} assets")
```

---

## Health Checks

### Application Health Check

Implement health check endpoints for monitoring.

```python
# ✅ Good: Health check
def health_check() -> dict:
    """Check application health"""
    checks = {
        "google_keep_connection": check_google_keep_connection(),
        "data_cache": check_data_cache(),
        "disk_space": check_disk_space(),
    }

    all_healthy = all(checks.values())
    status = "healthy" if all_healthy else "degraded"

    return {
        "status": status,
        "checks": checks,
        "timestamp": datetime.datetime.now().isoformat(),
    }

def check_google_keep_connection() -> bool:
    """Check Google Keep connection"""
    try:
        keep.resume()
        return True
    except:
        return False

# Display health status
if st.button("Health Check"):
    health = health_check()
    st.json(health)
    if health["status"] == "healthy":
        st.success("All systems operational")
    else:
        st.warning("Some systems degraded")
```

---

## Testing Strategies

### Unit Testing

Test individual components in isolation.

```python
# ✅ Good: Unit tests
def test_portfolio_total_value_empty():
    """Test total value with no assets"""
    portfolio = Portfolio(assets=[])
    assert portfolio.total_value().amount == Decimal("0")

def test_portfolio_total_value_single_asset():
    """Test total value with single asset"""
    asset = InvestmentAsset(
        name="Stock A",
        quantity=10,
        unit_price=Money(amount=Decimal("100000"), currency="KRW")
    )
    portfolio = Portfolio(assets=[asset])
    assert portfolio.total_value().amount == Decimal("1000000")
```

### Integration Testing

Test components working together.

```python
# ✅ Good: Integration tests
def test_fetch_and_parse_flow():
    """Test complete fetch and parse flow"""
    # Setup
    mock_keep = Mock()
    mock_keep.find.return_value = [create_mock_note()]

    # Test
    repository = GKeepRepository(mock_keep)
    assets = repository.fetch_investment_notes("투자")

    # Verify
    assert len(assets) == 1
    assert assets[0].name == "Stock A"
```

### End-to-End Testing

Test complete user flows.

```python
# ✅ Good: End-to-end tests
def test_dashboard_displays_portfolio():
    """Test dashboard displays portfolio correctly"""
    # Setup
    assets = create_test_assets()
    mock_streamlit = Mock()

    # Test
    show_dashboard(assets, mock_streamlit)

    # Verify
    assert mock_streamlit.metric.call_count == 3
    assert mock_streamlit.plotly_chart.call_count >= 1
```

---

## Circuit Breaker Pattern

Implement circuit breaker to prevent cascading failures.

```python
# ✅ Good: Circuit breaker
class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker"""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout_seconds:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"

            raise e

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=60)

def safe_fetch_data(label: str):
    try:
        return circuit_breaker.call(fetch_investment_data, label)
    except Exception as e:
        st.error(f"Circuit breaker triggered: {e}")
        return []
```

---

## Deployment Reliability

### Graceful Shutdown

Handle shutdown gracefully to complete in-flight operations.

```python
# ✅ Good: Graceful shutdown
import signal
import sys

class GracefulShutdown:
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self._handler)
        signal.signal(signal.SIGTERM, self._handler)

    def _handler(self, signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.shutdown = True

    def is_shutdown_requested(self):
        return self.shutdown

# Usage
shutdown_handler = GracefulShutdown()

while not shutdown_handler.is_shutdown_requested():
    try:
        process_requests()
    except Exception as e:
        logger.error(f"Error processing requests: {e}")

logger.info("Graceful shutdown complete")
```

### Configuration Validation

Validate configuration at startup.

```python
# ✅ Good: Configuration validation
def validate_config():
    """Validate application configuration"""
    errors = []

    # Check environment variables
    if not os.getenv("GOOGLE_KEEP_EMAIL"):
        errors.append("GOOGLE_KEEP_EMAIL not set")
    if not os.getenv("GOOGLE_KEEP_PASSWORD"):
        errors.append("GOOGLE_KEEP_PASSWORD not set")

    # Check directory structure
    required_dirs = ["backups", "logs"]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except Exception as e:
                errors.append(f"Cannot create directory {dir_path}: {e}")

    if errors:
        raise ValueError(f"Configuration validation failed: {errors}")

# Validate at startup
try:
    validate_config()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)
```

---

## Incident Response

### Incident Classification

Classify incidents by severity:

| Severity | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| P1 - Critical | Complete outage | < 15 minutes | Application down, no data available |
| P2 - High | Major functionality broken | < 1 hour | Cannot fetch data, partial outage |
| P3 - Medium | Minor functionality broken | < 4 hours | Slow performance, data display issues |
| P4 - Low | Cosmetic issues | < 24 hours | UI bugs, formatting issues |

### Incident Response Steps

1. **Detect:** Identify incident via monitoring or user reports
2. **Assess:** Determine severity and impact
3. **Contain:** Limit damage (disable broken feature, use cache)
4. **Mitigate:** Provide temporary workaround
5. **Resolve:** Fix root cause
6. **Post-Mortem:** Document and learn from incident

---

## Best Practices Summary

1. **Handle errors gracefully:** Never crash the application
2. **Implement retries:** Retry transient failures
3. **Validate all inputs:** Don't trust user input
4. **Cache strategically:** Reduce API calls and improve performance
5. **Monitor everything:** Log errors and track performance
6. **Test thoroughly:** Unit, integration, and E2E tests
7. **Backup regularly:** Have recovery plan for data loss
8. **Plan for failures:** Circuit breaker, graceful degradation
9. **Monitor health:** Health checks and monitoring
10. **Learn from incidents:** Post-mortems and continuous improvement

---

## References

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Reliability Engineering](https://www.oreilly.com/library/view/site-reliability-engineering/9781491959358/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial reliability documentation |
