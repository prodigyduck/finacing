<template>
  <div id="app">
    <nav class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-icon">W</span>
        <span class="brand-text">Financing</span>
      </div>
      <div class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
          <span>Dashboard</span>
        </router-link>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --sidebar-width: 220px;
  --bg-primary: #f5f5f7;
  --bg-card: #ffffff;
  --bg-sidebar: rgba(255, 255, 255, 0.72);
  --bg-sidebar-hover: rgba(0, 0, 0, 0.04);
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  --text-tertiary: #86868b;
  --accent: #007AFF;
  --accent-light: rgba(0, 122, 255, 0.1);
  --green: #34C759;
  --orange: #FF9500;
  --red: #FF3B30;
  --border: rgba(0, 0, 0, 0.06);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
  --radius: 12px;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app { display: flex; min-height: 100vh; }

.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-sidebar);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid var(--border);
  padding: 20px 12px;
  position: fixed; top: 0; left: 0; bottom: 0;
  display: flex; flex-direction: column; z-index: 100;
}

.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 8px 12px; margin-bottom: 24px; }
.brand-icon {
  width: 32px; height: 32px; background: linear-gradient(135deg, var(--accent), #5856D6);
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; font-size: 16px;
}
.brand-text { font-size: 17px; font-weight: 600; color: var(--text-primary); }

.sidebar-nav { display: flex; flex-direction: column; gap: 2px; }
.nav-item {
  display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px;
  text-decoration: none; color: var(--text-secondary); font-size: 14px; font-weight: 500;
  transition: all 0.15s ease;
}
.nav-item:hover { background: var(--bg-sidebar-hover); color: var(--text-primary); }
.nav-item.active { background: var(--accent-light); color: var(--accent); }

.main-content { margin-left: var(--sidebar-width); flex: 1; padding: 32px; max-width: calc(100vw - var(--sidebar-width)); }
</style>
