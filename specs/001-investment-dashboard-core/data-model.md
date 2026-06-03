# 데이터 모델 (data-model.md)

## 엔티티 및 구조

### Data Format (Input)
- `YYYY.MM.DD 억`

### AverageRecord (Application Domain)
- `date`: string (YYYY-MM-DD)
- `amount`: float
- `period`: string (day/week/month)
- `label`: string (X축 표시용 레이블 - e.g., '1월', '3주')

### AnalysisResult
- `records`: List[AverageRecord]
- `summary`: dict (total_change, return_rate)
