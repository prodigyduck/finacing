# Core Beliefs

## Overview

This document articulates the core beliefs that guide the design and architecture of the Financing project. These beliefs inform technical decisions, code organization, and development practices.

---

## Architectural Beliefs

### 1. Simplicity Over Complexity

**Belief:** Simple solutions are almost always better than complex ones.

**Implications:**
- Prefer straightforward implementations over clever optimizations
- Avoid over-engineering for unlikely future requirements
- Clear code beats clever code
- Fewer moving parts means fewer points of failure

**Application:**
- Clean Architecture with clear layer separation
- Simple domain models without excessive abstraction
- Straightforward use cases without unnecessary complexity
- Direct API calls rather than complex patterns

---

### 2. Clarity Over Brevity

**Belief:** Code should be readable and self-explanatory.

**Implications:**
- Use descriptive names for variables, functions, and classes
- Write clear docstrings for public APIs
- Avoid cryptic one-liners in favor of explicit code
- Comments should explain "why", not "what"

**Application:**
- Function names describe their purpose (e.g., `calculate_portfolio_return`)
- Variable names indicate their domain (e.g., `total_value`, not `tv`)
- Docstrings explain business logic, not just repeat code

---

### 3. Consistency Over Convention

**Belief:** Internal consistency is more important than following external conventions.

**Implications:**
- Follow project-specific patterns over general best practices
- Maintain consistency within the codebase
- When in doubt, match existing style
- Document deviations from conventions

**Application:**
- Consistent naming conventions across the project
- Uniform error handling patterns
- Standard testing structure
- Predictable file organization

---

### 4. Testability Over Convenience

**Belief:** Code should be designed for testing from the start.

**Implications:**
- Dependency injection enables testability
- Pure functions are easier to test
- Avoid global state and side effects
- Design for unit, integration, and E2E tests

**Application:**
- Domain layer has no dependencies → 100% testable
- Ports allow mocking in tests
- Use cases test orchestration logic
- Infrastructure tests validate external integrations

---

### 5. Reliability Over Performance

**Belief:** A reliable system is better than a fast, unreliable one.

**Implications:**
- Prioritize correctness over optimization
- Implement proper error handling
- Validate all inputs
- Use proven patterns over experimental ones

**Application:**
- Comprehensive error handling in use cases
- Input validation at boundaries
- Graceful degradation on failures
- Retry logic for transient failures

---

## Domain Beliefs

### 6. Domain-Driven Design

**Belief:** The code should reflect the business domain.

**Implications:**
- Use domain language in code (Ubiquitous Language)
- Value objects represent domain concepts precisely
- Entities have meaningful identity and behavior
- Business logic lives in the domain layer

**Application:**
- `Money` value object represents monetary values
- `Portfolio` entity aggregates investment assets
- `AssetType` enum defines investment categories
- Domain methods (`total_value`, `allocation_by_type`) reflect business concepts

---

### 7. Value Objects Are Immutable

**Belief:** Value objects should never change after creation.

**Implications:**
- Use `@dataclass(frozen=True)` or enforce immutability
- Create new instances rather than modify existing ones
- No setters, only getters
- Value equality based on attributes, not identity

**Application:**
- `Money` objects are immutable (frozen dataclass)
- `AssetType` enum is immutable by definition
- Create new `Money` instance for currency conversion, don't modify

---

### 8. Entities Have Identity

**Belief:** Entities are identified by unique identity, not attributes.

**Implications:**
- Entities can change but remain the same entity
- Identity is stable over time
- Equality based on identity, not attributes
- Entities encapsulate business logic

**Application:**
- `InvestmentAsset` has name as identity (simplified)
- `Portfolio` aggregates assets by name identity
- Entity methods change internal state but preserve identity

---

## Technical Beliefs

### 9. Type Safety Matters

**Belief:** Static type checking catches errors early.

**Implications:**
- Use type hints for all public APIs
- Enable mypy for strict type checking
- Avoid `Any` type (unless necessary)
- Fix type errors, don't suppress them

**Application:**
- All functions have type hints
- Mypy configured for strict checking
- No type errors in the codebase
- Domain models use proper types (Decimal for money, not float)

---

### 10. Explicit is Better Than Implicit

**Belief:** Code should be clear about what it does.

**Implications:**
- Avoid magic methods unless necessary
- Be explicit about dependencies
- Use clear function names
- Don't hide important logic

**Application:**
- Use cases explicitly take repository dependencies
- Repository methods clearly describe their purpose
- Error messages are specific and actionable
- No hidden side effects in pure functions

---

### 11. Fail Fast and Loudly

**Belief:** Errors should be caught early and reported clearly.

**Implications:**
- Validate inputs at boundaries
- Raise exceptions for invalid states
- Provide meaningful error messages
- Don't silently ignore errors

**Application:**
- `ValueError` for invalid inputs (negative quantity, etc.)
- Custom domain exceptions for business rule violations
- Clear error messages in UI
- Logging for debugging and monitoring

---

### 12. Separation of Concerns

**Belief:** Each component should have a single, well-defined responsibility.

**Implications:**
- Layers have clear boundaries
- No mixing of concerns (e.g., UI logic in domain)
- Dependency direction is inward (outer layers depend on inner)
- Ports and adapters for external integrations

**Application:**
- Domain layer: business logic only
- Application layer: orchestration only
- Infrastructure layer: external integrations only
- Presentation layer: UI and user interaction only

---

## Development Beliefs

### 13. Test-Driven Development

**Belief:** Tests should drive development, not follow it.

**Implications:**
- Write tests before implementation (TDD)
- Tests define the expected behavior
- Red-Green-Refactor cycle
- Tests as living documentation

**Application:**
- Domain tests drive entity and value object design
- Application tests drive use case behavior
- Infrastructure tests validate integration
- Tests cover happy paths and error cases

---

### 14. Refactoring is Continuous

**Belief:** Code should be improved continuously, not just when adding features.

**Implications:**
- Refactor when adding features, not as a separate phase
- Keep the codebase clean over time
- Pay down technical debt regularly
- Don't tolerate code smells

**Application:**
- Extract common logic into reusable functions
- Simplify complex functions
- Remove duplicate code
- Improve naming as understanding deepens

---

### 15. Documentation is Code

**Belief:** Documentation should be kept in sync with code.

**Implications:**
- Docstrings for public APIs
- README reflects current state
- Architecture docs updated with changes
- Design docs inform implementation

**Application:**
- Comprehensive docstrings in domain layer
- Clear function signatures with type hints
- README is up-to-date with installation instructions
- Architecture docs reflect actual structure

---

## User Experience Beliefs

### 16. Privacy First

**Belief:** User data should stay under user control.

**Implications:**
- No central database for user data
- Data in Google Keep (user-controlled)
- No unnecessary data collection
- Transparent data handling

**Application:**
- Investment data stored in user's Google Keep
- No account registration required
- No tracking or analytics on user behavior
- Credentials stored locally in `.env` file

---

### 17. Simplicity for Users

**Belief:** Complex functionality should be simple to use.

**Implications:**
- Minimal configuration required
- Intuitive user interface
- Clear error messages
- Helpful defaults

**Application:**
- Natural language parsing for investment notes
- Simple dashboard with key metrics
- Clear error messages when data is invalid
- One-click data refresh

---

### 18. Progressive Disclosure

**Belief:** Start simple, reveal complexity when needed.

**Implications:**
- Basic features accessible to beginners
- Advanced features available when needed
- Don't overwhelm users with options
- Provide context-sensitive help

**Application:**
- Simple dashboard overview
- Advanced analytics available on demand
- Clear navigation between views
- Helpful tooltips and explanations

---

## When Beliefs Conflict

Beliefs sometimes conflict. When they do, prioritize:

1. **User Value** - What benefits the user most?
2. **Reliability** - What's most reliable long-term?
3. **Maintainability** - What's easiest to maintain?
4. **Performance** - What performs best?

Example: **Simplicity vs. Performance**
- Simple implementation vs. optimized version
- Choose simple unless performance is critical
- Measure before optimizing
- Optimize only when necessary

---

## Updating Core Beliefs

Core beliefs evolve as the project matures. To update a core belief:

1. **Justification** - Why is this belief no longer valid?
2. **Examples** - Specific cases where belief conflicts with reality
3. **Replacement** - What new belief replaces it?
4. **Impact** - How does this change affect the codebase?

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial core beliefs documentation |
