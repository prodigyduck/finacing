# Security

## Overview

This document outlines security considerations, best practices, and guidelines for the Financing project. The application reads investment data from a local Obsidian vault, so security focuses on local file system protection, input validation, and API security.

## Security Principles

1. **Defense in Depth:** Multiple layers of security controls
2. **Least Privilege:** Minimal permissions and access rights
3. **Secure by Default:** Secure configurations by default
4. **Fail Securely:** System fails to a secure state on errors
5. **Zero Trust:** Verify all requests and inputs

---

## Local File Security

### Obsidian Vault Access

**Current Implementation:**
- Reads investment data from `~/git/obsidian/투자/투자.md`
- No authentication required (local file access)
- No credentials stored anywhere in the application
- Read-only access to the Obsidian vault

**Security Advantages:**
- No external credentials to protect
- No third-party API dependencies
- Data stays entirely on the local machine
- No network exposure for data retrieval

**File Path Security:**
```python
# Good: Safe path handling
from pathlib import Path

def get_vault_path() -> Path:
    """Get the Obsidian vault file path from config."""
    vault_path = Path(os.getenv(
        "OBSIDIAN_VAULT_PATH",
        str(Path.home() / "git" / "obsidian" / "투자" / "투자.md")
    ))
    # Ensure path is within expected directory
    resolved = vault_path.resolve()
    expected_root = Path.home() / "git" / "obsidian"
    if not str(resolved).startswith(str(expected_root.resolve())):
        raise ValueError("Vault path is outside the expected directory")
    return resolved

# Bad: Unvalidated path from user input
def get_vault_path(user_input: str) -> Path:
    return Path(user_input)  # Path traversal vulnerability
```

### File Permissions

**Critical Files:**
```bash
# Obsidian vault file - readable by owner (600 or 644)
chmod 600 ~/git/obsidian/투자/투자.md

# Configuration files - restricted to owner
chmod 600 .env

# Verify permissions
ls -l ~/git/obsidian/투자/투자.md
# Expected: -rw------- or -rw-r--r-- (owner read/write)
```

**Directory Permissions:**
```bash
# Obsidian vault directory
chmod 700 ~/git/obsidian/투자

# Application directory
chmod 755 /path/to/financing
```

---

## Data Protection

### Sensitive Data Classification

| Data Type | Sensitivity | Storage | Handling |
|-----------|-------------|---------|----------|
| Obsidian vault path | LOW | Environment variables | Never logged in full |
| Investment portfolio data | MEDIUM | Local Obsidian vault | User-controlled |
| API responses | MEDIUM | In-memory only | No persistent storage |
| Application logs | LOW | Local filesystem | No sensitive data |

### Encryption

**Local File Access:**
- Obsidian vault files are local (no network transit)
- FastAPI serves data over localhost by default
- Use HTTPS/TLS when deploying to remote access

**In Transit (when accessing via browser):**
- FastAPI backend serves over HTTP by default
- For remote access, use a reverse proxy with TLS
- No sensitive data leaves the local machine in default setup

**At Rest:**
- Investment data stored in local Obsidian vault (file system security)
- No database or external storage
- No credential storage required

### Logging Security

**Logging Policy:**
- Never log investment amounts or personal data
- Never log full file paths in production logs
- Sanitize logs before output

```python
# Good: Secure logging
import logging

logger = logging.getLogger(__name__)

def read_vault(path: Path):
    logger.info(f"Reading vault from configured path")
    try:
        content = path.read_text(encoding="utf-8")
        logger.info(f"Successfully read {len(content)} characters")
    except Exception as e:
        logger.error(f"Failed to read vault file")
        raise

# Bad: Logging sensitive data
def read_vault(path: Path):
    logger.info(f"Reading vault from {path}")  # Full path logged
    content = path.read_text()
    logger.info(f"Content: {content}")  # Investment data logged!
```

---

## Input Validation

### File Input Validation

All file reads must be validated before processing:

```python
# Good: File input validation
def validate_vault_path(path: Path) -> Path:
    """Validate Obsidian vault file path"""
    resolved = path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Vault file not found: {resolved.name}")
    if not resolved.is_file():
        raise ValueError(f"Vault path is not a file: {resolved.name}")
    if resolved.suffix != ".md":
        raise ValueError(f"Vault file must be a markdown file, got: {resolved.suffix}")
    if not os.access(resolved, os.R_OK):
        raise PermissionError(f"No read permission for vault file")
    return resolved

# Bad: No validation
def read_vault(path: str):
    with open(path) as f:  # No validation of path
        return f.read()
```

### Data Parsing Validation

Validate parsed investment data:

```python
# Good: Validate parsed data
def parse_line(line: str) -> InvestmentRecord:
    """Parse investment line with validation"""
    try:
        date_str, amount_str = line.strip().split()
    except ValueError as e:
        raise ValueError(f"Invalid line format: {e}")

    if not amount_str.endswith("억"):
        raise ValueError(f"Amount must end with '억': {amount_str}")

    amount = Decimal(amount_str.rstrip("억"))
    if amount < 0:
        raise ValueError("Amount cannot be negative")

    return InvestmentRecord(date=date_str, amount=amount)

# Bad: No validation
def parse_line(line: str) -> InvestmentRecord:
    date_str, amount_str = line.split()
    return InvestmentRecord(date=date_str, amount=amount_str)
```

---

## API Security

### FastAPI Endpoint Security

**Current Endpoints:**
- `GET /api/v1/history` - Returns portfolio history from local Obsidian data

**Security Measures:**
```python
# Good: Input validation on API endpoints
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

@app.get("/api/v1/history")
async def get_history():
    """Get portfolio history from Obsidian vault"""
    try:
        vault_path = get_vault_path()  # Validated path
        validate_vault_path(vault_path)
        records = parser.fetch_investment_records(vault_path)
        return PortfolioHistory(records=records).model_dump()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Vault file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Cannot access vault file")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid data: {e}")

# Bad: Unvalidated endpoint
@app.get("/api/v1/history")
async def get_history():
    data = open("some/path").read()  # No validation
    return {"data": data}
```

### CORS Configuration

Restrict CORS to known origins:

```python
# Good: Restricted CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server only
    allow_methods=["GET"],
    allow_headers=[],
)

# Bad: Open CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origin
)
```

---

## Dependency Security

### Third-Party Dependencies

**Current Dependencies:**
- `fastapi>=0.100.0` - Web framework
- `uvicorn>=0.20.0` - ASGI server
- `pandas>=2.2.0` - Data processing
- `pydantic>=2.0.0` - Data validation

**Security Measures:**
1. **Regular Updates:** Keep dependencies up-to-date
2. **Vulnerability Scanning:** Use `pip-audit` or `safety` to check for vulnerabilities
3. **Pin Versions:** Use exact versions in requirements.txt
4. **Review Dependencies:** Monitor for security advisories

**Dependency Auditing:**
```bash
# Install security audit tools
pip install pip-audit

# Run security audit
pip-audit

# Expected output: No known vulnerabilities found
```

**Dependency Updates:**
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all dependencies
pip install --upgrade -r requirements.txt
```

---

## Access Control

### Application Access

**Current Deployment:**
- Local deployment via FastAPI + Uvicorn
- No authentication at application level
- Access restricted by deployment method
- No credential storage needed

**Recommended Security Practices:**
1. **Deploy behind VPN:** Use Tailscale Funnel or SSH tunneling
2. **Network Isolation:** Deploy on private network
3. **Firewall Rules:** Restrict inbound/outbound traffic

**Deployment Options:**
```bash
# Option 1: Local only (default)
uvicorn src.presentation.app:app --host 127.0.0.1 --port 8000

# Option 2: Tailscale Funnel (Recommended for personal use)
tailscale funnel 8000

# Option 3: SSH Tunneling
ssh -L 8000:localhost:8000 user@remote-server
```

### File System Permissions

**Critical Files:**
```bash
# .env file - 600 (read/write for owner only)
chmod 600 .env

# Virtual environment - 755 (standard)
chmod 755 venv

# Source code - 644 (readable by all)
chmod 644 src/**/*.py

# Obsidian vault - 600 or 644 (readable by owner)
chmod 600 ~/git/obsidian/투자/투자.md
```

---

## Error Handling & Information Disclosure

### Secure Error Messages

Never expose sensitive information in error messages:

```python
# Good: Generic error messages
def fetch_investment_data():
    try:
        vault_path = get_vault_path()
        return parser.fetch_investment_records(vault_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data source not available")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Cannot access data source")

# Bad: Detailed error messages
def fetch_investment_data():
    try:
        vault_path = get_vault_path()
        return parser.fetch_investment_records(vault_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # May reveal internal structure
```

### Debug Mode

**Never enable debug mode in production:**

```python
# Bad: Debug mode enabled
DEBUG = True  # Exposes sensitive information

# Good: Debug mode disabled in production
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## Backup & Recovery

### Local File Backup

**Data Location:**
- Investment data stored in local Obsidian vault
- Obsidian provides version history (if using Obsidian app)
- Git can be used for vault version control

**Recommended Backup Strategy:**
1. **Obsidian Version History:** Use Obsidian's built-in file recovery
2. **Git Version Control:** Keep vault under git for history
3. **Manual Export:** Periodically export investment data as JSON/CSV
4. **Cloud Sync:** Use Obsidian Sync or similar for off-device backup

**Export Procedure:**
```bash
# Export investment data from API
curl http://localhost:8000/api/v1/history -o backup.json
```

---

## Security Testing

### Automated Security Checks

**Run security checks regularly:**

```bash
# Dependency vulnerability scan
pip-audit

# Code security analysis (if using bandit)
pip install bandit
bandit -r src/

# Secret scanning (if using truffleHog)
pip install truffleHog
trufflehog --regex --entropy=False /path/to/repo
```

### Manual Security Review

**Checklist:**
- [ ] No credentials in code (none needed for local file access)
- [ ] `.env` file in `.gitignore`
- [ ] Input validation on all user inputs
- [ ] No sensitive data in logs
- [ ] Dependencies up-to-date
- [ ] File permissions set correctly
- [ ] Debug mode disabled in production
- [ ] CORS properly configured
- [ ] Vault path validated and restricted

---

## Incident Response

### Security Incident Types

1. **Data Exposure:** Unauthorized access to investment data
2. **File Tampering:** Modification of Obsidian vault files
3. **Malicious Code:** Third-party dependency vulnerability
4. **Denial of Service:** Application unavailable due to attack

### Incident Response Plan

**Immediate Actions:**
1. **Isolate:** Disconnect application from network
2. **Assess:** Determine scope and impact
3. **Contain:** Restore vault from backup, restrict access
4. **Document:** Log all actions taken

**Post-Incident:**
1. **Investigate:** Root cause analysis
2. **Remediate:** Fix vulnerabilities
3. **Review:** Update security practices
4. **Monitor:** Watch for signs of compromise

**Contact:**
- Report security issues via GitHub Security Advisories
- For urgent issues, contact project maintainers directly

---

## Compliance & Regulations

### Data Privacy

**GDPR Considerations:**
- Investment data is personal data
- User controls data via local Obsidian vault
- No data processing beyond what user authorizes
- No data leaves the local machine

**Best Practices:**
- Minimize data collection
- Provide data export options via API
- Allow data deletion through Obsidian vault management

### Financial Data

**SEC/FINRA Considerations:**
- Not providing financial advice
- Data is for informational purposes only
- No automated trading or recommendations

**Disclaimer:**
```python
# Include disclaimer in API responses
DISCLAIMER = (
    "This application is for informational purposes only. "
    "It does not provide financial advice or recommendations. "
    "Please consult a qualified financial advisor for investment decisions."
)
```

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-19 | Updated for Obsidian local file architecture |
| 1.0.0 | 2026-03-29 | Initial security documentation |
