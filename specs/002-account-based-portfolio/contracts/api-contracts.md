# API Contracts: Account-Based Portfolio Tracking

**Feature**: Account-Based Portfolio Tracking
**Date**: 2026-06-03
**Status**: Phase 1 - Complete

---

## Overview

이 문서는 계좌별 포트폴리오 추적 API의 엔드포인트, 요청/응답 형식, 그리고 계약을 정의합니다. 기존 `/api/v1/history` 엔드포인트를 확장하여 계좌별 데이터를 지원합니다.

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Get Portfolio History with Accounts

전체 포트폴리오 및 계좌별 시계열 데이터를 조회합니다.

**Endpoint**:
```
GET /api/v1/history
```

**Query Parameters**:
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| `year` | `integer` | No | 조회 연도 (기본: 현재 연도) | `2026` |
| `account` | `string` | No | 특정 계좌 필터 (기본: 전체) | `증권계좌` |

**Examples**:

```bash
# 전체 포트폴리오 + 모든 계좌 (2026년)
GET /api/v1/history?year=2026

# 특정 계좌만
GET /api/v1/history?year=2026&account=증권계좌
```

---

### 2. Health Check

서버 상태를 확인합니다.

**Endpoint**:
```
GET /health
```

**Response**:
```json
{
  "status": "healthy"
}
```

---

## Response Formats

### Success Response (200 OK)

#### 1. 전체 포트폴리오 (계좌 필터 없음)

```json
{
  "records": [
    {
      "date": "2026-06-03",
      "amount": 5.61
    },
    {
      "date": "2026-05-27",
      "amount": 5.58
    }
  ],
  "latest": {
    "date": "2026-06-03",
    "amount": 5.61
  },
  "earliest": {
    "date": "2025-01-06",
    "amount": 4.52
  },
  "total_change": 1.09,
  "return_rate": 0.241,
  "projections": {
    "3month": {
      "dates": ["2026-06-10", "2026-06-17", ...],
      "amounts": [5.67, 5.73, ...]
    },
    "6month": {
      "dates": ["2026-06-10", "2026-06-17", ...],
      "amounts": [5.70, 5.79, ...]
    },
    "12month": {
      "dates": ["2026-06-10", "2026-06-17", ...],
      "amounts": [5.76, 5.91, ...]
    }
  },
  "accounts": [
    {
      "name": "증권계좌",
      "latest_amount": 3.50,
      "allocation": 0.624,
      "records": [
        {
          "date": "2026-06-03",
          "amount": 3.50
        },
        {
          "date": "2026-05-27",
          "amount": 3.45
        }
      ],
      "projections": {
        "3month": {
          "dates": ["2026-06-10", "2026-06-17", ...],
          "amounts": [3.56, 3.62, ...]
        },
        "6month": {
          "dates": ["2026-06-10", "2026-06-17", ...],
          "amounts": [3.58, 3.66, ...]
        },
        "12month": {
          "dates": ["2026-06-10", "2026-06-17", ...],
          "amounts": [3.61, 3.72, ...]
        }
      },
      "holdings": [
        {
          "name": "삼성전자",
          "quantity": null,
          "value": null
        },
        {
          "name": "NAVER",
          "quantity": null,
          "value": null
        }
      ]
    },
    {
      "name": "ISA",
      "latest_amount": 2.00,
      "allocation": 0.356,
      "records": [
        {
          "date": "2026-06-03",
          "amount": 2.00
        }
      ],
      "projections": {
        "3month": {
          "dates": ["2026-06-10", "2026-06-17", ...],
          "amounts": [2.02, 2.04, ...]
        }
      },
      "holdings": [
        {
          "name": "KB국책주성",
          "quantity": null,
          "value": null
        }
      ]
    },
    {
      "name": "IRA",
      "latest_amount": 0.11,
      "allocation": 0.020,
      "records": [
        {
          "date": "2026-06-03",
          "amount": 0.11
        }
      ],
      "projections": {
        "3month": {
          "dates": ["2026-06-10", "2026-06-17", ...],
          "amounts": [0.11, 0.11, ...]
        }
      },
      "holdings": []
    }
  ],
  "comparison": {
    "best_performer": {
      "name": "ISA",
      "return_rate": 0.350
    },
    "worst_performer": {
      "name": "IRA",
      "return_rate": 0.100
    },
    "allocation_table": [
      {
        "name": "증권계좌",
        "amount": 3.50,
        "allocation": 0.624
      },
      {
        "name": "ISA",
        "amount": 2.00,
        "allocation": 0.356
      },
      {
        "name": "IRA",
        "amount": 0.11,
        "allocation": 0.020
      }
    ]
  }
}
```

#### 2. 특정 계좌 필터

```json
{
  "account": "증권계좌",
  "records": [
    {
      "date": "2026-06-03",
      "amount": 3.50
    },
    {
      "date": "2026-05-27",
      "amount": 3.45
    }
  ],
  "latest": {
    "date": "2026-06-03",
    "amount": 3.50
  },
  "projections": {
    "3month": {
      "dates": ["2026-06-10", "2026-06-17", ...],
      "amounts": [3.56, 3.62, ...]
    }
  },
  "holdings": [
    {
      "name": "삼성전자",
      "quantity": null,
      "value": null
    }
  ]
}
```

---

### Error Responses

#### 400 Bad Request

```json
{
  "detail": "Invalid year parameter"
}
```

#### 404 Not Found

```json
{
  "detail": "Account not found: UnknownAccount"
}
```

#### 500 Internal Server Error

```json
{
  "detail": "Failed to parse investment data"
}
```

---

## Data Types

### Record (시계열 레코드)

```typescript
interface Record {
  date: string;      // ISO 8601 date format (YYYY-MM-DD)
  amount: number;    // Amount in 억 (100 million KRW)
}
```

### Latest/Earliest (최신/최초)

```typescript
interface LatestOrEarliest {
  date: string;
  amount: number;
}
```

### Projections (예측)

```typescript
interface Projections {
  "3month"?: ProjectionData;
  "6month"?: ProjectionData;
  "12month"?: ProjectionData;
}

interface ProjectionData {
  dates: string[];
  amounts: number[];
}
```

### Account (계좌)

```typescript
interface Account {
  name: string;              // 계좌명
  latest_amount: number;     // 최신 총액 (억)
  allocation: number;        // 전체 대비 비중 (0~1)
  records: Record[];         // 시계열 레코드
  projections: Projections;   // 예측 데이터
  holdings: Holding[];       // 보유 종목
}
```

### Holding (보유 종목)

```typescript
interface Holding {
  name: string;           // 종목명
  quantity: number | null; // 수량 (현재 버전에서는 null)
  value: number | null;    // 평가금액 (현재 버전에서는 null)
}
```

### Comparison (비교)

```typescript
interface Comparison {
  best_performer: {
    name: string;
    return_rate: number;
  };
  worst_performer: {
    name: string;
    return_rate: number;
  };
  allocation_table: Array<{
    name: string;
    amount: number;
    allocation: number;
  }>;
}
```

---

## Backward Compatibility

기존 클라이언트가 계좌 데이터를 무시하고 작동할 수 있도록, 다음 필드들은 기존 형식을 유지합니다:

- `records`: 전체 합계 시계열 (필수)
- `latest`: 최신 전체 합계 (필수)
- `earliest`: 최초 전체 합계 (필수)
- `total_change`: 전체 증가액 (필수)
- `return_rate`: 전체 수익률 (필수)
- `projections`: 전체 예측 (필수)

**새로운 필드** (선택사항):
- `accounts`: 계좌별 데이터 배열
- `comparison`: 계좌간 비교

---

## Performance Requirements

### Response Time Targets

| 쿼리 유형 | 목표 응답 시간 | 최대 응답 시간 |
|-----------|---------------|---------------|
| 전체 포트폴리오 (10년 데이터) | < 100ms | < 200ms |
| 단일 계좌 필터 | < 50ms | < 100ms |
| Health check | < 10ms | < 20ms |

### Payload Size Targets

| 시나리오 | 예상 크기 |
|---------|-----------|
| 1년 전체 데이터 (3개 계좌) | ~50KB |
| 10년 전체 데이터 (3개 계좌) | ~500KB |
| 단일 계좌 1년 | ~15KB |

---

## Testing Contracts

### Contract Tests

API 계약을 검증하는 테스트 케이스:

```python
# tests/unit/test_api_contracts.py
def test_history_response_contains_required_fields():
    """필수 필드 검증"""
    response = client.get("/api/v1/history?year=2026")
    assert response.status_code == 200
    data = response.json()
    
    # 필수 필드
    assert "records" in data
    assert "latest" in data
    assert "earliest" in data
    assert "total_change" in data
    assert "return_rate" in data
    assert "projections" in data
    
    # 선택적 필드
    assert "accounts" in data
    assert "comparison" in data

def test_account_filter_response():
    """계좌 필터 응답 검증"""
    response = client.get("/api/v1/history?year=2026&account=증권계좌")
    assert response.status_code == 200
    data = response.json()
    
    assert "account" in data
    assert data["account"] == "증권계좌"
    assert "records" in data
    assert "holdings" in data

def test_invalid_year_returns_400():
    """잘못된 연도 파라미터 처리"""
    response = client.get("/api/v1/history?year=invalid")
    assert response.status_code == 400

def test_unknown_account_returns_404():
    """존재하지 않는 계좌 처리"""
    response = client.get("/api/v1/history?account=UnknownAccount")
    assert response.status_code == 404
```

---

## Versioning

현재 버전: `v1`

### Breaking Changes

다음 변경 사항은 주 버전 업데이트(v2)를 필요로 합니다:
- 필수 필드 제거
- 데이터 타입 변경
- 엔드포인트 경로 변경

### Non-Breaking Changes

다음 변경 사항은 마이너 버전 업데이트(v1.1, v1.2 등)로 가능합니다:
- 새로운 선택적 필드 추가
- 새로운 쿼리 파라미터 추가
- 응답 데이터 순서 변경

---

## Security Considerations

1. **Read-only**: 데이터는 읽기 전용이며, 수정 엔드포인트는 없습니다
2. **No Authentication**: 로컬 전용 도구이므로 인증이 없습니다
3. **Input Validation**: 모든 입력 파라미터는 검증되어야 합니다
4. **Rate Limiting**: (선택사항) 로컬이므로 필요하지 않을 수 있음

---

**문서 버전**: 1.0
**마지막 수정**: 2026-06-03
**다음 단계**: Quick Start Guide (`quickstart.md`)
