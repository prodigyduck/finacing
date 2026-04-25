<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

interface Props {
  data: { date: string; value: number }[]
  projections: { months: number; date: string; amount: number }[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const TREND_COLORS: Record<number, string> = {
  3: '#34C759',
  6: '#FF9500',
  12: '#FF3B30',
}

function fmtLabel(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function render() {
  if (!chartRef.value || !props.data.length) return
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  const lastActual = props.data[props.data.length - 1]
  const allLabels = [
    ...props.data.map(d => fmtLabel(d.date)),
    ...props.projections.map(p => fmtLabel(p.date)),
  ]

  const series: echarts.SeriesOption[] = [
    {
      name: 'Actual',
      type: 'line',
      data: [...props.data.map(d => d.value), ...props.projections.map(() => null)],
      smooth: 0.3,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#007AFF', width: 2.5 },
      itemStyle: { color: '#007AFF', borderColor: '#fff', borderWidth: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0,122,255,0.18)' },
          { offset: 1, color: 'rgba(0,122,255,0)' },
        ]),
      },
    },
  ]

  for (const proj of props.projections) {
    const data = new Array(allLabels.length).fill(null)
    const lastIdx = props.data.length - 1
    data[lastIdx] = lastActual.value
    const projIdx = allLabels.length - props.projections.length + props.projections.indexOf(proj)
    data[projIdx] = proj.amount

    series.push({
      name: `+${proj.months}M (${proj.amount})`,
      type: 'line',
      data,
      smooth: false,
      symbol: 'circle',
      symbolSize: (value: number | null, params: { dataIndex: number }) => {
        if (value == null) return 0
        return params.dataIndex === projIdx ? 14 : 0
      },
      lineStyle: {
        color: TREND_COLORS[proj.months] || '#8E8E93',
        width: 3,
        type: [8, 5],
      },
      itemStyle: {
        color: TREND_COLORS[proj.months] || '#8E8E93',
        borderColor: '#fff',
        borderWidth: 2,
      },
      label: {
        show: true,
        position: 'right',
        formatter: (params: { dataIndex: number; value: number | null }) => {
          if (params.value == null || params.dataIndex !== projIdx) return ''
          return `${proj.amount}`
        },
        color: TREND_COLORS[proj.months] || '#8E8E93',
        fontWeight: 'bold' as const,
        fontSize: 12,
      },
    })
  }

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0,0,0,0.8)',
      borderColor: 'transparent',
      textStyle: { color: '#fff', fontFamily: 'Inter' },
      formatter: (params: { axisValue: string; marker: string; seriesName: string; value: number | null }[]) => {
        let html = `<b>${params[0].axisValue}</b><br/>`
        for (const p of params) {
          if (p.value != null) {
            html += `${p.marker} ${p.seriesName}: <b>${p.value}</b><br/>`
          }
        }
        return html
      },
    },
    legend: {
      top: 0,
      right: 0,
      icon: 'roundRect',
      itemWidth: 16,
      itemHeight: 3,
      textStyle: { fontFamily: 'Inter', fontSize: 11, color: '#6e6e73' },
    },
    grid: { left: 50, right: 60, top: 40, bottom: 30 },
    xAxis: {
      type: 'category',
      data: allLabels,
      axisLine: { lineStyle: { color: '#e0e0e0' } },
      axisTick: { show: false },
      axisLabel: { fontFamily: 'Inter', fontSize: 11, color: '#8E8E93' },
    },
    yAxis: {
      type: 'value',
      min: 3,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: 'rgba(0,0,0,0.04)' } },
      axisLabel: {
        fontFamily: 'Inter',
        fontSize: 11,
        color: '#8E8E93',
        formatter: '{value}',
      },
    },
    series,
    dataZoom: [
      { type: 'inside', start: 0, end: 100 },
    ],
  })
}

function handleResize() { chart?.resize() }

onMounted(() => {
  render()
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  chart = null
})
watch(() => [props.data, props.projections], () => render(), { deep: true })
</script>
