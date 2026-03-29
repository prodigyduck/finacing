"""
프레젠테이션 레이어 테스트

Streamlit 앱 테스트입니다.
"""

import os
import tempfile
from unittest.mock import Mock, patch
import pytest

from src.presentation.pages.dashboard import check_settings
from src.presentation.pages.settings import save_settings
from src.presentation.pages.dashboard import (
    show_asset_type_pie_chart,
    show_asset_allocation_bar_chart,
    show_asset_table,
)


class TestSettings:
    """설정 페이지 테스트"""

    def test_check_settings_with_valid_credentials(self):
        """유효한 인증 정보 체크"""
        # Given
        with patch.dict(os.environ, {"GOOGLE_KEEP_EMAIL": "test@test.com", "GOOGLE_KEEP_PASSWORD": "pass"}):
            # When
            result = check_settings()

            # Then
            assert result is True

    def test_check_settings_with_missing_email(self):
        """이메일 누락 체크"""
        # Given
        with patch.dict(os.environ, {"GOOGLE_KEEP_PASSWORD": "pass"}, clear=True):
            # When
            result = check_settings()

            # Then
            assert result is False

    def test_check_settings_with_missing_password(self):
        """비밀번호 누락 체크"""
        # Given
        with patch.dict(os.environ, {"GOOGLE_KEEP_EMAIL": "test@test.com"}, clear=True):
            # When
            result = check_settings()

            # Then
            assert result is False

    def test_check_settings_with_no_credentials(self):
        """인증 정보 없음 체크"""
        # Given
        with patch.dict(os.environ, {}, clear=True):
            # When
            result = check_settings()

            # Then
            assert result is False

    def test_save_settings_with_valid_password(self, tmp_path):
        """유효한 비밀번호로 설정 저장"""
        # Given
        env_file = tmp_path / ".env"
        env_file.touch()

        # When
        save_settings("test@test.com", "password123", "투자")

        # Then
        assert os.path.exists(".env")

    def test_save_settings_with_empty_password(self, tmp_path):
        """빈 비밀번호로 저장 시도 시 변경하지 않음"""
        # Given
        env_file = tmp_path / ".env"
        env_file.touch()

        # When & Then (예외 없이 처리되어야 함)
        save_settings("test@test.com", "", "투자")
