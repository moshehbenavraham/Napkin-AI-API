"""
Utility functions and helpers for Napkin AI API.

Provides common utilities for file handling, validation, and logging setup.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from rich.logging import RichHandler


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    use_rich: bool = True,
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional file path for logging.
        use_rich: Whether to use Rich formatting for console output.
    
    Returns:
        Configured logger instance.
    """
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    if use_rich:
        console_handler = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=False,
        )
        console_handler.setFormatter(
            logging.Formatter("%(message)s")
        )
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
    
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(file_handler)
    
    return logger


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for filesystem.
    
    Args:
        filename: Original filename.
    
    Returns:
        Sanitized filename.
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"|?*\\/\r\n\t'
    for char in unsafe_chars:
        filename = filename.replace(char, "_")
    
    # Limit length
    max_length = 255
    if len(filename) > max_length:
        # Keep extension if present
        parts = filename.rsplit(".", 1)
        if len(parts) == 2:
            name, ext = parts
            max_name_length = max_length - len(ext) - 1
            filename = f"{name[:max_name_length]}.{ext}"
        else:
            filename = filename[:max_length]
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(". ")
    
    # Default if empty
    if not filename:
        filename = "untitled"
    
    return filename


def ensure_directory(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path.
    
    Returns:
        Path object.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes.
    
    Returns:
        Formatted size string.
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds.
    
    Returns:
        Formatted duration string.
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def validate_language_code(code: str) -> bool:
    """
    Validate BCP 47 language code format.
    
    Args:
        code: Language code to validate.
    
    Returns:
        True if valid, False otherwise.
    """
    # Basic validation for common formats
    # Full BCP 47 validation is complex, this covers common cases
    import re
    
    # Pattern for common language codes (e.g., "en", "en-US", "zh-Hans-CN")
    pattern = r"^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?$"
    return bool(re.match(pattern, code))


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate.
        max_length: Maximum length.
        suffix: Suffix to add when truncated.
    
    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    
    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp string.
    
    Args:
        format: Timestamp format.
    
    Returns:
        Formatted timestamp.
    """
    return datetime.utcnow().strftime(format)


def parse_csv_file(file_path: Path) -> list[dict]:
    """
    Parse CSV file for batch processing.
    
    Args:
        file_path: Path to CSV file.
    
    Returns:
        List of dictionaries with CSV data.
    """
    import csv
    
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    return data


def write_json_file(data: Any, file_path: Path, indent: int = 2):
    """
    Write data to JSON file.
    
    Args:
        data: Data to write.
        file_path: Output file path.
        indent: JSON indentation.
    """
    import json
    
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)


def read_json_file(file_path: Path) -> Any:
    """
    Read data from JSON file.
    
    Args:
        file_path: Input file path.
    
    Returns:
        Parsed JSON data.
    """
    import json
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get boolean value from environment variable.
    
    Args:
        key: Environment variable key.
        default: Default value if not set.
    
    Returns:
        Boolean value.
    """
    value = os.getenv(key, "").lower()
    if not value:
        return default
    
    return value in {"true", "1", "yes", "on"}


def mask_secret(secret: str, visible_chars: int = 4) -> str:
    """
    Mask a secret value for display.
    
    Args:
        secret: Secret value to mask.
        visible_chars: Number of characters to show at end.
    
    Returns:
        Masked secret.
    """
    if not secret:
        return ""
    
    if len(secret) <= visible_chars * 2:
        return "****"
    
    return f"{secret[:visible_chars]}...{secret[-visible_chars:]}"