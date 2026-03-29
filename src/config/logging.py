import logging
import sys
from logging import Formatter
from pathlib import Path


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Simple formatter with timestamp
    fmt = Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # Stream handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    # File handler
    logs_dir = Path(".sisyphus/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(logs_dir / "agent-fallback.log")
    fh.setFormatter(fmt)
    root.addHandler(fh)
