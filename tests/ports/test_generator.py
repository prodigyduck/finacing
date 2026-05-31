"""
Unit tests for ports_generate_env.py
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path to import scripts module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.ports_generate_env import (
    find_available_port,
    find_service,
    is_port_available,
    load_ports,
    parse_ephemeral_range,
    write_env_file,
)


class TestLoadPorts:
    """Test ports.json loading."""

    def test_load_valid_ports(self, tmp_path):
        """Test loading valid ports.json file."""
        ports_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "test-service",
                    "name": "Test Service",
                    "path": ".",
                    "port": 9999,
                    "env_var": "TEST_PORT",
                    "owner": {"team": "test"},
                    "status": "active"
                }
            ]
        }

        ports_file = tmp_path / "ports.json"
        with open(ports_file, 'w') as f:
            json.dump(ports_data, f)

        loaded = load_ports(ports_file)
        assert loaded == ports_data

    def test_load_missing_file(self):
        """Test that missing file causes exit."""
        with pytest.raises(SystemExit) as exc_info:
            load_ports(Path("/nonexistent/ports.json"))
        assert exc_info.value.code == 1


class TestFindService:
    """Test service lookup functionality."""

    def test_find_by_id(self):
        """Test finding service by ID."""
        ports = {
            "services": [
                {"id": "frontend", "name": "Frontend", "path": "frontend", "port": 5173, "env_var": "VITE_PORT", "owner": {"team": "frontend"}, "status": "active"},
                {"id": "backend", "name": "Backend", "path": ".", "port": 8000, "env_var": "BACKEND_PORT", "owner": {"team": "backend"}, "status": "active"}
            ]
        }

        service = find_service(ports, service_id="frontend")
        assert service is not None
        assert service["id"] == "frontend"

    def test_find_by_path(self):
        """Test finding service by path."""
        ports = {
            "services": [
                {"id": "frontend", "name": "Frontend", "path": "frontend", "port": 5173, "env_var": "VITE_PORT", "owner": {"team": "frontend"}, "status": "active"}
            ]
        }

        service = find_service(ports, service_path="frontend")
        assert service is not None
        assert service["path"] == "frontend"

    def test_not_found(self):
        """Test when service is not found."""
        ports = {
            "services": [
                {"id": "frontend", "name": "Frontend", "path": "frontend", "port": 5173, "env_var": "VITE_PORT", "owner": {"team": "frontend"}, "status": "active"}
            ]
        }

        service = find_service(ports, service_id="nonexistent")
        assert service is None


class TestIsPortAvailable:
    """Test port availability checking."""

    def test_high_port_available(self):
        """Test that a high port number is available."""
        # Use a high port that's likely free
        assert is_port_available(54321)

    def test_low_port_unavailable(self):
        """Test that low privileged ports may be unavailable."""
        # Port 22 (SSH) is likely unavailable
        result = is_port_available(22)
        # We don't assert False because it might vary, but it shouldn't raise


class TestFindAvailablePort:
    """Test port finding with fallbacks."""

    def test_primary_available(self, tmp_path):
        """Test using primary port when available."""
        # Use a high port that's likely free
        primary_port = 54321
        fallbacks = [54322, 54323]

        port, source = find_available_port(
            primary_port,
            fallbacks,
            allow_fallback=True,
            ephemeral_range=(30000, 31999)
        )

        assert port == primary_port
        assert source == 'primary'

    def test_fallback_used(self):
        """Test using fallback when primary is in use."""
        # Find a port that's likely in use
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 0))
        busy_port = s.getsockname()[1]

        try:
            # Make busy_port the primary
            primary_port = busy_port
            fallbacks = [54322, 54323]

            port, source = find_available_port(
                primary_port,
                fallbacks,
                allow_fallback=True,
                ephemeral_range=(30000, 31999)
            )

            assert port != primary_port
            assert source == 'fallback' or source == 'ephemeral'
        finally:
            s.close()


class TestWriteEnvFile:
    """Test .env file writing."""

    def test_write_env_file(self, tmp_path):
        """Test writing .env.local file."""
        output_path = tmp_path / ".env.local"

        write_env_file(output_path, "VITE_PORT", 5173)

        assert output_path.exists()

        with open(output_path) as f:
            content = f.read()

        expected_content = "# GENERATED FROM ports.json - DO NOT COMMIT\nVITE_PORT=5173\n"
        assert content == expected_content

    def test_write_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created."""
        output_path = tmp_path / "subdir" / ".env.local"

        write_env_file(output_path, "VITE_PORT", 5173)

        assert output_path.exists()


class TestParseEphemeralRange:
    """Test ephemeral range parsing."""

    def test_valid_range(self):
        """Test parsing a valid range."""
        start, end = parse_ephemeral_range("30000-31999")
        assert start == 30000
        assert end == 31999

    def test_invalid_format(self):
        """Test that invalid format causes exit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_ephemeral_range("invalid")
        assert exc_info.value.code == 1

    def test_invalid_ports(self):
        """Test that invalid ports cause exit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_ephemeral_range("100-200")  # Too low
        assert exc_info.value.code == 1

    def test_inverted_range(self):
        """Test that inverted range causes exit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_ephemeral_range("31999-30000")  # Start > end
        assert exc_info.value.code == 1
