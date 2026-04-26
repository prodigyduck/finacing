from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, field_validator
import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Optional

from src.config.logging import configure_logging
from src.infrastructure.parsers.obsidian_parser import ObsidianParser
from src.application.use_cases.analyze_history import AnalyzeHistory

logger = logging.getLogger(__name__)

parser = ObsidianParser()
analyze_use_case = AnalyzeHistory()


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
    def validate_day(cls, v: int) -> int:
        if not 1 <= v <= 31:
            raise ValueError("day must be 1-31")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: str) -> str:
        Decimal(v)
        return v


class RawDataRequest(BaseModel):
    year: int
    frontmatter: str
    records: list[RawRecord]


@app.get("/")
async def root():
    return {"message": "Financing API", "version": "2.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
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
        )


@app.get("/api/v1/history")
async def get_history(year: Optional[int] = None):
    try:
        parser.pull()
        history = parser.parse(year=year)
        return analyze_use_case.execute(history)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse investment data: {str(e)}",
        )


@app.get("/api/v1/raw-data")
async def get_raw_data(year: Optional[int] = None):
    try:
        return parser.read_raw(year=year)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read raw data: {str(e)}",
        )


@app.put("/api/v1/raw-data")
async def put_raw_data(request: RawDataRequest, commit: bool = Query(default=True)):
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save raw data: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
