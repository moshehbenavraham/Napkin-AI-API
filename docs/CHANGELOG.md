# Changelog

All notable changes to this project will be documented in this file. The format follows Keep a Changelog principles where practical.

## 2025-08-06

### Added
- Implemented HTTPX-based API client with Bearer token authentication, including:
  - POST /v1/visual
  - GET /v1/visual/:id/status
  - GET /v1/visual/:id/file/:file-id
  - Request/response logging
- Added Tenacity-based retry logic with exponential backoff and rate-limit (429) handling, with configurable maximum retries.
- Created Pydantic v2 models: VisualRequest, VisualResponse, GeneratedFile, RequestStatus, with strict types and validators.
- Implemented configuration via Pydantic Settings, including:
  - Environment variable loading and .env support
  - Defaults and validation
  - Environment template (.env.example)
- Added style constants and helpers, including built-in style IDs and categories (Colorful, Casual, Hand-drawn, Formal, Monochrome).
- Implemented Typer-based CLI:
  - Main entrypoint
  - generate command with options (--content, --style, --format, --language, --context-before/after, --variations, --width/height, --transparent, --inverted, --output)
  - Rich-based terminal feedback (spinner, success/error formatting, generated file paths)
- Implemented core visual generation with async support:
  - Create visual request
  - Poll status with exponential backoff
  - Download generated files (via file IDs and/or direct URLs)
  - Save to local storage with consistent naming
  - Return saved paths

### Changed
- Updated Pydantic v2 serialization behavior by changing ser_json_timedelta to "float" to ensure compatibility and consistent JSON output.

### Notes
- These entries consolidate previously completed items from TODO.md, preserving scope and intent without duplicating in-progress work.