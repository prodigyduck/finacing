<template>
  <div class="dashboard">
    <header>
      <h1>💰 Financing - Investment Dashboard</h1>
      <nav>
        <router-link to="/" active-class="active">Dashboard</router-link>
        <router-link to="/settings" active-class="active">Settings</router-link>
      </nav>
    </header>

    <main>
      <div v-if="authStore.needsAuth" class="auth-warning">
        <p>⚠️ Please configure Google Keep authentication in Settings page.</p>
        <router-link to="/settings">Go to Settings</router-link>
      </div>

      <div v-else>
        <button @click="fetchData" :disabled="loading">
          {{ loading ? 'Loading...' : '📥 Fetch Data from Google Keep' }}
        </button>

        <div v-if="portfolioStore.portfolio" class="portfolio-content">
          <section class="overview">
            <div class="metric">
              <h2>Total Assets</h2>
              <p class="value">
                {{ formatCurrency(portfolioStore.portfolio.total_value) }}
              </p>
            </div>
            <div class="metric">
              <h2>Asset Count</h2>
              <p class="value">{{ portfolioStore.portfolio.asset_count }}</p>
            </div>
          </section>

          <section class="charts">
            <div class="chart-container">
              <h2>Asset Type Distribution</h2>
              <PieChart :data="allocationData" />
            </div>
            <div class="chart-container">
              <h2>Asset Allocation</h2>
              <BarChart :data="assetsData" />
            </div>
          </section>

          <section class="asset-table">
            <h2>Asset Details</h2>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Total Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="asset in portfolioStore.portfolio.assets" :key="asset.name">
                  <td>{{ asset.name }}</td>
                  <td>{{ asset.type }}</td>
                  <td>{{ formatNumber(asset.quantity) }}</td>
                  <td>{{ formatCurrency(asset.unit_price) }}</td>
                  <td>{{ formatCurrency(asset.total_value) }}</td>
                </tr>
              </tbody>
            </table>
          </section>
        </div>

        <div v-else-if="!loading" class="no-data">
          <p>📊 Dashboard will be displayed after fetching data.</p>
        </div>

        <div v-if="error" class="error">
          <p>❌ {{ error }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, usePortfolioStore } from '@/stores'
import PieChart from '@/components/PieChart.vue'
import BarChart from '@/components/BarChart.vue'

const router = useRouter()
const authStore = useAuthStore()
const portfolioStore = usePortfolioStore()

const loading = computed(() => portfolioStore.loading)
const error = computed(() => portfolioStore.error)

const allocationData = computed(() => {
  if (!portfolioStore.portfolio) return []
  return Object.entries(portfolioStore.portfolio.allocation).map(([type, ratio]) => ({
    type,
    ratio
  }))
})

const assetsData = computed(() => {
  if (!portfolioStore.portfolio) return []
  return portfolioStore.portfolio.assets.map(asset => ({
    name: asset.name,
    ratio: (asset.total_value.amount / portfolioStore.portfolio.total_value.amount) * 100
  }))
})

function formatCurrency(value: { amount: number; currency: string }): string {
  return `${value.amount.toLocaleString()} ${value.currency}`
}

function formatNumber(num: number): string {
  return num.toLocaleString()
}

async function fetchData() {
  await portfolioStore.fetchPortfolio()
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  text-decoration: none;
  color: #333;
  padding: 8px 16px;
  border-radius: 4px;
}

nav a.active {
  background-color: #42b883;
  color: white;
}

.auth-warning {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric h2 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #666;
}

.metric .value {
  font-size: 2rem;
  font-weight: bold;
  color: #42b883;
}

.charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-container h2 {
  margin: 0 0 20px;
  font-size: 1.2rem;
  color: #333;
}

button {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.asset-table table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.asset-table th,
.asset-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.asset-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.no-data,
.error {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>
