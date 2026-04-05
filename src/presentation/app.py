"""
Main FastAPI Application

Financing investment dashboard main application with REST API endpoints.
"""

from fastapi import FastAPI, HTTPException, status
import datetime
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app, CollectorRegistry

from src.config.logging import configure_logging
from src.config.agent_config import load_config
from src.application.services.agent_orchestrator import AgentOrchestrator

from src.infrastructure.repositories.gkeep_repository import GKeepRepository
from src.infrastructure.repositories.repository_factory import RepositoryFactory
from src.application.use_cases.fetch_investment_data import FetchInvestmentData
from src.domain.entities.portfolio import Portfolio
from src.presentation.validators import (
    validate_email,
    validate_label,
    sanitize_label,
    validate_password,
)


# Lifespan for managing repository connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Configure logging
    configure_logging()
    
    # Load agent config and initialize orchestrator if enabled
    config = load_config()
    if config.enabled:
        orch = AgentOrchestrator(
            chain=config.chain,
            timeout_ms=config.timeout_ms,
            cooldown_ms=config.cooldown_ms,
            failure_threshold=config.failure_threshold,
        )
        app.state.orchestrator = orch
        app.state.agent_config = config
        app.state.repository = None
        app.state.repository_factory = None

        # Register agent adapters (will be replaced after authentication)
        # Start with simulated adapters that will be replaced with real ones
        app.state.agent_adapters = {
            'sisyphus': lambda label: [],
            'prometheus': lambda label: [],
            'atlas': lambda label: [],
        }
    else:
        app.state.orchestrator = None
        app.state.agent_config = config
        app.state.repository = None
        app.state.repository_factory = None
    
    yield
    
    # Shutdown
    app.state.repository = None
    app.state.orchestrator = None


# Create FastAPI application
app = FastAPI(
    title="Financing API",
    description="Investment dashboard API for portfolio management",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount metrics app at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add CORS middleware - allow requests from any origin for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for external access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financing API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.get("/api/v1/portfolio")
async def get_portfolio(label: str = "투자"):
    """
    Get portfolio data from Google Keep

    Args:
        label: Google Keep label to filter notes

    Returns:
        Portfolio data including total value and allocation
    """
    # Validate and sanitize label
    if not validate_label(label):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid label format"
        )
    
    sanitized_label = sanitize_label(label)
    
    try:
        # Get repository from app state
        repository: GKeepRepository = app.state.repository
        
        if not repository:
            return {"error": "Repository not initialized. Call POST /api/v1/auth first"}
        
        # Fetch investment data
        fetch_use_case = FetchInvestmentData(repository=repository, orchestrator=app.state.orchestrator)
        
        # Build agent callables mapping if orchestrator present and adapters registered
        if getattr(app.state, "orchestrator", None) and getattr(app.state, "agent_adapters", None):
            adapters = app.state.agent_adapters
            
            # Pass mapping through orchestrator by calling execute_with_fallback with mapping
            assets = app.state.orchestrator.execute_with_fallback(adapters)
        else:
            assets = fetch_use_case.execute(label=sanitized_label)
        
        # Create portfolio
        portfolio = Portfolio(assets=assets)
        
        # Calculate metrics
        total_value = portfolio.total_value()
        allocation = portfolio.allocation_by_type()
        
        return {
            "total_value": {
                "amount": float(total_value.amount),
                "currency": total_value.currency,
            },
            "allocation": {
                asset_type.display_name(): ratio
                for asset_type, ratio in allocation.items()
            },
            "assets": [
                {
                    "name": asset.name,
                    "type": asset.asset_type.display_name(),
                    "quantity": asset.quantity,
                    "unit_price": {
                        "amount": float(asset.unit_price.amount),
                        "currency": asset.unit_price.currency,
                    },
                    "total_value": {
                        "amount": float(asset.total_value().amount),
                        "currency": asset.total_value().currency,
                    },
                }
                for asset in portfolio.assets
            ],
            "asset_count": len(portfolio.assets),
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch portfolio: {str(e)}"
        )


@app.post("/api/v1/auth")
async def authenticate(email: str, password: str):
    """
    Authenticate with Google Keep

    Args:
        email: Google account email
        password: Google account password or app password

    Returns:
        Authentication status
    """
    # Validate inputs
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )
    
    if not validate_password(password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is required"
        )
    
    try:
        # Create repository with credentials
        repository = GKeepRepository(email=email, password=password)

        # Store repository in app state
        app.state.repository = repository

        # Create repository factory and real agent adapters
        factory = RepositoryFactory(repository)
        app.state.repository_factory = factory
        app.state.agent_adapters = factory.create_all_adapters()

        return {"status": "authenticated", "email": email}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
