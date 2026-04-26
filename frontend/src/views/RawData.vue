<template>
  <v-container fluid class="pa-6" style="max-width: 1200px;">
    <!-- Top Bar -->
    <div class="d-flex justify-space-between align-start mb-6">
      <div>
        <div class="text-h4 font-weight-bold">Raw Data</div>
        <div class="text-body-2 text-medium-emphasis mt-1">Edit investment records in 투자.md</div>
      </div>
      <div class="d-flex align-center ga-3">
        <v-select
          v-model="selectedYear"
          :items="yearOptions"
          density="compact"
          variant="outlined"
          hide-details
          style="max-width: 100px;"
          @update:model-value="onYearChange"
        />
        <v-btn
          variant="outlined"
          size="small"
          :loading="rawDataStore.loading"
          @click="rawDataStore.syncAndFetch()"
        >
          <v-icon start>mdi-source-branch-sync</v-icon>
          Git Pull
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          :loading="rawDataStore.saving"
          @click="handleSave"
        >
          <v-icon start>mdi-content-save</v-icon>
          Save
        </v-btn>
      </div>
    </div>

    <!-- Error -->
    <v-alert v-if="rawDataStore.error" type="error" variant="tonal" rounded="lg" class="mb-4">
      {{ rawDataStore.error }}
    </v-alert>

    <!-- Table -->
    <v-card rounded="lg" variant="flat">
      <v-table density="comfortable">
        <thead>
          <tr>
            <th style="width: 200px;">Date (M.DD)</th>
            <th style="width: 200px;">Amount (억)</th>
            <th style="width: 80px;"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, idx) in rows" :key="idx">
            <td>
              <v-text-field
                v-model="record.display"
                density="compact"
                variant="outlined"
                hide-details
                placeholder="M.DD"
                :error="record.dateError"
                @blur="parseDate(idx)"
                @keydown.enter="parseDate(idx)"
                style="max-width: 140px;"
              />
            </td>
            <td>
              <v-text-field
                v-model="record.amount"
                density="compact"
                variant="outlined"
                hide-details
                placeholder="0.00"
                style="max-width: 160px;"
              />
            </td>
            <td>
              <v-btn icon size="x-small" variant="text" color="error" @click="removeRow(idx)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
      <v-divider />
      <v-card-actions class="pa-4">
        <v-btn variant="text" prepend-icon="mdi-plus" @click="addRow">
          Add Record
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Empty State -->
    <v-card
      v-if="!rawDataStore.loading && rows.length === 0"
      rounded="lg"
      variant="flat"
      class="py-12 text-center"
    >
      <v-icon size="48" color="grey-lighten-1">mdi-database-off-outline</v-icon>
      <div class="text-body-1 text-medium-emphasis mt-2">No records found</div>
    </v-card>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { useRawDataStore } from '@/stores'
import type { RawRecord } from '@/api'

interface Row {
  month: number
  day: number
  amount: string
  display: string
  dateError: boolean
}

const rawDataStore = useRawDataStore()

const currentYear = new Date().getFullYear()
const selectedYear = ref(currentYear)
const yearOptions = [currentYear - 2, currentYear - 1, currentYear, currentYear + 1]

const rows = reactive<Row[]>([])

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

function recordsToRows(records: RawRecord[]): Row[] {
  return records.map(r => ({
    month: r.month,
    day: r.day,
    amount: r.amount,
    display: `${r.month}.${r.day}`,
    dateError: false,
  }))
}

function syncFromStore() {
  rows.splice(0, rows.length, ...recordsToRows(rawDataStore.records))
}

watch(() => rawDataStore.records, syncFromStore, { deep: true })

onMounted(async () => {
  await rawDataStore.fetchRawData(selectedYear.value)
  syncFromStore()
})

async function onYearChange(year: number) {
  await rawDataStore.fetchRawData(year)
  syncFromStore()
}

function parseDate(idx: number) {
  const row = rows[idx]
  const parts = row.display.split('.')
  if (parts.length === 2) {
    const m = parseInt(parts[0], 10)
    const d = parseInt(parts[1], 10)
    if (m >= 1 && m <= 12 && d >= 1 && d <= 31) {
      row.month = m
      row.day = d
      row.dateError = false
      return
    }
  }
  row.dateError = true
}

function addRow() {
  const today = new Date()
  rows.push({
    month: today.getMonth() + 1,
    day: today.getDate(),
    amount: '',
    display: `${today.getMonth() + 1}.${today.getDate()}`,
    dateError: false,
  })
}

function removeRow(idx: number) {
  rows.splice(idx, 1)
}

async function handleSave() {
  // Sync display → month/day
  for (const r of rows) {
    const parts = r.display.split('.')
    if (parts.length === 2) {
      r.month = parseInt(parts[0], 10)
      r.day = parseInt(parts[1], 10)
    }
  }

  // Validate
  for (const r of rows) {
    if (r.month < 1 || r.month > 12 || r.day < 1 || r.day > 31) {
      snackbarText.value = `잘못된 날짜: ${r.display}`
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }
    if (!r.amount || isNaN(parseFloat(r.amount))) {
      snackbarText.value = `잘못된 금액: ${r.amount || '(empty)'}`
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }
  }

  // Copy local rows into store records before save
  rawDataStore.records.splice(0, rawDataStore.records.length, ...rows.map(r => ({
    month: r.month,
    day: r.day,
    amount: r.amount,
  })))

  const result = await rawDataStore.saveRawData()
  if (result) {
    snackbarText.value = `Saved ${result.record_count} records${result.commit ? ` (${result.commit})` : ''}`
    snackbarColor.value = 'success'
    snackbar.value = true
  }
}
</script>
