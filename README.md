# Financing - Investment Dashboard

Obsidian 로컬 마크다운에서 투자 데이터를 읽어 포트폴리오 가치 추이를 분석·시각화하는 대시보드.

## Tech Stack

**Backend:** Python 3.9+ / FastAPI / Pydantic
**Frontend:** Vue.js 3 / TypeScript / Pinia / Chart.js / Vite

## Getting Started

### 실행

```bash
./start.sh
```

Backend: http://localhost:8000 | Frontend: http://localhost:5180 | API Docs: http://localhost:8000/docs

### 수동 실행

```bash
# Backend
source .venv/bin/activate
python -m uvicorn src.presentation.app:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend && npx vite --host 0.0.0.0 --port 5180
```

### 데이터 소스

`~/git/obsidian/투자/투자.md` 파일에서 `M.DD 억` 형식의 데이터를 읽습니다.

```
1.13 4.4
1.14 4.43
4.17 4.95
```

## Architecture

Clean Architecture (4계층):

```
src/domain/         → InvestmentRecord, PortfolioHistory
src/application/    → AnalyzeHistory (추세 분석 + 예측)
src/infrastructure/ → ObsidianParser
src/presentation/   → FastAPI REST API
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | 헬스체크 |
| GET | `/api/v1/history?year=2026` | 시계열 데이터 + 3/6/12개월 추세 예측 |

### Response Example

```json
{
  "records": [{"date": "2026-01-13", "amount": 4.4}],
  "latest": {"date": "2026-04-17", "amount": 4.95},
  "total_change": 0.55,
  "return_rate": 12.5,
  "projections": [
    {"months": 3, "date": "2026-07-16", "amount": 5.28},
    {"months": 6, "date": "2026-10-14", "amount": 5.68},
    {"months": 12, "date": "2027-04-12", "amount": 6.48}
  ]
}
```

## Testing

```bash
source .venv/bin/activate

# Unit tests
pytest tests/unit/ -v

# E2E tests (requires running servers)
pytest tests/e2e/ -v --no-cov

# All quality checks
black src tests && ruff check src tests && mypy src
```

## Documentation

- [CLAUDE.md](CLAUDE.md) — Claude Code 프로젝트 컨텍스트
- [ARCHITECTURE.md](ARCHITECTURE.md) — 아키텍처 상세
- [AGENTS.md](AGENTS.md) — AI 에이전트 정의
- [PORTS.md](PORTS.md) — 포트 관리 레지스트리
- [CONTRIBUTING.md](CONTRIBUTING.md) — 기여 가이드
