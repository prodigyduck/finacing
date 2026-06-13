# Implementation Plan: Interactive Features

**Branch**: `006-interactive-features` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)

## Summary

그래프 인터랙션(툴팝, 레전드 클릭, 줌), 계좌 드릴다운(보유 종목 상세), 계좌 비교 모드 기능을 추가한다. ECharts 인터랙션 API와 Vue Router를 활용하며, 백엔드는 기존 API 사용.

## Technical Context

**Language/Version**: TypeScript/JavaScript (ES2022+), Python 3.11+

**Primary Dependencies**: Vue.js 3, ECharts, Vue Router, Vitest

**Testing**: Vitest, Playwright

**Target Platform**: Local web application

**Project Type**: Web service (FastAPI + Vue.js SPA)

**Performance Goals**: 툴팅 100ms, 줌 200ms

**Constraints**: Clean Architecture 유지

**Scale/Scope**: 최대 10개 계좌, 2개 계좌 비교

## Constitution Check

**Status**: ✅ ALL PASSED

## Project Structure

```text
frontend/src/
├── components/
│   ├── ChartTooltip.vue          # 툴팅 컴포넌트
│   ├── AccountDetailModal.vue    # 드릴다운 모달
│   ├── CompareMode.vue           # 비교 모드 UI
│   └── HoldingChart.vue          # 종목별 차트
├── composables/
│   ├── useChartInteraction.ts   # 그래프 인터랙션
│   └── useAccountComparison.ts  # 비교 로직
└── router/
    └── routes.ts                 # 드릴다운 라우트
```

## Phase 0: Research

- ECharts 인터랙션 API: tooltip, legend, dataZoom
- Vue Router 드릴다운: 동적 라우팅
- 비교 로직: 두 계좌 선택, 증감율 계산

## Phase 1: Design

### Data Model

```typescript
interface ChartInteraction {
  tooltip: {
    show: boolean;
    formatter: (params: any) => string;
  };
  legend: {
    selectedMode: 'single' | 'multiple';
  };
  dataZoom: {
    start: number;
    end: number;
  };
}

interface ComparisonData {
  account1: string;
  account2: string;
  period: { start: Date; end: Date };
  difference: number;
  percentage: number;
}
```

## Constitution Check (Post-Design)

**Status**: ✅ ALL PASSED
