# Changelog

All notable changes to this project are documented in this file.
The format follows Keep a Changelog, and the project aims to follow Semantic Versioning.

## [0.1.2] - 2025-08-06
### Added
- Consolidated documentation navigation and executive summaries for faster onboarding.

### Changed
- Normalized repository documentation to reflect the current CLI/client scope only.
- Clarified environment variables (NAPKIN_*) and platform-specific setup instructions.
- Standardized headings, terminology, and code block languages for readability and accessibility.

### Fixed
- Removed or clearly marked references to non-implemented features (interactive TUI, batch engine, gallery/SQLite, web UI).
- Corrected example paths and Windows-specific instructions.
- Aligned API/CLI references and examples with implemented methods and options.

### Security
- Documented secure token handling and transport guidance; noted responsible disclosure channel (assumed contact pending verification).

## [0.1.1] - 2025-08-01
### Added
- Troubleshooting and FAQ sections to usage and setup guides.
- Explicit download behavior and filename/MIME precedence rules in the API reference.

### Changed
- Refined rate-limit notes and error-handling guidance for retries and backoff.
- Improved examples and annotations to ensure runnable snippets.

### Fixed
- Resolved inconsistencies in CLI option names and parameter mapping presented in examples.

## [0.1.0] - 2025-07-25
### Added
- Async HTTP client (httpx) with Bearer authentication.
- Endpoints:
  - POST /v1/visual
  - GET /v1/visual/:id/status
  - GET /v1/visual/:id/file/:file-id
- Retry/backoff using Tenacity, including 429 handling.
- Pydantic v2 models: VisualRequest, VisualResponse, GeneratedFile, StatusResponse, ErrorResponse, RateLimitInfo.
- Configuration via Pydantic BaseSettings with .env support and validation (NAPKIN_* variables).
- Typer-based CLI commands: generate, styles, config, version.
- Core generation workflow with async orchestration, polling, and streamed downloads.
- Style constants, categories, and mapping helpers for consistent style IDs.