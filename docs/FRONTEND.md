# Frontend Architecture

## Overview

The Financing project uses **Vue.js 3** with TypeScript as the frontend framework, communicating with a FastAPI backend via REST API. This document outlines frontend architecture, component structure, and UI patterns.

## Technology Stack

- **Framework:** Vue.js 3.4.0+
- **Language:** TypeScript 5.2.0+
- **State Management:** Pinia 2.1.7+
- **Routing:** Vue Router 4.2.5+
- **Build Tool:** Vite 5.0.0+
- **HTTP Client:** Axios 1.6.5+
- **Charts:** Chart.js 4.4.0+

---

## Architecture Overview

### Frontend-Backend Separation

```
User Browser → Vue.js SPA (Frontend)
                   ↓
            REST API Calls (Axios)
                   ↓
         FastAPI Server (Backend)
                   ↓
           Application Layer → Domain Layer
                   ↑
         Infrastructure Layer (Obsidian vault)
```

**Key Characteristics:**
- **Single Page Application:** Vue.js SPA with Vue Router for navigation
- **REST API Communication:** Axios for HTTP requests to FastAPI backend
- **State Management:** Pinia stores for global state (auth, portfolio)
- **Component-Based:** Reusable Vue components for UI elements
- **Type Safety:** TypeScript for compile-time type checking

### Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── index.ts           # Axios HTTP client configuration
│   ├── components/
│   │   ├── PieChart.vue        # Asset allocation pie chart
│   │   └── BarChart.vue        # Asset allocation bar chart
│   ├── router/
│   │   └── index.ts           # Vue Router configuration
│   ├── stores/
│   │   ├── index.ts           # Pinia store initialization
│   │   ├── auth.ts           # Authentication state
│   │   └── portfolio.ts      # Portfolio data state
│   ├── views/
│   │   ├── Dashboard.vue       # Dashboard page
│   │   └── Settings.vue       # Settings page
│   ├── App.vue               # Root Vue component
│   └── main.ts              # Application entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

---

## Component Architecture

### Main Application (`App.vue`)

**Responsibilities:**
- Render router-view for page navigation
- Apply global styles

### Views

#### Dashboard View (`Dashboard.vue`)

**Responsibilities:**
- Display portfolio overview
- Visualize asset allocation
- Show asset details table
- Fetch portfolio data from API

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  Header: Title + Navigation           │
├─────────────────────────────────────────┤
│  Auth Warning (if not authenticated) │
├─────────────────────────────────────────┤
│  Fetch Button                         │
├─────────────────────────────────────────┤
│  Overview Cards (Total Value, Count)  │
├─────────────────────────────────────────┤
│  Charts (Pie Chart, Bar Chart)        │
├─────────────────────────────────────────┤
│  Asset Table                         │
└─────────────────────────────────────────┘
```

#### Settings View (`Settings.vue`)

**Responsibilities:**
- Configure Obsidian vault path
- Display connection status
- Provide environment variable instructions

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  Header: Title + Back Link          │
├─────────────────────────────────────────┤
│  Info Box (Authentication guide)     │
├─────────────────────────────────────────┤
│  Form (Email, Password, Label)      │
├─────────────────────────────────────────┤
│  Submit Button                       │
├─────────────────────────────────────────┤
│  Status Message (Success/Error)      │
├─────────────────────────────────────────┤
│  Environment Variables Info           │
└─────────────────────────────────────────┘
```

### Chart Components

#### Pie Chart (`PieChart.vue`)

**Responsibilities:**
- Render pie chart for asset type distribution
- Handle data updates reactively

**Props:**
```typescript
interface Props {
  data: { type: string; ratio: number }[]
}
```

#### Bar Chart (`BarChart.vue`)

**Responsibilities:**
- Render bar chart for asset allocation
- Handle data updates reactively

**Props:**
```typescript
interface Props {
  data: { name: string; ratio: number }[]
}
```

---

## State Management

### Pinia Stores

#### Auth Store (`stores/auth.ts`)

**State:**
- `isAuthenticated`: Boolean flag for authentication status
- `email`: User email (if authenticated)

**Actions:**
- `authenticate(email, password)`: Authenticate with backend
- `logout()`: Clear authentication state

**Computed:**
- `needsAuth`: Whether authentication is required

#### Portfolio Store (`stores/portfolio.ts`)

**State:**
- `portfolio`: Portfolio data object (null if not loaded)
- `loading`: Loading state flag
- `error`: Error message (null if no error)

**Actions:**
- `fetchPortfolio(label)`: Fetch portfolio data from API
- `clear()`: Clear portfolio data

---

## API Communication

### Axios Client (`api/index.ts`)

**Configuration:**
- Base URL: `http://localhost:8000`
- Default headers: `Content-Type: application/json`
- Methods: GET, POST, PUT, DELETE

**Usage:**
```typescript
import api from '@/api'

// GET request
const response = await api.get('/api/v1/portfolio')

// POST request
const response = await api.post('/api/v1/auth', { email, password })
```

---

## Routing

### Vue Router (`router/index.ts`)

**Routes:**
- `/` → Dashboard
- `/settings` → Settings

**Navigation:**
```typescript
import { useRouter } from 'vue-router'

const router = useRouter()
router.push('/settings')
```

---

## Development

### Running Development Server

```bash
cd frontend
npm install
npm run dev
```

**Access:** http://localhost:5173

### API Proxy

Vite configuration proxies `/api` requests to FastAPI backend:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## Building for Production

```bash
cd frontend
npm run build
```

**Output:** `frontend/dist/`

---

## Type Safety

### TypeScript Configuration

- **Strict Mode:** Enabled
- **No Unused Locals:** Enforced
- **No Unused Parameters:** Enforced
- **Path Aliases:** `@/` → `./src/`

### Component Props

All component props use TypeScript interfaces:

```typescript
interface Props {
  data: Asset[]
  loading: boolean
}

const props = defineProps<Props>()
```

---

## Styling

### Scoped Styles

Each Vue component uses scoped styles to prevent CSS leakage:

```vue
<style scoped>
.dashboard {
  /* Component-specific styles */
}
</style>
```

### CSS Variables

No global CSS variables currently. Component-specific styles used.

---

## Testing

### Unit Testing

**Framework:** Vitest (planned, not yet implemented)

**Test Coverage Goal:** 70% for frontend

### E2E Testing

**Framework:** Not yet implemented

---

## Deployment

### Development

**Frontend:** Vite dev server on port 5173
**Backend:** FastAPI with Uvicorn on port 8000

### Production

**Frontend:** Build with `npm run build`, serve with nginx
**Backend:** Run with Uvicorn production server

```bash
# Backend
uvicorn src.presentation.app:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
# Serve dist/ with nginx or static file server
```

---

## Best Practices

1. **Component Modularity:** Small, reusable components
2. **Type Safety:** Use TypeScript for all components and props
3. **State Isolation:** Use Pinia stores for global state
4. **Error Handling:** Catch and display API errors gracefully
5. **Loading States:** Show loading indicators during data fetching
6. **Responsive Design:** CSS Grid and Flexbox for responsive layouts
7. **Code Organization:** Clear separation of concerns (views, components, stores, api)

---

## Migration from Streamlit

### Key Changes

1. **Architecture:** Streamlit → Vue.js SPA + FastAPI REST API
2. **State:** Streamlit Session State → Pinia stores
3. **UI Components:** Streamlit widgets → Vue.js components
4. **Charts:** Plotly → Chart.js
5. **HTTP:** Streamlit built-in → Axios + FastAPI
6. **Routing:** Streamlit sidebar → Vue Router

### Benefits

- **Better UX:** True SPA with smooth navigation
- **Type Safety:** TypeScript throughout
- **State Management:** Explicit Pinia stores
- **Separation:** Clear frontend/backend separation
- **Scalability:** Easier to scale with proper architecture

---

## References

- [Vue.js Documentation](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Chart.js Documentation](https://www.chartjs.org/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial Vue.js frontend documentation (migrated from Streamlit) |
