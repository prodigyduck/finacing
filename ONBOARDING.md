# ONBOARDING — Financing 프로젝트

## 1. 프로젝트 개요

Financing은 Obsidian 로컬 마크다운 파일(`투자.md`)에서 포트폴리오 가치 기록을 읽어 시계열 추이를 분석·시각화하는 투자 대시보드입니다. 백엔드는 Python/FastAPI로 Clean Architecture를 따르고, 프론트엔드는 Vue.js 3 + ECharts로 차트를 렌더링합니다. 인증 없이 로컬에서만 동작하는 개인 도구입니다.

## 2. 디렉토리 구조

```
financing/
├── src/                          # Python 백엔드
│   ├── domain/entities/          # 핵심 비즈니스 객체 (의존성 없음)
│   ├── application/use_cases/    # 도메인 객체를 조율하는 유스케이스
│   ├── infrastructure/parsers/   # 외부 데이터(Obsidian)를 도메인으로 변환
│   ├── config/                   # 로깅 등 애플리케이션 설정
│   └── presentation/             # FastAPI REST API
├── frontend/src/                 # Vue.js 프론트엔드
│   ├── api/                      # Axios로 백엔드 API 호출
│   ├── components/               # ECharts 차트 컴포넌트
│   ├── plugins/                  # Vuetify 테마 설정
│   ├── stores/                   # Pinia 상태 관리
│   ├── router/                   # Vue Router
│   └── views/                    # 페이지 단위 컴포넌트
├── tests/
│   ├── unit/                     # 도메인, 애플리케이션, 인프라 단위 테스트
│   └── e2e/                      # Playwright 브라우저 테스트
├── scripts/                      # pre-commit hook 등
├── docs/                         # 설계, 보안, 신뢰성 등 문서
├── start.sh                      # 백엔드+프론트엔드 동시 실행
└── pyproject.toml                # Python 의존성 및 도구 설정
```

### 의존성 방향

```
Presentation → Application → Domain ← Infrastructure
```

Presentation과 Infrastructure는 Domain 방향으로만 의존합니다. Domain은 외부 의존성이 없습니다.

## 3. 핵심 파일 5개

| 파일 | 역할 |
|------|------|
| `src/domain/entities/portfolio_history.py` | 시계열 레코드 컬렉션. 최신값, 변화량, 수익률 계산 |
| `src/application/use_cases/analyze_history.py` | 선형 회귀로 3/6/12개월 포트폴리오 가치 예측 |
| `src/domain/entities/investment_record.py` | 날짜+금액(억) 불변 엔티티, 음수 검증 |
| `src/infrastructure/parsers/obsidian_parser.py` | Obsidian 마크다운(`M.DD 억`)을 도메인 객체로 파싱 |
| `src/presentation/app.py` | FastAPI 엔드포인트. 파서→유스케이스→JSON 응답 연결 |

## 4. 주요 코드 흐름

```
사용자가 브라우저에서 http://localhost:5180 접속
    ↓
Vue.js Dashboard → Pinia store → Axios GET /api/v1/history
    ↓
FastAPI (app.py) → ObsidianParser.parse()
    ↓  ~/git/obsidian/투자/투자.md 읽기
PortfolioHistory (도메인 객체 생성)
    ↓
AnalyzeHistory.execute()
    ↓  선형 회귀 분석 + 3/6/12개월 예측값 계산
JSON 응답 { records, projections, latest, return_rate, ... }
    ↓
PortfolioChart.vue (ECharts)
    ↓  실제 데이터 라인 + 추세선(점선) 렌더링
```

## 5. 개발 시작하기

### 필수 조건

- Python 3.11+
- Node.js 18+
- Obsidian vault에 `~/git/obsidian/투자/투자.md` 파일 존재

### 설치

```bash
# 백엔드
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 프론트엔드
cd frontend
npm install
cd ..
```

### 실행

```bash
./start.sh
# Backend:  http://localhost:8000
# Frontend: http://localhost:5180
```

### 테스트

```bash
# 단위 테스트
source .venv/bin/activate && pytest tests/unit/ -v

# E2E 테스트 (서버 실행 중일 때)
source .venv/bin/activate && pytest tests/e2e/ -v --no-cov

# 프론트엔드 타입 체크
cd frontend && npx vue-tsc --noEmit

# 프론트엔드 빌드
cd frontend && npx vite build
```

### 코드 품질

```bash
black src tests          # 포맷팅
ruff check src tests     # 린트
mypy src                 # 타입 체크
```
