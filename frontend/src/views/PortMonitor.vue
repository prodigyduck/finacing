/**
 * Port Monitor Component
 *
 * Mac mini-style port status dashboard with real-time monitoring.
 */

<template>
  <div class="port-monitor">
    <header>
      <h1>📊 Port Status Monitor</h1>
      <button @click="refreshPorts" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Refreshing...' : '🔄 Refresh' }}
      </button>
      <div class="status-badge" :class="overallStatus.class">
        {{ overallStatus.text }}
      </div>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading port status...</p>
    </div>

    <div v-else class="port-grid">
      <div
        v-for="port in ports"
        :key="port.port"
        class="port-card"
        :class="{ 'in-use': port.in_use, 'available': !port.in_use }"
      >
        <div class="port-header">
          <div class="port-number">{{ port.port }}</div>
          <div class="port-status" :class="port.in_use ? 'status-in-use' : 'status-available'">
            {{ port.in_use ? '🔴 In Use' : '🟢 Available' }}
          </div>
        </div>

        <div class="port-details">
          <div v-if="port.in_use" class="process-info">
            <div class="info-item">
              <span class="label">Process:</span>
              <span class="value">{{ port.process_name || 'Unknown' }}</span>
            </div>
            <div v-if="port.process_id" class="info-item">
              <span class="label">PID:</span>
              <span class="value">{{ port.process_id }}</span>
            </div>
          </div>
          <div class="info-item">
            <span class="label">Last Checked:</span>
            <span class="value">{{ formatTime(port.last_checked) }}</span>
          </div>
        </div>

        <div class="actions" v-if="port.in_use">
          <button
            @click="killProcess(port.port)"
            class="kill-btn"
            :disabled="killing"
          >
            {{ killing ? 'Killing...' : '🛑 Kill Process' }}
          </button>
        </div>
      </div>
    </div>

    <div class="summary">
      <div class="summary-card">
        <h3>Summary</h3>
        <div class="summary-stats">
          <div class="stat">
            <span class="stat-value">{{ summary.total_ports }}</span>
            <span class="stat-label">Total Ports</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ summary.in_use_count }}</span>
            <span class="stat-label">In Use</span>
          </div>
          <div class="stat available">
            <span class="stat-value">{{ summary.available_count }}</span>
            <span class="stat-label">Available</span>
          </div>
        </div>
        <div class="last-updated">
          <span class="label">Last Updated:</span>
          <span class="value">{{ formatTime(summary.last_updated) }}</span>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>⚠️ {{ error }}</p>
      <button @click="refreshPorts" class="retry-btn">Retry</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/api'

interface PortInfo {
  port: number
  in_use: boolean
  process_name: string | null
  process_id: number | null
  last_checked: string
}

const loading = ref(false)
const ports = ref<PortInfo[]>([])
const error = ref<string | null>(null)
const killing = ref<number | null>(null)

const overallStatus = computed(() => {
  const inUseCount = ports.value.filter(p => p.in_use).length
  if (inUseCount === 0) {
    return { class: 'all-available', text: 'All Available' }
  } else if (inUseCount === ports.value.length) {
    return { class: 'all-in-use', text: 'All In Use' }
  } else {
    return { class: 'mixed', text: `${inUseCount} In Use` }
  }
})

const summary = computed(() => {
  const totalPorts = ports.value.length
  const inUseCount = ports.value.filter(p => p.in_use).length
  return {
    total_ports: totalPorts,
    in_use_count: inUseCount,
    available_count: totalPorts - inUseCount,
    last_updated: ports.value.length > 0 ? ports.value[0].last_checked : null,
  }
})

async function fetchPorts() {
  loading.value = true
  error.value = null

  try {
    const response = await api.get('/api/v1/ports')
    ports.value = response.data.ports
  } catch (err) {
    console.error('Failed to fetch port status:', err)
    error.value = 'Failed to fetch port status. Please try again.'
  } finally {
    loading.value = false
  }
}

async function killProcess(port: number) {
  killing.value = port

  try {
    const response = await api.post(`/api/v1/ports/${port}/kill`)

    if (response.data.status === 'success') {
      await fetchPorts() // Refresh after killing
    } else {
      alert('Failed to kill process. Please try again.')
    }
  } catch (err) {
    console.error('Failed to kill process:', err)
    alert('Error killing process. Please try again.')
  } finally {
    killing.value = null
  }
}

function formatTime(timeString: string): string {
  if (!timeString) return 'Never'

  const date = new Date(timeString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSeconds = Math.floor(diffMs / 1000)

  if (diffSeconds < 60) {
    return `${diffSeconds}s ago`
  } else if (diffSeconds < 3600) {
    const minutes = Math.floor(diffSeconds / 60)
    return `${minutes}m ago`
  } else {
    const hours = Math.floor(diffSeconds / 3600)
    return `${hours}h ago`
  }
}

async function refreshPorts() {
  await fetchPorts()
}

let refreshInterval: number | null = null

onMounted(async () => {
  await fetchPorts()
  
  // Auto-refresh every 5 seconds
  refreshInterval = window.setInterval(async () => {
    await fetchPorts()
  }, 5000) as unknown as number
})

onUnmounted(() => {
  if (refreshInterval !== null) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.port-monitor {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
}

header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.refresh-btn {
  padding: 10px 20px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #3a7bc8;
}

.refresh-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-badge.all-available {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.mixed {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.all-in-use {
  background-color: #f8d7da;
  color: #721c24;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #42b883;
  border-top: 4px solid #42b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.port-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.port-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s, transform 0.2s;
}

.port-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.port-card.in-use {
  border-left: 4px solid #dc3545;
}

.port-card.available {
  border-left: 4px solid #28a745;
}

.port-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.port-number {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.port-status {
  font-size: 1rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 6px;
}

.status-in-use {
  background-color: #fee2e2;
  color: white;
}

.status-available {
  background-color: #d4edda;
  color: white;
}

.port-details {
  font-size: 0.9rem;
}

.info-item {
  display: flex;
  margin-bottom: 8px;
  gap: 10px;
}

.info-item .label {
  font-weight: 600;
  color: #666;
  min-width: 80px;
}

.info-item .value {
  color: #333;
}

.actions {
  margin-top: 15px;
}

.kill-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.kill-btn:hover:not(:disabled) {
  background-color: #c82333;
  transform: scale(1.05);
}

.kill-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.summary {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat {
  text-align: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #42b883;
  display: block;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
}

.last-updated {
  grid-column: span 3;
  text-align: center;
  padding: 10px;
  background-color: #e9ecef;
  border-radius: 6px;
}

.last-updated .label {
  font-weight: 600;
  color: #666;
}

.last-updated .value {
  color: #333;
}

.error-message {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.error-message p {
  margin: 0 0 15px;
  color: #721c24;
  font-weight: 600;
}

.retry-btn {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #3a7bc8;
}
</style>
