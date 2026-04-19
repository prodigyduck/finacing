<template>
  <div class="line-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, ChartConfiguration, LineElement, LineController, PointElement, CategoryScale, LinearScale, Tooltip, Filler, Legend } from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Filler, Legend)

interface Props {
  data: { date: string; value: number }[]
  projections: { months: number; date: string; amount: number }[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLCanvasElement>()
let chartInstance: Chart | null = null

const TREND_COLORS: Record<number, string> = {
  3: '#34C759',
  6: '#FF9500',
  12: '#FF3B30',
}

function fmtLabel(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function renderChart() {
  if (!chartRef.value || !props.data.length) return
  const ctx = chartRef.value.getContext('2d')
  if (!ctx) return
  if (chartInstance) chartInstance.destroy()

  const lastActual = props.data[props.data.length - 1]

  // Combined labels: actual + projection dates
  const projLabels = props.projections.map(p => fmtLabel(p.date))
  const allLabels = [...props.data.map(d => fmtLabel(d.date)), ...projLabels]

  // Actual data — only has values for actual dates
  const actualData = [...props.data.map(d => d.value), ...props.projections.map(() => null as unknown as number)]

  const gradient = ctx.createLinearGradient(0, 0, 0, 320)
  gradient.addColorStop(0, 'rgba(0, 122, 255, 0.15)')
  gradient.addColorStop(1, 'rgba(0, 122, 255, 0)')

  const datasets: any[] = [{
    label: 'Actual',
    data: actualData,
    borderColor: '#007AFF',
    backgroundColor: gradient,
    borderWidth: 2,
    pointRadius: 3,
    pointBackgroundColor: '#007AFF',
    pointBorderColor: '#fff',
    pointBorderWidth: 1.5,
    tension: 0.3,
    fill: true,
    spanGaps: false,
  }]

  // One dashed dataset per projection
  for (const proj of props.projections) {
    const data = new Array(allLabels.length).fill(null)
    // Start from last actual point
    const lastIdx = props.data.length - 1
    data[lastIdx] = lastActual.value
    // End at projection
    data[allLabels.length - props.projections.length + props.projections.indexOf(proj)] = proj.amount

    datasets.push({
      label: `+${proj.months}M (${proj.amount}억)`,
      data,
      borderColor: TREND_COLORS[proj.months] || '#8E8E93',
      borderWidth: 2,
      borderDash: [6, 4],
      pointRadius: 4,
      pointBackgroundColor: TREND_COLORS[proj.months] || '#8E8E93',
      pointBorderColor: '#fff',
      pointBorderWidth: 1.5,
      tension: 0,
      fill: false,
      spanGaps: true,
    })
  }

  const config: ChartConfiguration = {
    type: 'line',
    data: { labels: allLabels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            maxTicksLimit: 14,
            font: { size: 11, family: 'Inter' },
            color: '#8E8E93',
          }
        },
        y: {
          grid: { color: 'rgba(0,0,0,0.04)', drawBorder: false },
          ticks: {
            callback: (val: any) => `${val}억`,
            font: { size: 11, family: 'Inter' },
            color: '#8E8E93',
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: {
            usePointStyle: true,
            pointStyle: 'line',
            font: { size: 11, family: 'Inter' },
            color: '#6e6e73',
            padding: 16,
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0,0,0,0.8)',
          titleFont: { size: 13, family: 'Inter' },
          bodyFont: { size: 12, family: 'Inter' },
          padding: 10,
          cornerRadius: 8,
          callbacks: {
            label: (context: any) => ` ${context.dataset.label}: ${context.raw}억`
          }
        }
      }
    }
  }

  chartInstance = new Chart(ctx, config)
}

onMounted(() => renderChart())
watch(() => [props.data, props.projections], () => renderChart(), { deep: true })
</script>

<style scoped>
.line-chart { height: 100%; width: 100%; }
</style>
