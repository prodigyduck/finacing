"""
대시보드 페이지 테스트

Streamlit 대시보드 테스트입니다.
"""

from unittest.mock import Mock, patch, MagicMock
import pytest

from src.presentation.pages.dashboard import (
    show_asset_type_pie_chart,
    show_asset_allocation_bar_chart,
    show_asset_table,
)


class TestDashboard:
    """대시보드 페이지 테스트"""

    @patch("src.presentation.pages.dashboard.px.pie")
    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_type_pie_chart_with_valid_data(self, mock_st, mock_pie, sample_portfolio):
        """유효한 데이터로 파이 차트 표시"""
        # Given
        mock_fig = MagicMock()
        mock_pie.return_value = mock_fig
        mock_st.dataframe = MagicMock()

        # When
        show_asset_type_pie_chart(sample_portfolio)

        # Then
        mock_pie.assert_called_once()
        mock_st.dataframe.assert_called_once()
        mock_st.plotly_chart.assert_called_once_with(mock_fig, use_container_width=True)

    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_type_pie_chart_with_empty_data(self, mock_st, empty_portfolio):
        """빈 데이터로 파이 차트 표시 시 정보 메시지"""
        # Given
        mock_st.info = MagicMock()

        # When
        show_asset_type_pie_chart(empty_portfolio)

        # Then
        mock_st.info.assert_called_once_with("데이터가 없습니다.")

    @patch("src.presentation.pages.dashboard.px.bar")
    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_allocation_bar_chart_with_valid_data(self, mock_st, mock_bar, sample_portfolio):
        """유효한 데이터로 바 차트 표시"""
        # Given
        mock_fig = MagicMock()
        mock_bar.return_value = mock_fig
        mock_st.dataframe = MagicMock()

        # When
        show_asset_allocation_bar_chart(sample_portfolio)

        # Then
        mock_bar.assert_called_once()
        mock_st.dataframe.assert_called_once()
        mock_st.plotly_chart.assert_called_once_with(mock_fig, use_container_width=True)

    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_allocation_bar_chart_with_empty_data(self, mock_st, empty_portfolio):
        """빈 데이터로 바 차트 표시 시 정보 메시지"""
        # Given
        mock_st.info = MagicMock()

        # When
        show_asset_allocation_bar_chart(empty_portfolio)

        # Then
        mock_st.info.assert_called_once_with("데이터가 없습니다.")

    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_table_with_valid_data(self, mock_st, sample_portfolio):
        """유효한 데이터로 테이블 표시"""
        # When
        show_asset_table(sample_portfolio)

        # Then
        mock_st.dataframe.assert_called()

    @patch("src.presentation.pages.dashboard.st")
    def test_show_asset_table_with_empty_data(self, mock_st, empty_portfolio):
        """빈 데이터로 테이블 표시 시 정보 메시지"""
        # Given
        mock_st.info = MagicMock()

        # When
        show_asset_table(empty_portfolio)

        # Then
        mock_st.info.assert_called_once_with("데이터가 없습니다.")
        mock_st.dataframe.assert_not_called()
