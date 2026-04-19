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
    } catch (e: any) {
      error.value = e?.response?.data?.detail || e?.message || 'Failed to fetch history'
    } finally {
      loading.value = false
    }
  }

  return { history, loading, error, fetchHistory }
})
