"""
Unit tests for repository_factory.py
"""
import sys
import pytest
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.infrastructure.repositories.repository_factory import (
    RepositoryFactory,
    AgentConfig,
)
from src.infrastructure.repositories.gkeep_repository import GKeepRepository


class TestAgentConfig:
    """Test AgentConfig dataclass."""

    def test_agent_config_creation(self):
        """Test creating an AgentConfig."""
        config = AgentConfig(
            name="test-agent",
            api_key="test-key",
            api_endpoint="https://api.example.com",
            timeout_ms=30000,
            max_retries=3,
        )

        assert config.name == "test-agent"
        assert config.api_key == "test-key"
        assert config.api_endpoint == "https://api.example.com"
        assert config.timeout_ms == 30000
        assert config.max_retries == 3

    def test_agent_config_defaults(self):
        """Test AgentConfig with default values."""
        config = AgentConfig(name="test-agent")

        assert config.name == "test-agent"
        assert config.api_key is None
        assert config.api_endpoint is None
        assert config.timeout_ms == 30000
        assert config.max_retries == 3


class TestRepositoryFactory:
    """Test RepositoryFactory functionality."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock GKeepRepository for testing."""
        class MockGKeepRepository:
            def fetch_notes(self, label: str):
                return [{"note": f"test-{label}"}]

        return MockGKeepRepository()

    def test_factory_initialization(self, mock_repository):
        """Test factory initialization with repository."""
        factory = RepositoryFactory(mock_repository)

        assert factory.base_repository == mock_repository
        assert len(factory.agent_configs) == 3
        assert 'sisyphus' in factory.agent_configs
        assert 'prometheus' in factory.agent_configs
        assert 'atlas' in factory.agent_configs

    def test_get_available_agents(self, mock_repository):
        """Test getting available agent names."""
        factory = RepositoryFactory(mock_repository)

        agents = factory.get_available_agents()

        assert len(agents) == 3
        assert 'sisyphus' in agents
        assert 'prometheus' in agents
        assert 'atlas' in agents

    def test_create_adapter_valid_agent(self, mock_repository):
        """Test creating adapter for valid agent."""
        factory = RepositoryFactory(mock_repository)

        adapter = factory.create_adapter('sisyphus')

        assert callable(adapter)

        # Test the adapter
        result = adapter('test-label')
        assert isinstance(result, list)

    def test_create_adapter_invalid_agent(self, mock_repository):
        """Test creating adapter for invalid agent raises ValueError."""
        factory = RepositoryFactory(mock_repository)

        with pytest.raises(ValueError) as exc_info:
            factory.create_adapter('unknown-agent')

        assert "Unknown agent" in str(exc_info.value)

    def test_create_all_adapters(self, mock_repository):
        """Test creating adapters for all agents."""
        factory = RepositoryFactory(mock_repository)

        adapters = factory.create_all_adapters()

        assert isinstance(adapters, dict)
        assert len(adapters) == 3
        assert 'sisyphus' in adapters
        assert 'prometheus' in adapters
        assert 'atlas' in adapters

        # All adapters should be callable
        for adapter in adapters.values():
            assert callable(adapter)

    def test_adapter_callable(self, mock_repository):
        """Test that adapter can be called with label."""
        factory = RepositoryFactory(mock_repository)

        sisyphus_adapter = factory.create_adapter('sisyphus')

        # Should not raise
        result = sisyphus_adapter('투자')

        assert isinstance(result, list)

    def test_multiple_adapters_callable(self, mock_repository):
        """Test that all created adapters are callable."""
        factory = RepositoryFactory(mock_repository)

        adapters = factory.create_all_adapters()

        for agent_name, adapter in adapters.items():
            result = adapter('투자')
            assert isinstance(result, list), f"Adapter for {agent_name} did not return list"

    def test_agent_configs_loaded(self, mock_repository):
        """Test that agent configs are loaded correctly."""
        factory = RepositoryFactory(mock_repository)

        sisyphus_config = factory.agent_configs['sisyphus']
        assert sisyphus_config.name == 'sisyphus'
        assert isinstance(sisyphus_config, AgentConfig)

        prometheus_config = factory.agent_configs['prometheus']
        assert prometheus_config.name == 'prometheus'
        assert isinstance(prometheus_config, AgentConfig)

        atlas_config = factory.agent_configs['atlas']
        assert atlas_config.name == 'atlas'
        assert isinstance(atlas_config, AgentConfig)
