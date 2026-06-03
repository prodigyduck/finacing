<script setup lang="ts">
import { computed } from 'vue';

interface Holding {
  symbol: string;
}

interface Props {
  holdings: Holding[];
  title?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: '보유 종목'
});

const holdingCount = computed(() => props.holdings.length);
</script>

<template>
  <div class="holdings-list">
    <h4 v-if="title" class="title">{{ title }}</h4>
    <div v-if="holdingCount === 0" class="empty-state">
      <p>보유 종목이 없습니다</p>
    </div>
    <ul v-else class="holdings">
      <li v-for="holding in holdings" :key="holding.symbol" class="holding-item">
        {{ holding.symbol }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.holdings-list {
  padding: 12px 0;
}

.title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.empty-state {
  padding: 16px;
  text-align: center;
  color: #999;
  font-size: 13px;
}

.holdings {
  list-style: none;
  padding: 0;
  margin: 0;
}

.holding-item {
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #333;
}

.holding-item:last-child {
  border-bottom: none;
}
</style>
