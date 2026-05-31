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
from src.config.logging import configure_logging
from src.infrastructure.parsers.obsidian_parser import ObsidianParser

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
async def get_history(year: Optional[int] = None):
    try:
        parser.pull()
        history = parser.parse(year=year)
        return analyze_use_case.execute(history)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse investment data: {str(e)}",
        ) from e


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
