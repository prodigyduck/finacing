"""E2E tests for account dashboard functionality"""
import { test, expect } from '@playwright/test';


test.describe('Account Dashboard E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5180');
  });

  test('displays account cards', async ({ page }) => {
    // 계좌 카드 표시 확인
    const accountCards = page.locator('.account-card');

    // 최소 하나의 계좌 카드가 있어야 함
    await expect(accountCards.first()).toBeVisible();
  });

  test('displays account name and amount', async ({ page }) => {
    // 계좌명과 금액 표시 확인
    const accountCard = page.locator('.account-card').first();

    await expect(accountCard).toContainText(/[A-Za-z가-힣]+/); // 계좌명
    await expect(accountCard).toContainText(/\d+\.?\d*억/); // 금액
  });

  test('displays holdings list', async ({ page }) => {
    // 보유 종목 리스트 표시 확인
    const holdings = page.locator('.holding-badge');

    // 계좌에 종목이 있는 경우 표시되어야 함
    const firstHolding = holdings.first();
    if (await firstHolding.isVisible()) {
      await expect(firstHolding).toContainText(/[A-Za-z0-9가-힣]+/);
    }
  });

  test('displays allocation percentage', async ({ page }) => {
    // 비중 퍼센트 표시 확인
    const accountCard = page.locator('.account-card').first();

    await expect(accountCard).toContainText(/\d+\.?\d*%/);
  });

  test('API returns accounts data', async ({ page }) => {
    // API 응답에 accounts 필드 확인 (네트워크 인터셉트)
    const apiResponse = await page.waitForResponse(
      response => response.url().includes('/api/v1/history') && response.status() === 200
    );

    const data = await apiResponse.json();
    expect(data).toHaveProperty('accounts');
    expect(Array.isArray(data.accounts)).toBe(true);
  });
});
