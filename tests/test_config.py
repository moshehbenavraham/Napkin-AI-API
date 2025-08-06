"""
Tests for configuration management.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch

from src.utils.config import Settings, get_settings, reload_settings


class TestSettings:
    """Test Settings configuration."""
    
    def test_required_api_token(self):
        """Test that API token is required."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(Exception) as exc_info:
                Settings()
            # Should fail due to missing required API token
            assert "api_token" in str(exc_info.value).lower()
    
    def test_settings_with_token(self):
        """Test settings with valid token."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings = Settings()
            assert settings.api_token == "test-token"
            assert settings.api_base_url == "https://api.napkin.ai"
            assert settings.api_version == "v1"
    
    def test_default_values(self):
        """Test default values are set correctly."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings = Settings()
            
            # Check defaults
            assert settings.default_style == "vibrant-strokes"
            assert settings.default_format == "svg"
            assert settings.default_language == "en-US"
            assert settings.default_variations == 1
            assert settings.max_retries == 3
            assert settings.timeout_seconds == 30
    
    def test_format_validation(self):
        """Test format validation."""
        with patch.dict(os.environ, {
            "NAPKIN_API_TOKEN": "test-token",
            "NAPKIN_DEFAULT_FORMAT": "invalid",
        }):
            with pytest.raises(Exception) as exc_info:
                Settings()
            assert "svg" in str(exc_info.value).lower()
    
    def test_log_level_validation(self):
        """Test log level validation."""
        with patch.dict(os.environ, {
            "NAPKIN_API_TOKEN": "test-token",
            "NAPKIN_LOG_LEVEL": "INVALID",
        }):
            with pytest.raises(Exception) as exc_info:
                Settings()
            assert "DEBUG" in str(exc_info.value)
    
    def test_api_url_property(self):
        """Test API URL construction."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings = Settings()
            assert settings.api_url == "https://api.napkin.ai/v1"
    
    def test_get_headers(self):
        """Test header generation."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings = Settings()
            headers = settings.get_headers()
            
            assert headers["Authorization"] == "Bearer test-token"
            assert headers["Content-Type"] == "application/json"
            assert headers["Accept"] == "application/json"
    
    def test_path_validation(self):
        """Test path fields create parent directories."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "nested" / "storage"
            db_path = Path(tmpdir) / "nested" / "db" / "napkin.db"
            
            with patch.dict(os.environ, {
                "NAPKIN_API_TOKEN": "test-token",
                "NAPKIN_STORAGE_PATH": str(storage_path),
                "NAPKIN_DATABASE_PATH": str(db_path),
            }):
                settings = Settings()
                
                # Parent directories should be created
                assert settings.storage_path.parent.exists()
                assert settings.database_path.parent.exists()


class TestSettingsSingleton:
    """Test settings singleton behavior."""
    
    def test_get_settings_singleton(self):
        """Test that get_settings returns singleton."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings1 = get_settings()
            settings2 = get_settings()
            assert settings1 is settings2
    
    def test_reload_settings(self):
        """Test reload_settings creates new instance."""
        with patch.dict(os.environ, {"NAPKIN_API_TOKEN": "test-token"}):
            settings1 = get_settings()
            
            # Change environment
            with patch.dict(os.environ, {
                "NAPKIN_API_TOKEN": "new-token",
                "NAPKIN_DEFAULT_STYLE": "sketch-notes",
            }):
                settings2 = reload_settings()
                
                # Should be different instance
                assert settings2 is not settings1
                assert settings2.api_token == "new-token"
                assert settings2.default_style == "sketch-notes"
                
                # get_settings should now return the new instance
                settings3 = get_settings()
                assert settings3 is settings2