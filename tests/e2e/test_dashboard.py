import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5180"


class TestDashboard:
    def test_page_loads(self, page: Page):
        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
        expect(page.locator("h1")).to_contain_text("Portfolio")

    def test_api_proxy_works(self, page: Page):
        api_response = page.request.get(f"{BASE_URL}/api/v1/history")
        assert api_response.ok
        data = api_response.json()
        assert data["record_count"] > 0
        assert data["latest"] is not None

    def test_history_data_renders(self, page: Page):
        page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
        page.click("text=Refresh")
        page.wait_for_timeout(3000)
        expect(page.locator(".metric-value").first).to_be_visible()
        expect(page.locator("table")).to_be_visible()
