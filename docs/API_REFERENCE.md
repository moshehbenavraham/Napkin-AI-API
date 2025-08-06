# API Reference

## Python Client Library

### Installation

```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

```python
# Library imports
from src.api.client import NapkinAPIClient
from src.api.models import VisualRequest, VisualResponse, StatusResponse
from src.core.generator import VisualGenerator
from src.cli.commands import app as cli_app
```

### Quick Start

```python
import asyncio
from src.api.client import NapkinAPIClient
from src.api.models import VisualRequest
from src.utils.config import get_settings

async def main():
    # Initialize client
    async with NapkinAPIClient() as client:
        # Create visual request
        request = VisualRequest(
            content="Machine Learning Pipeline",
            style_id="vibrant-strokes",
            format="svg",
            number_of_visuals=1,
            language="en-US",
            transparent_background=False,
            inverted_color=False,
        )
        
        # Submit request
        response = await client.create_visual(request)
        
        # Wait for completion
        status = await client.wait_for_completion(response.request_id)
        
        # Download files
        if status.files:
            for file_info in status.files:
                if 'url' in file_info:
                    content = await client.download_file_by_url(file_info['url'])
                    # Save content to file

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Classes

### NapkinAPIClient

Main async client for API interactions.

```python
class NapkinAPIClient:
    def __init__(
        self,
        settings: Optional[Settings] = None
    )
    # settings loaded from environment if not provided
```

#### Methods

##### create_visual()
```python
async def create_visual(
    self,
    request: VisualRequest,
) -> VisualResponse
```

##### get_status()
```python
async def get_status(
    self,
    request_id: str,
) -> StatusResponse
```

##### wait_for_completion()
```python
async def wait_for_completion(
    self,
    request_id: str,
    poll_interval: Optional[float] = None,
    max_attempts: Optional[int] = None,
) -> StatusResponse
```

##### download_file_by_url()
```python
async def download_file_by_url(
    self,
    url: str
) -> bytes
```

##### download_file_by_id()
```python
async def download_file_by_id(
    self,
    request_id: str,
    file_id: str
) -> bytes
```

##### get_rate_limit_status()
```python
def get_rate_limit_status(self) -> Optional[RateLimitInfo]
```

### VisualRequest

Pydantic v2 model for visual generation requests.

```python
from pydantic import BaseModel, Field
from typing import Optional
from src.api.models import OutputFormat

class VisualRequest(BaseModel):
    # Required
    content: str = Field(..., min_length=1, max_length=10000)
    
    # Format
    format: OutputFormat = Field(default=OutputFormat.SVG)
    
    # Optional context
    context_before: Optional[str] = Field(default=None, max_length=5000)
    context_after: Optional[str] = Field(default=None, max_length=5000)
    
    # Style and appearance
    style_id: Optional[str] = Field(default=None)
    language: str = Field(default="en-US")
    number_of_visuals: int = Field(default=1, ge=1, le=4)
    transparent_background: bool = Field(default=False)
    inverted_color: bool = Field(default=False)
    
    # PNG dimensions (only when format="png")
    width: Optional[int] = Field(default=None, ge=100, le=4096)
    height: Optional[int] = Field(default=None, ge=100, le=4096)
```

### VisualResponse

Response model for visual creation.

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from src.api.models import RequestStatus, GeneratedFile

class VisualResponse(BaseModel):
    request_id: str
    status: RequestStatus
    created_at: datetime
    files: List[GeneratedFile] = Field(default_factory=list)
    message: Optional[str] = None
    error: Optional[str] = None
```

### StatusResponse

Response model for status checks.

```python
class StatusResponse(BaseModel):
    request_id: str
    status: RequestStatus
    progress: Optional[float] = None
    message: Optional[str] = None
### GeneratedFile (API response for downloads)

Expected fields returned by status (authoritative list):
- id: string
- url: string (complete download URL; expires; requires Authorization)
- format: string ("svg" | "png")
- filename: string (optional)
- size_bytes: integer (optional)

Example:
```json
{
  "id": "426614174000-wdjvjhwv8",
  "url": "https://api.napkin.ai/v1/visual/123e4567-e89b-12d3-a456-426614174000/file/426614174000-wdjvjhwv8",
  "format": "svg",
  "filename": "visual.svg",
  "size_bytes": 245760
}
```

Download handling notes:
- Always include Authorization: Bearer <token> when using file URLs.
- Prefer the provided url for downloads. If a legacy response omits url but includes id, fallback to GET /v1/visual/:request-id/file/:file-id
- Filename precedence: Content-Disposition header > API filename field > synthesized "{request_id}_{file.id}.{ext}"
- MIME handling: use Content-Type; fallback from format mapping ("svg" -> image/svg+xml, "png" -> image/png).
- For large files, stream writes in chunks (default 64 KiB) to avoid memory spikes.

Client usage for downloads:
```python
# Given a completed StatusResponse 'status'
files = status.files or getattr(status, "generated_files", []) or []
for f in files:
    content = await NapkinAPIClient.download_file_by_url(f["url"])  # bytes-safe
    # Preferred in CLI flows:
    # await NapkinAPIClient.save_file_by_url(f["url"], output_dir)
```
    files_ready: int = 0
    files_total: int = 0
    files: Optional[List[Dict]] = None  # Raw file data from API
    error: Optional[str] = None
```

### GeneratedFile

Model for file metadata.

```python
class GeneratedFile(BaseModel):
    id: str
    url: Optional[str] = None
    format: str
    filename: Optional[str] = None
    size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None

@dataclass
class GeneratedFile:
    id: str
```

## Error Handling

### Exception Hierarchy

```python
class NapkinAPIError(Exception):
    """Base exception for all API errors."""
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None)

class AuthenticationError(NapkinAPIError):
    """API authentication failed (401)."""

class RateLimitError(NapkinAPIError):
    """Rate limit exceeded (429)."""
    retry_after: int  # Seconds to wait

class RequestError(NapkinAPIError):
    """Invalid request parameters (400)."""

class ProcessingError(NapkinAPIError):
    """Visual generation failed or timed out."""
```

### Error Response Model

```python
class ErrorResponse(BaseModel):
    error: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
```

## CLI Commands

### generate
```bash
napkin generate "content" [OPTIONS]
  --style, -s          Style name or ID
  --format, -f         Output format (svg/png)
  --output, -o         Output directory
  --variations, -n     Number of variations (1-4)
  --language, -l       Language code
  --context-before     Context before content
  --context-after      Context after content
  --width, -w          PNG width (100-4096)
  --height, -h         PNG height (100-4096)
  --transparent        Transparent background
  --inverted           Inverted colors
  --debug              Enable debug logging
```

### styles
```bash
napkin styles [OPTIONS]
  --list               List all available styles
  --category           Filter by category
  --show               Show details for a style
```

### config
```bash
napkin config [OPTIONS]
  --show               Show current configuration
  --check              Validate configuration
```

### version
```bash
napkin version        Show version information
```

## Configuration

### Settings Management

```python
from src.utils.config import Settings, get_settings

class Settings(BaseSettings):
    # Required
    api_token: SecretStr
    
    # API configuration
    api_base_url: str = "https://api.napkin.ai"
    api_version: str = "v1"
    
    # Defaults for generation
    default_style: str = "vibrant-strokes"
    default_format: str = "svg"
    default_language: str = "en-US"
    default_variations: int = 1
    
    # Storage paths
    storage_path: Path = Path("./data/visuals")
    database_path: Path = Path("./data/database/napkin.db")
    
    # Performance settings
    max_retries: int = 3
    timeout_seconds: int = 30
    poll_interval_seconds: float = 2.0
    max_poll_attempts: int = 30
    
    # Display settings
    log_level: str = "INFO"
    debug_mode: bool = False
    use_colors: bool = True
    show_progress: bool = True
```

### Environment Variables

All settings can be configured via environment variables with the `NAPKIN_` prefix:

```bash
NAPKIN_API_TOKEN=your_token_here
NAPKIN_DEFAULT_STYLE=sketch-notes
NAPKIN_STORAGE_PATH=/custom/path
NAPKIN_LOG_LEVEL=DEBUG
```

## Utilities

### Style Constants

```python
from src.utils.constants import STYLES, list_style_names, get_style_by_name

# Available style categories
STYLE_CATEGORIES = {
    "colorful": [...],
    "casual": [...],
    "hand-drawn": [...],
    "formal": [...],
    "monochrome": [...],
}

# Get all style names
style_names = list_style_names()

# Get style info
style = get_style_by_name("vibrant-strokes")
```

### Helper Functions

```python
from src.utils.helpers import (
    sanitize_filename,
    ensure_directory,
    mask_sensitive_data,
    format_size,
)
```

## Visual Generator (High-Level API)

```python
from src.core.generator import VisualGenerator

class VisualGenerator:
    """High-level interface for visual generation."""
    
    async def generate_single(
        self,
        content: str,
        style_id: Optional[str] = None,
        format: str = "svg",
        **kwargs
    ) -> Dict[str, Any]
    
    async def generate_batch(
        self,
        items: List[Dict[str, Any]],
        common_params: Optional[Dict] = None,
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]

## Usage Examples

### Basic Generation

```python
import asyncio
from src.core.generator import generate_visual

async def main():
    result = await generate_visual(
        content="Machine Learning Pipeline",
        style="vibrant-strokes",
        format="svg",
        output_dir="./output"
    )
    print(f"Generated {len(result['files'])} files")

if __name__ == "__main__":
    asyncio.run(main())
```

### With Error Handling

```python
import asyncio
from src.api.client import NapkinAPIClient, AuthenticationError, RateLimitError
from src.api.models import VisualRequest

async def safe_generate():
    try:
        async with NapkinAPIClient() as client:
            request = VisualRequest(
                content="Data Flow Diagram",
                style_id="sketch-notes"
            )
            response = await client.create_visual(request)
            status = await client.wait_for_completion(response.request_id)
            return status
    except AuthenticationError:
        print("Invalid API token")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(safe_generate())
```

### Batch Processing

```python
import asyncio
from src.core.generator import VisualGenerator

async def batch_example():
    generator = VisualGenerator()
    
    items = [
        {"content": "Item 1", "style_id": "vibrant-strokes"},
        {"content": "Item 2", "style_id": "sketch-notes"},
        {"content": "Item 3", "style_id": "elegant-outline"},
    ]
    
    results = await generator.generate_batch(
        items=items,
        common_params={"format": "png", "width": 1920},
        max_concurrent=3
    )
    
    for result in results:
        if result.get("success"):
            print(f"Generated: {result['files']}")
        else:
            print(f"Failed: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(batch_example())
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Rate Limiting

### RateLimitInfo Model

```python
class RateLimitInfo(BaseModel):
    limit: int
    remaining: int
    reset: Optional[datetime]
    retry_after: Optional[int]
```

### Handling Rate Limits

```python
async with NapkinAPIClient() as client:
    # Make request
    response = await client.create_visual(request)
    
    # Check rate limit status
    rate_info = client.get_rate_limit_status()
    if rate_info and rate_info.remaining < 10:
        print(f"Warning: Only {rate_info.remaining} requests remaining")
        if rate_info.reset:
            print(f"Reset at: {rate_info.reset}")
```

## Available Styles

### Colorful Styles
- `vibrant-strokes`: Vivid lines for bold notes
- `glowful-breeze`: Cheerful colors for laid-back planning
- `bold-canvas`: Lively shapes for dynamic content
- `radiant-blocks`: Bright solid colors for tasks
- `pragmatic-shades`: Blended hues for bold ideas

### Casual Styles
- `carefree-mist`: Calm tones for playful tasks
- `lively-layers`: Soft colors for bright ideas

### Hand-drawn Styles
- `artistic-flair`: Hand-drawn color for creative thinking
- `sketch-notes`: Free-flowing hand-drawn style

### Formal Styles
- `elegant-outline`: Refined black outline for clarity
- `subtle-accent`: Light color touch for documents
- `monochrome-pro`: Single-color focused presentations
- `corporate-clean`: Professional flat business diagrams

### Monochrome Styles
- `minimal-contrast`: Clean monochrome for focused work
- `silver-beam`: Grayscale with striking focus

## Additional Resources

- **[README.md](../README.md)** - Getting started guide
- **[USAGE.md](USAGE.md)** - Detailed CLI usage examples
- **[SETUP.md](SETUP.md)** - Installation and configuration
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **[PRD.md](PRD.md)** - Product requirements and roadmap
- **[napkin_ai_api.md](napkin_ai_api.md)** - Napkin API specifications
#### End-to-end verification steps

Manual verification (Windows CMD - copy/paste):
```bat
:: 1) Create a request
curl -sS -X POST "https://api.napkin.ai/v1/visual" ^
  -H "Authorization: Bearer %NAPKIN_API_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -H "Accept: application/json" ^
  -d "{\"format\":\"svg\",\"content\":\"Test visual\"}"

:: 2) Poll status (replace with actual request ID)
set ID=REPLACE_WITH_REQUEST_ID
for /l %i in (1,1,30) do (
  curl -sS -H "Authorization: Bearer %NAPKIN_API_TOKEN%" "https://api.napkin.ai/v1/visual/%ID%/status"
  timeout /t 3 >NUL
)

:: 3) Download the first generated file by URL
set URL=REPLACE_WITH_FILE_URL
curl -L "%URL%" -H "Authorization: Bearer %NAPKIN_API_TOKEN%" --output out.svg

:: 4) Inspect headers for filename/MIME
curl -I -L "%URL%" -H "Authorization: Bearer %NAPKIN_API_TOKEN%"
```

Automated tests (pytest):
- Unit tests:
  - Parse Content-Disposition (filename*, RFC 5987) and fallback to filename
  - MIME fallback to file.format when Content-Type missing
  - Synthesized filename correctness
- Integration (httpx+respx or responses):
  - Status returns generated_files with url; download returns 200 + Content-Disposition -> saves with correct name
  - Legacy: status.files instead of generated_files -> still downloads
  - Fallback: no url but id present -> GET /v1/visual/:request-id/file/:file-id works
  - Errors: 401/403, 404/410, 429 with retry, unexpected Content-Type
- Performance:
  - Verify streamed chunk writes (64 KiB default), not full-buffer memory usage
```

Configuration and environment variables:
- Required:
  - NAPKIN_API_TOKEN
- Optional:
  - NAPKIN_DOWNLOAD_CHUNK_SIZE (default 65536)
  - NAPKIN_DOWNLOAD_OVERWRITE (default false)
  - NAPKIN_FILE_LOGGING (default false)
```

Backwards compatibility / migration notes:
- Continue supporting both shapes:
  - status.generated_files (preferred)
  - status.files (legacy)
- Prefer file.url for download; fallback to GET /v1/visual/:request-id/file/:file-id when url is absent
- Do not change public method signatures; document filename/MIME precedence rules
```