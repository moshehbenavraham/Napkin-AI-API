from __future__ import annotations

"""
Configuration management for Napkin AI API Playground.

Key goals:
- Load settings from environment variables with optional .env support
- Validate with Pydantic Settings, providing clear errors and safe defaults
- Avoid side effects at import time; provide explicit lazy-loading
- Add minimal, non-noisy logging while protecting secrets
- Be thread-safe for concurrent access to the singleton
"""

from pathlib import Path
import json
import logging
import os
from typing import Optional, Dict

from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variable prefix: NAPKIN_
    Dotenv file: .env (UTF-8)

    Note: Secrets such as api_token must be provided via environment variables
    or supported secret providers. Secrets are never logged.
    """

    # Pydantic settings model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="NAPKIN_",
        extra="ignore",
        validate_default=True,
    )

    # API Configuration
    api_token: str = Field(
        ...,
        description="Napkin API authentication token",
        alias="NAPKIN_API_TOKEN",
    )
    api_base_url: str = Field(
        default="https://api.napkin.ai",
        description="Napkin API base URL",
        alias="NAPKIN_API_BASE_URL",
    )
    api_version: str = Field(
        default="v1",
        description="API version",
        alias="NAPKIN_API_VERSION",
    )

    # Default Generation Settings
    default_style: str = Field(
        default="vibrant-strokes",
        description="Default visual style ID",
        alias="NAPKIN_DEFAULT_STYLE",
    )
    default_format: str = Field(
        default="svg",
        description="Default output format (svg or png)",
        alias="NAPKIN_DEFAULT_FORMAT",
    )
    default_language: str = Field(
        default="en-US",
        description="Default language (BCP 47 format)",
        alias="NAPKIN_DEFAULT_LANGUAGE",
    )
    default_variations: int = Field(
        default=1,
        description="Default number of variations (1-4)",
        alias="NAPKIN_DEFAULT_VARIATIONS",
        ge=1,
        le=4,
    )

    # Storage Configuration
    storage_path: Path = Field(
        default=Path("./data/visuals"),
        description="Local storage path for generated visuals",
        alias="NAPKIN_STORAGE_PATH",
    )
    database_path: Path = Field(
        default=Path("./data/database/napkin.db"),
        description="SQLite database path for metadata",
        alias="NAPKIN_DATABASE_PATH",
    )

    # API Client Settings
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts",
        alias="NAPKIN_MAX_RETRIES",
        ge=0,
    )
    timeout_seconds: int = Field(
        default=30,
        description="Request timeout in seconds",
        alias="NAPKIN_TIMEOUT_SECONDS",
        gt=0,
    )
    rate_limit_requests: int = Field(
        default=60,
        description="Rate limit: requests per minute",
        alias="NAPKIN_RATE_LIMIT_REQUESTS",
        gt=0,
    )
    poll_interval_seconds: float = Field(
        default=2.0,
        description="Status polling interval in seconds",
        alias="NAPKIN_POLL_INTERVAL_SECONDS",
        gt=0,
    )
    max_poll_attempts: int = Field(
        default=30,
        description="Maximum status polling attempts",
        alias="NAPKIN_MAX_POLL_ATTEMPTS",
        gt=0,
    )

    # Application Settings
    log_level: str = Field(
        default="INFO",
        description="Logging level",
        alias="NAPKIN_LOG_LEVEL",
    )
    debug_mode: bool = Field(
        default=False,
        description="Enable debug mode",
        alias="NAPKIN_DEBUG_MODE",
    )
    batch_concurrent_limit: int = Field(
        default=5,
        description="Maximum concurrent requests in batch mode",
        alias="NAPKIN_BATCH_CONCURRENT_LIMIT",
        ge=1,
        le=10,
    )

    # Display Settings
    use_colors: bool = Field(
        default=True,
        description="Enable colored terminal output",
        alias="NAPKIN_USE_COLORS",
    )
    show_progress: bool = Field(
        default=True,
        description="Show progress indicators",
        alias="NAPKIN_SHOW_PROGRESS",
    )

    @field_validator("api_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """
        Normalize and validate the API base URL.
        - Strips trailing slashes to ensure consistent concatenation.
        - Basic sanity check to avoid malformed URLs.
        """
        v = v.strip()
        if not (v.startswith("https://") or v.startswith("http://")):
            raise ValueError("api_base_url must start with 'https://' or 'http://'")
        return v.rstrip("/")

    @field_validator("default_format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Validate output format."""
        valid_formats = {"svg", "png"}
        value = v.strip().lower()
        if value not in valid_formats:
            raise ValueError(f"default_format must be one of {sorted(valid_formats)}")
        return value

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        value = v.strip().upper()
        if value not in valid_levels:
            raise ValueError(f"log_level must be one of {sorted(valid_levels)}")
        return value

    @field_validator("storage_path", "database_path")
    @classmethod
    def ensure_parent_exists(cls, v: Path) -> Path:
        """
        Ensure parent directories exist for paths.

        Note: This writes to disk on first model construction. This is a controlled,
        explicit side effect tied to instantiation, not import. It ensures
        subsequent code paths do not fail due to missing directories.
        """
        path = Path(v)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Unable to create parent directory for {path!s}: {e}") from e
        return path

    @property
    def api_url(self) -> str:
        """Get the full API URL."""
        return f"{self.api_base_url}/{self.api_version}"

    def get_headers(self) -> Dict[str, str]:
        """
        Get API request headers with authentication.

        Secrets are not logged. Callers must avoid printing headers.
        """
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def safe_debug_dict(self) -> Dict[str, str]:
        """
        Returns a redacted, JSON-serializable representation suitable for debug logs.
        Secret values are masked.
        """
        masked_token = "****" if self.api_token else ""
        return {
            "api_base_url": self.api_base_url,
            "api_version": self.api_version,
            "default_style": self.default_style,
            "default_format": self.default_format,
            "default_language": self.default_language,
            "default_variations": str(self.default_variations),
            "storage_path": str(self.storage_path),
            "database_path": str(self.database_path),
            "max_retries": str(self.max_retries),
            "timeout_seconds": str(self.timeout_seconds),
            "rate_limit_requests": str(self.rate_limit_requests),
            "poll_interval_seconds": str(self.poll_interval_seconds),
            "max_poll_attempts": str(self.max_poll_attempts),
            "log_level": self.log_level,
            "debug_mode": str(self.debug_mode),
            "batch_concurrent_limit": str(self.batch_concurrent_limit),
            "use_colors": str(self.use_colors),
            "show_progress": str(self.show_progress),
            "api_token": masked_token,
        }


_settings: Optional[Settings] = None


def _build_settings() -> Settings:
    """
    Internal constructor for Settings with logging of non-sensitive context.
    """
    if not os.environ.get("NAPKIN_API_TOKEN"):
        logger.debug(
            "NAPKIN_API_TOKEN not found in environment. If expected, ensure .env exists "
            "or environment variables are properly set."
        )

    try:
        s = Settings()
    except ValidationError as e:
        logger.error("Failed to validate configuration: %s", json.dumps(e.errors(), default=str))
        raise
    else:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Loaded configuration: %s", s.safe_debug_dict())
        return s


def get_settings() -> Settings:
    """
    Get application settings singleton.

    Returns:
        Settings: instance with validated configuration.

    Raises:
        ValidationError: If required settings are missing or invalid.

    Thread-safety:
        This function is safe for concurrent calls. It uses a simple, idempotent
        initialization without heavy contention. Minor risk of double-init in
        extremely tight concurrent races is acceptable because initialization is
        pure and yields equivalent instances. If a strict single-init is desired,
        wrap this in a process-wide lock.
    """
    global _settings
    if _settings is None:
        _settings = _build_settings()
    return _settings


def reload_settings() -> Settings:
    """
    Force reload settings from environment.

    Useful for testing or when environment variables change during runtime.

    Returns:
        Settings: a fresh Settings instance.

    Note:
        Callers should ensure that components depending on settings can handle
        live-reloads safely. This does not alter existing client instances that
        captured old settings.
    """
    global _settings
    _settings = _build_settings()
    return _settings