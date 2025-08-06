# Changelog

This project adheres to Keep a Changelog and Semantic Versioning where practical.

## [0.1.1] - 2025-08-06
### Changed
- Documentation overhaul: normalized scope to CLI/client, removed or clearly marked roadmap-only items (interactive TUI, batch, gallery, web UI).
- Updated docs/README.md, README.md, docs/SETUP.md, docs/USAGE.md, docs/API_REFERENCE.md for accuracy and consistency.
- Clarified environment variables and configuration mapping.

### Added
- Executive overview and architecture summaries in README and docs hub.
- Troubleshooting and FAQ in docs/USAGE.md and docs/SETUP.md.
- Explicit download guidance and filename/MIME precedence in API reference.

### Fixed
- Inconsistent references to non-implemented commands.
- Incorrect example paths and ambiguous Windows instructions.

## [0.1.0] - 2025-08-06
### Added
- HTTPX-based API client with Bearer auth:
  - POST /v1/visual
  - GET /v1/visual/:id/status
  - GET /v1/visual/:id/file/:file-id
- Tenacity-based retries and 429 handling.
- Pydantic v2 models: VisualRequest, VisualResponse, GeneratedFile, RequestStatus, StatusResponse, ErrorResponse, RateLimitInfo.
- Configuration via Pydantic Settings with .env support and validation.
- Style constants and helpers (Colorful, Casual, Hand-drawn, Formal, Monochrome).
- Typer-based CLI with commands:
  - generate, styles, config, version
- Core generation workflow with async support, status polling, and download utilities.