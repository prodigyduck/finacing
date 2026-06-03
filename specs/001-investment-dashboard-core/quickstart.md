# 퀵스타트 (quickstart.md)

## 기능 개요
수익률 트렌드 차트의 일/주/월별 X축 표시 개선.

## 개발 가이드
1. `src/application/analyze_history.py`에서 날짜별 그룹화 및 평균 계산 로직 구현.
2. `frontend/src/components/PortfolioChart.vue`에서 ECharts의 `xAxis.axisLabel.formatter`를 사용하여 레이블 표시 방식 정의.
3. API 응답 데이터에 `label` 필드를 추가하여 프론트엔드에서 표시할 값을 명확히 함.
