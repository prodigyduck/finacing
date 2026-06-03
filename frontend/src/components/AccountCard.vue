<script setup lang="ts">
import { computed } from 'vue';

interface Holding {
  symbol: string;
}

interface Account {
  name: string;
  latest_amount: number;
  allocation: number;
  holdings: Holding[];
}

const props = defineProps<{
  account: Account;
}>();

const allocationPercent = computed(() => (props.account.allocation * 100).toFixed(1));
</script>

<template>
  <div class="account-card">
    <div class="account-header">
      <h3 class="account-name">{{ account.name }}</h3>
      <span class="allocation">{{ allocationPercent }}%</span>
    </div>
    <div class="amount">{{ account.latest_amount.toFixed(2) }}억</div>
    <div class="holdings">
      <span
        v-for="holding in account.holdings"
        :key="holding.symbol"
        class="holding-badge"
      >
        {{ holding.symbol }}
      </span>
      <span v-if="account.holdings.length === 0" class="no-holdings">
        (종목 없음)
      </span>
    </div>
  </div>
</template>

<style scoped>
.account-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 8px;
  background: white;
  transition: box-shadow 0.2s ease;
}

.account-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.account-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.allocation {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.amount {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #111;
}

.holdings {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.holding-badge {
  display: inline-block;
  padding: 4px 8px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
  color: #555;
}

.no-holdings {
  font-size: 12px;
  color: #999;
  font-style: italic;
}
</style>
