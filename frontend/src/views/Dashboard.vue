<template>
  <div class="dashboard">
    <div class="top-bar">
      <div>
        <h1 class="page-title">Portfolio</h1>
        <p class="page-subtitle">Investment value history from Obsidian</p>
      </div>
      <div class="top-actions">
        <span class="last-updated" v-if="lastUpdated">Updated {{ lastUpdated }}</span>
        <button class="btn-refresh" @click="fetchData" :disabled="historyStore.loading">
          <svg v-if="historyStore.loading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          {{ historyStore.loading ? 'Fetching...' : 'Refresh' }}
        </button>
      </div>
    </div>

    <template v-if="historyStore.history && historyStore.history.record_count > 0">
      <div class="metrics-row">
        <div class="metric-card">
          <span class="metric-label">Latest Value</span>
          <span class="metric-value">{{ historyStore.history.latest?.amount.toFixed(2) }}억</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Change</span>
          <span class="metric-value" :class="changeClass">{{ formatChange(historyStore.history.total_change) }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Return Rate</span>
          <span class="metric-value" :class="changeClass">{{ formatRate(historyStore.history.return_rate) }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Records</span>
          <span class="metric-value">{{ historyStore.history.record_count }}</span>
        </div>
      </div>

      <div class="card chart-card">
        <div class="card-header">
          <h3>Portfolio Value Over Time</h3>
        </div>
        <div class="chart-body">
          <LineChart :data="lineData" :projections="projectionsData" />
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>Daily Records</h3>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th class="right">Value (억)</th>
                <th class="right">Change</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, idx) in historyStore.history.records" :key="record.date">
                <td>{{ formatDate(record.date) }}</td>
                <td class="right">{{ record.amount.toFixed(2) }}</td>
                <td class="right" :class="dailyChangeClass(idx)">{{ formatDailyChange(idx) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <div v-if="!historyStore.loading && (!historyStore.history || historyStore.history.record_count === 0)" class="card empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" stroke-width="1.5">
        <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
      </svg>
      <h3>No data yet</h3>
      <p>Click Refresh to fetch your investment data.</p>
    </div>

    <div v-if="historyStore.error" class="card error-state">
      <p>{{ historyStore.error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useHistoryStore } from '@/stores'
import LineChart from '@/components/LineChart.vue'

const historyStore = useHistoryStore()
const lastUpdated = ref<string | null>(null)

const changeClass = computed(() => {
  const change = historyStore.history?.total_change
  if (change == null) return ''
  return change > 0 ? 'positive' : change < 0 ? 'negative' : ''
})

const lineData = computed(() => {
  if (!historyStore.history?.records) return []
  return historyStore.history.records.map(r => ({ date: r.date, value: r.amount }))
})

const projectionsData = computed(() => {
  return historyStore.history?.projections ?? []
})

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function formatChange(change: number | null | undefined): string {
  if (change == null) return '-'
  const sign = change > 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}억`
}

function formatRate(rate: number | null | undefined): string {
  if (rate == null) return '-'
  const sign = rate > 0 ? '+' : ''
  return `${sign}${rate.toFixed(2)}%`
}

function dailyChangeClass(idx: number): string {
  if (idx === 0) return ''
  const records = historyStore.history?.records
  if (!records) return ''
  const diff = records[idx].amount - records[idx - 1].amount
  return diff > 0 ? 'positive' : diff < 0 ? 'negative' : ''
}

function formatDailyChange(idx: number): string {
  if (idx === 0) return '-'
  const records = historyStore.history?.records
  if (!records) return '-'
  const diff = records[idx].amount - records[idx - 1].amount
  const sign = diff > 0 ? '+' : ''
  return `${sign}${diff.toFixed(2)}`
}

async function fetchData() {
  await historyStore.fetchHistory()
  lastUpdated.value = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.dashboard { max-width: 1100px; margin: 0 auto; }

.top-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.page-title { font-size: 28px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
.page-subtitle { font-size: 14px; color: var(--text-tertiary); margin-top: 4px; }
.top-actions { display: flex; align-items: center; gap: 12px; }
.last-updated { font-size: 13px; color: var(--text-tertiary); }

.btn-refresh {
  display: flex; align-items: center; gap: 6px; padding: 8px 16px;
  background: var(--accent); color: white; border: none; border-radius: 8px;
  font-size: 13px; font-weight: 600; cursor: pointer; transition: opacity 0.15s;
}
.btn-refresh:hover { opacity: 0.85; }
.btn-refresh:disabled { opacity: 0.5; cursor: not-allowed; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.card {
  background: var(--bg-card); border-radius: var(--radius);
  box-shadow: var(--shadow-sm); border: 1px solid var(--border);
}

.metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }

.metric-card {
  background: var(--bg-card); border-radius: var(--radius); padding: 20px 24px;
  box-shadow: var(--shadow-sm); border: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 6px;
}
.metric-label { font-size: 13px; font-weight: 500; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.5px; }
.metric-value { font-size: 28px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
.metric-value.positive { color: var(--green); }
.metric-value.negative { color: var(--red); }

.chart-card { padding: 20px; margin-bottom: 24px; }
.chart-card .card-header { margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.chart-body { height: 320px; }

.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
thead th {
  padding: 12px 16px; font-size: 12px; font-weight: 600; color: var(--text-tertiary);
  text-transform: uppercase; letter-spacing: 0.5px; text-align: left;
  border-bottom: 1px solid var(--border);
}
thead th.right { text-align: right; }
tbody td { padding: 14px 16px; font-size: 14px; border-bottom: 1px solid var(--border); }
.right { text-align: right; }
.positive { color: var(--green); font-weight: 600; }
.negative { color: var(--red); font-weight: 600; }

.empty-state, .error-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 60px 20px; gap: 12px;
}
.empty-state h3 { font-size: 17px; font-weight: 600; color: var(--text-secondary); }
.empty-state p { font-size: 14px; color: var(--text-tertiary); }
.error-state { color: var(--red); font-size: 14px; }

@media (max-width: 768px) {
  .metrics-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
