<template>
  <div class="bar-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, ChartConfiguration, BarElement, BarController, CategoryScale, LinearScale, Tooltip } from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip)

interface Props {
  data: { name: string; ratio: number }[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLCanvasElement>()
let chartInstance: Chart | null = null

const COLORS = [
  '#007AFF', '#5856D6', '#34C759', '#FF9500', '#FF3B30',
  '#AF52DE', '#5AC8FA', '#FFCC00', '#30B0C7', '#64D2FF'
]

function renderChart() {
  if (!chartRef.value || !props.data.length) return

  const ctx = chartRef.value.getContext('2d')
  if (!ctx) return

  if (chartInstance) chartInstance.destroy()

  const config: ChartConfiguration = {
    type: 'bar',
    data: {
      labels: props.data.map(d => d.name),
      datasets: [{
        data: props.data.map(d => +d.ratio.toFixed(1)),
        backgroundColor: props.data.map((_, i) => COLORS[i % COLORS.length]),
        borderRadius: 6,
        borderSkipped: false,
        maxBarThickness: 40,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          grid: { color: 'rgba(0,0,0,0.04)', drawBorder: false },
          ticks: {
            callback: (val: any) => `${val}%`,
            font: { size: 11, family: 'Inter' },
            color: '#8E8E93',
          }
        },
        y: {
          grid: { display: false },
          ticks: {
            font: { size: 12, family: 'Inter' },
            color: '#1d1d1f',
          }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(0,0,0,0.8)',
          titleFont: { size: 13, family: 'Inter' },
          bodyFont: { size: 12, family: 'Inter' },
          padding: 10,
          cornerRadius: 8,
          callbacks: {
            label: (context: any) => ` ${context.raw}%`
          }
        }
      }
    }
  }

  chartInstance = new Chart(ctx, config)
}

onMounted(() => renderChart())
watch(() => props.data, () => renderChart())
</script>

<style scoped>
.bar-chart {
  height: 100%;
  width: 100%;
}
</style>
