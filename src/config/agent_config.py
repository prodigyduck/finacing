import os
from typing import List, Optional


def _parse_bool(v: Optional[str], default: bool = False) -> bool:
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")


class AgentConfig:
    def __init__(self):
        self.enabled = _parse_bool(os.getenv("AGENT_FALLBACK_ENABLED"), False)
        chain = os.getenv("AGENT_CHAIN", "sisyphus,prometheus,atlas")
        self.chain = [c.strip() for c in chain.split(",") if c.strip()]
        self.timeout_ms = int(os.getenv("AGENT_TIMEOUT_MS", "2000"))
        self.retry_attempts = int(os.getenv("AGENT_RETRY_ATTEMPTS", "3"))
        self.cooldown_ms = int(os.getenv("AGENT_COOLDOWN_MS", "60000"))
        self.failure_threshold = int(os.getenv("AGENT_FAILURE_THRESHOLD", "3"))


def load_config() -> AgentConfig:
    return AgentConfig()
