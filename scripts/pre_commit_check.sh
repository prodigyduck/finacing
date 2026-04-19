#!/bin/bash
# Pre-commit smoke test for Financing project
# Runs before every commit to verify Obsidian data, backend, and frontend

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

PASS=0
FAIL=0

green() { printf "\033[32m[PASS]\033[0m %s\n" "$1"; PASS=$((PASS+1)); }
red()   { printf "\033[31m[FAIL]\033[0m %s\n" "$1"; FAIL=$((FAIL+1)); }
info()  { printf "\n>>> %s\n" "$1"; }

# ── 1. Obsidian data file exists ─────────────────────────────────────
info "1. Obsidian 투자 데이터 확인"

OBSIDIAN_PATH="${OBSIDIAN_VAULT_PATH:-$HOME/git/obsidian}"
INVESTMENT_FILE="$OBSIDIAN_PATH/투자/투자.md"

if [ -f "$INVESTMENT_FILE" ]; then
    RECORD_COUNT=$(grep -cE '^[0-9]+\.[0-9]+\s+[0-9]+\.?[0-9]*\s*$' "$INVESTMENT_FILE" || echo "0")
    green "투자 데이터 확인 (${RECORD_COUNT}개 레코드)"
else
    red "투자 파일 없음: $INVESTMENT_FILE"
fi

# ── 2. Backend health check ─────────────────────────────────────────
info "2. 백엔드 health check"

HEALTH=$(curl -s --max-time 5 http://localhost:8000/health 2>/dev/null || echo "")
if echo "$HEALTH" | grep -q "healthy"; then
    green "백엔드 실행 중 (health=healthy)"
else
    red "백엔드가 실행 중이 아닙니다. 먼저 ./start.sh 를 실행하세요."
fi

# ── 3. History API returns data ──────────────────────────────────────
info "3. /api/v1/history 엔드포인트 확인"

HISTORY_RESP=$(curl -s --max-time 10 http://localhost:8000/api/v1/history 2>/dev/null || echo "")
if echo "$HISTORY_RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
count = d.get('record_count', 0)
if count == 0:
    print('  레코드 0개')
    sys.exit(1)
latest = d.get('latest', {})
print(f'  {count}개 레코드, 최신: {latest.get(\"amount\", \"?\")}억')
" 2>&1; then
    green "History API 정상 응답"
else
    red "History API 응답 오류"
fi

# ── 4. Frontend dev server check ───────────────────────────────────
info "4. 프론트엔드 서버 확인"

FRONTEND=$(curl -s --max-time 5 http://localhost:5180/ 2>/dev/null || echo "")
if echo "$FRONTEND" | grep -qi "html\|vite\|vue\|financing"; then
    green "프론트엔드 서버 실행 중 (:5180)"
else
    red "프론트엔드 서버 응답 없음"
fi

# ── 5. Python tests ─────────────────────────────────────────────────
info "5. 단위 테스트 실행"

if [ -d "venv" ] || [ -d ".venv" ]; then
    VENV=".venv"
    [ -d "venv" ] && VENV="venv"
    TEST_OUTPUT=$(source "$VENV/bin/activate" && python -m pytest tests/unit/ -q --no-header --tb=short 2>&1)
    TEST_EXIT=$?
    if [ $TEST_EXIT -eq 0 ]; then
        green "단위 테스트 통과"
    else
        red "단위 테스트 실패"
        echo "$TEST_OUTPUT" | tail -20
    fi
else
    red "venv 없음 - 테스트 불가"
fi

# ── Summary ─────────────────────────────────────────────────────────
echo ""
echo "========================================"
printf "\033[32mPASS: %d\033[0m  \033[31mFAIL: %d\033[0m\n" "$PASS" "$FAIL"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "검증 실패. 커밋을 중단합니다."
    echo "   실패 항목을 수정한 후 다시 커밋하세요."
    exit 1
fi

echo ""
echo "모든 검증 통과. 커밋을 진행합니다."
exit 0
