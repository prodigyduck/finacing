import { describe, it, expect, vi, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useHistoryStore } from "./history";
import * as api from "@/api";

vi.mock("@/api");

const mockHistoryResponse: api.HistoryResponse = {
  records: [
    { date: "2026-01-13", amount: 4.4 },
    { date: "2026-01-20", amount: 4.5 },
    { date: "2026-02-01", amount: 4.6 },
  ],
  latest: { date: "2026-02-01", amount: 4.6 },
  earliest: { date: "2026-01-13", amount: 4.4 },
  total_change: 0.2,
  return_rate: 4.55,
  record_count: 3,
  projections: [
    { months: 3, date: "2026-05-01", amount: 4.8 },
    { months: 6, date: "2026-08-01", amount: 5.0 },
    { months: 12, date: "2027-02-01", amount: 5.4 },
  ],
};

describe("useHistoryStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("초기 상태는 비어있어야 한다", () => {
    const store = useHistoryStore();
    expect(store.history).toBeNull();
    expect(store.loading).toBe(false);
    expect(store.syncing).toBe(false);
    expect(store.error).toBeNull();
  });

  it("fetchHistory 성공 시 history를 설정한다", async () => {
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const store = useHistoryStore();

    await store.fetchHistory(2026);

    expect(api.fetchHistory).toHaveBeenCalledWith(2026);
    expect(store.history).toEqual(mockHistoryResponse);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it("fetchHistory 실패 시 error를 설정한다", async () => {
    vi.mocked(api.fetchHistory).mockRejectedValue(new Error("Network error"));
    const store = useHistoryStore();

    await store.fetchHistory(2026);

    expect(store.history).toBeNull();
    expect(store.error).toBe("Network error");
    expect(store.loading).toBe(false);
  });

  it("fetchHistory 중에 loading=true다", async () => {
    let resolvePromise!: (v: api.HistoryResponse) => void;
    vi.mocked(api.fetchHistory).mockImplementation(
      () => new Promise((resolve) => (resolvePromise = resolve))
    );
    const store = useHistoryStore();

    const promise = store.fetchHistory(2026);
    expect(store.loading).toBe(true);

    resolvePromise(mockHistoryResponse);
    await promise;
    expect(store.loading).toBe(false);
  });

  it("syncAndFetch는 sync 후 fetchHistory를 호출한다", async () => {
    vi.mocked(api.syncVault).mockResolvedValue({ status: "synced", detail: "ok" });
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const store = useHistoryStore();

    await store.syncAndFetch();

    expect(api.syncVault).toHaveBeenCalled();
    expect(api.fetchHistory).toHaveBeenCalled();
    expect(store.syncing).toBe(false);
  });

  it("syncAndFetch 실패해도 fetchHistory는 시도한다", async () => {
    vi.mocked(api.syncVault).mockRejectedValue(new Error("sync failed"));
    vi.mocked(api.fetchHistory).mockResolvedValue(mockHistoryResponse);
    const store = useHistoryStore();

    await store.syncAndFetch();

    expect(api.fetchHistory).toHaveBeenCalled();
    expect(store.history).toEqual(mockHistoryResponse);
  });
});
