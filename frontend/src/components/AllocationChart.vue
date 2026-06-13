<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

interface AllocationRow {
  account: string;
  amount: number;
  percentage: number;
}

interface Props {
  allocations: AllocationRow[];
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement>();
const chartInstance = ref<echarts.ECharts>();

// Chart data with colors
const chartData = computed(() => {
  return props.allocations.map((alloc, index) => ({
    name: alloc.account,
    value: alloc.amount,
    percentage: alloc.percentage,
    // Toss-style colors: blue, green, purple, orange, gray
    itemStyle: {
      color: [
        '#3b82f6', // blue
        '#10b981', // green
        '#8b5cf6', // purple
        '#f59e0b', // orange
        '#6b7280', // gray
      ][index % 5]
    }
  }));
});

// Chart option
const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'item',
    formatter: (params: any) => {
      if (!params) return '';
      const data = params.data as typeof chartData.value[0];
      return `${data.name}<br/>${data.value.toFixed(2)}억 (${data.percentage.toFixed(1)}%)`;
    }
  },
  legend: {
    orient: 'horizontal',
    bottom: 0,
    itemWidth: 12,
    itemHeight: 12,
    textStyle: {
      fontSize: 12
    }
  },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'], // Donut chart
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold',
          formatter: (params: any) => {
            return `${params.name}\n${params.value?.toFixed(1)}%`;
          }
        }
      },
      labelLine: {
        show: false
      },
      data: chartData.value
    }
  ]
}));

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
watch(() => props.allocations, () => {
  if (chartInstance.value) {
    chartInstance.value.setOption(chartOption.value);
  }
}, { deep: true });

onMounted(() => {
  initChart();
});
</script>

<template>
  <div class="allocation-chart">
    <h3 class="chart-title">자산 배분</h3>
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<style scoped>
.allocation-chart {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.chart-container {
  width: 100%;
  height: 250px;
}
</style>
