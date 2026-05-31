from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.presentation.app import app
from tests.conftest import FakeObsidianParser


@pytest.fixture
def client(fake_parser: FakeObsidianParser):
    with patch("src.presentation.app.parser", fake_parser):
        with patch("src.presentation.app.analyze_use_case"):
            yield TestClient(app)


@pytest.fixture
def client_with_raw(fake_parser_with_raw: FakeObsidianParser):
    with patch("src.presentation.app.parser", fake_parser_with_raw):
        yield TestClient(app), fake_parser_with_raw


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestRootEndpoint:
    def test_root_returns_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "2.0.0"
        assert "Financing" in data["message"]


class TestHistoryEndpoint:
    def test_get_history_success(self, client, fake_parser):
        resp = client.get("/api/v1/history")
        assert resp.status_code == 200
        assert fake_parser.pull_called >= 1
        assert fake_parser.parse_called == 1

    def test_get_history_with_year(self, client, fake_parser):
        resp = client.get("/api/v1/history?year=2026")
        assert resp.status_code == 200

    def test_get_history_file_not_found(self, client):
        empty_parser = FakeObsidianParser(history=None)
        with patch("src.presentation.app.parser", empty_parser):
            resp = client.get("/api/v1/history")
        assert resp.status_code == 404

    def test_history_response_structure(self, client, fake_parser):
        from src.application.use_cases.analyze_history import AnalyzeHistory

        with patch("src.presentation.app.analyze_use_case", AnalyzeHistory()):
            resp = client.get("/api/v1/history")
        data = resp.json()
        assert "records" in data
        assert "latest" in data
        assert "earliest" in data
        assert "total_change" in data
        assert "return_rate" in data
        assert "record_count" in data
        assert "projections" in data

    def test_history_records_count(self, client, fake_parser):
        from src.application.use_cases.analyze_history import AnalyzeHistory

        with patch("src.presentation.app.analyze_use_case", AnalyzeHistory()):
            resp = client.get("/api/v1/history")
        data = resp.json()
        assert data["record_count"] == 6
        assert len(data["records"]) == 6

    def test_history_has_projections(self, client, fake_parser):
        from src.application.use_cases.analyze_history import AnalyzeHistory

        with patch("src.presentation.app.analyze_use_case", AnalyzeHistory()):
            resp = client.get("/api/v1/history")
        data = resp.json()
        assert len(data["projections"]) == 3
        assert all("months" in p for p in data["projections"])
        assert all("date" in p for p in data["projections"])
        assert all("amount" in p for p in data["projections"])


class TestSyncEndpoint:
    def test_sync_success(self, client, fake_parser):
        resp = client.post("/api/v1/sync")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "synced"

    def test_sync_calls_pull(self, client, fake_parser):
        client.post("/api/v1/sync")
        assert fake_parser.pull_called == 1


class TestRawDataEndpoints:
    def test_get_raw_data(self, client_with_raw):
        client, parser = client_with_raw
        resp = client.get("/api/v1/raw-data")
        assert resp.status_code == 200
        data = resp.json()
        assert data["year"] == 2026
        assert len(data["records"]) == 2

    def test_get_raw_data_not_found(self, client):
        empty_parser = FakeObsidianParser(raw_data=None)
        with patch("src.presentation.app.parser", empty_parser):
            resp = client.get("/api/v1/raw-data")
        assert resp.status_code == 404

    def test_put_raw_data(self, client_with_raw):
        client, parser = client_with_raw
        payload = {
            "year": 2026,
            "frontmatter": "---\ntags:\n---\n",
            "records": [
                {"month": 1, "day": 13, "amount": "4.40"},
                {"month": 1, "day": 20, "amount": "4.55"},
            ],
        }
        resp = client.put(
            "/api/v1/raw-data?commit=true",
            json=payload,
            headers={"x-api-key": "local-dev-only"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "saved"
        assert data["record_count"] == 2
        assert parser.write_raw_called == 1
        assert parser.commit_called == 1

    def test_put_raw_data_without_commit(self, client_with_raw):
        client, parser = client_with_raw
        payload = {
            "year": 2026,
            "frontmatter": "",
            "records": [{"month": 1, "day": 13, "amount": "4.40"}],
        }
        resp = client.put(
            "/api/v1/raw-data?commit=false",
            json=payload,
            headers={"x-api-key": "local-dev-only"},
        )
        assert resp.status_code == 200
        assert parser.commit_called == 0

    def test_put_raw_data_invalid_month(self, client_with_raw):
        client, _ = client_with_raw
        payload = {
            "year": 2026,
            "frontmatter": "",
            "records": [{"month": 13, "day": 1, "amount": "4.40"}],
        }
        resp = client.put("/api/v1/raw-data", json=payload)
        assert resp.status_code == 422

    def test_put_raw_data_invalid_amount(self, client_with_raw):
        client, _ = client_with_raw
        payload = {
            "year": 2026,
            "frontmatter": "",
            "records": [{"month": 1, "day": 13, "amount": "not_a_number"}],
        }
        resp = client.put("/api/v1/raw-data", json=payload)
        assert resp.status_code == 422
