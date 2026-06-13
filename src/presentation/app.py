import datetime
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict

from src.application.use_cases.analyze_history import AnalyzeHistory, ParserPort
from src.application.use_cases.analyze_accounts import AnalyzeAccounts
from src.config.logging import configure_logging
from src.infrastructure.parsers.obsidian_parser import ObsidianParser
from src.infrastructure.parsers.account_parser import AccountParser
from src.infrastructure.parsers.legacy_parser import LegacyParser
from src.infrastructure.parsers.parser_chain import ParserChain

logger = logging.getLogger(__name__)

# --- Dependency Injection ---

def get_parser() -> ParserPort:
    """Factory function to create parser instance.

    In production, returns real ObsidianParser.
    In tests, can be mocked via patching.
    """
    return ObsidianParser()


def get_analyze_use_case() -> AnalyzeHistory:
    """Factory function to create AnalyzeHistory with injected parser."""
    parser = get_parser()
    return AnalyzeHistory(parser=parser)


# Create instances
parser = get_parser()
analyze_use_case = get_analyze_use_case()

# Simple API key for local development (override with FINANCING_API_KEY env var)
API_KEY = os.environ.get("FINANCING_API_KEY", "local-dev-only")


async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key for write operations."""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[FastAPI]:
    configure_logging()
    yield


app = FastAPI(
    title="Financing API",
    description="Investment dashboard API — Obsidian-based portfolio tracking",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5180", "http://127.0.0.1:5180"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)


# --- Schemas ---


class RawRecord(BaseModel):
    month: int
    day: int
    amount: str

    @field_validator("month")
    @classmethod
    def validate_month(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("month must be 1-12")
        return v

    @field_validator("day")
    @classmethod
    def validate_day(cls, v: int, info) -> int:
        if not 1 <= v <= 31:
            raise ValueError("day must be 1-31")

        # Validate month-specific max day
        month = info.data.get("month")
        if month is not None:
            import calendar

            max_day = calendar.monthrange(2024, month)[1]  # Use leap year for safety
            if v > max_day:
                raise ValueError(f"day must be 1-{max_day} for month {month}")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: str) -> str:
        from decimal import InvalidOperation

        try:
            result = Decimal(v)
            if result < 0:
                raise ValueError("amount must be non-negative")
        except (ValueError, TypeError, InvalidOperation) as e:
            raise ValueError(f"amount must be a valid non-negative number: {v}") from e
        return str(result)  # Return normalized format


class RawDataRequest(BaseModel):
    year: int
    frontmatter: str
    records: list[RawRecord]


class AccountRecordRequest(BaseModel):
    """계좌별 형식 저장 요청"""
    date: str  # YYYY-MM-DD
    accounts: list[dict]  # List of {name: str, amount: str, holdings: list[str]}

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        from datetime import datetime

        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format")
        return v

    @field_validator("accounts")
    @classmethod
    def validate_accounts(cls, v: list) -> list:
        for acc in v:
            if not acc.get("name"):
                raise ValueError("account name is required")
            if not acc.get("amount"):
                raise ValueError("account amount is required")
        return v


class RootResponse(TypedDict):
    message: str
    version: str
    docs: str


class HealthResponse(TypedDict):
    status: str
    timestamp: str


@app.get("/")
async def root() -> RootResponse:
    return {"message": "Financing API", "version": "2.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check() -> HealthResponse:
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}


@app.post("/api/v1/sync")
async def sync_vault():
    try:
        result = parser.pull()
        return {"status": "synced", "detail": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Git pull failed: {str(e)}",
        ) from e


@app.get("/api/v1/history")
async def get_history(year: Optional[int] = None, account: Optional[str] = None):
    try:
        parser.pull()

        # Use AccountParser (supports both account-based and legacy formats)
        account_parser = AccountParser()
        text = (parser.vault_path / parser.investment_file).read_text(encoding="utf-8")

        if not account_parser.can_parse(text):
            raise ValueError("투자.md 파일 형식을 확인하세요 (M.DD 억 형식 또는 계좌별 형식)")

        snapshots = account_parser.parse(text, year or datetime.date.today().year)

        if not snapshots or len(snapshots) == 0:
            raise ValueError(f"{year or datetime.date.today().year}년 데이터를 찾을 수 없습니다")

        # Get the latest snapshot (most recent date)
        latest_snapshot = snapshots[-1]

        # Analyze account data
        analyze_accounts = AnalyzeAccounts()
        account_data = analyze_accounts.execute(latest_snapshot)

        # Generate account history from all snapshots
        account_history = _generate_account_history(snapshots)

        # For backward compatibility, also generate history data
        history = parser.parse(year=year)
        base_result = analyze_use_case.execute(history)

        # Merge account data and history into base result
        base_result.update(account_data)
        base_result["account_history"] = account_history
        return base_result

    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse investment data: {str(e)}",
        ) from e


def _generate_account_history(snapshots: list) -> dict:
    """스냅샷 리스트에서 계좌별 시계열 데이터 생성 (6월 이후만, 총계좌 제외)"""
    from collections import defaultdict

    # 6월 이후의 스냅샷만 필터링
    filtered_snapshots = [s for s in snapshots if s.date.month >= 6]

    if not filtered_snapshots:
        # 6월 데이터가 없으면 빈 결과 반환
        return {"dates": [], "series": []}

    # 모든 계좌명 수집 (총계좌 제외)
    all_accounts = set()
    for snapshot in filtered_snapshots:
        for acc in snapshot.accounts:
            if acc.account_name != "총계좌":  # 총계좌는 제외
                all_accounts.add(acc.account_name)

    # 날짜별 계좌 데이터 수집
    account_series = defaultdict(list)
    dates = []

    for snapshot in filtered_snapshots:
        date_str = snapshot.date.strftime("%Y-%m-%d")
        dates.append(date_str)

        # 각 계좌의 금액 수집 (총계좌 제외)
        account_map = {acc.account_name: acc.total_amount_억 for acc in snapshot.accounts if acc.account_name != "총계좌"}
        for acc_name in all_accounts:
            amount = float(account_map.get(acc_name, 0))
            account_series[acc_name].append(amount)

    # ECharts용 데이터 구조로 변환
    result = {
        "dates": dates,
        "series": []
    }

    colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#6b7280"]
    for i, (acc_name, values) in enumerate(sorted(account_series.items())):
        result["series"].append({
            "name": acc_name,
            "data": values,
            "color": colors[i % len(colors)]
        })

    return result


@app.get("/api/v1/raw-data")
async def get_raw_data(year: Optional[int] = None):
    try:
        return parser.read_raw(year=year)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read raw data: {str(e)}",
        ) from e


@app.put("/api/v1/raw-data")
async def put_raw_data(
    request: RawDataRequest,
    commit: bool = Query(default=True, description="Git commit 여부"),
    x_api_key: str = Header(...),
):
    # Verify API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    try:
        parser.write_raw(
            year=request.year,
            frontmatter=request.frontmatter,
            records=[r.model_dump() for r in request.records],
        )
        commit_hash = None
        if commit:
            commit_hash = parser.commit(
                f"Update investment data via Financing app ({len(request.records)} records)"
            )
        return {"status": "saved", "record_count": len(request.records), "commit": commit_hash}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save raw data: {str(e)}",
        ) from e


@app.post("/api/v1/account-data")
async def save_account_data(
    request: AccountRecordRequest,
    commit: bool = Query(default=True, description="Git commit 여부"),
    x_api_key: str = Header(...),
):
    """계좌별 형식 데이터 저장 (기존 날짜가 있으면 교체)"""
    # Verify API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")

    try:
        file_path = parser.vault_path / parser.investment_file
        current_content = file_path.read_text(encoding="utf-8")
        lines = current_content.splitlines()

        # 기존 날짜 섹션 찾기 및 제거
        date_header = f"## {request.date}"
        filtered_lines = []
        skip_until_next_date = False

        for i, line in enumerate(lines):
            # 날짜 헤더 확인
            if line.startswith("## ") and line.strip() == date_header:
                skip_until_next_date = True
                continue

            # 다음 날짜 헤더를 만나면 skip 중단
            if skip_until_next_date and line.startswith("## "):
                skip_until_next_date = False

            # skip 중이 아니면 추가
            if not skip_until_next_date:
                filtered_lines.append(line)

        # Build account markdown
        account_markdown = [f"\n{date_header}", ""]
        for acc in request.accounts:
            account_markdown.append(f"### 계좌: {acc['name']}")
            account_markdown.append(f"총액: {acc['amount']}억")
            holdings = acc.get("holdings", [])
            if holdings and any(h.strip() for h in holdings):
                account_markdown.append(f"보유종목: {', '.join(holdings)}")
            else:
                account_markdown.append("보유종목:")
            account_markdown.append("")

        # Combine and write
        updated_content = "\n".join(filtered_lines + account_markdown)
        file_path.write_text(updated_content, encoding="utf-8")

        # Git commit if requested
        commit_hash = None
        if commit:
            commit_hash = parser.commit(
                f"Update account data for {request.date} ({len(request.accounts)} accounts)"
            )

        return {
            "status": "saved",
            "date": request.date,
            "account_count": len(request.accounts),
            "commit": commit_hash
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save account data: {str(e)}",
        ) from e


@app.get("/api/v1/account-data")
async def get_account_data(date: str = Query(..., description="날짜 (YYYY-MM-DD)")):
    """특정 날짜의 계좌 데이터 조회"""
    try:
        file_path = parser.vault_path / parser.investment_file
        content = file_path.read_text(encoding="utf-8")

        # 해당 날짜의 계좌 데이터 찾기
        date_header = f"## {date}"
        lines = content.splitlines()

        accounts = []
        in_target_section = False
        current_account = None

        for line in lines:
            # 날짜 헤더 확인
            if line.startswith("## ") and line.strip() == date_header:
                in_target_section = True
                continue

            # 다른 날짜 헤더를 만나면 중단
            if in_target_section and line.startswith("## ") and line.strip() != date_header:
                break

            # 계좌 헤더 확인
            if in_target_section and line.startswith("### 계좌:"):
                if current_account:
                    accounts.append(current_account)
                current_account = {"name": line.split(":", 1)[1].strip(), "amount": "", "holdings": []}
                continue

            # 총액 확인
            if in_target_section and current_account and "총액:" in line:
                current_account["amount"] = line.split(":", 1)[1].strip().replace("억", "")
                continue

            # 보유종목 확인
            if in_target_section and current_account and "보유종목:" in line:
                holdings_str = line.split(":", 1)[1].strip()
                if holdings_str:
                    current_account["holdings"] = [h.strip() for h in holdings_str.split(",")]
                else:
                    current_account["holdings"] = []
                continue

        # 마지막 계좌 추가
        if current_account:
            accounts.append(current_account)

        return {"date": date, "accounts": accounts}

    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load account data: {str(e)}",
        ) from e

        # Git commit if requested
        commit_hash = None
        if commit:
            commit_hash = parser.commit(
                f"Update account data for {request.date} ({len(request.accounts)} accounts)"
            )

        return {
            "status": "saved",
            "date": request.date,
            "account_count": len(request.accounts),
            "commit": commit_hash
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save account data: {str(e)}",
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
