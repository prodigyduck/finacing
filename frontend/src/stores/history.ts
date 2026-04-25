import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchHistory as fetchHistoryApi, type HistoryResponse } from '../api'

export const useHistoryStore = defineStore('history', () => {
  const history = ref<HistoryResponse | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchHistory(year?: number) {
    loading.value = true
    error.value = null
    try {
      history.value = await fetchHistoryApi(year)
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } }; message?: string }
      error.value = err?.response?.data?.detail || err?.message || 'Failed to fetch history'
    } finally {
      loading.value = false
    }
  }

  return { history, loading, error, fetchHistory }
})
