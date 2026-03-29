import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { pinia } from './stores'
import './utils/startup'

const app = createApp(App)

app.use(router)
app.use(pinia)

app.mount('#app')
