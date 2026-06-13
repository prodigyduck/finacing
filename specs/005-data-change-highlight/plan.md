# Implementation Plan: Data Change Highlight

**Branch**: `005-data-change-highlight` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)

## Summary

전일 대비 증감 표시, 기간 선택(일별/주별/월별), 요약 정보 상단 표시 기능을 추가한다. 프론트엔드에서 증감 계산, 기간 필터링, 요약 바 컴포넌트를 구현하며, 백엔드 API는 기존을 그대로 사용한다.

## Technical Context

**Language/Version**: TypeScript/JavaScript (ES2022+), Python 3.11+

**Primary Dependencies**: Vue.js 3, ECharts, Vuetify, Vite, Vitest

**Storage**: Obsidian markdown files - 기존 유지

**Testing**: Vitest, Playwright

**Target Platform**: Local web application

**Project Type**: Web service (FastAPI + Vue.js SPA)

**Performance Goals**: 증감 계산 100ms, 기간 전환 300ms

**Constraints**: Clean Architecture 유지, 백엔드 API 변경 없음

**Scale/Scope**: 최대 10개 계좌, 10년 데이터

## Constitution Check

**Status**: ✅ ALL PASSED - 프론트엔드만 수정

## Project Structure

```text
frontend/src/
├── components/
│   ├── ChangeIndicator.vue       # 증감 아이콘 + 색상
│   ├── PeriodSelector.vue         # 기간 선택 탭
│   └── SummaryBar.vue             # 상단 요약 바
├── composables/
│   ├── useChangeCalculation.ts    # 증감 계산
│   └── usePeriodFilter.ts         # 기간 필터링
└── utils/
    └── dateHelpers.ts             # 날짜 집계 헬퍼
```

## Phase 0: Research

- 전일 대비 계산: 직전 영업일 찾기
- 주별/월별 집계: 마지막 날짜 기준
- Vue.js Composables: 로직 재사용
- 색맹 친화: 아이콘 + 텍스트 라벨

## Phase 1: Design

### Data Model

```typescript
interface ChangeInfo {
  amount: number;
  percentage: number;
  type: 'increase' | 'decrease' | 'neutral';
  icon: '🔺' | '🔻' | '−';
  color: string;
}

interface PeriodFilter {
  type: 'daily' | 'weekly' | 'monthly';
}
```

## Constitution Check (Post-Design)

**Status**: ✅ ALL PASSED
