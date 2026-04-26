import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import RawData from '../views/RawData.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/raw-data',
    name: 'RawData',
    component: RawData,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
