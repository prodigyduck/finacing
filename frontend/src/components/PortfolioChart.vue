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
  3: '#90EE90',  // Light green
  6: '#FFD700',  // Gold
  12: '#FF6B6B', // Light red
}

function fmtLabel(dateStr: string): string {
  // Check if it's a weekly format (e.g., "2026-W15")
  const weekMatch = dateStr.match(/(\d+)-W(\d+)/)
  if (weekMatch) {
    const year = weekMatch[1]
    const week = weekMatch[2]
    return `${year.slice(2)}/${week}주`  // "26/15주"
  }

  // Check if it's a monthly format (e.g., "2026-05")
  const monthMatch = dateStr.match(/(\d+)-(\d+)/)
  if (monthMatch && monthMatch[1].length === 4) {
    const year = monthMatch[1]
    const month = monthMatch[2]
    return `${year.slice(2)}/${month}월`  // "26/05월"
  }

  // Daily format (ISO date string)
  const d = new Date(dateStr)
  if (!isNaN(d.getTime())) {
    return `${d.getMonth() + 1}/${d.getDate()}`  // "5/15"
  }

  return dateStr  // Fallback
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
      lineStyle: { color: '#00BFFF', width: 2.5 },
      itemStyle: { color: '#00BFFF', borderColor: '#fff', borderWidth: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0,191,255,0.18)' },
          { offset: 1, color: 'rgba(0,191,255,0)' },
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
      axisLabel: {
        fontFamily: 'Inter',
        fontSize: 9,   // Even smaller
        color: '#8E8E93',
        // Smart interval: show labels based on data density
        interval: allLabels.length > 100 ? 4 : allLabels.length > 60 ? 2 : 0,
        // Rotate vertically for very dense data
        rotate: allLabels.length > 60 ? 90 : allLabels.length > 40 ? 45 : 30,
        formatter: (value: string) => value,
      },
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
