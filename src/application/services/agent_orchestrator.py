import time
import logging
from typing import Callable, Any, Dict, List, Optional, Union

from prometheus_client import Counter, Histogram, REGISTRY
from prometheus_client.core import CollectorRegistry

# Create or reuse global metrics to avoid duplicate registration across tests
def _get_or_create_counter(name, documentation, labelnames):
    try:
        return Counter(name, documentation, labelnames)
    except ValueError:
        # Already registered - fetch existing collector from registry
        coll = REGISTRY._names_to_collectors.get(name)
        if isinstance(coll, Counter):
            return coll
        # Fallback: create a new counter in a private registry
        return Counter(name, documentation, labelnames, registry=CollectorRegistry())

def _get_or_create_histogram(name, documentation, labelnames):
    try:
        return Histogram(name, documentation, labelnames)
    except ValueError:
        coll = REGISTRY._names_to_collectors.get(name)
        if isinstance(coll, Histogram):
            return coll
        return Histogram(name, documentation, labelnames, registry=CollectorRegistry())


class AgentOrchestrator:
    """Orchestrator that attempts a chain of agents with circuit-breaking and metrics."""

    def __init__(
        self,
        chain: List[str],
        logger: Optional[logging.Logger] = None,
        metrics_registry=None,
        timeout_ms: int = 2000,
        cooldown_ms: int = 60000,
        failure_threshold: int = 3,
    ):
        self.chain = chain
        self.logger = logger or logging.getLogger(__name__)
        self.timeout_ms = timeout_ms
        self.cooldown_ms = cooldown_ms
        self.failure_threshold = failure_threshold

        # State per agent
        self._failures: Dict[str, int] = {a: 0 for a in chain}
        self._circuit_open_until: Dict[str, float] = {a: 0.0 for a in chain}

        # Metrics (reuse if already registered)
        self.agent_attempts = _get_or_create_counter(
            "agent_attempts_total", "Attempts made to agents", ["agent", "outcome"]
        )
        self.agent_circuit_open = _get_or_create_counter(
            "agent_circuit_open_total", "Times agent circuit opened", ["agent"]
        )
        self.agent_latency = _get_or_create_histogram(
            "agent_latency_seconds", "Latency of agent calls", ["agent"]
        )

    def _is_circuit_open(self, agent: str) -> bool:
        until = self._circuit_open_until.get(agent, 0)
        return time.time() < until

    def _record_failure(self, agent: str):
        self._failures[agent] += 1
        if self._failures[agent] >= self.failure_threshold:
            self._circuit_open_until[agent] = time.time() + (self.cooldown_ms / 1000.0)
            self.agent_circuit_open.labels(agent=agent).inc()
            self.logger.warning(f"Circuit opened for agent {agent}")

    def _record_success(self, agent: str):
        self._failures[agent] = 0

    def execute_with_fallback(self, callables: Union[Dict[str, Callable[[], Any]], Callable[[], Any]]) -> Any:
        """
        Either:
        - callables: mapping of agent name -> zero-arg callable
        - or a single callable: called directly (backward compatible)

        Returns result of first successful agent or raises aggregated error
        """
        # Backward compatibility: single callable provided
        if callable(callables):
            try:
                return callables()
            except Exception as e:
                # Record a generic attempt
                self.agent_attempts.labels(agent="single", outcome=type(e).__name__).inc()
                raise
        errors = {}

        for agent in self.chain:
            if agent not in callables:
                self.logger.debug(f"No callable provided for agent {agent}, skipping")
                continue

            if self._is_circuit_open(agent):
                self.agent_attempts.labels(agent=agent, outcome="skipped").inc()
                continue

            fn = callables[agent]

            start = time.time()
            try:
                result = fn()
                duration = time.time() - start
                self.agent_latency.labels(agent=agent).observe(duration)
                self.agent_attempts.labels(agent=agent, outcome="success").inc()
                self._record_success(agent)
                return result
            except Exception as e:
                duration = time.time() - start
                self.agent_latency.labels(agent=agent).observe(duration)
                self.agent_attempts.labels(agent=agent, outcome=type(e).__name__).inc()
                errors[agent] = str(e)
                self._record_failure(agent)
                self.logger.exception(f"Agent {agent} failed: {e}")
                continue

        # All agents exhausted
        raise RuntimeError(f"All agents failed: {errors}")
