# Process Manager

This script helps manage processes running on development ports.

## Features

- **Port Checking:** Check which processes are using specific ports
- **Process Termination:** Kill processes on specified ports
- **Bulk Cleanup:** Kill processes on multiple ports at once

## Usage

### Check processes on a port

```bash
python scripts/process_manager.py --check-port 5173
python scripts/process_manager.py --check-port 8000
```

### Kill processes on a port

```bash
python scripts/process_manager.py --kill-port 5173
```

### Cleanup multiple ports

```bash
python scripts/process_manager.py --cleanup-ports 5173 8000
```

## Vue.js Instance Management

The Vue.js frontend has built-in single instance management:

**Features:**
1. **Instance Detection:** Checks localStorage for existing instances
2. **User Confirmation:** Prompts user before replacing existing instance
3. **Heartbeat:** Periodic health checks to detect crashed instances
4. **Cleanup:** Automatic cleanup on page unload

**How it works:**
- On startup, Vue.js checks if another instance is running
- If found, shows confirmation dialog
- User can choose to replace or cancel
- Automatically cleans up when page is closed or navigated away

## Manual Process Management

If automatic cleanup fails, use the process manager:

```bash
# Kill frontend process
python scripts/process_manager.py --kill-port 5173

# Kill backend process
python scripts/process_manager.py --kill-port 8000

# Cleanup both
python scripts/process_manager.py --cleanup-ports 5173 8000
```

## Port Management

**Default Ports:**
- Frontend (Vue.js): 5173
- Backend (FastAPI): 8000

**Port Conflicts:**
The system will automatically find available ports if defaults are in use.

**Backend Port Configuration:**
```python
# .env
BACKEND_PORT=8000

# Or run with custom port
python -m src.presentation.app --port 3000
```

**Frontend Port Configuration:**
```typescript
// frontend/vite.config.ts
export default defineConfig({
  server: {
    port: 5173,  // Change this if needed
  }
})
```

Or use environment variable:
```bash
cd frontend
npm run dev -- --port 3000
```

## Troubleshooting

### Multiple instances running

**Symptom:** Multiple Vue.js windows showing same app
**Solution:** The frontend will automatically detect and prompt to close existing instance

### Port already in use

**Symptom:** Error message "Address already in use"
**Solution:**
1. Use process manager to find and kill conflicting process
2. The system will automatically find alternative port

### Instance not responding

**Symptom:** Vue.js app running but not updating
**Solution:**
1. Check browser console for errors
2. Verify backend is running
3. Use health check: http://localhost:8000/health
