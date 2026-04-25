# Design Principles & Patterns

## Overview

This document defines the core design principles and coding patterns used throughout the Financing project. These principles ensure code quality, maintainability, and consistency.

## Core Principles

### 1. SOLID Principles

#### Single Responsibility Principle (SRP)
Every module, class, or function should have one, and only one, reason to change.

**Examples:**
- `Portfolio` entity focuses only on portfolio aggregation logic
- `ObsidianParser` handles only text parsing, not data retrieval
- `FetchInvestmentData` use case orchestrates only data fetching

```python
# Good: Single responsibility
class Portfolio:
    def total_value(self) -> Money:
        """Only calculates total value"""

# Bad: Multiple responsibilities
class Portfolio:
    def total_value(self) -> Money:  # Business logic
    def fetch_from_api(self) -> None:  # I/O operation
    def render_ui(self) -> None:  # Presentation
```

#### Open/Closed Principle (OCP)
Software entities should be open for extension but closed for modification.

**Examples:**
- New asset types can be added by extending `AssetType` enum
- New parsers can implement `IDataParser` port
- New use cases can be added without modifying existing ones

```python
# Good: Extensible through interfaces
class IDataParser(ABC):
    @abstractmethod
    def fetch_investment_records(self, label: str) -> List[InvestmentRecord]:
        pass

# New implementations can be added without modifying existing code
```

#### Liskov Substitution Principle (LSP)
Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

**Examples:**
- Any `IDataParser` implementation can be substituted
- Mock parsers can replace real parsers in tests

#### Interface Segregation Principle (ISP)
Clients should not depend on interfaces they don't use.

**Examples:**
- `IDataParser` defines only data parsing operations
- Separate interfaces for read vs. write operations (if needed)

```python
# Good: Focused interface
class IDataParser(ABC):
    @abstractmethod
    def fetch_investment_records(self, label: str) -> List[InvestmentRecord]:
        pass

# Bad: Bloated interface
class IDataParser(ABC):
    @abstractmethod
    def fetch_investment_records(self, label: str) -> List[InvestmentRecord]:
        pass
    @abstractmethod
    def authenticate(self, email: str, password: str) -> bool:  # Unrelated
    @abstractmethod
    def send_email(self, recipient: str, message: str) -> bool:  # Unrelated
```

#### Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions.

**Examples:**
- Use cases depend on `IDataParser` port, not `ObsidianParser` implementation
- Domain layer has no dependencies on outer layers

```python
# Good: Depend on abstraction
class FetchInvestmentData:
    def __init__(self, parser: IDataParser):  # Abstract interface
        self._parser = parser

# Bad: Depend on concrete
class FetchInvestmentData:
    def __init__(self, parser: ObsidianParser):  # Concrete implementation
        self._parser = parser
```

---

### 2. Clean Code Principles

#### Meaningful Names
Names should reveal intent, avoid disinformation, and be pronounceable.

```python
# Good: Clear, descriptive names
def calculate_portfolio_return_rate(portfolio: Portfolio) -> Decimal:
    """Calculates annualized return rate for portfolio"""

class InvestmentRecord:
    def __init__(self, date: str, amount: Decimal):
        pass

# Bad: Vague, misleading names
def calc(x, y):
    pass

class Record:
    def __init__(self, d, a):
        pass
```

#### Functions Should Do One Thing
Each function should have a single responsibility and be small.

```python
# Good: Single responsibility, well-named
def parse_investment_line(line: str) -> InvestmentRecord:
    """Parses a single investment line into an InvestmentRecord"""

def calculate_total_value(records: List[InvestmentRecord]) -> Money:
    """Calculates total value of all records"""

# Bad: Multiple responsibilities
def process_investment_data(text: str) -> Tuple[Money, Dict[str, float]]:
    """Parses, validates, calculates, and formats in one function"""
    # ... 50 lines of mixed logic
```

#### Don't Repeat Yourself (DRY)
Avoid code duplication. Extract common logic into reusable functions.

```python
# Good: Reusable helper function
def format_currency(amount: Decimal, currency: str) -> str:
    """Formats a monetary amount for display"""
    return f"{amount:,.2f} {currency}"

# Usage in multiple places
display_total = format_currency(total.amount, total.currency)
display_gain = format_currency(gain.amount, gain.currency)

# Bad: Duplicated logic
def display_total(total: Money) -> str:
    return f"{total.amount:,.2f} {total.currency}"

def display_gain(gain: Money) -> str:
    return f"{gain.amount:,.2f} {total.currency}"  # Same formatting logic
```

---

### 3. Testing Principles

#### Test Isolation
Each test should be independent and not depend on other tests.

```python
# Good: Independent tests
def test_portfolio_empty():
    portfolio = Portfolio(assets=[])
    assert portfolio.total_value().amount == Decimal("0")

def test_portfolio_single_asset():
    portfolio = Portfolio(assets=[asset])
    assert portfolio.total_value().amount == expected_value

# Bad: Dependent tests
test_portfolio_empty()
asset = create_test_asset()  # State shared across tests
```

#### Test Descriptive Names
Test names should clearly describe what is being tested and the expected outcome.

```python
# Good: Descriptive test names
def test_portfolio_total_value_returns_sum_of_all_assets():
    pass

def test_portfolio_allocation_calculates_correct_percentages():
    pass

# Bad: Vague test names
def test_portfolio_1():
    pass

def test_portfolio_2():
    pass
```

#### Test Coverage
Aim for high coverage, but prioritize testing critical paths and business logic.

**Coverage Goals:**
- Domain layer: 100% (pure business logic)
- Application layer: 100% (orchestration logic)
- Infrastructure layer: 80%+ (external integrations)
- Presentation layer: 50%+ (UI components)

---

## Design Patterns

### 1. Repository Pattern
Abstracts data access logic, providing a collection-like interface for domain objects.

```python
# Interface (Port)
class IDataParser(ABC):
    @abstractmethod
    def fetch_investment_records(self, label: str) -> List[InvestmentRecord]:
        pass

# Implementation (Adapter)
class ObsidianParser(IDataParser):
    def fetch_investment_records(self, label: str) -> List[InvestmentRecord]:
        # Read from Obsidian markdown file
        file_path = Path("~/git/obsidian/투자/투자.md").expanduser()
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self._parse_lines(content)
```

### 2. Dependency Injection
Pass dependencies (parsers, services) into objects rather than creating them internally.

```python
# Constructor injection
class FetchInvestmentData:
    def __init__(self, parser: IDataParser):
        self._parser = parser

# Usage
parser = ObsidianParser(vault_path="~/git/obsidian/투자/투자.md")
use_case = FetchInvestmentData(parser)
```

### 3. Value Object Pattern
Immutable objects that represent domain concepts with no identity.

```python
@dataclass(frozen=True)  # Immutability
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
```

### 4. Use Case Pattern
Encapsulates a specific business operation or user intent.

```python
class AnalyzePortfolio:
    def __init__(self, portfolio: Portfolio):
        self._portfolio = portfolio

    def execute(self) -> PortfolioAnalysis:
        """Orchestrates portfolio analysis"""
        total_value = self._portfolio.total_value()
        allocation = self._portfolio.allocation_by_type()
        return PortfolioAnalysis(total_value, allocation)
```

---

## Coding Standards

### Python Style Guide

The project follows [PEP 8](https://pep8.org/) with customizations:

**Formatting:**
- Line length: 100 characters (configurable in `pyproject.toml`)
- Use `black` for automatic formatting
- Use `ruff` for linting

**Type Hints:**
- All public functions and methods must have type hints
- Use `from typing import ...` for complex types
- Enable mypy for static type checking

**Docstrings:**
- Use Google-style docstrings
- Document all public APIs
- Include parameter and return type descriptions

```python
def calculate_return_rate(
    initial_value: Money,
    current_value: Money,
    days: int
) -> Decimal:
    """Calculates annualized return rate.

    Args:
        initial_value: Initial investment value
        current_value: Current investment value
        days: Number of days elapsed

    Returns:
        Annualized return rate as a decimal

    Raises:
        ValueError: If initial_value is zero or days is negative
    """
    if initial_value.amount == 0:
        raise ValueError("Initial value cannot be zero")
    # ... implementation
```

### Code Organization

**Import Order:**
1. Standard library imports
2. Third-party imports
3. Local application imports
4. Blank line between each group

```python
# Standard library
import os
from typing import List
from pathlib import Path

# Third-party
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Local
from src.domain.entities.portfolio import Portfolio
from src.application.use_cases.fetch_investment_data import FetchInvestmentData
```

**File Structure:**
- Imports at the top
- Constants after imports
- Classes/functions ordered by dependency
- Main execution guard at the bottom

```python
"""Module docstring"""

# Imports
import ...

# Constants
DEFAULT_OBSIDIAN_PATH = "~/git/obsidian/투자/투자.md"

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main
if __name__ == "__main__":
    my_function()
```

---

## Error Handling

### Principles

1. **Fail Fast:** Validate inputs early and fail with clear error messages
2. **Use Exceptions:** Don't use error codes or silent failures
3. **Handle Specific Exceptions:** Catch specific exceptions, not generic `Exception`
4. **Preserve Context:** Include relevant information in error messages

```python
# Good: Specific exception handling
def calculate_return_rate(initial: Money, current: Money, days: int) -> Decimal:
    if initial.amount == 0:
        raise ValueError(f"Initial value cannot be zero: {initial}")
    if days <= 0:
        raise ValueError(f"Days must be positive: {days}")

    try:
        return ((current.amount - initial.amount) / initial.amount) ** (365 / days)
    except ZeroDivisionError as e:
        raise ValueError(f"Cannot calculate return: {e}") from e

# Bad: Generic exception handling
def calculate_return_rate(initial: Money, current: Money, days: int) -> Decimal:
    try:
        return ((current.amount - initial.amount) / initial.amount) ** (365 / days)
    except Exception as e:
        print(f"Error: {e}")
        return Decimal("0")  # Silent failure
```

### Custom Exceptions

Define domain-specific exceptions for business logic errors.

```python
class DomainError(Exception):
    """Base exception for domain errors"""
    pass

class InvalidPortfolioError(DomainError):
    """Raised when portfolio is invalid"""
    pass

class AssetNotFoundError(DomainError):
    """Raised when asset is not found in portfolio"""
    pass
```

---

## Performance Considerations

### Principles

1. **Measure Before Optimize:** Profile before making performance changes
2. **Optimize Hot Paths:** Focus on frequently executed code
3. **Prevent Over-Optimization:** Don't sacrifice readability for premature optimization

### Guidelines

- Use list comprehensions for simple transformations
- Prefer built-in functions over custom implementations
- Cache expensive calculations when appropriate
- Use generators for large datasets

```python
# Good: List comprehension (fast and readable)
allocation = [asset.total_value() for asset in assets]

# Good: Generator for large datasets
total = sum(asset.total_value() for asset in large_dataset)

# Bad: Unnecessary optimization for small datasets
total = sum(map(lambda a: a.total_value(), assets))  # Less readable
```

---

## Security Considerations

### Principles

1. **Validate All Inputs:** Never trust user input or external data
2. **Use Environment Variables:** Store configuration in `.env` files
3. **Never Log Secrets:** Avoid logging passwords, tokens, or sensitive data
4. **Principle of Least Privilege:** Use minimal necessary file permissions

```python
# Good: Environment variables for configuration
import os
from pathlib import Path

OBSIDIAN_VAULT_PATH = os.getenv(
    "OBSIDIAN_VAULT_PATH",
    str(Path.home() / "git" / "obsidian" / "투자" / "투자.md")
)

# Bad: Hardcoded paths with potential sensitive info
FILE_PATH = "/home/username/git/obsidian/투자/투자.md"
```

---

## Documentation Standards

### Code Documentation

- Document all public APIs with docstrings
- Use descriptive variable and function names
- Add inline comments for complex logic
- Keep documentation up-to-date with code changes

### README Standards

- Clear project description
- Installation instructions
- Usage examples
- Contribution guidelines
- License information

---

## References

- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Test-Driven Development by Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-19 | Updated to reflect Obsidian-based architecture |
| 1.0.0 | 2026-03-29 | Initial design documentation |
