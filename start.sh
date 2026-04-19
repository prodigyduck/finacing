#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[financing]${NC} $1"; }
warn() { echo -e "${YELLOW}[financing]${NC} $1"; }
err()  { echo -e "${RED}[financing]${NC} $1" >&2; }

cleanup() {
    warn "Shutting down..."
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
    wait 2>/dev/null
    log "Done."
    exit 0
}
trap cleanup SIGINT SIGTERM

# --- Backend ---
log "Starting backend (FastAPI on :8000)..."
(
    source "$VENV_DIR/bin/activate"
    exec python -m uvicorn src.presentation.app:app --host 0.0.0.0 --port 8000 --reload
) &
BACKEND_PID=$!

# Wait for backend
for i in $(seq 1 15); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log "Backend ready."
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    err "Backend failed to start."
    cleanup
fi

# --- Frontend ---
log "Starting frontend (Vite on :5180)..."
(
    cd "$FRONTEND_DIR"
    exec npx vite --host 0.0.0.0 --port 5180
) &
FRONTEND_PID=$!

# Wait for frontend
for i in $(seq 1 15); do
    if curl -s http://localhost:5180 > /dev/null 2>&1; then
        log "Frontend ready."
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:5180 > /dev/null 2>&1; then
    err "Frontend failed to start."
    cleanup
fi

echo ""
log "========================================="
log "  Backend:  http://localhost:8000"
log "  Frontend: http://localhost:5180"
log "  API Docs: http://localhost:8000/docs"
log "========================================="
echo ""
log "Press Ctrl+C to stop."

wait
