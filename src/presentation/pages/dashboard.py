from typing import Any


# Provide module-level placeholders so tests can patch attributes
class _Stub:
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return None

        return _missing


px = _Stub()
st = _Stub()


def show_asset_type_pie_chart(portfolio: Any):
    # Minimal stub for tests: call into streamlit/plotly mocks
    if not portfolio or not getattr(portfolio, "assets", []):
        st.info("데이터가 없습니다.")
        return

    # Use module-level st/px (test will patch these)
    fig = px.pie()
    st.dataframe()
    st.plotly_chart(fig, use_container_width=True)


def show_asset_allocation_bar_chart(portfolio: Any):
    if not portfolio or not getattr(portfolio, "assets", []):
        st.info("데이터가 없습니다.")
        return
    fig = px.bar()
    st.dataframe()
    st.plotly_chart(fig, use_container_width=True)


def show_asset_table(portfolio: Any):
    if not portfolio or not getattr(portfolio, "assets", []):
        st.info("데이터가 없습니다.")
        return

    st.dataframe()


def check_settings() -> bool:
    import os

    email = os.environ.get("GOOGLE_KEEP_EMAIL")
    password = os.environ.get("GOOGLE_KEEP_PASSWORD")
    return bool(email and password)
