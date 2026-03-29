<template>
  <div class="bar-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, ChartConfiguration, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend)

interface Props {
  data: { name: string; ratio: number }[]
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
    type: 'bar',
    data: {
      labels: props.data.map(d => d.name),
      datasets: [{
        label: 'Allocation (%)',
        data: props.data.map(d => d.ratio),
        backgroundColor: '#42b883'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: 'Percentage'
          }
        }
      },
      plugins: {
        legend: {
          display: false
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
.bar-chart {
  height: 300px;
  width: 100%;
}
</style>
