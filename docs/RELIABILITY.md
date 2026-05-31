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
# Good: Graceful degradation for file I/O
def fetch_investment_data(vault_path: Path) -> List[InvestmentRecord]:
    try:
        content = vault_path.read_text(encoding="utf-8")
        records = parse_lines(content)
        return records
    except FileNotFoundError:
        logger.warning("Vault file not found. Returning cached data.")
        return load_cached_data()
    except PermissionError:
        logger.warning("Cannot read vault file. Returning cached data.")
        return load_cached_data()
    except UnicodeDecodeError:
        logger.warning("Vault file encoding error. Returning cached data.")
        return load_cached_data()
    except Exception as e:
        logger.error(f"Unexpected error reading vault: {e}")
        return []

# Bad: No error handling
def fetch_investment_data(vault_path: Path) -> List[InvestmentRecord]:
    content = vault_path.read_text(encoding="utf-8")  # May crash
    return parse_lines(content)
```

### 2. Retry Logic for File I/O

Implement retry logic for transient file system failures (file locks, concurrent access).

```python
# Good: Retry with exponential backoff
import time
from functools import wraps

def retry(max_attempts=3, delay=0.5):
    """Decorator for retry logic on file operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (IOError, OSError) as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def read_vault_file(path: Path) -> str:
    """Read vault file with retry on transient errors"""
    return path.read_text(encoding="utf-8")
```

### 3. Timeout Handling

Set timeouts for file read operations to prevent hanging on large files or network-mounted drives.

```python
# Good: Timeout handling for file reads
import signal

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("File read timed out")

def read_with_timeout(path: Path, timeout_seconds=10):
    """Read file with timeout"""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        result = path.read_text(encoding="utf-8")
        signal.alarm(0)  # Disable alarm
        return result
    except TimeoutError:
        logger.error("File read timed out")
        raise HTTPException(status_code=504, detail="Data source read timed out")
```

---

## Data Validation

### Input Validation

Validate all inputs before processing.

```python
# Good: File path validation
def validate_vault_path(path: Path) -> Path:
    """Validate Obsidian vault file path"""
    resolved = path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Vault file not found: {resolved.name}")
    if not resolved.is_file():
        raise ValueError(f"Path is not a file: {resolved.name}")
    if resolved.suffix != ".md":
        raise ValueError(f"Expected .md file, got: {resolved.suffix}")
    return resolved

# Usage
try:
    vault_path = validate_vault_path(user_configured_path)
    records = fetch_investment_data(vault_path)
except FileNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except ValueError as e:
    raise HTTPException(status_code=422, detail=str(e))
```

### Data Integrity Checks

Validate parsed investment data.

```python
# Good: Data integrity checks
def validate_record(record: InvestmentRecord) -> InvestmentRecord:
    """Validate investment record data"""
    if not record.date or not record.date.strip():
        raise ValueError("Record date cannot be empty")
    if record.amount < 0:
        raise ValueError(f"Amount cannot be negative: {record.amount}")
    return record

# Usage in parser
def parse_line(line: str) -> InvestmentRecord:
    """Parse a single line (format: M.DD 억)"""
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Invalid format, expected 'M.DD 억': {line}")
    date_str = parts[0]
    amount_str = parts[1]
    if not amount_str.endswith("억"):
        raise ValueError(f"Amount must end with '억': {amount_str}")
    amount = Decimal(amount_str.rstrip("억"))
    record = InvestmentRecord(date=date_str, amount=amount)
    return validate_record(record)
```

---

## Caching Strategies

### 1. Application-Level Caching

Cache parsed data to reduce file reads.

```python
# Good: Application caching
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

def get_investment_data(vault_path: Path):
    cache_key = str(vault_path)
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = read_and_parse_vault(vault_path)
    cache.set(cache_key, data)
    return data
```

### 2. FastAPI Response Caching

Use FastAPI middleware or decorators for response caching.

```python
# Good: API response caching
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time

_cache = {}
_CACHE_TTL = 300  # 5 minutes

@app.get("/api/v1/history")
async def get_history():
    cache_key = "portfolio_history"
    if cache_key in _cache:
        data, timestamp = _cache[cache_key]
        if time.time() - timestamp < _CACHE_TTL:
            return JSONResponse(content=data)

    vault_path = get_vault_path()
    records = parser.fetch_investment_records(vault_path)
    history = PortfolioHistory(records=records).model_dump()
    _cache[cache_key] = (history, time.time())
    return JSONResponse(content=history)
```

---

## Monitoring & Logging

### Structured Logging

Use structured logging for better debugging and monitoring.

```python
# Good: Structured logging
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
logger.info("Reading Obsidian vault", extra={"file": "투자.md", "attempt": 1})
```

### Error Tracking

Track errors for monitoring and debugging.

```python
# Good: Error tracking
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
    tracker.track_error(e, context={"file": "투자.md"})
    raise HTTPException(status_code=500, detail="Failed to fetch data")
```

### Performance Monitoring

Track performance metrics to identify bottlenecks.

```python
# Good: Performance monitoring
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
    records = fetch_investment_data(vault_path)
```

---

## Backup & Recovery

### Data Backup

Regularly backup critical data.

```python
# Good: Data backup
import json
import os
from datetime import datetime

def backup_investment_data(records: List[InvestmentRecord], backup_dir="backups"):
    """Backup investment data to file"""
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"investment_data_{timestamp}.json")

    data = [record.to_dict() for record in records]
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Backup created: {backup_file}")

# Scheduled backup
def scheduled_backup():
    """Run scheduled backup"""
    records = fetch_investment_data(vault_path)
    backup_investment_data(records)
```

### Data Recovery

Restore from backup when needed.

```python
# Good: Data recovery
def restore_from_backup(backup_file: str) -> List[InvestmentRecord]:
    """Restore investment data from backup"""
    with open(backup_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = [InvestmentRecord.from_dict(r) for r in data]
    logger.info(f"Restored {len(records)} records from {backup_file}")
    return records
```

---

## Health Checks

### Application Health Check

Implement health check endpoints for monitoring.

```python
# Good: Health check
@app.get("/health")
async def health_check():
    """Check application health"""
    checks = {
        "obsidian_vault": check_vault_accessibility(),
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

def check_vault_accessibility() -> bool:
    """Check Obsidian vault file accessibility"""
    try:
        vault_path = get_vault_path()
        return vault_path.exists() and vault_path.is_file()
    except Exception:
        return False
```

---

## Testing Strategies

### Unit Testing

Test individual components in isolation.

```python
# Good: Unit tests
def test_portfolio_total_value_empty():
    """Test total value with no records"""
    portfolio = Portfolio(records=[])
    assert portfolio.total_value().amount == Decimal("0")

def test_portfolio_total_value_single_record():
    """Test total value with single record"""
    record = InvestmentRecord(date="4.19", amount=Decimal("1.5"))
    portfolio = Portfolio(records=[record])
    assert portfolio.total_value().amount == Decimal("1.5")
```

### Integration Testing

Test components working together.

```python
# Good: Integration tests
def test_fetch_and_parse_flow(tmp_path):
    """Test complete file read and parse flow"""
    # Setup
    vault_file = tmp_path / "투자.md"
    vault_file.write_text("4.19 1.5억\n4.18 1.3억\n", encoding="utf-8")

    # Test
    parser = ObsidianParser(vault_path=vault_file)
    records = parser.fetch_investment_records()

    # Verify
    assert len(records) == 2
    assert records[0].amount == Decimal("1.5")
```

### End-to-End Testing

Test complete user flows.

```python
# Good: End-to-end tests
from fastapi.testclient import TestClient

def test_history_endpoint_returns_data(client: TestClient):
    """Test /api/v1/history returns portfolio data"""
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
```

---

## Circuit Breaker Pattern

Implement circuit breaker to prevent cascading failures.

```python
# Good: Circuit breaker for file reads
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

def safe_fetch_data(vault_path: Path):
    try:
        return circuit_breaker.call(read_and_parse_vault, vault_path)
    except Exception as e:
        logger.error(f"Circuit breaker triggered: {e}")
        return load_cached_data()
```

---

## Deployment Reliability

### Graceful Shutdown

Handle shutdown gracefully to complete in-flight operations.

```python
# Good: Graceful shutdown
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

# Usage with FastAPI
import uvicorn

shutdown_handler = GracefulShutdown()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

logger.info("Graceful shutdown complete")
```

### Configuration Validation

Validate configuration at startup.

```python
# Good: Configuration validation
def validate_config():
    """Validate application configuration"""
    errors = []

    # Check Obsidian vault path
    vault_path = Path(os.getenv(
        "OBSIDIAN_VAULT_PATH",
        str(Path.home() / "git" / "obsidian" / "투자" / "투자.md")
    ))
    if not vault_path.exists():
        errors.append(f"Obsidian vault file not found: {vault_path}")
    if vault_path.exists() and not os.access(vault_path, os.R_OK):
        errors.append(f"No read permission for vault file: {vault_path}")

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
| P2 - High | Major functionality broken | < 1 hour | Cannot read vault file, API errors |
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
2. **Implement retries:** Retry transient file I/O failures
3. **Validate all inputs:** Don't trust user input or file content
4. **Cache strategically:** Reduce file reads and improve performance
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
| 1.1.0 | 2026-04-19 | Updated for Obsidian file I/O error patterns |
| 1.0.0 | 2026-03-29 | Initial reliability documentation |
