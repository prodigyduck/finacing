"""
Unit tests for ports_validate.py
"""
import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path to import scripts module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.ports_validate import check_duplicates, load_ports, load_schema, validate_schema


class TestValidateSchema:
    """Test schema validation functionality."""

    def test_schema_valid(self):
        """Test that valid ports.json passes schema validation."""
        valid_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "frontend",
                    "name": "Frontend",
                    "path": "frontend",
                    "port": 5173,
                    "fallbacks": [5174, 5175],
                    "env_var": "VITE_PORT",
                    "owner": {"team": "frontend", "contact": "test@example.com"},
                    "status": "active"
                }
            ]
        }

        schema = load_schema(Path(__file__).parent.parent.parent / "ports.schema.json")
        errors = validate_schema(valid_data, schema)
        assert errors == []

    def test_schema_missing_required_field(self):
        """Test that missing required fields are detected."""
        invalid_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "frontend",
                    "name": "Frontend",
                    "path": "frontend",
                    # Missing 'port' field
                    "env_var": "VITE_PORT",
                    "owner": {"team": "frontend"},
                    "status": "active"
                }
            ]
        }

        schema = load_schema(Path(__file__).parent.parent.parent / "ports.schema.json")
        errors = validate_schema(invalid_data, schema)
        assert any("missing required field" in error for error in errors)

    def test_schema_invalid_port_range(self):
        """Test that ports outside valid range are detected."""
        invalid_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "frontend",
                    "name": "Frontend",
                    "path": "frontend",
                    "port": 70000,  # Invalid port
                    "env_var": "VITE_PORT",
                    "owner": {"team": "frontend"},
                    "status": "active"
                }
            ]
        }

        schema = load_schema(Path(__file__).parent.parent.parent / "ports.schema.json")
        errors = validate_schema(invalid_data, schema)
        assert any("invalid port" in error for error in errors)

    def test_schema_invalid_status(self):
        """Test that invalid status values are detected."""
        invalid_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "frontend",
                    "name": "Frontend",
                    "path": "frontend",
                    "port": 5173,
                    "env_var": "VITE_PORT",
                    "owner": {"team": "frontend"},
                    "status": "invalid_status"  # Invalid status
                }
            ]
        }

        schema = load_schema(Path(__file__).parent.parent.parent / "ports.schema.json")
        errors = validate_schema(invalid_data, schema)
        assert any("invalid status" in error for error in errors)

    def test_schema_missing_owner_team(self):
        """Test that missing team in owner is detected."""
        invalid_data = {
            "schema_version": "1.0",
            "services": [
                {
                    "id": "frontend",
                    "name": "Frontend",
                    "path": "frontend",
                    "port": 5173,
                    "env_var": "VITE_PORT",
                    "owner": {"contact": "test@example.com"},  # Missing team
                    "status": "active"
                }
            ]
        }

        schema = load_schema(Path(__file__).parent.parent.parent / "ports.schema.json")
        errors = validate_schema(invalid_data, schema)
        assert any("missing required field: team" in error for error in errors)


class TestCheckDuplicates:
    """Test duplicate port detection."""

    def test_no_duplicates(self):
        """Test that no duplicates returns empty list."""
        data = {
            "services": [
                {
                    "id": "frontend",
                    "port": 5173,
                    "fallbacks": [5174, 5175],
                    "status": "active"
                },
                {
                    "id": "backend",
                    "port": 8000,
                    "status": "active"
                }
            ]
        }

        errors = check_duplicates(data)
        assert errors == []

    def test_duplicate_primary_ports(self):
        """Test that duplicate primary ports are detected."""
        data = {
            "services": [
                {
                    "id": "frontend",
                    "port": 5173,
                    "status": "active"
                },
                {
                    "id": "other-service",
                    "port": 5173,  # Duplicate
                    "status": "active"
                }
            ]
        }

        errors = check_duplicates(data)
        assert len(errors) == 1
        assert "port 5173 conflict" in errors[0]

    def test_duplicate_fallback_with_primary(self):
        """Test that fallback conflicts with primary port are detected."""
        data = {
            "services": [
                {
                    "id": "frontend",
                    "port": 5173,
                    "fallbacks": [8000],
                    "status": "active"
                },
                {
                    "id": "backend",
                    "port": 8000,
                    "status": "active"
                }
            ]
        }

        errors = check_duplicates(data)
        assert len(errors) == 1
        assert "port 8000 conflict" in errors[0]

    def test_retired_services_ignored(self):
        """Test that retired services are not checked for duplicates."""
        data = {
            "services": [
                {
                    "id": "frontend",
                    "port": 5173,
                    "status": "active"
                },
                {
                    "id": "old-service",
                    "port": 5173,
                    "status": "retired"
                }
            ]
        }

        errors = check_duplicates(data)
        assert errors == []

    def test_reserved_services_checked(self):
        """Test that reserved services ARE checked for duplicates."""
        data = {
            "services": [
                {
                    "id": "frontend",
                    "port": 5173,
                    "status": "active"
                },
                {
                    "id": "reserved-service",
                    "port": 5173,
                    "status": "reserved"
                }
            ]
        }

        errors = check_duplicates(data)
        assert len(errors) == 1
