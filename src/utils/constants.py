from __future__ import annotations

"""
Constants and style definitions for Napkin AI API.

This module centralizes:
- Supported output formats and style categories
- Built-in visual styles with metadata
- API endpoints, defaults, constraints, rate limits, and HTTP status codes

Design goals:
- Strong typing for safer usage across the codebase
- Immutable, read-only mappings to avoid accidental mutation
- Helper functions with clear errors and predictable behavior
"""

from enum import Enum
from typing import Dict, List, Mapping, NamedTuple, Sequence


class OutputFormat(str, Enum):
    """Supported output formats for visuals."""
    SVG = "svg"
    PNG = "png"


class StyleCategory(str, Enum):
    """Visual style categories."""
    COLORFUL = "colorful"
    CASUAL = "casual"
    HAND_DRAWN = "hand_drawn"
    FORMAL = "formal"
    MONOCHROME = "monochrome"
    CUSTOM = "custom"


class Style(NamedTuple):
    """Visual style definition."""
    id: str
    name: str
    description: str
    category: StyleCategory


# Built-in visual styles from Napkin API
# Exposed as a Mapping to signal read-only usage; do not mutate at runtime.
STYLES: Mapping[str, Style] = {
    # Colorful Styles
    "vibrant-strokes": Style(
        id="CDQPRVVJCSTPRBBCD5Q6AWR",
        name="Vibrant Strokes",
        description="A flow of vivid lines for bold notes",
        category=StyleCategory.COLORFUL,
    ),
    "glowful-breeze": Style(
        id="CDQPRVVJCSTPRBBKDXK78",
        name="Glowful Breeze",
        description="A swirl of cheerful color for laid-back planning",
        category=StyleCategory.COLORFUL,
    ),
    "bold-canvas": Style(
        id="CDQPRVVJCSTPRBB6DHGQ8",
        name="Bold Canvas",
        description="A vivid field of shapes for lively notes",
        category=StyleCategory.COLORFUL,
    ),
    "radiant-blocks": Style(
        id="CDQPRVVJCSTPRBB6D5P6RSB4",
        name="Radiant Blocks",
        description="A bright spread of solid color for tasks",
        category=StyleCategory.COLORFUL,
    ),
    "pragmatic-shades": Style(
        id="CDQPRVVJCSTPRBB7E9GP8TB5DST0",
        name="Pragmatic Shades",
        description="A palette of blended hues for bold ideas",
        category=StyleCategory.COLORFUL,
    ),

    # Casual Styles
    "carefree-mist": Style(
        id="CDGQ6XB1DGPQ6VV6EG",
        name="Carefree Mist",
        description="A wisp of calm tones for playful tasks",
        category=StyleCategory.CASUAL,
    ),
    "lively-layers": Style(
        id="CDGQ6XB1DGPPCTBCDHJP8",
        name="Lively Layers",
        description="A breeze of soft color for bright ideas",
        category=StyleCategory.CASUAL,
    ),

    # Hand-drawn Styles
    "artistic-flair": Style(
        id="D1GPWS1DCDQPRVVJCSTPR",
        name="Artistic Flair",
        description="A splash of hand-drawn color for creative thinking",
        category=StyleCategory.HAND_DRAWN,
    ),
    "sketch-notes": Style(
        id="D1GPWS1DDHMPWSBK",
        name="Sketch Notes",
        description="A hand-drawn style for free-flowing ideas",
        category=StyleCategory.HAND_DRAWN,
    ),

    # Formal Styles
    "elegant-outline": Style(
        id="CSQQ4VB1DGPP4V31CDNJTVKFBXK6JV3C",
        name="Elegant Outline",
        description="A refined black outline for professional clarity",
        category=StyleCategory.FORMAL,
    ),
    "subtle-accent": Style(
        id="CSQQ4VB1DGPPRTB7D1T0",
        name="Subtle Accent",
        description="A light touch of color for professional documents",
        category=StyleCategory.FORMAL,
    ),
    "monochrome-pro": Style(
        id="CSQQ4VB1DGPQ6TBECXP6ABB3DXP6YWG",
        name="Monochrome Pro",
        description="A single-color approach for focused presentations",
        category=StyleCategory.FORMAL,
    ),
    "corporate-clean": Style(
        id="CSQQ4VB1DGPPTVVEDXHPGWKFDNJJTSKCC5T0",
        name="Corporate Clean",
        description="A professional flat style for business diagrams",
        category=StyleCategory.FORMAL,
    ),

    # Monochrome Styles
    "minimal-contrast": Style(
        id="DNQPWVV3D1S6YVB55NK6RRBM",
        name="Minimal Contrast",
        description="A clean monochrome style for focused work",
        category=StyleCategory.MONOCHROME,
    ),
    "silver-beam": Style(
        id="CXS62Y9DCSQP6XBK",
        name="Silver Beam",
        description="A spotlight of gray scale ease with striking focus",
        category=StyleCategory.MONOCHROME,
    ),
}


# API Endpoints
API_ENDPOINTS: Mapping[str, str] = {
    "create_visual": "/visual",
    "get_status": "/visual/{request_id}/status",
    "get_file": "/visual/{request_id}/file/{file_id}",
}


# Default values
DEFAULTS: Mapping[str, object] = {
    "style": "vibrant-strokes",
    "format": OutputFormat.SVG,
    "language": "en-US",
    "number_of_visuals": 1,
    "transparent_background": False,
    "inverted_color": False,
    "width": None,  # PNG only
    "height": None,  # PNG only
}


# Validation constraints
CONSTRAINTS: Mapping[str, int] = {
    "min_visuals": 1,
    "max_visuals": 4,
    "min_width": 100,
    "max_width": 4096,
    "min_height": 100,
    "max_height": 4096,
    "max_content_length": 10000,
    "max_context_length": 5000,
}


# Rate limiting
RATE_LIMITS: Mapping[str, int] = {
    "requests_per_minute": 60,
    "retry_after_default": 60,  # seconds
}


# HTTP Status codes
HTTP_STATUS: Mapping[str, int] = {
    "created": 201,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "gone": 410,
    "rate_limit": 429,
    "server_error": 500,
}


def get_style_by_id(style_id: str) -> Style:
    """
    Get style by ID.

    Args:
        style_id: The style ID to look up.

    Returns:
        Style object if found.

    Raises:
        ValueError: If style ID is not found.
    """
    # Fast path: build once and reuse a reverse index by ID if needed.
    for style in STYLES.values():
        if style.id == style_id:
            return style
    raise ValueError(f"Style ID not found: {style_id!r}")


def get_style_by_name(name: str) -> Style:
    """
    Get style by name or slug.

    Args:
        name: Style name or slug (e.g., "vibrant-strokes" or "Vibrant Strokes").

    Returns:
        Style object if found.

    Raises:
        ValueError: If style name is not found.
    """
    # Try as slug first
    slug = name.strip().lower().replace(" ", "-")
    if slug in STYLES:
        return STYLES[slug]

    # Try case-insensitive name match
    for style in STYLES.values():
        if style.name.lower() == name.strip().lower():
            return style

    # Helpful message shows valid names without leaking internal IDs
    valid = ", ".join(sorted(STYLES.keys()))
    raise ValueError(f"Style not found: {name!r}. Valid options: {valid}")


def get_styles_by_category(category: StyleCategory) -> List[Style]:
    """
    Get all styles in a category.

    Args:
        category: The style category to filter by.

    Returns:
        List of styles in the category.
    """
    return [style for style in STYLES.values() if style.category == category]


def list_style_names() -> List[str]:
    """
    Get list of all available style names.

    Returns:
        List of style names (slugs).
    """
    return list(STYLES.keys())


def list_style_ids() -> List[str]:
    """
    Get list of all available style IDs.

    Returns:
        List of style IDs.
    """
    return [style.id for style in STYLES.values()]
