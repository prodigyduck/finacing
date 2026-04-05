#!/usr/bin/env python3
"""
Repository factory for agent-specific adapters.

Creates repository instances configured for specific AI agents
(Sisyphus, Prometheus, Atlas).
"""

import logging
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass

from src.infrastructure.repositories.gkeep_repository import GKeepRepository
from src.config.agent_config import load_config


logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for an AI agent."""
    name: str
    api_key: Optional[str] = None
    api_endpoint: Optional[str] = None
    timeout_ms: int = 30000
    max_retries: int = 3


class RepositoryFactory:
    """
    Factory for creating agent-specific repository adapters.

    Each agent (Sisyphus, Prometheus, Atlas) gets its own
    repository instance configured with agent-specific settings.
    """

    def __init__(self, base_repository: GKeepRepository):
        """
        Initialize factory with base repository.

        Args:
            base_repository: Base GKeepRepository instance for Google Keep access
        """
        self.base_repository = base_repository
        self.config = load_config()
        self.agent_configs = self._load_agent_configs()

    def _load_agent_configs(self) -> Dict[str, AgentConfig]:
        """Load agent configurations from environment variables."""
        return {
            'sisyphus': AgentConfig(
                name='sisyphus',
                api_key=self._get_env('SISYPHUS_API_KEY'),
                api_endpoint=self._get_env('SISYPHUS_API_ENDPOINT'),
                timeout_ms=self.config.timeout_ms,
            ),
            'prometheus': AgentConfig(
                name='prometheus',
                api_key=self._get_env('PROMETHEUS_API_KEY'),
                api_endpoint=self._get_env('PROMETHEUS_API_ENDPOINT'),
                timeout_ms=self.config.timeout_ms,
            ),
            'atlas': AgentConfig(
                name='atlas',
                api_key=self._get_env('ATLAS_API_KEY'),
                api_endpoint=self._get_env('ATLAS_API_ENDPOINT'),
                timeout_ms=self.config.timeout_ms,
            ),
        }

    def _get_env(self, var_name: str) -> Optional[str]:
        """Get environment variable value safely."""
        import os
        return os.environ.get(var_name)

    def create_adapter(self, agent_name: str) -> Callable[[str], list[Any]]:
        """
        Create an adapter callable for the specified agent.

        Args:
            agent_name: Name of the agent (sisyphus, prometheus, atlas)

        Returns:
            Callable that takes a label and returns a list of assets

        Raises:
            ValueError: If agent_name is not recognized
        """
        if agent_name not in self.agent_configs:
            raise ValueError(f"Unknown agent: {agent_name}. Available: {list(self.agent_configs.keys())}")

        agent_config = self.agent_configs[agent_name]

        # For now, all agents use the base GKeepRepository
        # In the future, each agent can have its own implementation
        def adapter(label: str) -> list[Any]:
            """
            Adapter callable that fetches data using the agent.

            Args:
                label: Google Keep label to filter notes

            Returns:
                List of assets from the repository

            Note:
                Currently all agents use GKeepRepository.
                Future implementations can have agent-specific logic.
            """
            logger.info(f"Fetching data with agent: {agent_name}, label: {label}")

            try:
                # Use base repository to fetch notes
                notes = self.base_repository.fetch_notes(label=label)

                # Process notes based on agent configuration
                # (agent-specific processing can be added here)
                processed = self._process_notes(notes, agent_config)

                return processed
            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {e}")
                raise

        return adapter

    def _process_notes(self, notes: list[Any], config: AgentConfig) -> list[Any]:
        """
        Process notes with agent-specific logic.

        Args:
            notes: Raw notes from repository
            config: Agent configuration

        Returns:
            Processed notes/assets

        Note:
            This is where agent-specific processing logic would go.
            For now, returns notes as-is.
        """
        # Agent-specific processing can be added here
        # Examples:
        # - Sisyphus: use advanced parsing
        # - Prometheus: add metadata enrichment
        # - Atlas: apply filtering/transformations

        return notes

    def create_all_adapters(self) -> Dict[str, Callable[[str], list[Any]]]:
        """
        Create adapters for all configured agents.

        Returns:
            Dict mapping agent names to adapter callables
        """
        return {
            agent_name: self.create_adapter(agent_name)
            for agent_name in self.agent_configs.keys()
        }

    def get_available_agents(self) -> list[str]:
        """
        Get list of available agent names.

        Returns:
            List of agent names
        """
        return list(self.agent_configs.keys())
