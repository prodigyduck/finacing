# Frontend Architecture

## Overview

The Financing project uses **Streamlit** as the frontend framework. Streamlit is a Python-based web framework that allows for rapid development of data applications with minimal code. This document outlines the frontend architecture, component structure, and UI patterns.

## Technology Stack

- **Framework:** Streamlit 1.31.0+
- **Visualization:** Plotly 5.18.0+
- **UI Components:** Streamlit native components
- **State Management:** Streamlit Session State
- **Deployment:** Local development, Tailscale Funnel, or SSH tunneling

---

## Architecture Overview

### Streamlit Architecture

```
User Browser → Streamlit Server (Python) → Application Logic
     ↓                    ↓
  React UI           Backend Processing
  (Auto-generated)   (Fast, Pythonic)
```

**Key Characteristics:**
- **Auto-Generated UI:** Streamlit automatically generates React UI from Python code
- **Stateless by Default:** Each interaction re-runs the entire script
- **Session State:** Persist data across reruns using `st.session_state`
- **Reactive:** UI updates automatically when data changes

### Application Structure

```
src/presentation/
├── app.py                 # Main application entry point
└── pages/
    ├── __init__.py
    ├── dashboard.py        # Portfolio visualization
    └── settings.py        # Google Keep authentication
```

---

## Page Architecture

### Main Application (`app.py`)

**Responsibilities:**
- Initialize Streamlit app configuration
- Manage page navigation
- Handle global app state

**Code Structure:**
```python
def main():
    # Page configuration
    st.set_page_config(
        page_title="Financing - 투자 대시보드",
        page_icon="💰",
        layout="wide",
    )

    # App title
    st.title("💰 Financing - 투자 대시보드")

    # Page navigation (sidebar)
    page = st.sidebar.radio("페이지 선택", ["대시보드", "설정"])

    # Route to appropriate page
    if page == "대시보드":
        show_dashboard()
    elif page == "설정":
        show_settings()
```

**Key Patterns:**
- Use `st.set_page_config()` once at the start
- Sidebar for navigation
- Page functions are pure (no state)
- Page selection determines which page function to call

---

### Dashboard Page (`dashboard.py`)

**Responsibilities:**
- Display portfolio overview
- Visualize asset allocation
- Show investment returns
- Provide interactive filters

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  Portfolio Overview Cards               │
│  Total Value | Total Gain | Asset Count │
├─────────────────────────────────────────┤
│  Asset Allocation Chart (Pie Chart)     │
├─────────────────────────────────────────┤
│  Asset List Table                      │
│  Name | Type | Quantity | Value | Gain   │
└─────────────────────────────────────────┘
```

**Implementation Patterns:**
```python
def show_dashboard():
    # Fetch data
    assets = fetch_investment_data()

    # Overview cards (columns layout)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Value", format_money(total_value))
    with col2:
        st.metric("Total Gain", format_money(total_gain))
    with col3:
        st.metric("Asset Count", len(assets))

    # Allocation chart
    fig = create_allocation_chart(allocation)
    st.plotly_chart(fig)

    # Asset table
    df = create_asset_dataframe(assets)
    st.dataframe(df)
```

**State Management:**
- No persistent state in dashboard
- All data fetched fresh on each interaction
- Uses caching for expensive operations (`@st.cache_data`)

---

### Settings Page (`settings.py`)

**Responsibilities:**
- Configure Google Keep authentication
- Test connection to Google Keep
- Manage application settings

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  Google Keep Authentication             │
│  Email: [____________]                   │
│  Password: [____________]               │
│  Master Token (optional): [________]     │
│  [Test Connection] [Save]               │
├─────────────────────────────────────────┤
│  Connection Status: ✓ Connected         │
└─────────────────────────────────────────┘
```

**Implementation Patterns:**
```python
def show_settings():
    st.subheader("Google Keep Authentication")

    # Input form
    with st.form("auth_form"):
        email = st.text_input("Email", value=os.getenv("GOOGLE_KEEP_EMAIL", ""))
        password = st.text_input("Password", type="password")
        master_token = st.text_input("Master Token (2FA)", type="password")

        # Form buttons
        col1, col2 = st.columns(2)
        with col1:
            test_button = st.form_submit_button("Test Connection")
        with col2:
            save_button = st.form_submit_button("Save")

    # Handle form submission
    if test_button:
        test_connection(email, password, master_token)
    if save_button:
        save_credentials(email, password, master_token)
```

**State Management:**
- Credentials stored in `.env` file (not session state)
- Form submission triggers file write
- Connection test uses ephemeral authentication

---

## Component Patterns

### 1. Metric Cards

Display key metrics with optional delta (change) indicators.

```python
# Simple metric
st.metric("Total Value", "₩10,000,000")

# Metric with delta
st.metric("Total Value", "₩10,000,000", "+₩500,000 (5.2%)")

# Color-coded delta
st.metric("Total Value", "₩10,000,000", "-₩100,000 (-1.0%)")
```

**Best Practices:**
- Use for key performance indicators (KPIs)
- Format numbers with appropriate units
- Show delta for trends over time
- Use color coding (green for positive, red for negative)

---

### 2. Data Tables

Display structured data with sorting and filtering.

```python
# Simple table
df = pd.DataFrame({
    "Name": ["Stock A", "Stock B", "ETF C"],
    "Value": [1000000, 2000000, 3000000]
})
st.dataframe(df)

# Styled table with formatting
st.dataframe(
    df,
    column_config={
        "Value": st.column_config.NumberColumn(
            "Value (KRW)",
            format="₩%d"
        )
    }
)
```

**Best Practices:**
- Use `st.dataframe` for interactive tables
- Use `st.table` for static tables
- Format columns appropriately (currency, percentage, etc.)
- Use column configuration for better UX

---

### 3. Charts

Visualize data using Plotly charts.

```python
# Pie chart for allocation
fig = px.pie(
    values=[30, 50, 20],
    names=["Stocks", "ETFs", "Cash"],
    title="Asset Allocation"
)
st.plotly_chart(fig)

# Bar chart for comparison
fig = px.bar(
    x=["Stock A", "Stock B", "ETF C"],
    y=[1000000, 2000000, 3000000],
    title="Asset Values"
)
st.plotly_chart(fig)
```

**Best Practices:**
- Use Plotly for interactive charts
- Add titles and labels for clarity
- Use appropriate chart types for data
- Responsive charts adjust to container width

---

### 4. Forms

Collect user input with validation.

```python
# Simple form
with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")

    if submitted:
        process_form(name, email)

# Form with validation
with st.form("validated_form"):
    email = st.text_input("Email")

    if st.form_submit_button("Submit"):
        if not validate_email(email):
            st.error("Invalid email format")
        else:
            process_email(email)
```

**Best Practices:**
- Use forms for multi-field inputs
- Validate input before submission
- Show error messages inline
- Use appropriate input types (password, number, etc.)

---

### 5. Sidebar

Use sidebar for navigation and global controls.

```python
# Navigation
page = st.sidebar.radio("Page", ["Dashboard", "Settings"])

# Global controls
st.sidebar.checkbox("Show Details", key="show_details")
st.sidebar.slider("Date Range", 1, 365, 30)

# Information
st.sidebar.info("App Version 1.0.0")
```

**Best Practices:**
- Use sidebar for navigation
- Keep sidebar controls simple
- Avoid complex forms in sidebar
- Group related controls

---

## State Management

### Streamlit Session State

Persist data across reruns using `st.session_state`.

```python
# Initialize state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Update state
st.session_state.authenticated = True

# Read state
if st.session_state.authenticated:
    show_protected_content()
```

**Use Cases:**
- User authentication status
- Page navigation state
- User preferences (theme, language)
- Cached computation results

**Best Practices:**
- Initialize state at the top of the script
- Use descriptive keys for state variables
- Clean up unused state
- Avoid storing large objects in state

### Caching

Cache expensive computations to improve performance.

```python
# Data caching (expires after app restart)
@st.cache_data
def fetch_expensive_data():
    # Expensive operation
    return data

# Resource caching (persists across reruns)
@st.cache_resource
def initialize_model():
    # Expensive resource initialization
    return model
```

**Best Practices:**
- Use `@st.cache_data` for data
- Use `@st.cache_resource` for resources
- Add hash_funcs for unhashable arguments
- Clear cache selectively with `st.cache_data.clear()`

---

## Error Handling & User Feedback

### Error Messages

Provide clear, actionable error messages to users.

```python
# Success message
st.success("Data fetched successfully!")

# Info message
st.info("Loading data...")

# Warning message
st.warning("Some data is missing")

# Error message
st.error("Failed to connect to Google Keep. Please check your credentials.")
```

**Best Practices:**
- Use appropriate message type (success, info, warning, error)
- Provide actionable guidance
- Avoid technical jargon
- Never expose sensitive information

### Loading Indicators

Show loading state for long-running operations.

```python
# Simple loading
with st.spinner("Fetching data..."):
    data = fetch_data()

# Custom loading
loading_text = st.empty()
loading_text.text("Processing...")
# ... long operation
loading_text.empty()
```

**Best Practices:**
- Use loading indicators for operations > 1 second
- Provide context about what's happening
- Update loading text for multi-step operations
- Clear loading indicator when done

---

## Responsive Design

### Layout Responsiveness

Streamlit automatically adjusts to screen size.

```python
# Wide layout for large screens
st.set_page_config(layout="wide")

# Columns adjust to screen width
col1, col2, col3 = st.columns(3)  # Equal width columns

# Responsive columns (specify ratios)
col1, col2 = st.columns([2, 1])  # 2:1 ratio
```

**Best Practices:**
- Use wide layout for data-rich applications
- Use column ratios to prioritize content
- Test on different screen sizes
- Consider mobile users (simplify UI if needed)

---

## Accessibility

### Visual Accessibility

Ensure UI is accessible to all users.

```python
# Use clear, descriptive labels
st.text_input("Email address")  # ✅ Good
st.text_input("Email")  # ✅ Better

# Use icons for visual context
st.metric("Total Value", "₩10,000,000", icon="💰")

# Use color coding carefully (don't rely on color alone)
st.success("Connected")  # ✅ Clear
st.error("Failed")  # ✅ Clear
```

**Best Practices:**
- Use clear, descriptive labels
- Use icons for visual context
- Provide alternative text for images
- Don't rely on color alone to convey information

---

## Performance Optimization

### 1. Minimize Reruns

Use caching and state management to minimize script reruns.

```python
# ❌ Bad: Expensive operation runs on every interaction
def show_dashboard():
    data = fetch_expensive_data()  # Runs every time
    st.dataframe(data)

# ✅ Good: Cache expensive operation
@st.cache_data
def get_data():
    return fetch_expensive_data()

def show_dashboard():
    data = get_data()  # Runs only once
    st.dataframe(data)
```

### 2. Lazy Loading

Load data only when needed.

```python
# ❌ Bad: Load all data upfront
all_data = load_all_data()

def show_dashboard():
    st.dataframe(all_data)

# ✅ Good: Load data on demand
def show_dashboard():
    if st.button("Load Data"):
        data = load_data()
        st.dataframe(data)
```

### 3. Pagination

Paginate large datasets for better performance.

```python
def show_paginated_table(df, page_size=10):
    total_pages = (len(df) // page_size) + 1
    page = st.number_input("Page", 1, total_pages)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    st.dataframe(df.iloc[start_idx:end_idx])
```

---

## Testing

### UI Testing Strategy

**Test Coverage Goal:** 50% for presentation layer

**Testing Tools:**
- `pytest` for unit tests
- Custom fixtures for Streamlit components
- Integration tests for page flows

**Example Test:**
```python
# tests/unit/presentation/test_dashboard.py
def test_show_dashboard_renders_metrics(mock_st):
    """Test that dashboard renders key metrics"""
    # Mock data
    assets = create_test_assets()

    # Show dashboard
    show_dashboard(assets)

    # Verify metrics displayed
    assert mock_st.metric.call_count == 3
```

---

## Deployment

### Local Development

```bash
# Run locally
streamlit run src/presentation/app.py

# Access at http://localhost:8501
```

### Remote Access

**Option 1: Tailscale Funnel**
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Streamlit
streamlit run src/presentation/app.py &

# Expose via Funnel
tailscale funnel 8501
```

**Option 2: SSH Tunneling**
```bash
# Local machine
ssh -L 8501:localhost:8501 user@remote-server

# Access at http://localhost:8501
```

**Option 3: VPN**
```bash
# Deploy on internal network
# Access via VPN connection
```

---

## Best Practices Summary

1. **Keep pages simple:** Each page should have a single responsibility
2. **Use caching:** Cache expensive operations with `@st.cache_data`
3. **Manage state carefully:** Initialize state at the top, clean up when done
4. **Provide feedback:** Use success/error messages and loading indicators
5. **Responsive design:** Use wide layout and flexible columns
6. **Test thoroughly:** Write tests for UI components and page flows
7. **Secure deployment:** Use VPN or SSH tunneling for remote access
8. **Monitor performance:** Use Streamlit's built-in performance tools

---

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cheatsheet](https://cheat-sheet.streamlit.app/)
- [Plotly Documentation](https://plotly.com/python/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial frontend architecture documentation |
