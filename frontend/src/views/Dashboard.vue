<template>
  <v-container fluid class="pa-6" style="max-width: 1200px;">
    <!-- Top Bar -->
    <div class="d-flex justify-space-between align-start mb-6">
      <div>
        <div class="text-h4 font-weight-bold">Portfolio</div>
        <div class="text-body-2 text-medium-emphasis mt-1">Investment value history from Obsidian</div>
      </div>
      <div class="d-flex align-center ga-3">
        <span v-if="lastUpdated" class="text-caption text-medium-emphasis">Updated {{ lastUpdated }}</span>
        <v-btn
          variant="outlined"
          size="small"
          :loading="historyStore.syncing"
          @click="syncAndFetch"
        >
          <v-icon start>mdi-source-branch-sync</v-icon>
          Git Pull
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          :loading="historyStore.loading"
          @click="fetchData"
        >
          <v-icon start>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </div>
    </div>

    <template v-if="historyStore.history && historyStore.history.record_count > 0">
      <!-- Time Period Selector -->
      <div class="d-flex justify-end mb-4">
        <v-btn-toggle
          v-model="timePeriod"
          mandatory
          color="primary"
          variant="outlined"
          density="compact"
          class="rounded-lg"
        >
          <v-btn value="daily" class="text-caption">
            일간
          </v-btn>
          <v-btn value="weekly" class="text-caption">
            주간
          </v-btn>
          <v-btn value="monthly" class="text-caption">
            월간
          </v-btn>
        </v-btn-toggle>
      </div>
      <!-- Metrics -->
      <v-row dense class="mb-6">
        <v-col cols="6" md="3">
          <v-card rounded="lg" variant="flat" class="pa-5">
            <div class="text-overline text-medium-emphasis mb-1">Latest Value</div>
            <div class="text-h4 font-weight-bold">{{ historyStore.history.latest?.amount.toFixed(2) }}</div>
          </v-card>
        </v-col>
        <v-col cols="6" md="3">
          <v-card rounded="lg" variant="flat" class="pa-5">
            <div class="text-overline text-medium-emphasis mb-1">Change</div>
            <div class="text-h4 font-weight-bold" :class="changeColor">
              {{ formatChange(historyStore.history.total_change) }}
            </div>
          </v-card>
        </v-col>
        <v-col cols="6" md="3">
          <v-card rounded="lg" variant="flat" class="pa-5">
            <div class="text-overline text-medium-emphasis mb-1">Return Rate</div>
            <div class="text-h4 font-weight-bold" :class="changeColor">
              {{ formatRate(historyStore.history.return_rate) }}
            </div>
          </v-card>
        </v-col>
        <v-col cols="6" md="3">
          <v-card rounded="lg" variant="flat" class="pa-5">
            <div class="text-overline text-medium-emphasis mb-1">Records</div>
            <div class="text-h4 font-weight-bold">{{ historyStore.history.record_count }}</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Chart -->
      <v-card rounded="lg" variant="flat" class="mb-6 pa-4">
        <v-card-title class="text-subtitle-1 font-weight-bold px-2">
          포트폴리오 추이 ({{ timePeriodLabel }})
        </v-card-title>
        <PortfolioChart :data="lineData" :projections="timePeriod === 'daily' ? projectionsData : []" />
      </v-card>

      <!-- Account Cards -->
      <v-card v-if="historyStore.history?.accounts && historyStore.history.accounts.length > 0" rounded="lg" variant="flat" class="mb-6 pa-4">
        <v-card-title class="text-subtitle-1 font-weight-bold px-2">
          계좌별 현황
        </v-card-title>
        <v-row dense>
          <v-col v-for="account in historyStore.history.accounts" :key="account.name" cols="12" sm="6" md="4">
            <AccountCard :account="account" />
          </v-col>
        </v-row>
      </v-card>

      <!-- Account Chart -->
      <v-card v-if="historyStore.history?.accounts && historyStore.history.accounts.length > 0" rounded="lg" variant="flat" class="mb-6 pa-4">
        <AccountChart
          :accounts="historyStore.history.accounts"
          :account-history="historyStore.history.account_history"
        />
      </v-card>

      <!-- Comparison and Allocation -->
      <v-row v-if="historyStore.history?.comparison" dense class="mb-6">
        <v-col cols="12" md="8">
          <ComparisonTable :comparison="historyStore.history.comparison" />
        </v-col>
        <v-col cols="12" md="4">
          <AllocationChart :allocations="historyStore.history.comparison.allocation_table" />
        </v-col>
      </v-row>

      <!-- Table -->
      <v-card rounded="lg" variant="flat">
        <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">
          {{ timePeriodLabel }} 기록
        </v-card-title>
        <v-table density="comfortable" class="mt-2">
          <thead>
            <tr>
              <th>날짜</th>
              <th class="text-right">금액 (억)</th>
              <th class="text-right">변동</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(record, idx) in aggregatedData" :key="record.date">
              <td>{{ formatAggregateDate(record.date) }}</td>
              <td class="text-right font-weight-medium">{{ record.value.toFixed(2) }}</td>
              <td class="text-right" :class="aggregateChangeColor(idx)">
                {{ formatAggregateChange(idx) }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </template>

    <!-- Empty State -->
    <v-card v-if="!historyStore.loading && (!historyStore.history || historyStore.history.record_count === 0)" rounded="lg" variant="flat" class="py-16 text-center">
      <v-icon size="64" color="text-disabled">mdi-chart-bar</v-icon>
      <div class="text-h6 text-secondary mt-4">데이터가 없습니다</div>
      <div class="text-body-2 text-tertiary mb-6">Obsidian 투자.md 파일에서 데이터를 가져오세요</div>
      <v-btn color="primary" variant="flat" @click="syncAndFetch">
        <v-icon start>mdi-source-branch-sync</v-icon>
        Git Pull로 데이터 가져오기
      </v-btn>
    </v-card>

    <!-- Error -->
    <v-alert v-if="historyStore.error" type="error" variant="tonal" rounded="lg" class="mt-4" closable>
      <template v-slot:title>
        <span class="text-subtitle-2">데이터를 불러오지 못했어요</span>
      </template>
      <div class="text-body-2 mt-1">{{ userFriendlyError }}</div>
      <template v-slot:actions>
        <v-btn variant="text" @click="fetchData">다시 시도</v-btn>
        <v-btn variant="text" @click="syncAndFetch">Git Pull</v-btn>
      </template>
    </v-alert>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHistoryStore } from '@/stores'
import PortfolioChart from '@/components/PortfolioChart.vue'
import AccountCard from '@/components/AccountCard.vue'
import AccountChart from '@/components/AccountChart.vue'
import ComparisonTable from '@/components/ComparisonTable.vue'
import AllocationChart from '@/components/AllocationChart.vue'

const historyStore = useHistoryStore()
const lastUpdated = ref<string | null>(null)

// Time period selection: 'daily' | 'weekly' | 'monthly'
const timePeriod = ref<'daily' | 'weekly' | 'monthly'>('daily')

// Auto-fetch on mount
onMounted(async () => {
  await fetchData()
})

// Aggregate data based on time period
const aggregatedData = computed(() => {
  if (!historyStore.history?.records) return []

  const records = [...historyStore.history.records] // Copy to avoid mutation

  if (timePeriod.value === 'daily') {
    return records.map(r => ({ date: r.date, value: r.amount }))
  }

  if (timePeriod.value === 'weekly') {
    return aggregateByWeek(records)
  }

  if (timePeriod.value === 'monthly') {
    return aggregateByMonth(records)
  }

  return records.map(r => ({ date: r.date, value: r.amount }))
})

// Weekly aggregation: get last value of each week
function aggregateByWeek(records: Array<{ date: string; amount: number }>) {
  const weeks: Map<string, number> = new Map()

  for (const record of records) {
    const date = new Date(record.date)
    const year = date.getFullYear()
    const week = getWeekNumber(date)
    const key = `${year}-W${week}`

    // Use the last value of the week (most recent)
    weeks.set(key, record.amount)
  }

  return Array.from(weeks.entries()).map(([key, value]) => ({
    date: key,
    value,
  }))
}

// Monthly aggregation: get last value of each month
function aggregateByMonth(records: Array<{ date: string; amount: number }>) {
  const months: Map<string, number> = new Map()

  for (const record of records) {
    const date = new Date(record.date)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`

    // Use the last value of the month (most recent)
    months.set(key, record.amount)
  }

  return Array.from(months.entries()).map(([key, value]) => ({
    date: key,
    value,
  }))
}

// Get ISO week number
function getWeekNumber(date: Date): number {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  const dayNum = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
  return Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7)
}

const changeColor = computed(() => {
  const change = historyStore.history?.total_change
  if (change == null) return ''
  return change > 0 ? 'text-success' : change < 0 ? 'text-error' : ''
})

const userFriendlyError = computed(() => {
  const error = historyStore.error
  if (!error) return ''

  if (error.includes('fetch') || error.includes('network')) {
    return '인터넷 연결을 확인하거나 나중에 다시 시도하세요'
  }
  if (error.includes('git') || error.includes('pull')) {
    return 'Git 동기화에 실패했습니다. Obsidian 경로를 확인하세요'
  }
  if (error.includes('parse') || error.includes('format')) {
    return '투자.md 파일 형식을 확인하세요 (M.DD 억 형식)'
  }
  return '문제가 발생했습니다. 다시 시도해주세요'
})

const lineData = computed(() => aggregatedData.value)

const projectionsData = computed(() => historyStore.history?.projections ?? [])

// Time period label for display
const timePeriodLabel = computed(() => {
  switch (timePeriod.value) {
    case 'daily': return '일간'
    case 'weekly': return '주간'
    case 'monthly': return '월간'
    default: return '일간'
  }
})

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function formatChange(change: number | null | undefined): string {
  if (change == null) return '-'
  const sign = change > 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}`
}

function formatRate(rate: number | null | undefined): string {
  if (rate == null) return '-'
  const sign = rate > 0 ? '+' : ''
  return `${sign}${rate.toFixed(2)}%`
}

function dailyChangeColor(idx: number): string {
  if (idx === 0 || !historyStore.history?.records) return ''
  const diff = historyStore.history.records[idx].amount - historyStore.history.records[idx - 1].amount
  return diff > 0 ? 'text-success font-weight-bold' : diff < 0 ? 'text-error font-weight-bold' : ''
}

function formatDailyChange(idx: number): string {
  if (idx === 0 || !historyStore.history?.records) return '-'
  const diff = historyStore.history.records[idx].amount - historyStore.history.records[idx - 1].amount
  const sign = diff > 0 ? '+' : ''
  return `${sign}${diff.toFixed(2)}`
}

// Functions for aggregated data display
function formatAggregateDate(dateStr: string): string {
  if (timePeriod.value === 'daily') {
    const d = new Date(dateStr)
    return `${d.getMonth() + 1}/${d.getDate()}`
  }
  if (timePeriod.value === 'weekly') {
    // Format: 2024-W15
    const match = dateStr.match(/(\d+)-W(\d+)/)
    if (match) {
      const year = match[1]
      const week = match[2]
      return `${year.slice(2)}/${week}주`
    }
    return dateStr
  }
  if (timePeriod.value === 'monthly') {
    // Format: 2024-05
    const parts = dateStr.split('-')
    if (parts.length === 2) {
      const year = parts[0]
      const month = parts[1]
      return `${year.slice(2)}/${month}월`
    }
    return dateStr
  }
  return dateStr
}

function aggregateChangeColor(idx: number): string {
  if (idx === 0 || !aggregatedData.value) return ''
  const diff = aggregatedData.value[idx].value - aggregatedData.value[idx - 1].value
  return diff > 0 ? 'text-success font-weight-bold' : diff < 0 ? 'text-error font-weight-bold' : ''
}

function formatAggregateChange(idx: number): string {
  if (idx === 0 || !aggregatedData.value) return '-'
  const diff = aggregatedData.value[idx].value - aggregatedData.value[idx - 1].value
  const sign = diff > 0 ? '+' : ''
  return `${sign}${diff.toFixed(2)}`
}

async function fetchData() {
  await historyStore.fetchHistory()
  lastUpdated.value = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}

async function syncAndFetch() {
  await historyStore.syncAndFetch()
  lastUpdated.value = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}
</script>
