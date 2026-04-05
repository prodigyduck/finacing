# Financing - Investment Dashboard

Google Keep investment data portfolio management dashboard with Vue.js frontend and FastAPI backend.

## Tech Stack

**Backend:**
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework for building APIs
- **gkeepapi** - Google Keep API unofficial library
- **Pandas** - Data processing
- **Uvicorn** - ASGI server

**Frontend:**
- **Vue.js 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe development
- **Pinia** - State management
- **Vue Router** - Official router
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **Vite** - Build tool

## Clean Architecture

```
src/
├── domain/          # Entities + Business Logic
├── application/     # Use Cases + Ports
├── infrastructure/  # Google Keep integration
└── presentation/    # FastAPI REST API

frontend/
├── src/
│   ├── api/           # Axios HTTP client
│   ├── components/     # Reusable Vue components
│   ├── stores/        # Pinia state management
│   ├── router/        # Vue Router configuration
│   └── views/         # Page components (Dashboard, Settings)
```

## Getting Started

### Backend Setup

**1. Create virtual environment and activate**

\`\`\`bash
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\\Scripts\\activate   # Windows
\`\`\`

**2. Install dependencies**

\`\`\`bash
pip install -r requirements.txt
\`\`\`

**3. Configure Google Keep**

Create \`.env\` file:

\`\`\`bash
cp .env.example .env
# Edit .env with your credentials
\`\`\`

**4. Run backend**

\`\`\`bash
python -m src.presentation.app
\`\`\`

Backend will run on http://localhost:8000

**Note**: See [PORTS.md](PORTS.md) for port assignment and how to generate local \`.env.local\` files with fallback support.

API Documentation: http://localhost:8000/docs

### Frontend Setup

**1. Install dependencies**

\`\`\`bash
cd frontend
npm install
\`\`\`

**2. Run development server**

\`\`\`bash
npm run dev
\`\`\`

Frontend will run on http://localhost:5173

## Testing

\`\`\`bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration
\`\`\`

## Code Formatting & Linting

\`\`\`bash
# Format Python code
black src tests

# Lint Python code
ruff check src tests

# Type check
mypy src
\`\`\`

## Development Plan

- [x] Project initial setup
- [x] Google Keep data format confirmation
- [x] Domain layer TDD
- [x] Application layer TDD
- [x] Infrastructure TDD
- [x] FastAPI backend implementation
- [x] Vue.js frontend implementation
- [ ] Add input validation
- [ ] Implement retry logic
- [ ] Add comprehensive error handling

## Implementation Completed

### Domain Layer
- [x] Money Value Object
- [x] AssetType Enum
- [x] InvestmentAsset Entity
- [x] Portfolio Entity

### Application Layer
- [x] IKeepRepository Port
- [x] FetchInvestmentData Use Case
- [x] AnalyzePortfolio Use Case
- [x] CalculateReturns Use Case

### Infrastructure Layer
- [x] NoteParser
- [x] GKeepRepository

### Presentation Layer
- [x] FastAPI application
- [x] REST API endpoints (\`/api/v1/portfolio\`, \`/api/v1/auth\`)
- [x] CORS configuration
- [x] Health check endpoint

### Frontend Layer
- [x] Vue.js application structure
- [x] Dashboard view with portfolio visualization
- [x] Settings view with authentication
- [x] Pinia stores (auth, portfolio)
- [x] Vue Router configuration
- [x] Chart.js components (Pie chart, Bar chart)
- [x] Axios HTTP client with proxy configuration

## API Endpoints

### GET \`/health\`
Health check endpoint

### GET \`/api/v1/portfolio\`
Fetch portfolio data from Google Keep

**Query Parameters:**
- \`label\`: Google Keep label (default: "투자")

**Returns:**
\`\`\`json
{
  "total_value": { "amount": 1000000, "currency": "KRW" },
  "allocation": { "Stock": 0.6, "ETF": 0.4 },
  "assets": [...],
  "asset_count": 10
}
\`\`\`

### POST \`/api/v1/auth\`
Authenticate with Google Keep

**Request Body:**
\`\`\`json
{
  "email": "your_email@gmail.com",
  "password": "your_app_password"
}
\`\`\`

**Returns:**
\`\`\`json
{
  "status": "authenticated",
  "email": "your_email@gmail.com"
}
\`\`\`

## Documentation

- [AGENTS.md](AGENTS.md) - AI agents and their roles
- [ARCHITECTURE.md](ARCHITECTURE.md) - Clean Architecture layers and patterns
- [PORTS.md](PORTS.md) - Port management registry and usage
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines and development workflow
- [docs/DESIGN.md](docs/DESIGN.md) - Design principles and coding standards
- [docs/FRONTEND.md](docs/FRONTEND.md) - Vue.js frontend architecture
- [docs/SECURITY.md](docs/SECURITY.md) - Security considerations
- [docs/RELIABILITY.md](docs/RELIABILITY.md) - Reliability practices
- [docs/QUALITY_SCORE.md](docs/QUALITY_SCORE.md) - Quality standards and metrics
- [docs/PLANS.md](docs/PLANS.md) - Development roadmap
- [docs/PRODUCT_SENSE.md](docs/PRODUCT_SENSE.md) - Product vision and user value

## License

MIT License - See LICENSE file for details
