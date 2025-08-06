## Current Issues & Improvements (January 2025)
### Status Summary (MVP)
- Core flow validated end-to-end:
  - Create visual
  - Poll status
1. **API Response Parsing**
   - [x] Debug actual API response format for files/urls field
   - [x] Update StatusResponse to properly handle file URLs from API (treat `generated_files` as authoritative; accept legacy `files`)
   - [x] Fix file download logic to handle actual API response structure (prefer `generated_files[].url`; fallback to GET /v1/visual/:id/file/:file-id)
  - Download generated files (schema-aligned with generated_files[].url)
- Remaining: pre-commit hooks, expanded tests, optional file logging, and doc consolidation.

### Critical Fixes Needed
1. **API Response Parsing**
   - [ ] Debug actual API response format for files/urls field
   - [ ] Update StatusResponse to properly handle file URLs from API
   - [ ] Fix file download logic to handle actual API response structure

2. **Pydantic v2 Compatibility**
   - [ ] Review other model configurations for v2 compatibility

### Code Quality Improvements
1. **Unify OutputFormat enum**
   - [ ] Remove duplicate enum from src/utils/constants.py
   - [ ] Import from src/api/models.py everywhere
   - [ ] Update DEFAULTS to use models.OutputFormat

2. **Datetime imports cleanup**
   - [ ] Replace dynamic `__import__` with normal imports in client.py
   - [ ] Ensure timezone-aware UTC consistently

3. **Interactive CLI**
   - [ ] Either implement or remove src/cli/interactive.py stub

4. **Testing improvements**
   - [ ] Add mock tests for API client
   - [ ] Test retry logic with mocked responses
   - [ ] Add integration tests for file downloads
# Napkin AI API Playground - Implementation TODO

> **📋 Status Check**: This TODO is aligned with the comprehensive documentation in `/docs/`:
> - **PRD.md**: Product requirements and architecture
> - **API_REFERENCE.md**: Complete API documentation
> - **CONTRIBUTING.md**: Development workflow and tools
> - **SETUP.md**: Installation and configuration guide
> - **napkin_ai_api.md**: Napkin API specifications
>
> **🎯 Focus**: Phase 1 implements the MVP - single visual generation via CLI

## Phase 1: Core Foundation (Week 1) - CRITICAL

### 1. Project Initialization
- [-] Set up development environment
  - [ ] Configure pre-commit hooks (.pre-commit-config.yaml)
  - [x] Add Ruff for linting and formatting
  - [x] Add mypy for type checking
  - [x] Configure pytest for testing

### 2. Core API Client Implementation
- [x] Implement HTTPX-based API client (`src/api/client.py`)
  - [x] Initialize with Bearer token authentication
  - [x] Implement POST /v1/visual endpoint
  - [x] Implement GET /v1/visual/:id/status endpoint
  - [x] Implement GET /v1/visual/:id/file/:file-id endpoint
  - [x] Add request/response logging
- [x] Add Tenacity for retry logic
  - [x] Exponential backoff strategy
  - [x] Handle rate limiting (429 responses)
  - [x] Maximum retry configuration
- [x] Create Pydantic v2 models (`src/api/models.py`)
  - [x] VisualRequest, VisualResponse, GeneratedFile, RequestStatus

### 3. Configuration Management
- [x] Implement Pydantic Settings (`src/utils/config.py`)
- [x] Create environment template (`.env.example`)
- [x] Add style constants (`src/utils/constants.py`)

### 4. Basic CLI with Typer
- [x] CLI structure and generate command implemented with Rich output

### 5. Core Generation Logic
- [x] Visual generator implemented with async support

### 6. Error Handling & Logging
- [x] Structured logging and exception hierarchy
- [ ] Optional file logging to disk

### 7. Basic Testing
- [ ] Client unit tests and integration tests pending

### 8. Documentation
- **MVP Status**: Core functionality implemented; file download schema alignment COMPLETED (using generated_files[].url with legacy files fallback)
- **Pending Items**:
  - Pre-commit hooks configuration
  - Expanded test coverage
  - Optional file logging
  - API response format documentation consolidation
- [ ] README updates and inline docstrings pending

## Success Criteria for Phase 1

- [-] User can generate a single visual via CLI: `napkin generate "Test content"`
  - [x] CLI command works and connects to API
  - [x] Request is created successfully
  - [ ] Files are properly downloaded (API response format issue)
- [-] At least 50% test coverage for core functionality

## Notes

- **MVP Status**: Core functionality implemented; main gap remains file download schema alignment
- **Pending Items**:
  - ⚠️ Fix file download from API response
  - Pre-commit hooks configuration
  - Expanded test coverage
  - Optional file logging
  - API response format documentation

## Next Steps

1. **Immediate Priority**: Debug actual API response format
2. **Documentation**: Update API response format documentation
3. **Testing**: Add integration tests with mocked API responses
## Current Issues & Improvements (January 2025)

### Status Summary (MVP)
- Core flow validated end-to-end:
  - Create visual
  - Poll status
  - Download generated files (schema-aligned with generated_files[].url)
- Remaining: pre-commit hooks, expanded tests, optional file logging, and doc consolidation.

### Critical Fixes Needed
1. **API Response Parsing**
   - [x] Debug actual API response format for files/urls field
   - [x] Update StatusResponse to properly handle file URLs from API (treat `generated_files` as authoritative; accept legacy `files`)
   - [x] Fix file download logic to handle actual API response structure (prefer `generated_files[].url`; fallback to GET /v1/visual/:id/file/:file-id)

2. **Pydantic v2 Compatibility**
   - [ ] Review other model configurations for v2 compatibility

### Code Quality Improvements
1. **Unify OutputFormat enum**
   - [ ] Remove duplicate enum from src/utils/constants.py
   - [ ] Import from src/api/models.py everywhere
   - [ ] Update DEFAULTS to use models.OutputFormat

2. **Datetime imports cleanup**
   - [ ] Replace dynamic `__import__` with normal imports in client.py
   - [ ] Ensure timezone-aware UTC consistently

3. **Interactive CLI**
   - [ ] Either implement or remove src/cli/interactive.py stub

4. **Testing improvements**
   - [ ] Add mock tests for API client
   - [ ] Test retry logic with mocked responses
   - [ ] Add integration tests for file downloads

# Napkin AI API Playground - Implementation TODO

> **📋 Status Check**  
> Aligned with `/docs/`: PRD.md, API_REFERENCE.md, CONTRIBUTING.md, SETUP.md, napkin_ai_api.md  
> **🎯 Focus**: Phase 1 MVP – single visual generation via CLI

## Phase 1: Core Foundation (Week 1) - CRITICAL

### 1. Project Initialization
- [-] Set up development environment
  - [ ] Configure pre-commit hooks (.pre-commit-config.yaml)
  - [x] Add Ruff for linting and formatting
  - [x] Add mypy for type checking
  - [x] Configure pytest for testing

### 2. Core API Client Implementation
- [x] Implement HTTPX-based API client (`src/api/client.py`)
  - [x] Initialize with Bearer token authentication
  - [x] Implement POST /v1/visual endpoint
  - [x] Implement GET /v1/visual/:id/status endpoint
  - [x] Implement GET /v1/visual/:id/file/:file-id endpoint
  - [x] Add request/response logging
- [x] Add Tenacity for retry logic
  - [x] Exponential backoff strategy
  - [x] Handle rate limiting (429 responses)
  - [x] Maximum retry configuration
- [x] Create Pydantic v2 models (`src/api/models.py`)
  - [x] VisualRequest, VisualResponse, GeneratedFile, RequestStatus

### 3. Configuration Management
- [x] Implement Pydantic Settings (`src/utils/config.py`)
- [x] Create environment template (`.env.example`)
- [x] Add style constants (`src/utils/constants.py`)

### 4. Basic CLI with Typer
- [x] CLI structure and generate command implemented with Rich output

### 5. Core Generation Logic
- [x] Visual generator implemented with async support

### 6. Error Handling & Logging
- [x] Structured logging and exception hierarchy
- [ ] Optional file logging to disk

### 7. Basic Testing
- [ ] Client unit tests and integration tests pending

### 8. Documentation
- [ ] README updates and inline docstrings pending

## Success Criteria for Phase 1

- [-] User can generate a single visual via CLI: `napkin generate "Test content"`
  - [x] CLI command works and connects to API
  - [x] Request is created successfully
  - [x] Files are properly downloaded (schema-aligned)
- [-] At least 50% test coverage for core functionality

## Implementation Plan: File Download Schema Alignment (Minimal, Correct)
- Expected API response (current):
  - Status: `{ id, status, request, generated_files: [{ id, url, format, filename?, size_bytes? }] }`
  - File download: binary with `Content-Type` image/svg+xml or image/png; optional `Content-Disposition` filename.
- Corrected usage in client:
  - Treat `generated_files` as authoritative; continue supporting legacy `files` if present.
  - For each file object, prefer `url` for download; if missing, build fallback path: `/v1/visual/{request_id}/file/{file_id}`.
- Client-side flow:
  1) Poll until `status == "completed"`.
  2) Iterate `generated_files` (or legacy `files`).
  3) Download with headers:
     - Authorization: Bearer <token>
     - Accept: based on format if known, else `*/*`.
  4) Filename inference (priority):
     - Content-Disposition (RFC 6266 / 5987: filename* then filename)
     - API metadata `filename`
     - Synthesized: `{request_id}_{file.id}.{ext}` where ext from format or from Content-Type.
  5) MIME handling:
     - Trust `Content-Type` if present; fallback from `format`.
     - Save bytes without decoding; always binary-safe streaming/chunking.
  6) Large files:
     - Stream with 64KiB chunks (configurable via env).
  7) Errors/edges:
     - Unexpected `Content-Type`: log warning, save with ext from format.
     - Missing headers: proceed with synthesized filename.
     - 401/403 -> AuthenticationError; 404/410 -> expired; 429 -> retry with backoff.
- Backwards compatibility / migration:
  - Continue accepting both `generated_files` and legacy `files`.
  - Maintain existing `download_file_by_url(url) -> bytes` for compatibility, but internally stream to BytesIO; recommend using streaming save in CLI paths.
  - Document new precedence rules and fallbacks.

## Verification & Test Plan
Manual verification (Windows CMD; copy-paste):
- Create:
  - curl -sS -X POST "https://api.napkin.ai/v1/visual" -H "Authorization: Bearer %NAPKIN_API_TOKEN%" -H "Content-Type: application/json" -H "Accept: application/json" -d "{\"format\":\"svg\",\"content\":\"Test visual\"}"
- Poll:
  - set ID=REPLACE_WITH_REQUEST_ID
  - for /l %i in (1,1,30) do ( curl -sS -H "Authorization: Bearer %NAPKIN_API_TOKEN%" "https://api.napkin.ai/v1/visual/%ID%/status" & timeout /t 3 >NUL )
- Download first file by URL:
  - set URL=REPLACE_WITH_FILE_URL
  - curl -L "%URL%" -H "Authorization: Bearer %NAPKIN_API_TOKEN%" --output out.svg
- Inspect headers:
  - curl -I -L "%URL%" -H "Authorization: Bearer %NAPKIN_API_TOKEN%"

Automated tests (pytest, httpx/respx, pytest-asyncio):
- Unit:
  - Content-Disposition parsing (filename*, filename); unicode and spaces.
  - MIME fallback from format when header missing.
  - Filename synthesis logic.
- Integration (mocked):
  - Status returns generated_files with url -> download returns 200 with Content-Disposition -> path and content correct.
  - Legacy shape: files instead of generated_files.
  - Fallback path when url missing -> GET /v1/visual/:id/file/:file-id.
  - Error paths: 401, 404, 410, 429 retry; unexpected content-type.
- Performance:
  - Streamed chunks; assert chunked writes occur (spy on write calls or count).

## Documentation Snippet: API Response & Client Usage
- API response format (GeneratedFile):
  - id: string
  - url: string (expires; Authorization required)
  - format: "svg" | "png"
  - filename: string (optional)
  - size_bytes: integer (optional)
- Example:
  ```json
  {
    "id": "426614174000-wdjvjhwv8",
    "url": "https://api.napkin.ai/v1/visual/123e.../file/4266...wdjvjhwv8",
    "format": "svg",
    "filename": "visual.svg",
    "size_bytes": 245760
  }
  ```
- Client usage:
  ```python
  # Iterate files from status (supports generated_files and legacy files)
  file_list = status.files or getattr(status, "generated_files", []) or []
  for f in file_list:
      content = await client.download_file_by_url(f["url"])  # binary-safe
      # Or prefer streaming save in CLI paths:
      # await client.save_file_by_url(f["url"], output_dir)
  ```
- Behavior:
  - Filename precedence: Content-Disposition > API filename > synthesized
  - MIME: use Content-Type, fallback to format mapping
  - Stream for large files

## Configuration / Environment
- Required:
  - NAPKIN_API_TOKEN
- Optional (sensible defaults):
  - NAPKIN_DOWNLOAD_CHUNK_SIZE (default: 65536)
  - NAPKIN_DOWNLOAD_OVERWRITE (default: false)
  - NAPKIN_FILE_LOGGING (default: false; see pending items)

## Pending Items & Next Steps
- Pre-commit hooks configuration
  - Hooks: ruff-format, ruff-check, mypy, pytest (quick), detect-secrets (optional)
  - Enable:
    - pipx install pre-commit
    - pre-commit install
    - Create .pre-commit-config.yaml with repos:
      - ruff, mypy, detect-secrets (optional), local pytest hook
- Expanded test coverage
  - Priority: download path, retry logic (429/5xx), StatusResponse mapping, filename inference, streaming writes
  - Tooling: pytest, respx, pytest-asyncio, coverage
- Optional file logging
  - Use cases: audit/debugging for batch ops
  - Toggle: NAPKIN_FILE_LOGGING=true
  - Default: disabled; rolling file, size-limited
- API response format documentation
  - Source of truth: docs/API_REFERENCE.md
  - Cross-reference: docs/napkin_ai_api.md
  - Ownership: API team (format), SDK team (mapping)