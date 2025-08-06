# API Reference

Overview
This reference documents the Python client and high-level generator API implemented in the codebase today. It aligns with src/api/client.py, src/api/models.py, src/core/generator.py, and src/utils/config.py.

Installation
```bash
# Local development
poetry install
# Or
pip install -r requirements.txt
```

Minimal Example (async)
```python
import asyncio
from src.api.client import NapkinAPIClient
from src.api.models import VisualRequest, OutputFormat

async def main():
    async with NapkinAPIClient() as client:
        req = VisualRequest(
            content="Machine Learning Pipeline",
            format=OutputFormat.SVG,
            style_id="vibrant-strokes",  # slug is also accepted downstream via generator; here pass ID or slug
            number_of_visuals=1,
            language="en-US",
        )
        resp = await client.create_visual(req)
        status = await client.wait_for_completion(resp.request_id)
        if status.files:
            for f in status.files:
                if "url" in f:
                    data = await client.download_file_by_url(f["url"])
                    with open("output.svg", "wb") as fh:
                        fh.write(data)

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Classes

NapkinAPIClient
Main async client for API interactions. Settings are loaded from environment/.env if not provided.

```python
class NapkinAPIClient:
    def __init__(self, settings: Optional[Settings] = None): ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def close(self): ...
    async def create_visual(self, request: VisualRequest) -> VisualResponse: ...
    async def get_status(self, request_id: str) -> StatusResponse: ...
    async def wait_for_completion(self, request_id: str, poll_interval: Optional[float] = None, max_attempts: Optional[int] = None) -> StatusResponse: ...
    async def download_file_by_url(self, url: str) -> bytes: ...
    async def download_file_by_id(self, request_id: str, file_id: str) -> bytes: ...
    async def save_file_by_url(self, url: str, output_dir: Union[str, Path], inferred_name: Optional[str] = None, request_id: Optional[str] = None, file_id: Optional[str] = None) -> Path: ...
    def get_rate_limit_status(self) -> Optional[RateLimitInfo]: ...
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

VisualRequest
Pydantic v2 request model with constraints. See src/api/models.py for full details.

Key fields
- content: str (1..10000)
- format: "svg" | "png"
- style_id: Optional[str] (slug or ID)
- language: BCP 47 (e.g., en-US)
- number_of_visuals: 1..4
- transparent_background / inverted_color: bool
- width / height: PNG-only, 100..4096
- visual_id / visual_ids / visual_query / visual_queries: mutually exclusive visual selection helpers

Validation
- width/height only when format=png
- non-empty lists for visual_ids/visual_queries when provided

VisualResponse
Response envelope capturing request_id, status, timestamps, and files.

Important properties
- is_completed / is_failed / is_expired / is_terminal booleans

StatusResponse
Lightweight status view with:
- request_id, status, progress, message, files_ready, files_total, error
- files: optional raw list from API (generated_files/files/urls normalized by client)

Download Guidance
- Prefer file.url from status; if absent, fallback to GET /v1/visual/:request-id/file/:file-id
- Always send Authorization header when hitting file URLs
- Filename precedence: Content-Disposition > API filename > synthesized name
- Stream writes for large files; default chunk size 64 KiB

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

Exception Hierarchy
- NapkinAPIError(message, code?, details?)
- AuthenticationError (401)
- RateLimitError (429, retry_after)
- RequestError (400)
- ProcessingError (failed/expired/timeout in long poll)

### Error Response Model

```python
class ErrorResponse(BaseModel):
    error: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
```

## CLI Reference

generate
```bash
napkin generate "content" [OPTIONS]
  --style, -s            Style name or ID
  --format, -f           svg|png
  --output, -o           Output directory
  --variations, -n       1..4
  --language, -l         BCP 47 language
  --context-before       Context before content
  --context-after        Context after content
  --width, -w            PNG width (100..4096)
  --height, -h           PNG height (100..4096)
  --transparent          Transparent background
  --inverted             Inverted colors
  --debug                Enable debug logging
```

styles
```bash
napkin styles --list
napkin styles --category colorful
```

config
```bash
napkin config --show
napkin config --check
```

version
```bash
napkin version
```

## Configuration

Settings Management
See src/utils/config.py (Pydantic BaseSettings). Key environment variables:

Required
- NAPKIN_API_TOKEN

Optional (common)
- NAPKIN_API_BASE_URL (default https://api.napkin.ai)
- NAPKIN_API_VERSION (default v1)
- NAPKIN_DEFAULT_STYLE (default vibrant-strokes)
- NAPKIN_DEFAULT_FORMAT (default svg)
- NAPKIN_DEFAULT_LANGUAGE (default en-US)
- NAPKIN_DEFAULT_VARIATIONS (default 1)
- NAPKIN_STORAGE_PATH (default ./data/visuals)
- NAPKIN_TIMEOUT_SECONDS (default 30)
- NAPKIN_POLL_INTERVAL_SECONDS (default 2.0)
- NAPKIN_MAX_POLL_ATTEMPTS (default 30)
- NAPKIN_LOG_LEVEL (INFO|DEBUG|WARNING|ERROR|CRITICAL)

### Environment Variables

All settings can be configured via environment variables with the `NAPKIN_` prefix:

```bash
NAPKIN_API_TOKEN=your_token_here
NAPKIN_DEFAULT_STYLE=sketch-notes
NAPKIN_STORAGE_PATH=/custom/path
NAPKIN_LOG_LEVEL=DEBUG
```

## Utilities

Styles
```python
from src.utils.constants import STYLES, list_style_names, get_style_by_name, get_styles_by_category
style_names = list_style_names()
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
from src.api.client import NapkinAPIClient, AuthenticationError, RateLimitError, ProcessingError
from src.api.models import VisualRequest, OutputFormat

async def safe_generate():
    try:
        async with NapkinAPIClient() as client:
            request = VisualRequest(
                content="Data Flow Diagram",
                style_id="sketch-notes",
                format=OutputFormat.SVG,
            )
            response = await client.create_visual(request)
            status = await client.wait_for_completion(response.request_id)
            return status
    except AuthenticationError:
        print("Invalid API token")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
    except ProcessingError as e:
        print(f"Processing failed: {e}")
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

RateLimitInfo
- limit, remaining, reset (datetime), retry_after (seconds, optional)

Handling Rate Limits
```python
async with NapkinAPIClient() as client:
    response = await client.create_visual(request)
    info = client.get_rate_limit_status()
    if info and info.remaining < 10:
        print(f"Remaining: {info.remaining}, reset: {info.reset}")
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

- README.md (project root) — Overview and quick start
- docs/USAGE.md — CLI usage
- docs/SETUP.md — Installation and configuration
- docs/PRD.md — Roadmap (may include future features)
- docs/NAPKIN_AI_API.md — API specification and styles

Verification Snippets (Windows CMD)
```bat
:: Create a request
curl -sS -X POST "https://api.napkin.ai/v1/visual" ^
  -H "Authorization: Bearer %NAPKIN_API_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -H "Accept: application/json" ^
  -d "{\"format\":\"svg\",\"content\":\"Test visual\"}"

:: Poll status
set ID=REPLACE_WITH_REQUEST_ID
for /l %i in (1,1,30) do (
  curl -sS -H "Authorization: Bearer %NAPKIN_API_TOKEN%" "https://api.napkin.ai/v1/visual/%ID%/status"
  timeout /t 3 >NUL
)

:: Download by URL
set URL=REPLACE_WITH_FILE_URL
curl -L "%URL%" -H "Authorization: Bearer %NAPKIN_API_TOKEN%" --output out.svg
```

Environment variables
- Required: NAPKIN_API_TOKEN
- Optional:
  - NAPKIN_DOWNLOAD_CHUNK_SIZE (default 65536)
  - NAPKIN_DOWNLOAD_OVERWRITE (default false)

Compatibility Notes
- status.generated_files preferred; status.files supported
- Prefer file.url; fallback to GET /v1/visual/:request-id/file/:file-id
- Filename/MIME precedence documented above