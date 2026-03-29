# Security

## Overview

This document outlines security considerations, best practices, and guidelines for the Financing project. Security is critical as the application handles sensitive financial data and Google Keep authentication credentials.

## Security Principles

1. **Defense in Depth:** Multiple layers of security controls
2. **Least Privilege:** Minimal permissions and access rights
3. **Secure by Default:** Secure configurations by default
4. **Fail Securely:** System fails to a secure state on errors
5. **Zero Trust:** Verify all requests and inputs

---

## Authentication & Authorization

### Google Keep Authentication

**Current Implementation:**
- Uses `gkeepapi` (unofficial Google Keep API)
- Email and password stored in environment variables
- Optional 2FA (Two-Factor Authentication) support

**Security Measures:**
- Credentials stored in `.env` file (never in code)
- `.env` file excluded from git via `.gitignore`
- No credential logging or error messages

**Best Practices:**
```bash
# ✅ Good: Credentials in .env file
GOOGLE_KEEP_EMAIL=your_email@gmail.com
GOOGLE_KEEP_PASSWORD=your_password
GOOGLE_KEEP_MASTER_TOKEN=your_2fa_token

# ❌ Bad: Hardcoded credentials
EMAIL = "your_email@gmail.com"
PASSWORD = "your_password"
```

**Authentication Flow:**
```
User enters credentials → Stored in .env → gkeepapi authenticates → Session token stored
```

**2FA Setup:**
If you have 2FA enabled on your Google account, you need to generate an app-specific password:
1. Go to Google Account Security
2. Enable 2FA if not already enabled
3. Generate app-specific password for "Mail/Calendar"
4. Use this password in `.env` file

**Authentication Error Handling:**
```python
# ✅ Good: Secure error handling
try:
    keep.login(email, password)
except gkeepapi.LoginException as e:
    st.error("Authentication failed. Please check your credentials.")
    # Never log or display the actual error message which may contain sensitive info

# ❌ Bad: Leaking sensitive information
try:
    keep.login(email, password)
except Exception as e:
    st.error(f"Login failed: {e}")  # May reveal sensitive details
```

---

## Data Protection

### Sensitive Data Classification

| Data Type | Sensitivity | Storage | Handling |
|-----------|-------------|---------|----------|
| Google Keep credentials | HIGH | Environment variables | Never logged |
| Investment portfolio data | MEDIUM | Google Keep (external) | Encrypted in transit |
| User notes | MEDIUM | Google Keep (external) | User-controlled |
| Application logs | LOW | Local filesystem | No sensitive data |

### Encryption

**In Transit:**
- All Google Keep API calls use HTTPS (gkeepapi default)
- No custom encryption needed for HTTPS

**At Rest:**
- Investment data stored in Google Keep (encrypted by Google)
- Credentials stored in `.env` file (file system permissions)
- No local database or persistent storage of sensitive data

**File Permissions:**
```bash
# Restrict .env file permissions (chmod 600)
chmod 600 .env

# Verify permissions
ls -l .env
# Expected output: -rw------- 1 user group ... .env
```

### Logging Security

**Logging Policy:**
- Never log credentials (email, password, tokens)
- Never log sensitive investment data
- Sanitize logs before output

```python
# ✅ Good: Secure logging
import logging

logger = logging.getLogger(__name__)

def login(email: str, password: str):
    logger.info(f"Attempting login for {email[:3]}***")  # Partial email only
    try:
        keep.login(email, password)
        logger.info("Login successful")
    except Exception as e:
        logger.error("Login failed")
        raise

# ❌ Bad: Logging sensitive data
def login(email: str, password: str):
    logger.info(f"Login attempt: {email}, {password}")  # Full credentials logged!
```

---

## Input Validation

### User Input Validation

All user inputs must be validated before processing:

```python
# ✅ Good: Input validation
def validate_label(label: str) -> str:
    """Validate Google Keep label"""
    if not label or not label.strip():
        raise ValueError("Label cannot be empty")
    if len(label) > 100:
        raise ValueError("Label too long (max 100 characters)")
    return label.strip()

def fetch_data(label: str):
    validated_label = validate_label(label)
    # Process validated label
    return repository.fetch_investment_notes(validated_label)

# ❌ Bad: No validation
def fetch_data(label: str):
    return repository.fetch_investment_notes(label)  # Direct use
```

### Data Parsing Validation

Validate parsed investment data:

```python
# ✅ Good: Validate parsed data
def parse_note(note_text: str) -> InvestmentAsset:
    """Parse investment note with validation"""
    try:
        name, quantity, price = parse_text(note_text)
    except ValueError as e:
        raise ValueError(f"Invalid note format: {e}")

    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if price.amount < 0:
        raise ValueError("Price cannot be negative")

    return InvestmentAsset(name, quantity, price)

# ❌ Bad: No validation
def parse_note(note_text: str) -> InvestmentAsset:
    name, quantity, price = parse_text(note_text)
    return InvestmentAsset(name, quantity, price)
```

---

## Dependency Security

### Third-Party Dependencies

**Current Dependencies:**
- `gkeepapi>=0.13.10` - Google Keep API (unofficial)
- `streamlit>=1.31.0` - Web framework
- `pandas>=2.2.0` - Data processing
- `plotly>=5.18.0` - Visualization
- `requests>=2.31.0` - HTTP client

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
pip install --upgrade gkeepapi

# Update all dependencies
pip install --upgrade -r requirements.txt
```

### gkeepapi Security Considerations

**Risks:**
- Unofficial API (not maintained by Google)
- May break if Google changes API
- Potential security vulnerabilities in third-party code

**Mitigations:**
- Monitor gkeepapi for security updates
- Consider official Google Keep API when available
- Implement fallback mechanisms for API failures
- Limit data stored in Google Keep (read-only where possible)

---

## Access Control

### Application Access

**Current Deployment:**
- Local deployment via Streamlit
- No authentication at application level
- Access restricted by deployment method

**Recommended Security Practices:**
1. **Deploy behind VPN:** Use Tailscale Funnel or SSH tunneling
2. **Network Isolation:** Deploy on private network
3. **Firewall Rules:** Restrict inbound/outbound traffic

**Deployment Options:**
```bash
# Option 1: Tailscale Funnel (Recommended for personal use)
tailscale funnel 8501

# Option 2: SSH Tunneling
ssh -L 8501:localhost:8501 user@remote-server

# Option 3: VPN (Corporate environment)
# Deploy on internal network behind VPN
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
```

---

## Error Handling & Information Disclosure

### Secure Error Messages

Never expose sensitive information in error messages:

```python
# ✅ Good: Generic error messages
def fetch_investment_data(label: str):
    try:
        notes = keep.find(labels=[label])
        return notes
    except gkeepapi.APIException:
        st.error("Failed to fetch data from Google Keep. Please try again later.")
        # No stack traces or API details exposed

# ❌ Bad: Detailed error messages
def fetch_investment_data(label: str):
    try:
        notes = keep.find(labels=[label])
        return notes
    except Exception as e:
        st.error(f"Error: {e}")  # May reveal internal structure
        import traceback
        st.error(traceback.format_exc())  # Exposes stack trace
```

### Debug Mode

**Never enable debug mode in production:**

```python
# ❌ Bad: Debug mode enabled
DEBUG = True  # Exposes sensitive information

# ✅ Good: Debug mode disabled in production
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## Session Management

### Streamlit Session Security

**Current Implementation:**
- Streamlit manages sessions automatically
- Session state stored in browser (no server-side storage)
- No custom session management needed

**Best Practices:**
- Don't store sensitive data in session state
- Use `st.session_state` for UI state only
- Clear session state on logout

```python
# ✅ Good: Non-sensitive session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ❌ Bad: Storing credentials in session state
st.session_state.password = password  # Dangerous!
```

---

## Backup & Recovery

### Google Keep Backup

**Data Location:**
- Investment data stored in Google Keep
- Google Keep provides automatic backups
- No local backup required for investment data

**Recommended Backup Strategy:**
1. **Google Keep Native Backup:** Export notes regularly
2. **Manual Export:** Periodically export investment notes as JSON/text
3. **Version Control:** Use Git for code and configuration files (excluding `.env`)

**Export Procedure:**
```bash
# Export investment notes manually (via gkeepapi)
python scripts/export_investment_notes.py --format json --output backup.json
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
- [ ] No credentials in code
- [ ] `.env` file in `.gitignore`
- [ ] Input validation on all user inputs
- [ ] No sensitive data in logs
- [ ] Dependencies up-to-date
- [ ] HTTPS enabled for all external calls
- [ ] File permissions set correctly
- [ ] Debug mode disabled in production

---

## Incident Response

### Security Incident Types

1. **Credential Exposure:** `.env` file compromised
2. **Data Breach:** Unauthorized access to investment data
3. **Malicious Code:** Third-party dependency vulnerability
4. **Denial of Service:** Application unavailable due to attack

### Incident Response Plan

**Immediate Actions:**
1. **Isolate:** Disconnect application from network
2. **Assess:** Determine scope and impact
3. **Contain:** Change credentials, revoke access
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
- User controls data via Google Keep
- No data processing beyond what user authorizes

**Best Practices:**
- Minimize data collection
- Provide data export options
- Allow data deletion

### Financial Data

**SEC/FINRA Considerations:**
- Not providing financial advice
- Data is for informational purposes only
- No automated trading or recommendations

**Disclaimer:**
```python
# Include disclaimer in UI
st.warning("""
**Disclaimer:** This application is for informational purposes only.
It does not provide financial advice or recommendations.
Please consult a qualified financial advisor for investment decisions.
""")
```

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial security documentation |
