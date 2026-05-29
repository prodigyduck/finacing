import logging
import os
import sys
from logging import Formatter
from pathlib import Path
from typing import Optional


def configure_logging(log_file: Optional[str] = None):
    """Configure logging with optional file output.

    Args:
        log_file: Optional path to log file. If not provided, uses FINANCING_LOG_FILE env var,
                  or defaults to .sisyphus/logs/agent-fallback.log
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Simple formatter with timestamp
    fmt = Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # Stream handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    # File handler (optional)
    if log_file is None:
        log_file = os.environ.get("FINANCING_LOG_FILE", ".sisyphus/logs/agent-fallback.log")

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path)
        fh.setFormatter(fmt)
        root.addHandler(fh)

    # Simple formatter with timestamp
    fmt = Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # Stream handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    # File handler (optional)
    if log_file is None:
        log_file = os.environ.get("FINANCING_LOG_FILE", ".sisyphus/logs/agent-fallback.log")

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path)
        fh.setFormatter(fmt)
        root.addHandler(fh)
