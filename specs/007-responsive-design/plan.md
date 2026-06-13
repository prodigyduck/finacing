# Implementation Plan: Responsive Design

**Branch**: `007-responsive-design` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)

## Summary

모바일/태블릿/데스크톱 반응형 레이아웃을 구현한다. CSS Grid, Flexbox, 미디어 쿼리를 활용하며, 폰트와 간격을 화면 크기에 맞게 조절한다.

## Technical Context

**Language/Version**: TypeScript/JavaScript (ES2022+), SCSS

**Primary Dependencies**: Vue.js 3, Vuetify, SCSS

**Testing**: Playwright (반응형 테스트)

**Target Platform**: 모바일 (375px+) ~ 데스크톱 (2560px+)

**Project Type**: Web service (SPA)

**Performance Goals**: 레이아웃 재배치 1초 이내

**Constraints**: 최소 375px 지원

**Scale/Scope**: 3단계 반응형 (모바일/태블릿/데스크톱)

## Constitution Check

**Status**: ✅ ALL PASSED

## Project Structure

```text
frontend/src/
├── styles/
│   ├── responsive.scss           # 반응형 스타일
│   └── breakpoints.scss          # 미디어 쿼리 변수
├── components/
│   ├── ResponsiveGrid.vue        # 반응형 그리드
│   └── Sidebar.vue               # 데스크톱 사이드바
└── composables/
    └── useBreakpoints.ts         # 브레이크포인트 hooks
```

## Phase 0: Research

- CSS Grid vs Flexbox: 레이아웃 패턴
- 미디어 쿼리: 모바일 우선 vs 데스크톱 우선
- 폰트 크기: clamp(), 미디어 쿼리

## Phase 1: Design

### Data Model

```typescript
interface Breakpoints {
  mobile: number;    // 375px
  tablet: number;    // 768px
  desktop: number;   // 1920px
}

interface ResponsiveConfig {
  columns: {
    mobile: number;   // 1
    tablet: number;   // 2
    desktop: number;  // 3
  };
  fontSize: {
    mobile: string;   // '12px ~ 14px'
    tablet: string;   // '14px ~ 16px'
    desktop: string;  // '16px ~ 18px'
  };
}
```

## Constitution Check (Post-Design)

**Status**: ✅ ALL PASSED
