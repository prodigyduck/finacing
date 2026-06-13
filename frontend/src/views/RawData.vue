<template>
  <v-container fluid class="pa-6" style="max-width: 1200px;">
    <!-- Top Bar -->
    <div class="d-flex justify-space-between align-start mb-6">
      <div>
        <div class="text-h4 font-weight-bold">Raw Data</div>
        <div class="text-body-2 text-medium-emphasis mt-1">투자.md의 기록을 편집하세요</div>
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
          @click="handleGitPull"
        >
          <v-icon start>mdi-source-branch-sync</v-icon>
          Git Pull
        </v-btn>
        <v-btn
          variant="outlined"
          size="small"
          :loading="pushing"
          @click="handleGitPush"
        >
          <v-icon start>mdi-source-branch-push</v-icon>
          Git Push
        </v-btn>
      </div>
    </div>

    <!-- Error -->
    <v-alert v-if="rawDataStore.error" type="error" variant="tonal" rounded="lg" class="mb-4">
      {{ rawDataStore.error }}
    </v-alert>

    <!-- Format Tabs -->
    <v-tabs v-model="activeTab" class="mb-4">
      <v-tab value="legacy">레거시 형식</v-tab>
      <v-tab value="account">계좌별 형식</v-tab>
    </v-tabs>

    <!-- Legacy Format Editor -->
    <v-card v-if="activeTab === 'legacy'" rounded="lg" variant="flat">
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
        <v-spacer />
        <v-btn
          color="primary"
          variant="flat"
          :loading="rawDataStore.saving"
          @click="handleSaveLegacy"
        >
          <v-icon start>mdi-content-save</v-icon>
          저장
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Account Format Editor -->
    <v-card v-if="activeTab === 'account'" rounded="lg" variant="flat" class="pa-4">
      <v-card-title class="text-subtitle-1 font-weight-bold px-0">
        계좌별 기록
      </v-card-title>

      <!-- Date Input -->
      <v-row dense class="mb-4">
        <v-col cols="12" sm="4">
          <v-text-field
            v-model="accountDate"
            label="날짜 (YYYY-MM-DD)"
            type="date"
            density="compact"
            variant="outlined"
            hide-details
          />
        </v-col>
      </v-row>

      <!-- Account Cards -->
      <div v-for="(account, accIdx) in accountRows" :key="accIdx" class="mb-4">
        <v-card rounded="lg" variant="outlined" class="pa-4">
          <div class="d-flex justify-space-between align-center mb-3">
            <v-text-field
              v-model="account.name"
              label="계좌명"
              density="compact"
              variant="outlined"
              hide-details
              style="max-width: 200px;"
            />
            <v-btn icon size="small" variant="text" color="error" @click="removeAccount(accIdx)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>

          <v-row dense class="mb-3">
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="account.amount"
                label="총액 (억)"
                type="number"
                density="compact"
                variant="outlined"
                hide-details
                placeholder="0.00"
              />
            </v-col>
          </v-row>

          <div class="mb-2 text-caption text-medium-emphasis">보유종목</div>
          <v-row dense>
            <v-col v-for="(holding, hIdx) in account.holdings" :key="hIdx" cols="12" sm="6">
              <div class="d-flex align-center ga-2">
                <v-text-field
                  v-model="holding.symbol"
                  label="종목명"
                  density="compact"
                  variant="outlined"
                  hide-details
                  style="flex: 1;"
                />
                <v-btn icon size="x-small" variant="text" color="error" @click="removeHolding(accIdx, hIdx)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </v-col>
            <v-col cols="12">
              <v-btn variant="text" size="small" prepend-icon="mdi-plus" @click="addHolding(accIdx)">
                종목 추가
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </div>

      <v-btn variant="text" prepend-icon="mdi-plus" @click="addAccount" class="mb-4">
        계좌 추가
      </v-btn>

      <v-divider class="my-4" />

      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn
          color="primary"
          variant="flat"
          :loading="rawDataStore.saving"
          @click="handleSaveAccount"
        >
          <v-icon start>mdi-content-save</v-icon>
          저장
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Empty State -->
    <v-card
      v-if="!rawDataStore.loading && rows.length === 0 && accountRows.length === 0"
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
import { useRouter } from 'vue-router'
import { useRawDataStore } from '@/stores'
import type { RawRecord } from '@/api'
import axios from 'axios'

const router = useRouter()

interface Row {
  month: number
  day: number
  amount: string
  display: string
  dateError: boolean
}

interface Holding {
  symbol: string
}

interface AccountRow {
  name: string
  amount: string
  holdings: Holding[]
}

const rawDataStore = useRawDataStore()

const currentYear = new Date().getFullYear()
const selectedYear = ref(currentYear)
const yearOptions = [currentYear - 2, currentYear - 1, currentYear, currentYear + 1]

const rows = reactive<Row[]>([])
const accountRows = reactive<AccountRow[]>([])
const accountDate = ref(new Date().toISOString().split('T')[0])
const activeTab = ref<'legacy' | 'account'>('legacy')
const pushing = ref(false)

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

  // Load existing account data for today
  await loadAccountData()
})

async function onYearChange(year: number) {
  await rawDataStore.fetchRawData(year)
  syncFromStore()
}

async function loadAccountData() {
  try {
    const response = await axios.get('/api/v1/account-data', {
      params: { date: accountDate.value }
    })

    if (response.data.accounts && response.data.accounts.length > 0) {
      // Convert API response to accountRows format
      accountRows.splice(0, accountRows.length,
        ...response.data.accounts.map((acc: any) => ({
          name: acc.name,
          amount: acc.amount,
          holdings: (acc.holdings || []).map((h: string) => ({ symbol: h }))
        }))
      )
    }
  } catch (e: unknown) {
    // No existing data for this date, that's ok
    console.log('No existing account data for this date')
  }
}

// Watch account date change to reload data
watch(accountDate, () => {
  loadAccountData()
})

async function handleGitPull() {
  await rawDataStore.syncAndFetch()
  snackbarText.value = 'Git Pull 완료'
  snackbarColor.value = 'success'
  snackbar.value = true
}

async function handleGitPush() {
  pushing.value = true
  try {
    await axios.post('/api/v1/sync', {}, {
      headers: {
        'X-API-Key': 'local-dev-only'
      }
    })
    snackbarText.value = 'Git Push 완료'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: string } }; message?: string }
    snackbarText.value = err?.response?.data?.detail || err?.message || 'Git Push 실패'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    pushing.value = false
  }
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

async function handleSaveLegacy() {
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
    snackbarText.value = `${result.record_count}개 기록을 저장했어요`
    snackbarColor.value = 'success'
    snackbar.value = true

    setTimeout(() => {
      router.push('/')
    }, 1500)
  }
}

// Account format functions
function addAccount() {
  accountRows.push({
    name: '',
    amount: '',
    holdings: []
  })
}

function removeAccount(idx: number) {
  accountRows.splice(idx, 1)
}

function addHolding(accIdx: number) {
  accountRows[accIdx].holdings.push({ symbol: '' })
}

function removeHolding(accIdx: number, hIdx: number) {
  accountRows[accIdx].holdings.splice(hIdx, 1)
}

async function handleSaveAccount() {
  // Validate
  if (!accountDate.value) {
    snackbarText.value = '날짜를 선택해주세요'
    snackbarColor.value = 'error'
    snackbar.value = true
    return
  }

  for (const acc of accountRows) {
    if (!acc.name) {
      snackbarText.value = '계좌명을 입력해주세요'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }
    if (!acc.amount || isNaN(parseFloat(acc.amount))) {
      snackbarText.value = `${acc.name || '(계좌)'}의 금액을 확인해주세요`
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }
  }

  // Convert account data to markdown
  const date = new Date(accountDate.value)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const dateStr = `${year}-${month}-${day}`

  let markdown = `\n## ${dateStr}\n\n`

  for (const acc of accountRows) {
    markdown += `### 계좌: ${acc.name}\n`
    markdown += `총액: ${parseFloat(acc.amount).toFixed(2)}억\n`
    if (acc.holdings.length > 0) {
      const symbols = acc.holdings.map(h => h.symbol).filter(s => s).join(', ')
      if (symbols) {
        markdown += `보유종목: ${symbols}\n`
      } else {
        markdown += `보유종목:\n`
      }
    } else {
      markdown += `보유종목:\n`
    }
    markdown += '\n'
  }

  // Save via API
  rawDataStore.saving = true
  try {
    const response = await axios.post('/api/v1/account-data', {
      date: dateStr,
      accounts: accountRows.map(acc => ({
        name: acc.name,
        amount: acc.amount,
        holdings: acc.holdings.map(h => h.symbol).filter(s => s)
      }))
    }, {
      headers: {
        'X-API-Key': 'local-dev-only'
      }
    })

    snackbarText.value = `${response.data.account_count}개 계좌 기록을 저장했어요`
    snackbarColor.value = 'success'
    snackbar.value = true

    // Clear form
    accountRows.splice(0, accountRows.length)
    accountDate.value = new Date().toISOString().split('T')[0]

    // Redirect to Dashboard after successful save
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: string } }; message?: string }
    snackbarText.value = err?.response?.data?.detail || err?.message || '저장 실패'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    rawDataStore.saving = false
  }
}
</script>
