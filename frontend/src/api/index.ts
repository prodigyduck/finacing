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

export interface Holding {
  symbol: string;
}

export interface Account {
  name: string;
  latest_amount: number;
  allocation: number;
  holdings: Holding[];
}

export interface Comparison {
  best_performer: string;
  worst_performer: string;
  allocation_table: Array<{
    account: string;
    amount: number;
    percentage: number;
  }>;
}

export interface HistoryResponse {
  records: HistoryRecord[]
  latest: { date: string; amount: number } | null
  earliest: { date: string; amount: number } | null
  total_change: number | null
  return_rate: number | null
  record_count: number
  projections: Projection[]
  // New fields for account-based portfolio
  accounts?: Account[];
  comparison?: Comparison;
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

export interface RawRecord {
  month: number
  day: number
  amount: string
}

export interface RawDataResponse {
  year: number
  frontmatter: string
  records: RawRecord[]
}

export interface SaveRawDataResponse {
  status: string
  record_count: number
  commit: string | null
}

export async function fetchRawData(year?: number): Promise<RawDataResponse> {
  const params: Record<string, unknown> = {}
  if (year) params.year = year
  const { data } = await api.get<RawDataResponse>('/api/v1/raw-data', { params })
  return data
}

export async function saveRawData(
  year: number,
  frontmatter: string,
  records: RawRecord[],
  commit = true,
): Promise<SaveRawDataResponse> {
  const { data } = await api.put<SaveRawDataResponse>(
    '/api/v1/raw-data',
    { year, frontmatter, records },
    { params: { commit } },
  )
  return data
}
