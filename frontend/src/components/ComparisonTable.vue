<script setup lang="ts">
import { computed } from 'vue';

interface AllocationRow {
  account: string;
  amount: number;
  percentage: number;
}

interface Comparison {
  best_performer: string | null;
  worst_performer: string | null;
  allocation_table: AllocationRow[];
}

interface Props {
  comparison: Comparison;
}

const props = defineProps<Props>();

// Sort allocation table by amount (highest first)
const sortedAllocations = computed(() => {
  return [...props.comparison.allocation_table].sort((a, b) => b.amount - a.amount);
});

// Get badge color for performance
const getPerformanceBadge = (accountName: string) => {
  if (props.comparison.best_performer === accountName) return 'success';
  if (props.comparison.worst_performer === accountName) return 'error';
  return 'default';
};

const getPerformanceLabel = (accountName: string) => {
  if (props.comparison.best_performer === accountName) return '최우수';
  if (props.comparison.worst_performer === accountName) return '최저';
  return '';
};
</script>

<template>
  <div class="comparison-table">
    <h3 class="table-title">계좌별 배분 및 성과</h3>

    <v-table density="comfortable" class="align-center">
      <thead>
        <tr>
          <th>계좌</th>
          <th class="text-right">금액 (억)</th>
          <th class="text-right">비중</th>
          <th class="text-center">성과</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in sortedAllocations" :key="row.account">
          <td class="font-weight-medium">{{ row.account }}</td>
          <td class="text-right">{{ row.amount.toFixed(2) }}</td>
          <td class="text-right">{{ row.percentage.toFixed(1) }}%</td>
          <td class="text-center">
            <v-chip
              v-if="getPerformanceLabel(row.account)"
              :color="getPerformanceBadge(row.account)"
              size="small"
              class="text-caption"
            >
              {{ getPerformanceLabel(row.account) }}
            </v-chip>
            <span v-else class="text-medium-emphasis text-caption">-</span>
          </td>
        </tr>
      </tbody>
    </v-table>

    <div class="summary mt-4">
      <div class="summary-item">
        <span class="summary-label">최우수 성과:</span>
        <span class="summary-value font-weight-bold text-success">
          {{ comparison.best_performer || '-' }}
        </span>
      </div>
      <div class="summary-item">
        <span class="summary-label">최저 성과:</span>
        <span class="summary-value font-weight-bold text-error">
          {{ comparison.worst_performer || '-' }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comparison-table {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.summary {
  display: flex;
  gap: 24px;
  padding-top: 12px;
  border-top: 1px solid #f5f5f5;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-label {
  font-size: 13px;
  color: #666;
}

.summary-value {
  font-size: 14px;
}
</style>
