import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  fetchRawData as fetchRawDataApi,
  saveRawData as saveRawDataApi,
  syncVault as syncVaultApi,
  type RawRecord,
} from '../api'

export const useRawDataStore = defineStore('rawData', () => {
  const records = ref<RawRecord[]>([])
  const frontmatter = ref('')
  const year = ref(new Date().getFullYear())
  const loading = ref(false)
  const saving = ref(false)
  const error = ref<string | null>(null)

  async function fetchRawData(targetYear?: number) {
    loading.value = true
    error.value = null
    try {
      const resp = await fetchRawDataApi(targetYear)
      records.value = resp.records
      frontmatter.value = resp.frontmatter
      year.value = resp.year
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } }; message?: string }
      error.value = err?.response?.data?.detail || err?.message || 'Failed to fetch raw data'
    } finally {
      loading.value = false
    }
  }

  async function saveRawData() {
    saving.value = true
    error.value = null
    try {
      return await saveRawDataApi(year.value, frontmatter.value, records.value)
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } }; message?: string }
      error.value = err?.response?.data?.detail || err?.message || 'Failed to save'
      return null
    } finally {
      saving.value = false
    }
  }

  async function syncAndFetch() {
    loading.value = true
    error.value = null
    try {
      await syncVaultApi()
      await fetchRawData(year.value)
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } }; message?: string }
      error.value = err?.response?.data?.detail || err?.message || 'Sync failed'
    } finally {
      loading.value = false
    }
  }

  return { records, frontmatter, year, loading, saving, error, fetchRawData, saveRawData, syncAndFetch }
})
