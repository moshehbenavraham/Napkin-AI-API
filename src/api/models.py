"""
Revised Pydantic v2 models for Napkin AI API.

Changelog:
- Adopted Pydantic v2 features: strict types, field/model validators, Annotated constraints, and BaseModel config.
- Added strong validation for IDs, URLs, emails, language tags, and list bounds with patterns.
- Normalized response envelopes and enhanced error modeling with codes and details.
- Improved serialization settings (from_attributes, ser_json_timedelta/bytes) and schema examples.
- Added docstrings, field descriptions, and test-friendly snippets; redaction for sensitive fields.
- Ensured OpenAPI/JSON Schema compatibility and consistent naming conventions.

Model overview:
- VisualRequest: client request for visual generation, with constraints and PNG-specific rules.
- GeneratedFile: metadata for produced outputs.
- VisualResponse: detailed status with files, timestamps, and error message when present.
- StatusResponse: lightweight progress/status view.
- ErrorResponse: normalized error envelope with code/details and timestamp.
- RateLimitInfo: rate limits from headers with helper properties.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, List, Optional, Dict, Any

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    SecretStr,
    field_validator,
    model_validator,
)

# Common constrained aliases
NonEmptyStr = Annotated[StrictStr, Field(min_length=1)]
ShortText = Annotated[StrictStr, Field(min_length=1, max_length=5000)]
LongText = Annotated[StrictStr, Field(min_length=1, max_length=10000)]
LangCode = Annotated[
    StrictStr,
    Field(min_length=2, max_length=35, pattern=r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$"),
]
IdStr = Annotated[
    StrictStr, Field(min_length=8, max_length=64, pattern=r"^[A-Za-z0-9_\-]+$")
]
PositiveSmallInt = Annotated[StrictInt, Field(ge=1, le=4)]
PngDim = Annotated[StrictInt, Field(ge=100, le=4096)]
PercentFloat = Annotated[StrictFloat, Field(ge=0, le=100)]
BytesCount = Annotated[StrictInt, Field(ge=0)]


class RequestStatus(str, Enum):
    """Visual generation request status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class OutputFormat(str, Enum):
    """Supported output formats."""

    SVG = "svg"
    PNG = "png"


class VisualRequest(BaseModel):
    """Request model for creating a visual.

    Notes:
    - PNG dimensions (width/height) are only allowed when format=png.
    - Lists, when provided, must not be empty and must contain non-empty identifiers.
    """

    # Required
    content: LongText = Field(
        ...,
        description="The text content to generate visuals from (1..10000 chars).",
        examples=["Machine Learning Pipeline"],
    )
    format: OutputFormat = Field(
        default=OutputFormat.SVG,
        description="Desired output format.",
        examples=["svg"],
    )

    # Optional context
    context_before: Optional[ShortText] = Field(
        default=None,
        description="Optional context preceding the main content (<=5000 chars).",
    )
    context_after: Optional[ShortText] = Field(
        default=None,
        description="Optional context following the main content (<=5000 chars).",
    )

    # Style and appearance
    style_id: Optional[IdStr] = Field(
        default=None,
        description="Visual style ID (built-in or custom, 8..64 chars, [A-Za-z0-9_-]).",
    )
    language: LangCode = Field(
        default="en-US",
        description="Language code in BCP 47 format (e.g., en, en-US, fr-FR).",
    )
    transparent_background: StrictBool = Field(
        default=False,
        description="Enable transparent background for PNG output.",
    )
    inverted_color: StrictBool = Field(
        default=False,
        description="Invert colors in the generated visual.",
    )

    # Generation options
    number_of_visuals: PositiveSmallInt = Field(
        default=1,
        description="Number of visual variations to generate (1..4).",
    )

    # PNG-specific options
    width: Optional[PngDim] = Field(
        default=None,
        description="PNG width in pixels (100..4096, only with format=png).",
    )
    height: Optional[PngDim] = Field(
        default=None,
        description="PNG height in pixels (100..4096, only with format=png).",
    )

    # References (optional)
    visual_id: Optional[IdStr] = Field(
        default=None,
        description="Reference a single existing visual by ID.",
    )
    visual_ids: Optional[List[IdStr]] = Field(
        default=None,
        description="Reference multiple existing visuals by ID (non-empty list).",
        min_length=1,
        max_length=20,
    )
    visual_query: Optional[ShortText] = Field(
        default=None,
        description="Query for selecting a single visual.",
    )
    visual_queries: Optional[List[ShortText]] = Field(
        default=None,
        description="Queries for selecting multiple visuals (non-empty list).",
        min_length=1,
        max_length=20,
    )

    # Optional sensitive token (example of redaction)
    api_token: Optional[SecretStr] = Field(
        default=None,
        description="Optional bearer token; excluded from serialized output.",
        exclude=True,
    )

    @model_validator(mode="after")
    def _validate_png_dimensions(self):
        """Ensure width/height only set when format is PNG."""
        if self.format != OutputFormat.PNG:
            if self.width is not None or self.height is not None:
                raise ValueError("width and height can only be set when format=png")
        return self

    @field_validator("visual_ids")
    @classmethod
    def _validate_visual_ids(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("visual_ids must not be empty if provided")
        return v

    @field_validator("visual_queries")
    @classmethod
    def _validate_visual_queries(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("visual_queries must not be empty if provided")
        return v

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "ser_json_timedelta": "float",
        "ser_json_bytes": "base64",
        "json_schema_extra": {
            "examples": [
                {
                    "content": "Machine Learning Pipeline",
                    "format": "svg",
                    "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",
                    "language": "en-US",
                    "number_of_visuals": 2,
                },
                {
                    "content": "Data flow diagram",
                    "format": "png",
                    "width": 1024,
                    "height": 768,
                    "transparent_background": True,
                    "inverted_color": False,
                },
            ]
        },
    }


class GeneratedFile(BaseModel):
    """Metadata for a generated visual file."""

    id: IdStr = Field(
        ...,
        description="Unique file identifier.",
    )
    # Supports HTTP(S)
    url: Optional[HttpUrl] = Field(
        default=None,
        description="URL to download the file (requires Authorization; expires).",
    )
    format: OutputFormat = Field(
        ...,
        description="File format.",
    )
    # Optional filename provided by API (fallback if Content-Disposition absent)
    filename: Optional[StrictStr] = Field(
        default=None,
        description="Suggested filename (optional; may be overridden by Content-Disposition).",
        min_length=1,
        max_length=512,
    )
    width: Optional[PngDim] = Field(
        default=None,
        description="Width in pixels (PNG only).",
    )
    height: Optional[PngDim] = Field(
        default=None,
        description="Height in pixels (PNG only).",
    )
    size_bytes: Optional[BytesCount] = Field(
        default=None,
        description="File size in bytes (>=0).",
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="File creation timestamp (UTC).",
    )
    checksum: Optional[StrictStr] = Field(
        default=None,
        description="Optional checksum (e.g., SHA256 hex).",
        min_length=32,
        max_length=128,
        pattern=r"^[A-Fa-f0-9]+$",
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "426614174000-wdjvjhwv8",
                    "url": "https://api.napkin.ai/v1/visual/123e4567-e89b-12d3-a456-426614174000/file/426614174000-wdjvjhwv8",
                    "format": "svg",
                    "filename": "visual.svg",
                    "size_bytes": 245760,
                    "created_at": "2025-01-01T12:00:00Z",
                }
            ]
        },
    }


class VisualResponse(BaseModel):
    """Response model for visual creation request outcome."""

    request_id: IdStr = Field(
        ...,
        description="Unique request identifier.",
    )
    status: RequestStatus = Field(
        ...,
        description="Current request status.",
    )
    created_at: datetime = Field(
        ...,
        description="Request creation timestamp (UTC).",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp (UTC).",
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Request expiration timestamp (UTC).",
    )
    files: List[GeneratedFile] = Field(
        default_factory=list,
        description="List of generated files (empty until available).",
        max_length=10,
    )
    error: Optional[StrictStr] = Field(
        default=None,
        description="Error message if the request failed.",
        min_length=1,
        max_length=2000,
    )

    @property
    def is_completed(self) -> bool:
        """True if request reached COMPLETED state."""
        return self.status == RequestStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """True if request reached FAILED state."""
        return self.status == RequestStatus.FAILED

    @property
    def is_expired(self) -> bool:
        """True if request reached EXPIRED state."""
        return self.status == RequestStatus.EXPIRED

    @property
    def is_terminal(self) -> bool:
        """True if request is in a terminal state (completed/failed/expired)."""
        return self.status in {
            RequestStatus.COMPLETED,
            RequestStatus.FAILED,
            RequestStatus.EXPIRED,
        }

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "request_id": "REQ_abcd1234",
                    "status": "processing",
                    "created_at": "2025-01-01T12:00:00Z",
                    "updated_at": "2025-01-01T12:00:10Z",
                    "files": [],
                },
                {
                    "request_id": "REQ_abcd1234",
                    "status": "completed",
                    "created_at": "2025-01-01T12:00:00Z",
                    "updated_at": "2025-01-01T12:00:30Z",
                    "files": [
                        {
                            "id": "FILE_abc123",
                            "url": "https://cdn.example.com/files/FILE_abc123.png",
                            "format": "png",
                            "width": 1024,
                            "height": 768,
                            "size_bytes": 345678,
                        }
                    ],
                },
            ]
        },
    }


class StatusResponse(BaseModel):
    """Lightweight response for status polling and progress reporting."""

    request_id: IdStr = Field(
        ...,
        description="Request identifier.",
    )
    status: RequestStatus = Field(
        ...,
        description="Current status.",
    )
    progress: Optional[PercentFloat] = Field(
        default=None,
        description="Progress percentage (0..100).",
    )
    message: Optional[ShortText] = Field(
        default=None,
        description="Status message (<=5000 chars).",
    )
    files_ready: BytesCount = Field(
        default=0,
        description="Number of files ready (>=0).",
    )
    files_total: BytesCount = Field(
        default=0,
        description="Total number of files expected (>=0).",
    )
    eta: Optional[timedelta] = Field(
        default=None,
        description="Estimated time remaining, if known.",
    )
    error: Optional[StrictStr] = Field(
        default=None,
        description="Error message if failed.",
        min_length=1,
        max_length=2000,
    )
    # Raw file objects as returned by API (back-compat). Prefer parsing to List[GeneratedFile] upstream.
    files: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Raw files from API (generated_files/files). Client normalizes for download logic.",
    )

    @model_validator(mode="after")
    def _validate_file_counts(self):
        if self.files_total < 0 or self.files_ready < 0:
            raise ValueError("files_total and files_ready must be >= 0")
        if self.files_ready > self.files_total and self.files_total != 0:
            raise ValueError("files_ready cannot exceed files_total")
        return self

    model_config = {
        "from_attributes": True,
        "ser_json_timedelta": "iso8601",
        "json_schema_extra": {
            "examples": [
                {
                    "request_id": "REQ_abcd1234",
                    "status": "processing",
                    "progress": 42.5,
                    "message": "Rendering variants...",
                    "files_ready": 1,
                    "files_total": 3,
                }
            ]
        },
    }


class ErrorResponse(BaseModel):
    """Normalized API error response envelope."""

    error: NonEmptyStr = Field(
        ...,
        description="Human-readable error message.",
        examples=["Invalid width for PNG format"],
    )
    code: Optional[
        Annotated[
            StrictStr, Field(min_length=2, max_length=64, pattern=r"^[A-Z0-9_]+$")
        ]
    ] = Field(
        default=None,
        description="Machine-readable error code (e.g., VALIDATION_ERROR).",
        examples=["VALIDATION_ERROR"],
    )
    details: Optional[dict] = Field(
        default=None,
        description="Additional error details (field errors, hints).",
    )
    request_id: Optional[IdStr] = Field(
        default=None,
        description="Request ID if available for correlation.",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp (UTC).",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "width and height can only be set when format=png",
                    "code": "VALIDATION_ERROR",
                    "details": {"field": "width"},
                    "request_id": "REQ_abcd1234",
                    "timestamp": "2025-01-01T12:00:30Z",
                }
            ]
        }
    }


class RateLimitInfo(BaseModel):
    """Rate limit information derived from response headers."""

    limit: BytesCount = Field(
        ...,
        description="Request limit per window (>=0).",
    )
    remaining: BytesCount = Field(
        ...,
        description="Remaining requests in current window (>=0).",
    )
    reset: datetime = Field(
        ...,
        description="When the rate limit window resets (UTC).",
    )
    retry_after: Optional[Annotated[StrictInt, Field(ge=0)]] = Field(
        default=None,
        description="Seconds to wait before retrying (>=0).",
    )

    @property
    def is_exceeded(self) -> bool:
        """True when no remaining requests are available."""
        return self.remaining <= 0

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "limit": 60,
                    "remaining": 0,
                    "reset": "2025-01-01T12:01:00Z",
                    "retry_after": 30,
                }
            ]
        },
    }


# Usage examples (unit-test–friendly):
# Validate VisualRequest
# VisualRequest(content="Diagram", format="png", width=512, height=512)
# ErrorResponse(error="Bad input", code="VALIDATION_ERROR")

# TODO: Clarify if request_id, file id formats should be UUIDs rather than custom strings.
# TODO: Confirm maximum list sizes for visual_ids and visual_queries (assumed 20).
# TODO: Confirm checksum algorithm(s) and length guarantees for GeneratedFile.checksum.
