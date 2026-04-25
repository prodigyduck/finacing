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
        <v-card-title class="text-subtitle-1 font-weight-bold px-2">Portfolio Value Over Time</v-card-title>
        <PortfolioChart :data="lineData" :projections="projectionsData" />
      </v-card>

      <!-- Table -->
      <v-card rounded="lg" variant="flat">
        <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-0">Daily Records</v-card-title>
        <v-table density="comfortable" class="mt-2">
          <thead>
            <tr>
              <th>Date</th>
              <th class="text-right">Value (억)</th>
              <th class="text-right">Change</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(record, idx) in historyStore.history.records" :key="record.date">
              <td>{{ formatDate(record.date) }}</td>
              <td class="text-right font-weight-medium">{{ record.amount.toFixed(2) }}</td>
              <td class="text-right" :class="dailyChangeColor(idx)">
                {{ formatDailyChange(idx) }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </template>

    <!-- Empty State -->
    <v-card v-if="!historyStore.loading && (!historyStore.history || historyStore.history.record_count === 0)" rounded="lg" variant="flat" class="py-16 text-center">
      <v-icon size="64" color="grey-lighten-1">mdi-chart-bar</v-icon>
      <div class="text-h6 text-medium-emphasis mt-4">No data yet</div>
      <div class="text-body-2 text-medium-emphasis">Click Refresh to fetch your investment data.</div>
    </v-card>

    <!-- Error -->
    <v-alert v-if="historyStore.error" type="error" variant="tonal" rounded="lg" class="mt-4">
      {{ historyStore.error }}
    </v-alert>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useHistoryStore } from '@/stores'
import PortfolioChart from '@/components/PortfolioChart.vue'

const historyStore = useHistoryStore()
const lastUpdated = ref<string | null>(null)

const changeColor = computed(() => {
  const change = historyStore.history?.total_change
  if (change == null) return ''
  return change > 0 ? 'text-success' : change < 0 ? 'text-error' : ''
})

const lineData = computed(() => {
  if (!historyStore.history?.records) return []
  return historyStore.history.records.map(r => ({ date: r.date, value: r.amount }))
})

const projectionsData = computed(() => historyStore.history?.projections ?? [])

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

async function fetchData() {
  await historyStore.fetchHistory()
  lastUpdated.value = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}
</script>
