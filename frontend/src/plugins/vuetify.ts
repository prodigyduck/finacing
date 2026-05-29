import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

export const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        // Primary — Toss Blue (Brand Color)
        primary: '#00BFFF',
        'primary-light': '#33D9FF',
        'primary-dark': '#0099CC',

        // Semantic Colors
        success: '#00C853',
        error: '#FF3B30',
        warning: '#FF9500',
        info: '#5AC8FA',

        // Backgrounds
        background: '#F8F8F8',
        surface: '#FFFFFF',

        // Text Hierarchy
        'text-primary': '#000000',
        'text-secondary': '#666666',
        'text-tertiary': '#AAAAAA',
        'text-disabled': '#DDDDDD',

        // Data Visualization
        'chart-line': '#00BFFF',
        'chart-projection-3m': '#90EE90',
        'chart-projection-6m': '#FFD700',
        'chart-projection-12m': '#FF6B6B',

        // Dividers & Borders
        divider: 'rgba(0, 0, 0, 0.06)',
        'border-color': 'rgba(0, 0, 0, 0.10)',
      },
    },
  },
  defaults: {
    VCard: {
      borderRadius: '16px',
      elevation: 2,
    },
    VBtn: {
      borderRadius: '12px',
      styleText: 'text-transform: none; letter-spacing: normal;',
    },
    VTextField: {
      borderRadius: '8px',
    },
    VTable: {
      style: 'border-radius: 16px; overflow: hidden;',
    },
  },
})
