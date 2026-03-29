<template>
  <div class="settings">
    <header>
      <h1>⚙️ Settings</h1>
      <router-link to="/" active-class="active">Back to Dashboard</router-link>
    </header>

    <main>
      <section class="auth-section">
        <h2>Google Keep Authentication</h2>

        <div class="info-box">
          <h3>Google Keep Authentication</h3>
          <ul>
            <li>Google account email</li>
            <li>Google account password or app password</li>
            <li>Generate app password if 2FA is enabled</li>
          </ul>
          <a href="https://support.google.com/accounts/answer/185833" target="_blank">
            How to generate app password
          </a>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="credentials.email"
              type="email"
              placeholder="your_email@gmail.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="App password"
              required
            />
          </div>

          <div class="form-group">
            <label for="label">Label</label>
            <input
              id="label"
              v-model="credentials.label"
              type="text"
              placeholder="투자"
            />
          </div>

          <button type="submit" :disabled="loading">
            {{ loading ? 'Authenticating...' : 'Save & Authenticate' }}
          </button>
        </form>

        <div v-if="message" :class="['message', message.type]">
          {{ message.text }}
        </div>
      </section>

      <section class="env-info">
        <h2>📁 Environment Variables File</h2>
        <p v-if="envFileExists">✅ Environment file exists</p>
        <p v-else>⚠️ Environment file not found</p>
        <p>
          Copy <code>.env.example</code> to <code>.env</code> and configure your settings.
        </p>

        <pre><code>GOOGLE_KEEP_EMAIL=your_email@gmail.com
GOOGLE_KEEP_PASSWORD=your_app_password
GOOGLE_KEEP_LABEL=투자</code></pre>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  email: '',
  password: '',
  label: '투자'
})

const loading = ref(false)
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)
const envFileExists = ref(true)

async function handleLogin() {
  loading.value = true
  message.value = null

  try {
    const result = await authStore.authenticate(credentials.value)

    if (result.success) {
      message.value = { type: 'success', text: '✅ Authentication successful!' }
      setTimeout(() => {
        router.push('/')
      }, 1000)
    } else {
      message.value = { type: 'error', text: `❌ Authentication failed: ${result.error}` }
    }
  } catch (error) {
    message.value = { type: 'error', text: '❌ An error occurred during authentication' }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

a {
  text-decoration: none;
  color: #42b883;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid #42b883;
}

.auth-section {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.info-box {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.info-box h3 {
  margin-top: 0;
  color: #333;
}

.info-box ul {
  margin: 15px 0;
  padding-left: 20px;
}

.info-box li {
  margin-bottom: 8px;
}

.info-box a {
  color: #42b883;
  text-decoration: underline;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #42b883;
}

button {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 600;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.message {
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
  font-weight: 600;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
}

.env-info {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.env-info pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
}

.env-info code {
  font-family: monospace;
  color: #333;
}
</style>
