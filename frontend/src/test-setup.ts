import { config } from '@vue/test-utils'
import { createVuetify } from 'vuetify'

// Vuetify plugin for tests
const vuetify = createVuetify()

config.global.plugins = [vuetify]
