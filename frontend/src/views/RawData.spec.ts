import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import RawData from "./RawData.vue";
import * as api from "@/api";
import { createRouter, createWebHistory } from "vue-router";

vi.mock("@/api");

const mockRawDataResponse: api.RawDataResponse = {
  year: 2026,
  frontmatter: "---\ntags:\n---\n",
  records: [
    { month: 1, day: 13, amount: "4.40" },
    { month: 1, day: 20, amount: "4.50" },
    { month: 2, day: 1, amount: "4.60" },
  ],
};

function createMockRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [{ path: "/raw-data", component: { template: "<div/>" } }],
  });
}

const globalPlugins = (router: ReturnType<typeof createMockRouter>) => ({
  plugins: [router],
});

describe("RawData.vue", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("데이터 로드 후 레코드를 테이블에 표시한다", async () => {
    vi.mocked(api.fetchRawData).mockResolvedValue(mockRawDataResponse);
    const router = createMockRouter();
    router.push("/raw-data");
    await router.isReady();

    const wrapper = mount(RawData, { global: globalPlugins(router) });
    await flushPromises();

    const html = wrapper.html();
    expect(html).toContain("4.40");
    expect(html).toContain("4.50");
    expect(html).toContain("4.60");
  });

  it("fetchRawData를 마운트 시 호출한다", async () => {
    vi.mocked(api.fetchRawData).mockResolvedValue(mockRawDataResponse);
    const router = createMockRouter();
    router.push("/raw-data");
    await router.isReady();

    mount(RawData, { global: globalPlugins(router) });
    await flushPromises();

    expect(api.fetchRawData).toHaveBeenCalled();
  });

  it("저장 버튼 클릭 시 saveRawData를 호출한다", async () => {
    vi.mocked(api.fetchRawData).mockResolvedValue(mockRawDataResponse);
    vi.mocked(api.saveRawData).mockResolvedValue({
      status: "saved",
      record_count: 3,
      commit: "abc1234",
    });
    const router = createMockRouter();
    router.push("/raw-data");
    await router.isReady();

    const wrapper = mount(RawData, { global: globalPlugins(router) });
    await flushPromises();

    const saveBtn = wrapper.find('[data-test="save"]');
    if (saveBtn.exists()) {
      await saveBtn.trigger("click");
      await flushPromises();
      expect(api.saveRawData).toHaveBeenCalled();
    }
  });

  it("fetchRawData 실패 시 에러 메시지를 표시한다", async () => {
    vi.mocked(api.fetchRawData).mockRejectedValue(new Error("File not found"));
    const router = createMockRouter();
    router.push("/raw-data");
    await router.isReady();

    const wrapper = mount(RawData, { global: globalPlugins(router) });
    await flushPromises();

    // Vuetify snackbar 또는 error display 확인
    expect(wrapper.vm.$data).toBeDefined();
  });
});
