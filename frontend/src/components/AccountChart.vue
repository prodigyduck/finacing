<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

interface Account {
  name: string;
  latest_amount: number;
  allocation: number;
  holdings: Array<{ symbol: string }>;
}

interface AccountHistory {
  dates: string[];
  series: Array<{
    name: string;
    data: number[];
    color: string;
  }>;
}

interface Props {
  accounts: Account[];
  accountHistory?: AccountHistory;
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement>();
const chartInstance = ref<echarts.ECharts>();

// Chart option
const chartOption = computed<EChartsOption>(() => {
  if (!props.accountHistory || props.accountHistory.series.length === 0) {
    return {} as EChartsOption;
  }

  const series = props.accountHistory.series.map(s => ({
    name: s.name,
    type: 'line' as const,
    data: s.data,
    smooth: true,
    symbol: 'circle',
    symbolSize: 6,
    label: {
      show: true,
      position: 'top',
      fontSize: 10,
      color: '#333',
      formatter: (params: any) => {
        return params.value.toFixed(2);
      }
    },
    lineStyle: {
      color: s.color,
      width: 2
    },
    itemStyle: {
      color: s.color
    }
  }));

  // Y축 범위 동적 계산
  let allValues: number[] = [];
  props.accountHistory.series.forEach(s => {
    allValues = allValues.concat(s.data);
  });
  const maxValue = Math.max(...allValues);
  const minValue = Math.min(...allValues);

  // 범위 계산 (여유 10%)
  const range = maxValue - minValue;
  const yAxisMax = maxValue + (range * 0.1);
  const yAxisMin = Math.max(0, minValue - (range * 0.1));

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        if (!params || params.length === 0) return '';
        const date = params[0].name;
        let result = `${date}<br/>`;
        params.forEach((param: any) => {
          result += `${param.marker} ${param.seriesName}: ${param.value?.toFixed(2)}억<br/>`;
        });
        return result;
      }
    },
    legend: {
      data: props.accountHistory.series.map(s => s.name),
      bottom: 0,
      itemWidth: 12,
      itemHeight: 12,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.accountHistory.dates.map(d => {
        const date = new Date(d);
        return `${date.getMonth() + 1}/${date.getDate()}`;
      }),
      axisLine: {
        lineStyle: {
          color: '#e0e0e0'
        }
      },
      axisLabel: {
        fontSize: 11,
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      name: '금액 (억)',
      min: yAxisMin,
      max: yAxisMax,
      axisLine: {
        show: false
      },
      axisLabel: {
        fontSize: 11,
        color: '#666'
      },
      splitLine: {
        lineStyle: {
          color: '#f5f5f5',
          type: 'dashed'
        }
      }
    },
    series
  };
});

// Initialize chart
const initChart = () => {
  if (!chartRef.value) return;

  chartInstance.value = echarts.init(chartRef.value);
  chartInstance.value.setOption(chartOption.value);

  // Responsive resize
  window.addEventListener('resize', () => {
    chartInstance.value?.resize();
  });
};

// Watch for changes
watch([() => props.accountHistory, () => props.accounts], () => {
  if (chartInstance.value) {
    chartInstance.value.setOption(chartOption.value);
  }
}, { deep: true });

onMounted(() => {
  initChart();
});
</script>

<template>
  <div class="account-chart">
    <div class="chart-header">
      <h3 class="chart-title">계좌별 추이</h3>
    </div>
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<style scoped>
.account-chart {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.chart-container {
  width: 100%;
  height: 300px;
}
</style>
