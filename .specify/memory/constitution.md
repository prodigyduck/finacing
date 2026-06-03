<!-- 
Sync Impact Report:
- Version change: N/A -> 1.0.0
- Added sections: Core Principles, Governance
- Updated placeholders: All [PLACEHOLDERS] filled
- Templates requiring updates: ⚠ Plan Template, ⚠ Spec Template, ⚠ Tasks Template (Check against updated principles)
-->
# Financing Constitution

## Core Principles

### I. Code Quality (Clean Architecture)
Financing MUST adhere to a strict Clean Architecture. Business logic (Domain) MUST be independent of frameworks and infrastructure (Parsers, REST APIs). All code MUST have type hints (mypy), conform to Black formatting, and pass Ruff static analysis. Dependency direction: Infrastructure → Application → Domain.

### II. Testing Standards (TDD & Coverage)
Testing is NON-NEGOTIABLE. TDD is the preferred workflow for business logic (Domain/Application). All new features MUST have associated unit tests. E2E tests (Playwright) MUST verify critical user flows. CI pipeline coverage MUST reflect all code paths.

### III. User Experience Consistency (Toss-Style)
The UI/UX MUST maintain Toss-style design principles: extreme clarity, minimal visual noise, clear information hierarchy, and consistent interaction patterns. Components MUST be responsive and accessible. Design decisions MUST prioritize user trust and information digestibility.

### IV. Performance Requirements (Responsive & Efficient)
The application MUST be performant. Backend data processing (e.g., trend analysis) MUST be optimized for latency. Frontend MUST implement efficient query patterns to avoid redundant data fetching. UI interactions MUST be immediate and responsive to user input.

## Additional Standards

### Security & Data Integrity
Obsidian data MUST remain local and read-only. REST API endpoints MUST use API keys for any modification (if implemented). No PII or sensitive proprietary data MUST be exposed or transmitted insecurely.

## Development Workflow

### Quality Gates
Every PR MUST pass unit tests, E2E tests, mypy, and ruff before being merged. Code reviews MUST focus on adherence to Clean Architecture and Consistency with existing patterns. Code that bypasses quality gates MUST be strictly rejected.

## Governance

This Constitution supersedes all other practices. Amendments require a clear migration plan, documentation, and approval.

**Version**: 1.0.0 | **Ratified**: 2026-05-31 | **Last Amended**: 2026-05-31
