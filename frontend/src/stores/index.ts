import { createPinia } from 'pinia'

export const pinia = createPinia()

export { useHistoryStore } from './history'
export { useRawDataStore } from './rawData'
