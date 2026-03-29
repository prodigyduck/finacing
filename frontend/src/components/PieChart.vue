<template>
  <div class="pie-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, ChartConfiguration, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend)

interface Props {
  data: { type: string; ratio: number }[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLCanvasElement>()
let chartInstance: Chart | null = null

function renderChart() {
  if (!chartRef.value || !props.data.length) return

  const canvas = chartRef.value as HTMLCanvasElement
  const ctx = canvas.getContext('2d')

  if (!ctx) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const config: ChartConfiguration = {
    type: 'pie',
    data: {
      labels: props.data.map(d => d.type),
      datasets: [{
        data: props.data.map(d => d.ratio * 100),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF'
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: (context: any) => {
              const value = context.raw
              return `${value.toFixed(1)}%`
            }
          }
        }
      }
    }
  }

  chartInstance = new Chart(ctx, config)
}

onMounted(() => {
  renderChart()
})

watch(() => props.data, () => {
  renderChart()
})
</script>

<style scoped>
.pie-chart {
  height: 300px;
  width: 100%;
}
</style>
