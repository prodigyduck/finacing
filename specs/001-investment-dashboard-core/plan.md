# 구현 계획: 수익률 트렌드 차트 X축 시각화 개선

**브랜치**: `001-investment-dashboard-core` | **날짜**: 2026-05-31 | **명세**: [링크](specs/001-investment-dashboard-core/spec.md)

**입력**: 수익률 트렌드 차트의 일/주/월별 X축 표시 개선 및 평균화 로직 구현

## 요약

일별/주별/월별 차트에서 X축 값을 데이터의 성격(날짜, 주 평균, 월 평균)에 맞게 명확하게 표시하도록 시각화 로직을 개선합니다.

## 기술적 맥락

**언어/버전**: Python 3.11+, Vue.js 3 / TypeScript

**주요 의존성**: FastAPI, ECharts(Vue Wrapper)

**저장소**: Obsidian Markdown (로컬 파일)

**테스트**: Pytest (Backend), Vitest (Frontend)

**대상 플랫폼**: 로컬 웹 환경

**프로젝트 유형**: 웹 서비스 (Dashboard)

**성능 목표**: 차트 렌더링 및 데이터 변환 즉시 반응

**제약사항**: 데이터 파싱 및 가공 로직 내부에 일/주/월별 평균화 로직 구현

**규모/범위**: 포트폴리오 이력 데이터 시각화

## 헌법 검증

*   **코드 품질**: Clean Architecture 준수 및 테스트 코드 작성 필수.
*   **테스트 표준**: 파싱 및 평균화 로직에 대한 단위 테스트 작성.
*   **사용자 경험**: Toss-style의 명확한 차트 레이블링 제공.

## 프로젝트 구조

```text
src/application/analyze_history.py  # 평균화 및 시계열 가공 로직
frontend/src/components/PortfolioChart.vue # ECharts 레이블링 설정
```

**구조 결정**: Backend에서 데이터를 가공하여 프론트엔드로 전달하고, Frontend에서 ECharts 설정을 통해 X축 표시 형식을 제어합니다.
