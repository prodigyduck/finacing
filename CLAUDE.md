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

### Python
```bash
black src tests
ruff check src tests
mypy src
```

### Frontend
```bash
npm test          # Vitest 단위 테스트
npm run audit     # npm 보안 감사
npm run audit:fix # 취약성 자동 수정
```

## 하네스 목록

### Code Review

**목표:** 정확성, 보안, 스타일 관점에서 코드를 종합 검토하고 수정을 자동으로 적용

**트리거:** 코드 리뷰 관련 작업 요청 시 `code-review-harness` 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**에이전트 팀:**
- `correctness-reviewer` — 정확성 검토 (버그, 로직, 타입)
- `security-reviewer` — 보안 검토 (취약점, 인가)
- `style-reviewer` — 스타일 검토 (품질, 관용구)
- `fixer` — 수정 적용

### UI/UX Improvement

**목표:** 토스 스타일로 사용자 인터페이스와 사용자 경험을 개선

**트리거:** UI/UX 관련 작업 요청 시 `ui-ux-harness` 스킬을 사용하라. "토스 스타일 UI", "UI 개선", "UX 리디자인", "디자인 수정" 등.

**에이전트 팀:**
- `ux-designer` — UX 분석 및 개선안 설계
- `ui-designer` — 토스 스타일 비주얼 디자인
- `ui-implementer` — Vue.js 구현

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-05-29 | 초기 구성 | 전체 | 코드 리뷰 하네스 신규 구축 |
| 2026-05-29 | UI/UX 하네스 추가 | ui-ux-harness | 토스 스타일 UI/UX 개선 |

---

## 핵심 규칙

**참고:** 현재 구현은 문서화된 Clean Architecture와 부분적으로 다릅니다:
- 실제 의존성: Presentation (app.py) → Infrastructure (ObsidianParser) + Application (AnalyzeHistory) → Domain
- 이상적인 의존성: Presentation → Application → Domain ← Infrastructure
- 추후 리팩토링: Presentation에서 Infrastructure 직접 호출 제거하고 Use Case 통해 간접 접근

- Obsidian 데이터는 읽기 전용, 로컬 파일만 사용
- 인증 없음 — 로컬 전용 도구 (PUT 엔드포인트는 간단한 API key로 보호)
