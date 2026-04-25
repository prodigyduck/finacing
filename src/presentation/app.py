from fastapi import FastAPI, HTTPException, status
import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
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


@app.get("/")
async def root():
    return {"message": "Financing API", "version": "2.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
