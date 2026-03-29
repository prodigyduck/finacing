"""
Input Validation

Validation utilities for user inputs across the application.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_label(label: str) -> bool:
    """
    Validate Google Keep label.

    Args:
        label: Label to validate

    Returns:
        True if label is valid, False otherwise
    """
    if not label or not label.strip():
        return False

    if len(label) > 100:
        return False

    if not label.isprintable():
        return False

    return True


def sanitize_label(label: str) -> str:
    """
    Sanitize label for safe use in API calls.

    Args:
        label: Label to sanitize

    Returns:
        Sanitized label string
    """
    if not label:
        return ""

    return label.strip()[:100]


def validate_password(password: Optional[str]) -> bool:
    """
    Validate password presence.

    Args:
        password: Password to validate

    Returns:
        True if password is provided, False otherwise
    """
    return password is not None and len(password) > 0
