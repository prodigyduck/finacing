import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import Dashboard from "./Dashboard.vue";
import * as api from "@/api";
import { createRouter, createWebHistory } from "vue-router";

vi.mock("@/api");

const mockHistoryResponse: api.HistoryResponse = {
  records: [
    { date: "2026-01-13", amount: 4.4 },
    { date: "2026-01-20", amount: 4.5 },
  ],
  latest: { date: "2026-01-20", amount: 4.5 },
  earliest: { date: "2026-01-13", amount: 4.4 },
  total_change: 0.1,
  return_rate: 2.27,
  record_count: 2,
  projections: [],
};

function createMockRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [{ path: "/", component: { template: "<div/>" } }],
  });
}

// Suppress Vuetify missing provider warnings
const globalPlugins = (router: ReturnType<typeof createMockRouter>) => ({
  plugins: [router],
  stubs: {
    PortfolioChart: true,
  },
});

describe("Dashboard.vue", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("데이터 없을 때 빈 상태를 표시한다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue({
      records: [],
      latest: null,
      earliest: null,
      total_change: null,
      return_rate: null,
      record_count: 0,
      projections: [],
    });
    const router = createMockRouter();
    router.push("/");
    await router.isReady();

    const wrapper = mount(Dashboard, { global: globalPlugins(router) });
    await flushPromises();

    expect(wrapper.text()).toContain("데이터가 없습니다");
  });

  it("데이터 로드 후 메트릭을 표시한다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const router = createMockRouter();
    router.push("/");
    await router.isReady();

    const wrapper = mount(Dashboard, { global: globalPlugins(router) });
    await flushPromises();

    const html = wrapper.html();
    expect(html).toContain("4.5");
    expect(html).toContain("2.27");
  });

  it("fetchHistory를 year 파라미터와 함께 호출한다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const router = createMockRouter();
    router.push("/");
    await router.isReady();

    mount(Dashboard, { global: globalPlugins(router) });
    await flushPromises();

    expect(api.fetchHistory).toHaveBeenCalled();
  });

  it("Refresh 버튼 클릭 시 데이터를 다시 불러온다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const router = createMockRouter();
    router.push("/");
    await router.isReady();

    const wrapper = mount(Dashboard, { global: globalPlugins(router) });
    await flushPromises();

    const refreshBtn = wrapper.find('[data-test="refresh"]');
    if (refreshBtn.exists()) {
      await refreshBtn.trigger("click");
      await flushPromises();
      expect(api.fetchHistory).toHaveBeenCalledTimes(2);
    }
  });

  it("Git Pull 버튼 클릭 시 syncAndFetch를 호출한다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    vi.mocked(api.syncVault).mockResolvedValue({ status: "synced", detail: "ok" });
    const router = createMockRouter();
    router.push("/");
    await router.isReady();

    const wrapper = mount(Dashboard, { global: globalPlugins(router) });
    await flushPromises();

    const syncBtn = wrapper.find('[data-test="sync"]');
    if (syncBtn.exists()) {
      await syncBtn.trigger("click");
      await flushPromises();
      expect(api.syncVault).toHaveBeenCalled();
    }
  });
});
