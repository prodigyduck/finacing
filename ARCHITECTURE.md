# ARCHITECTURE

## Overview

The Financing project follows **Clean Architecture** principles with a clear separation of concerns across four distinct layers. This architecture ensures maintainability, testability, and independence from external dependencies.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  Vue.js UI (dashboard, settings, FastAPI REST)         │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│  Use Cases + Ports (FetchInvestmentData, AnalyzePortfolio) │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Domain Layer                              │
│  Entities + Value Objects (Portfolio, InvestmentAsset, Money)│
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│                Infrastructure Layer                         │
│  External Integrations (Google Keep API, NoteParser)        │
└─────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer (`src/domain/`)

**Purpose:** Contains the core business logic and domain models.

**Components:**
- **Value Objects:** Immutable objects that represent concepts in the domain
  - `Money`: Represents monetary values with currency and precision
  - `AssetType`: Enum defining asset categories (Stock, ETF, Bond, Cash, Other)

- **Entities:** Objects with unique identity and business logic
  - `InvestmentAsset`: Represents a single investment holding
  - `Portfolio`: Collection of assets with aggregate calculations

**Key Principles:**
- No external dependencies (framework-agnostic)
- Pure business logic only
- No data access or I/O operations
- Testable in isolation

**Example:**
```python
from src.domain.entities.portfolio import Portfolio
from src.domain.value_objects.money import Money

portfolio = Portfolio(assets=[...])
total = portfolio.total_value()  # Business logic, no I/O
```

---

### 2. Application Layer (`src/application/`)

**Purpose:** Orchestrates domain objects to execute use cases.

**Components:**
- **Use Cases:** Application-specific business operations
  - `FetchInvestmentData`: Retrieve investment data from Google Keep
  - `AnalyzePortfolio`: Calculate portfolio metrics and analysis
  - `CalculateReturns`: Compute investment returns

- **Ports:** Interfaces defining contracts with external systems
  - `IKeepRepository`: Abstract interface for Google Keep operations

**Key Principles:**
- Depends only on Domain layer
- Defines contracts (ports) for Infrastructure to implement
- Contains orchestration logic, not business logic
- No framework or UI dependencies

**Example:**
```python
from src.application.use_cases.fetch_investment_data import FetchInvestmentData

# Port interface is injected
use_case = FetchInvestmentData(repository=gkeep_repository)
assets = use_case.execute(label="투자")
```

---

### 3. Infrastructure Layer (`src/infrastructure/`)

**Purpose:** Implements ports defined by the Application layer.

**Components:**
- **Repositories:** Concrete implementations of ports
  - `GKeepRepository`: Google Keep API integration using gkeepapi library

- **Parsers:** External data format conversion
  - `NoteParser`: Parses Google Keep note text into domain objects

**Key Principles:**
- Implements Application layer ports
- Handles all external integrations (APIs, databases, file systems)
- Adapts external data to domain objects
- Depends on Domain and Application layers

**Example:**
```python
from src.infrastructure.repositories.gkeep_repository import GKeepRepository

# Implements IKeepRepository port
repository = GKeepRepository(email, password, master_token)
```

---

### 4. Presentation Layer (`src/presentation/`)

**Purpose:** Handles user interface and user interactions.

**Components:**
- **FastAPI Backend:** REST API server
  - `app.py`: Main FastAPI application with REST endpoints

- **Vue.js Frontend:** Single Page Application
  - `Dashboard.vue`: Asset visualization and portfolio overview
  - `Settings.vue`: Google Keep authentication configuration
  - `PieChart.vue`, `BarChart.vue`: Reusable chart components

**Key Principles:**
- Thin UI layer with minimal logic
- Delegates all business operations to Application layer
- Handles user input and displays output
- Depends on Application layer only

**Example:**
```python
from src.presentation.app import main

# Streamlit UI - delegates to use cases
if __name__ == "__main__":
    main()
```

---

## Dependency Flow

```
Presentation → Application → Domain
                  ↑
Infrastructure ──┘
```

**Critical Rule:** Dependencies point **inward**. The Domain layer is at the center and has no dependencies. Outer layers depend on inner layers.

## Data Flow

### 1. Fetching Investment Data

```
User Request (Streamlit)
    ↓
FetchInvestmentData Use Case (Application)
    ↓
IKeepRepository.fetch_investment_notes() (Port)
    ↓
GKeepRepository (Infrastructure) → Google Keep API
    ↓
NoteParser (Infrastructure) → Parses text to domain objects
    ↓
Returns List[InvestmentAsset] (Domain)
    ↓
Use Case returns to Presentation
    ↓
Display in Streamlit UI
```

### 2. Calculating Portfolio Metrics

```
User Request (Streamlit)
    ↓
AnalyzePortfolio Use Case (Application)
    ↓
Portfolio.total_value() (Domain - business logic)
Portfolio.allocation_by_type() (Domain - business logic)
    ↓
Returns calculated metrics (Domain value objects)
    ↓
Use Case returns to Presentation
    ↓
Visualize with Plotly in Streamlit
```

---

## Key Patterns

### Dependency Injection

Ports are injected into use cases, enabling testability and flexibility:

```python
# Production: Inject real repository
repository = GKeepRepository(email, password, master_token)
use_case = FetchInvestmentData(repository)

# Testing: Inject mock repository
mock_repo = Mock(spec=IKeepRepository)
use_case = FetchInvestmentData(mock_repo)
```

### Hexagonal Architecture

The project follows hexagonal architecture principles:
- **Domain:** Core business logic (inner hexagon)
- **Application:** Use cases orchestrate domain (middle hexagon)
- **Ports:** Interfaces for external integration (hexagon boundaries)
- **Adapters:** Infrastructure implements ports (outer hexagon)

### Value Object Immutability

Value objects are immutable to prevent bugs:

```python
from src.domain.value_objects.money import Money

# Cannot modify after creation
money = Money(amount=Decimal("1000"), currency="KRW")
# money.amount = 2000  # ❌ Error: dataclass with frozen=True
```

---

## Module Structure

```
src/
├── domain/
│   ├── entities/
│   │   ├── investment_asset.py
│   │   └── portfolio.py
│   └── value_objects/
│       ├── asset_type.py
│       └── money.py
├── application/
│   ├── ports/
│   │   └── keep_repository.py
│   └── use_cases/
│       ├── analyze_portfolio.py
│       ├── calculate_returns.py
│       └── fetch_investment_data.py
├── infrastructure/
│   ├── parsers/
│   │   └── note_parser.py
│   └── repositories/
│       └── gkeep_repository.py
└── presentation/
    ├── pages/
    │   ├── dashboard.py
    │   └── settings.py
    └── app.py
```

---

## Benefits of This Architecture

### 1. Testability
- Each layer can be tested in isolation
- Domain layer has no dependencies → 100% unit testable
- Ports can be mocked for application layer tests

### 2. Maintainability
- Clear separation of concerns
- Changes in one layer don't cascade to others
- Easy to locate and modify specific functionality

### 3. Flexibility
- External integrations can be swapped without affecting business logic
- UI can be changed (e.g., from Streamlit to React) without changing domain
- Multiple data sources can be added by implementing the same port

### 4. Scalability
- Business logic is centralized in Domain layer
- Infrastructure can be optimized independently
- Presentation layer can scale horizontally

---

## Testing Strategy

### Domain Layer Tests (100% Coverage)
- Test business logic in isolation
- No external dependencies
- Pure Python, no mocking needed

**Example:**
```python
# tests/unit/domain/test_portfolio.py
def test_portfolio_total_value():
    portfolio = Portfolio(assets=[...])
    total = portfolio.total_value()
    assert total.amount == expected_value
```

### Application Layer Tests (100% Coverage)
- Test use case orchestration
- Mock ports and repositories
- Verify correct interactions

**Example:**
```python
# tests/unit/application/test_fetch_investment_data.py
def test_fetch_investment_data(mock_repository):
    mock_repository.fetch_investment_notes.return_value = [...]
    use_case = FetchInvestmentData(mock_repository)
    assets = use_case.execute(label="투자")
    assert len(assets) > 0
```

### Infrastructure Layer Tests (84% Coverage)
- Test external integrations
- Use fixtures and real Google Keep sandbox (if available)
- Test parsing logic thoroughly

### Presentation Layer Tests (48% Coverage)
- Test Streamlit components with custom fixtures
- Verify page rendering and user interactions
- Note: Higher complexity due to Streamlit's nature

---

## Future Architecture Considerations

### Potential Enhancements

1. **Event-Driven Architecture**
   - Add domain events for portfolio changes
   - Implement event bus for cross-layer communication
   - Enable real-time updates

2. **CQRS (Command Query Responsibility Segregation)**
   - Separate read and write models
   - Optimize for different access patterns
   - Improve performance for complex queries

3. **Microservices Split**
   - Extract portfolio calculation service
   - Separate Google Keep sync service
   - Deploy independently for better scaling

### Architectural Constraints

- **Google Keep API Limitations:** Non-official API (gkeepapi) may break
- **Single-User Design:** Currently designed for personal use, not multi-tenant
- **Stateless UI:** Streamlit's stateless nature requires careful session management

---

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture by Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design by Eric Evans](https://domainlanguage.com/ddd/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial architecture documentation |
