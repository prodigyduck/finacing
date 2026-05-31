import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

// Toss-inspired design tokens
const tossColors = {
  // Brand Colors
  primary: '#00BFFF',
  'primary-light': '#33D9FF',
  'primary-dark': '#0099CC',

  // Semantic Colors (Korean stock market: Red=Up, Green=Down)
  success: '#00C853',  // Green (하락)
  error: '#FF3B30',    // Red (상승)
  warning: '#FF9500',
  info: '#5AC8FA',

  // Neutrals
  'gray-50': '#FAFAFA',
  'gray-100': '#F5F5F5',
  'gray-200': '#EEEEEE',
  'gray-300': '#E0E0E0',
  'gray-400': '#BDBDBD',
  'gray-500': '#9E9E9E',
  'gray-600': '#757575',
  'gray-700': '#616161',
  'gray-800': '#424242',
  'gray-900': '#212121',
}

export const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          ...tossColors,
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
      dark: {
        colors: {
          ...tossColors,
          background: '#121212',
          surface: '#1E1E1E',

          // Text Hierarchy (Dark Mode)
          'text-primary': '#FFFFFF',
          'text-secondary': '#B0B0B0',
          'text-tertiary': '#757575',
          'text-disabled': '#424242',

          // Data Visualization (Dark Mode)
          'chart-line': '#33D9FF',
          'chart-projection-3m': '#66BB6A',
          'chart-projection-6m': '#FFA726',
          'chart-projection-12m': '#EF5350',

          // Dividers & Borders (Dark Mode)
          divider: 'rgba(255, 255, 255, 0.06)',
          'border-color': 'rgba(255, 255, 255, 0.10)',
        },
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
      style: 'text-transform: none; letter-spacing: normal;',
      variant: 'flat',
    },
    VTextField: {
      variant: 'outlined',
      borderRadius: '8px',
    },
    VTable: {
      style: 'border-radius: 16px; overflow: hidden;',
    },
    VChip: {
      borderRadius: '8px',
    },
    VNavigationDrawer: {
      elevation: 2,
    },
    VAppBar: {
      elevation: 0,
      style: 'border-bottom: 1px solid rgba(0, 0, 0, 0.06);',
    },
  },
})
