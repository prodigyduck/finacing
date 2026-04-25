import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

export interface HistoryRecord {
  date: string
  amount: number
}

export interface Projection {
  months: number
  date: string
  amount: number
}

export interface HistoryResponse {
  records: HistoryRecord[]
  latest: { date: string; amount: number } | null
  earliest: { date: string; amount: number } | null
  total_change: number | null
  return_rate: number | null
  record_count: number
  projections: Projection[]
}

export async function fetchHistory(year?: number): Promise<HistoryResponse> {
  const params: Record<string, unknown> = {}
  if (year) params.year = year
  const { data } = await api.get<HistoryResponse>('/api/v1/history', { params })
  return data
}

export async function fetchHealth(): Promise<{ status: string }> {
  const { data } = await api.get('/health')
  return data
}

export async function syncVault(): Promise<{ status: string; detail: string }> {
  const { data } = await api.post('/api/v1/sync')
  return data
}
