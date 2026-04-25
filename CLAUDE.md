# CLAUDE.md — Financing Project

## 프로젝트 개요

Financing은 **Obsidian** 로컬 마크다운 파일에서 투자 데이터를 읽어 포트폴리오 가치 추이를 분석·시각화하는 투자 대시보드입니다.

- **데이터 소스**: `~/git/obsidian/투자/투자.md` — `M.DD 억` 형식의 시계열 포트폴리오 가치 기록
- **백엔드**: Python 3.11+ / FastAPI (Clean Architecture)
- **프론트엔드**: Vue.js 3 / TypeScript / ECharts / Vuetify / Vite

## 실행 방법

```bash
./start.sh
# Backend: http://localhost:8000
# Frontend: http://localhost:5180
```

## 구조

```
src/
├── domain/entities/          # InvestmentRecord, PortfolioHistory
├── application/use_cases/    # AnalyzeHistory (선형 회귀 예측 포함)
├── infrastructure/parsers/   # ObsidianParser (투자.md → PortfolioHistory)
├── config/                   # 로깅 설정
└── presentation/             # FastAPI app (GET /api/v1/history)

frontend/src/
├── api/         # Axios → /api/v1/history
├── components/  # PortfolioChart (ECharts 추세선)
├── plugins/     # Vuetify 테마 설정
├── stores/      # Pinia history store
├── router/      # Vue Router (/)
└── views/       # Dashboard.vue

tests/
├── unit/        # domain, application, infrastructure
└── e2e/         # Playwright 브라우저 테스트
```

## API

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /health` | 헬스체크 |
| `GET /api/v1/history?year=2026` | 시계열 데이터 + 3/6/12개월 추세 예측 |

## 테스트

```bash
# 단위 테스트
source .venv/bin/activate && pytest tests/unit/ -v

# E2E 테스트 (서버 실행 중일 때)
source .venv/bin/activate && pytest tests/e2e/ -v --no-cov

# Pre-commit hook
bash scripts/pre_commit_check.sh
```

## 코드 품질

```bash
black src tests
ruff check src tests
mypy src
```

## 핵심 규칙

- Clean Architecture 의존성 방향: Presentation → Application → Domain ← Infrastructure
- Obsidian 데이터는 읽기 전용, 로컬 파일만 사용
- 인증 없음 — 로컬 전용 도구
