"""Contract tests for /api/v1/history accounts field"""
import pytest
from fastapi.testclient import TestClient
from src.presentation.app import app


client = TestClient(app)


def test_history_response_contains_accounts_field():
    """/api/v1/history 응답에 accounts 필드 포함"""
    # This test will fail initially - Red phase
    response = client.get("/api/v1/history?year=2026")
    assert response.status_code == 200

    data = response.json()
    assert "accounts" in data
    assert isinstance(data["accounts"], list)


def test_history_account_has_required_fields():
    """accounts 배열의 각 항목에 필수 필드 포함"""
    response = client.get("/api/v1/history?year=2026")
    assert response.status_code == 200

    data = response.json()
    if len(data["accounts"]) > 0:
        account = data["accounts"][0]
        assert "name" in account
        assert "latest_amount" in account
        assert "allocation" in account
        assert "holdings" in account


def test_history_response_contains_comparison_field():
    """/api/v1/history 응답에 comparison 필드 포함"""
    response = client.get("/api/v1/history?year=2026")
    assert response.status_code == 200

    data = response.json()
    assert "comparison" in data
    assert "best_performer" in data["comparison"]
    assert "worst_performer" in data["comparison"]


def test_history_backward_compatibility():
    """기존 필드 유지 (호환성)"""
    response = client.get("/api/v1/history?year=2026")
    assert response.status_code == 200

    data = response.json()
    # 기존 필드들
    assert "records" in data
    assert "latest" in data
    assert "earliest" in data
    assert "total_change" in data
    assert "return_rate" in data
    assert "projections" in data
