# Feature Specification: System Documentation

**Feature Branch**: `[003-system-documentation]`

**Created**: 2026-06-06

**Status**: Draft

**Input**: User description: "현재 프로젝트의 구성을 분석해서 명세를 만들자"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Portfolio Overview (Priority: P1)

As an investor, I want to view my portfolio's current value, total change, and return rate in a single dashboard so that I can quickly assess my investment performance.

**Why this priority**: This is the primary use case and the most critical user journey. Users should be able to see their investment status at a glance.

**Independent Test**: Can be fully tested by accessing the dashboard and verifying that current portfolio metrics are displayed correctly with accurate calculations.

**Acceptance Scenarios**:

1. **Given** the system has investment data, **When** I open the dashboard, **Then** I should see the latest portfolio value displayed prominently
2. **Given** there are multiple investment records, **When** I view the dashboard, **Then** I should see the total change from the earliest record with appropriate color coding (positive=green, negative=red)
3. **Given** investment data exists, **When** I view the dashboard, **Then** I should see the return rate percentage displayed

---

### User Story 2 - Portfolio Trend Visualization (Priority: P1)

As an investor, I want to see my portfolio's value trend over time with projections so that I can understand my investment trajectory and make informed decisions.

**Why this priority**: Trend analysis is fundamental to investment decision-making. Users need visual representation of historical performance and future projections.

**Independent Test**: Can be tested by viewing the portfolio chart and verifying that historical data points and projection lines are displayed correctly.

**Acceptance Scenarios**:

1. **Given** there are 10+ investment records, **When** I view the portfolio chart, **Then** I should see a line chart showing portfolio value over time
2. **Given** the system has sufficient historical data, **When** I view the chart in daily mode, **Then** I should see 3, 6, and 12-month projection lines displayed
3. **Given** I switch between daily/weekly/monthly views, **When** I select a view, **Then** the chart should aggregate data appropriately (daily=all points, weekly=last value of each week, monthly=last value of each month)

---

### User Story 3 - Account-Level Analysis (Priority: P1)

As an investor with multiple accounts, I want to see individual account balances, allocations, and performance comparisons so that I can understand which accounts are performing best.

**Why this priority**: Users often spread investments across multiple accounts and need visibility into each account's contribution and performance.

**Independent Test**: Can be tested by viewing the dashboard with account-based data format and verifying that account cards, charts, and comparison tables are displayed correctly.

**Acceptance Scenarios**:

1. **Given** I have account-based data format, **When** I view the dashboard, **Then** I should see individual account cards showing each account's amount and allocation percentage
2. **Given** multiple accounts exist, **When** I view the account chart, **Then** I should see a line chart comparing each account's value over time (excluding the total account)
3. **Given** account data exists, **When** I view the comparison table, **Then** I should see which account has the highest and lowest allocation percentage
4. **Given** account data exists, **When** I view the allocation chart, **Then** I should see a pie or bar chart showing the percentage allocation across all accounts

---

### User Story 4 - Data Synchronization (Priority: P1)

As an investor who maintains my data in Obsidian, I want to sync my investment data from my Obsidian vault so that the dashboard always shows the latest information.

**Why this priority**: The system depends on Obsidian as the source of truth. Synchronization is critical for data freshness and accuracy.

**Independent Test**: Can be tested by modifying the Obsidian file, clicking the Git Pull button, and verifying that the dashboard reflects the changes.

**Acceptance Scenarios**:

1. **Given** I have new data in my Obsidian vault, **When** I click the Git Pull button, **Then** the system should fetch the latest data and refresh the dashboard
2. **Given** the Obsidian file has been modified, **When** I refresh the dashboard, **Then** I should see the updated data displayed
3. **Given** there are no new changes, **When** I sync the data, **Then** the system should report a successful sync without errors

---

### User Story 5 - Historical Data View (Priority: P2)

As an investor, I want to view detailed historical records in a table format so that I can review past investment values and day-to-day changes.

**Why this priority**: While visual charts are useful, some users prefer tabular data for detailed analysis and record-keeping.

**Independent Test**: Can be tested by scrolling through the data table and verifying that all records are listed with correct values and change calculations.

**Acceptance Scenarios**:

1. **Given** there are multiple investment records, **When** I scroll to the data table, **Then** I should see all records with date, amount, and change columns
2. **Given** I'm viewing daily data, **When** I look at the table, **Then** each row should show the change from the previous record
3. **Given** I'm viewing weekly/monthly data, **When** I look at the table, **Then** the change should be calculated between aggregated periods

---

### User Story 6 - Raw Data Management (Priority: P2)

As an advanced user, I want to view and edit raw investment data directly so that I can maintain complete control over my investment records.

**Why this priority**: Power users may prefer to work with raw data format for bulk updates or integration with other tools.

**Independent Test**: Can be tested by accessing the raw data view and verifying that data can be read, written, and persisted correctly.

**Acceptance Scenarios**:

1. **Given** I have investment data, **When** I access the raw data endpoint, **Then** I should see the complete data in its original format
2. **Given** I'm authenticated with API key, **When** I send updated raw data, **Then** the system should save the data to the Obsidian file
3. **Given** I save data with commit enabled, **When** the save completes, **Then** a git commit should be created with an appropriate message

---

### User Story 7 - Account Data Management (Priority: P2)

As an investor with multiple accounts, I want to view and edit account-based investment records so that I can maintain detailed per-account information including holdings.

**Why this priority**: Users with account-based data format need to update individual account records with their specific holdings and values.

**Independent Test**: Can be tested by retrieving account data for a specific date, modifying it, and saving it back with verification.

**Acceptance Scenarios**:

1. **Given** I have account-based data, **When** I request data for a specific date, **Then** I should receive all accounts with their amounts and holdings for that date
2. **Given** I'm authenticated with API key, **When** I submit account data for a date, **Then** the system should replace existing data for that date or append if new
3. **Given** I save account data, **When** the operation completes, **Then** the markdown file should be updated with proper formatting (## Date header, ### Account subheaders, 총액 and 보유종목 sections)

---

### Edge Cases

- What happens when the Obsidian file doesn't exist or is empty?
- What happens when the Obsidian file format is invalid or malformed?
- What happens when there are fewer than 2 data points (insufficient for projections)?
- What happens when git sync fails (network issues, merge conflicts)?
- What happens when the API key is missing or invalid for write operations?
- What happens when attempting to save data for a date that doesn't exist in the expected format (YYYY-MM-DD)?
- What happens when account names contain special characters or have inconsistent naming?
- What happens when the number of accounts exceeds the available colors for visualization?

## Requirements *(mandatory)*

### Functional Requirements

#### Data Ingestion & Parsing
- **FR-001**: System MUST read investment data from a specified local Obsidian markdown file location
- **FR-002**: System MUST support parsing legacy format data (M.DD 억 format)
- **FR-003**: System MUST support parsing account-based format data (structured with account names, amounts, and holdings)
- **FR-004**: System MUST automatically detect and use the appropriate parser based on file content
- **FR-005**: System MUST validate date, month, and day values are within valid ranges
- **FR-006**: System MUST validate that amounts are non-negative numeric values
- **FR-007**: System MUST handle both Korean Won (억) and numeric amount formats

#### Portfolio Analysis & Calculations
- **FR-008**: System MUST calculate total change (latest amount - earliest amount)
- **FR-009**: System MUST calculate return rate percentage ((total_change / earliest_amount) * 100)
- **FR-010**: System MUST generate linear regression projections for 3, 6, and 12 months into the future
- **FR-011**: System MUST aggregate data by week (using last value of each week) when weekly view is selected
- **FR-012**: System MUST aggregate data by month (using last value of each month) when monthly view is selected
- **FR-013**: System MUST calculate day-to-day change between consecutive records
- **FR-014**: System MUST apply color coding to positive (green), negative (red), and neutral changes

#### Account-Level Analysis
- **FR-015**: System MUST calculate allocation percentage for each account (account_amount / total_amount)
- **FR-016**: System MUST identify the account with the highest allocation percentage (best performer)
- **FR-017**: System MUST identify the account with the lowest allocation percentage (worst performer)
- **FR-018**: System MUST generate account history time-series data (6 months onwards only, excluding total account)
- **FR-019**: System MUST assign distinct colors to each account for visualization (cycling through color palette)
- **FR-020**: System MUST maintain holdings information (list of stock symbols or holdings) per account

#### Data Synchronization
- **FR-021**: System MUST support git pull to sync from the Obsidian vault
- **FR-022**: System MUST provide a sync button in the UI that triggers git pull
- **FR-023**: System MUST automatically sync data when fetching history
- **FR-024**: System MUST display sync status (loading, success, error) to the user
- **FR-025**: System MUST retry failed sync operations up to 3 times with exponential backoff

#### API Endpoints
- **FR-026**: System MUST provide GET /health endpoint that returns system health status
- **FR-027**: System MUST provide GET /api/v1/history endpoint that returns portfolio data with optional year filter
- **FR-028**: System MUST provide GET /api/v1/raw-data endpoint that returns raw investment data
- **FR-029**: System MUST provide PUT /api/v1/raw-data endpoint that accepts raw data updates
- **FR-030**: System MUST provide GET /api/v1/account-data endpoint that returns account data for a specific date
- **FR-031**: System MUST provide POST /api/v1/account-data endpoint that saves account data updates
- **FR-032**: System MUST provide POST /api/v1/sync endpoint that triggers git sync

#### Security & Access Control
- **FR-033**: System MUST require API key authentication for write operations (PUT/POST)
- **FR-034**: System MUST validate API key from HTTP header (X-API-Key)
- **FR-035**: System MUST return 403 Forbidden for invalid or missing API keys on write operations
- **FR-036**: System MUST use a default local-dev-only API key for development environments

#### Data Persistence
- **FR-037**: System MUST write raw data updates to the Obsidian markdown file
- **FR-038**: System MUST write account data updates to the Obsidian markdown file with proper markdown formatting
- **FR-039**: System MUST replace existing date sections when updating account data for the same date
- **FR-040**: System MUST optionally create git commits with descriptive messages when saving data
- **FR-041**: System MUST return git commit hash when commits are created successfully

#### Error Handling & User Feedback
- **FR-042**: System MUST display user-friendly error messages for common failure scenarios (network, parsing, git)
- **FR-043**: System MUST provide retry buttons for failed operations
- **FR-044**: System MUST return appropriate HTTP status codes (404 for not found, 422 for validation errors, 500 for server errors)
- **FR-045**: System MUST log all errors with sufficient context for debugging
- **FR-046**: System MUST display empty state when no investment data is available
- **FR-047**: System MUST display last update timestamp to indicate data freshness

#### Visualization & User Interface
- **FR-048**: System MUST display portfolio chart with historical data points
- **FR-049**: System MUST display projection lines on the chart (in daily view only)
- **FR-050**: System MUST allow switching between daily, weekly, and monthly time period views
- **FR-051**: System MUST display key metrics in cards (Latest Value, Change, Return Rate, Records)
- **FR-052**: System MUST display account cards for each account when account-based data is available
- **FR-053**: System MUST display account comparison chart showing historical account values
- **FR-054**: System MUST display comparison table with account rankings (best/worst performer by allocation)
- **FR-055**: System MUST display allocation chart showing percentage distribution across accounts
- **FR-056**: System MUST display data table with sorted historical records

### Key Entities

- **Investment Record**: A single point-in-time portfolio valuation with date, amount in 억 (100 million KRW), and derived change values
- **Portfolio History**: A time-ordered collection of investment records with calculated metrics (latest, total_change, return_rate) and projections
- **Account**: A named investment account with type (securities, ISA, IRA, pension, cash, other) and description
- **Account Record**: A snapshot of an account's state on a specific date with total amount and list of holdings (stocks or assets)
- **Portfolio Snapshot**: A collection of account records representing all accounts on a specific date
- **Holding**: A single asset or stock symbol held within an account
- **Projection**: A forecasted portfolio value at a future date (3, 6, or 12 months) based on linear regression

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dashboard loads and displays portfolio metrics within 2 seconds on a standard machine
- **SC-002**: Git pull synchronization completes within 5 seconds for typical file sizes
- **SC-003**: Data refresh (without git sync) completes within 1 second
- **SC-004**: All projections are calculated with at least 95% accuracy compared to linear regression baseline
- **SC-005**: Chart rendering supports up to 365 data points without performance degradation
- **SC-006**: Data parsing correctly handles both legacy and account-based formats with 100% success rate for valid inputs
- **SC-007**: API responses for history endpoint complete within 500ms
- **SC-008**: Write operations (raw data and account data) complete within 1 second
- **SC-009**: Git commits are successfully created for 100% of write operations when commit is enabled
- **SC-010**: Error messages are understandable and actionable for 90% of common error scenarios

## Assumptions

- The user maintains an Obsidian vault with investment data in a known file location
- The user has git installed and configured for the Obsidian vault
- The Obsidian file follows either legacy or account-based format consistently
- The user has access to the local filesystem where Obsidian stores its files
- API key for write operations can be set via environment variable (FINANCING_API_KEY)
- The system runs on a single-user local environment (no multi-user authentication required)
- Internet connectivity is available for git sync operations
- The user's Obsidian vault is a git repository
- Investment amounts are denominated in Korean Won (억 = 100 million)
- Historical data is sufficient for projections (minimum 2 data points)
- Total account (총계좌) exists in account-based format for aggregation
- The system has read-write permissions to the Obsidian file location
- Week numbers follow ISO 8601 standard for weekly aggregation
- Linear regression provides acceptable accuracy for investment projections
- Color palette provides sufficient contrast for account visualization
- Frontend and backend run on the same local machine (localhost)

## Scope Boundaries

### In Scope

- Reading and parsing investment data from Obsidian markdown files
- Calculating portfolio metrics and projections
- Visualizing portfolio trends and account-level analysis
- Git synchronization with Obsidian vault
- REST API for data access and updates
- Web-based dashboard with responsive design
- Support for both legacy and account-based data formats
- API key authentication for write operations
- Git commit integration for data changes

### Out of Scope

- Real-time stock price updates or market data integration
- Multi-user authentication and authorization
- Cloud hosting or remote data storage
- Mobile app development (responsive web only)
- Advanced portfolio optimization algorithms (beyond linear regression)
- Tax calculation or reporting features
- Trading or transaction execution
- Import from multiple data sources (Obsidian only)
- Historical data beyond what exists in Obsidian file
- Automated rebalancing recommendations
- Risk assessment or volatility metrics
- Integration with external financial APIs
- User accounts, profiles, or preferences persistence
- Email notifications or alerts
- Data export to other formats (markdown only)
- Backup or recovery features (git handles this)

## Dependencies

- Obsidian markdown file must exist at specified path
- Obsidian vault must be a git repository
- Python 3.9+ runtime environment
- Node.js runtime environment for frontend
- Git must be installed and accessible from system PATH
- Environment variable for API key configuration (FINANCING_API_KEY)
- Existing template files for markdown formatting
- System file system permissions for reading/writing Obsidian files

## Open Questions

None - All critical requirements are documented with reasonable assumptions.