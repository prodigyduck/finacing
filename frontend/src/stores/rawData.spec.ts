import { describe, it, expect, vi, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useRawDataStore } from "./rawData";
import * as api from "@/api";

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

describe("useRawDataStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("초기 상태는 비어있어야 한다", () => {
    const store = useRawDataStore();
    expect(store.records).toEqual([]);
    expect(store.frontmatter).toBe("");
    expect(store.loading).toBe(false);
    expect(store.saving).toBe(false);
    expect(store.error).toBeNull();
  });

  it("fetchRawData 성공 시 records와 frontmatter를 설정한다", async () => {
    vi.mocked(api.fetchRawData).mockResolvedValue(mockRawDataResponse);
    const store = useRawDataStore();

    await store.fetchRawData(2026);

    expect(api.fetchRawData).toHaveBeenCalledWith(2026);
    expect(store.records).toEqual(mockRawDataResponse.records);
    expect(store.frontmatter).toBe(mockRawDataResponse.frontmatter);
    expect(store.year).toBe(2026);
    expect(store.loading).toBe(false);
  });

  it("fetchRawData 실패 시 error를 설정한다", async () => {
    vi.mocked(api.fetchRawData).mockRejectedValue(new Error("File not found"));
    const store = useRawDataStore();

    await store.fetchRawData(2026);

    expect(store.error).toBe("File not found");
    expect(store.loading).toBe(false);
  });

  it("fetchRawData 중에 loading=true다", async () => {
    let resolvePromise!: (v: api.RawDataResponse) => void;
    vi.mocked(api.fetchRawData).mockImplementation(
      () => new Promise((resolve) => (resolvePromise = resolve))
    );
    const store = useRawDataStore();

    const promise = store.fetchRawData(2026);
    expect(store.loading).toBe(true);

    resolvePromise(mockRawDataResponse);
    await promise;
    expect(store.loading).toBe(false);
  });

  it("saveRawData 성공 시 saving=false, error=null", async () => {
    vi.mocked(api.saveRawData).mockResolvedValue({
      status: "saved",
      record_count: 3,
      commit: "abc1234",
    });
    const store = useRawDataStore();
    store.records = mockRawDataResponse.records;
    store.frontmatter = mockRawDataResponse.frontmatter;
    store.year = 2026;

    await store.saveRawData();

    expect(api.saveRawData).toHaveBeenCalledWith(
      2026,
      mockRawDataResponse.frontmatter,
      mockRawDataResponse.records
    );
    expect(store.saving).toBe(false);
    expect(store.error).toBeNull();
  });

  it("saveRawData 실패 시 error를 설정한다", async () => {
    vi.mocked(api.saveRawData).mockRejectedValue(new Error("Validation error"));
    const store = useRawDataStore();
    store.records = mockRawDataResponse.records;
    store.frontmatter = mockRawDataResponse.frontmatter;
    store.year = 2026;

    await store.saveRawData();

    expect(store.error).toBe("Validation error");
    expect(store.saving).toBe(false);
  });

  it("syncAndFetch는 sync 후 fetchRawData를 호출한다", async () => {
    vi.mocked(api.syncVault).mockResolvedValue({ status: "synced", detail: "ok" });
    vi.mocked(api.fetchRawData).mockResolvedValue(mockRawDataResponse);
    const store = useRawDataStore();
    store.year = 2026;

    await store.syncAndFetch();

    expect(api.syncVault).toHaveBeenCalled();
    expect(api.fetchRawData).toHaveBeenCalledWith(2026);
    expect(store.records).toEqual(mockRawDataResponse.records);
  });
});
