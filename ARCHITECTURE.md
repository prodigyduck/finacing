# ARCHITECTURE

## Overview

Financing은 **Clean Architecture** 원칙을 따르는 Obsidian 기반 투자 대시보드입니다.

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                   │
│   Vue.js UI (Dashboard) + FastAPI REST API       │
└─────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────┐
│              Application Layer                    │
│   Use Cases (AnalyzeHistory — 추세 분석 + 예측) │
└─────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────┐
│              Domain Layer                         │
│   Entities (InvestmentRecord, PortfolioHistory)   │
└─────────────────────────────────────────────────┘
                        ▲
┌─────────────────────────────────────────────────┐
│           Infrastructure Layer                    │
│   ObsidianParser (로컬 마크다운 파일 파싱)       │
└─────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer (`src/domain/`)

핵심 비즈니스 로직. 외부 의존성 없음.

- **InvestmentRecord**: 날짜 + 금액(억) 불변 값
- **PortfolioHistory**: 시계열 레코드 컬렉션 (최신값, 변화량, 수익률 계산)

### 2. Application Layer (`src/application/`)

도메인 객체를 조율하는 유스케이스.

- **AnalyzeHistory**: 시계열 분석 + 선형 회귀 기반 3/6/12개월 예측

### 3. Infrastructure Layer (`src/infrastructure/`)

외부 시스템과의 연동.

- **ObsidianParser**: `투자.md` 파일을 파싱하여 `PortfolioHistory` 생성

### 4. Presentation Layer (`src/presentation/`)

사용자 인터페이스.

- **FastAPI**: `GET /api/v1/history` 엔드포인트
- **Vue.js**: 시계열 라인 차트 + 추세선 대시보드 (ECharts)

### 5. Config Layer (`src/config/`)

애플리케이션 설정.

- **logging**: 콘솔 + 파일 로깅 설정

## Dependency Flow

```
Presentation → Application → Domain
                   ↑
Infrastructure ────┘
```

## Data Flow

```
GET /api/v1/history
    ↓
ObsidianParser.parse() → ~/git/obsidian/투자/투자.md 읽기
    ↓
PortfolioHistory (Domain)
    ↓
AnalyzeHistory.execute() → 분석 + 선형 회귀 예측
    ↓
JSON Response (records, projections)
    ↓
Vue.js PortfolioChart (실제 데이터 + 추세선)
```

## Module Structure

```
src/
├── domain/
│   └── entities/
│       ├── investment_record.py
│       └── portfolio_history.py
├── application/
│   └── use_cases/
│       └── analyze_history.py
├── infrastructure/
│   └── parsers/
│       └── obsidian_parser.py
├── config/
│   └── logging.py
└── presentation/
    └── app.py
```

## Testing Strategy

| 계층 | 커버리지 | 방식 |
|------|---------|------|
| Domain | 100% | 순수 단위 테스트 |
| Application | 100% | 단위 테스트 |
| Infrastructure | 90% | 파일 파싱 테스트 |
| E2E | Playwright | 브라우저 자동화 |

## Version History

| 버전 | 날짜 | 변경사항 |
|------|------|---------|
| 1.0.0 | 2026-03-29 | 초기 아키텍처 (Google Keep 기반) |
| 2.0.0 | 2026-04-19 | Obsidian 마이그레이션, 시계열 도메인 재설계 |
| 2.1.0 | 2026-04-25 | 데드 코드 정리, 미사용 모듈 제거 |
