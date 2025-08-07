# Changelog

All notable changes to this project are documented in this file.
The format follows Keep a Changelog, and the project aims to follow Semantic Versioning.

## [0.2.0] - 2025-08-07

### Added
- 🌐 **Streamlit Web Interface** - Interactive web application for visual generation
  - Real-time visual generation with progress indicators
  - Interactive style browser with categories and descriptions
  - Support for all 15+ visual styles with filtering
  - PNG/SVG format selection with custom dimensions
  - Multiple variations support (1-4 visuals)
  - Direct download buttons for generated visuals
  - Responsive layout for desktop and mobile
- Thread-safe async execution with dedicated event loop
- Enhanced error handling and validation in web UI
- Streamlit configuration with custom theme (.streamlit/config.toml)
- Resolution display with megapixel calculation
- 16MP safety cap for large images

### Changed
- Updated Python version requirement to 3.10+ for better compatibility with Streamlit and Dependabot
- Improved README.md with web interface documentation
- Enhanced project architecture to support both CLI and web interfaces
- Updated roadmap to reflect Phase 2 completion

### Fixed
- Fixed STYLES dictionary access in streamlit_app.py to use NamedTuple attributes
- Added proper error handling for empty STYLES or categories
- Implemented sanitize_filename for safe file downloads

## [0.1.3] - 2025-01-07

### Fixed
- Fixed failing tests by properly disabling .env file loading in test_required_api_token
- Fixed test assertion to match actual Pydantic validation error message format
- Fixed deprecation warnings by replacing datetime.utcnow() with datetime.now(timezone.utc)
- Fixed code formatting issues detected by ruff
- Fixed import order issues (E402: module level imports not at top of file)
- Fixed mypy type errors:
  - Added missing _dedupe_path method in NapkinAPIClient
  - Fixed format parameter type conversion to OutputFormat enum
  - Fixed variable name conflict causing type confusion
  - Added type annotation for console_handler
  - Fixed RateLimitInfo reset parameter to handle None values
- Removed unused imports across multiple modules

### Changed
- Updated README.md installation instructions to clarify Poetry usage and napkin CLI command
- Improved type safety throughout the codebase

## [0.1.2] - 2025-01-06

### Added
- Consolidated documentation navigation and executive summaries for faster onboarding

### Changed
- Normalized repository documentation to reflect the current CLI/client scope only
- Clarified environment variables (NAPKIN_*) and platform-specific setup instructions
- Standardized headings, terminology, and code block languages for readability

### Fixed
- Removed references to non-implemented features (interactive TUI, batch engine, gallery/SQLite, web UI)
- Corrected example paths and Windows-specific instructions
- Aligned API/CLI references and examples with implemented methods

### Security
- Documented secure token handling and transport guidance

## [0.1.1] - 2025-01-01

### Added
- Troubleshooting and FAQ sections to usage and setup guides
- Explicit download behavior and filename/MIME precedence rules in API reference

### Changed
- Refined rate-limit notes and error-handling guidance for retries and backoff
- Improved examples and annotations to ensure runnable snippets

### Fixed
- Resolved inconsistencies in CLI option names and parameter mapping in examples

## [0.1.0] - 2024-12-25 - Initial Release

### Phase 1: Project Foundation
- Initialized Python 3.9+ project with Poetry dependency management
- Configured development tools: Ruff (linting/formatting), mypy (type checking), pytest (testing)
- Created project structure with modular architecture (api, cli, core, utils)

### Phase 2: Configuration & Models
- Implemented Pydantic v2 BaseSettings for environment configuration
- Created comprehensive `.env.example` template with NAPKIN_* variables
- Defined all 15+ Napkin AI styles with categories and mappings in constants
- Built Pydantic v2 models: VisualRequest, VisualResponse, GeneratedFile, StatusResponse, ErrorResponse, RateLimitInfo

### Phase 3: API Client
- Developed async HTTPX client with Bearer token authentication
- Implemented core endpoints:
  - POST /v1/visual - Create visual request
  - GET /v1/visual/:id/status - Poll generation status
  - GET /v1/visual/:id/file/:file-id - Download generated files
- Added Tenacity for intelligent retry logic with exponential backoff
- Built comprehensive error handling for 401/404/410/429 responses
- Implemented request/response logging with configurable levels

### Phase 4: Business Logic
- Created VisualGenerator with async orchestration
- Implemented polling workflow with configurable intervals
- Added support for both `generated_files` and legacy `files` response formats
- Built streaming file downloads with chunked transfer (64KB default)
- Developed intelligent filename resolution (Content-Disposition → API metadata → synthesized)

### Phase 5: CLI Interface
- Built Typer-based CLI with Rich terminal output
- Implemented commands:
  - `generate` - Create visuals with all API parameters
  - `styles` - List/filter available styles by category
  - `config` - Show/validate configuration
  - `version` - Display version information
- Added progress indicators and formatted output tables
- Integrated comprehensive error messaging with user-friendly displays

### Phase 6: File Handling
- Implemented binary-safe file downloads with proper MIME type handling
- Added Content-Disposition header parsing (RFC 6266/5987 compliant)
- Built fallback logic for filename synthesis
- Created directory auto-creation for output paths
- Added overwrite protection with configurable behavior

### Phase 7: Documentation
- Created comprehensive README with quickstart guide
- Documented all API endpoints and parameters
- Added platform-specific setup instructions (Windows/macOS/Linux)
- Provided extensive CLI usage examples
- Included troubleshooting guide and FAQ

### Technical Achievements
- Full async/await implementation for optimal performance
- Type hints throughout with mypy validation
- Structured logging with contextual information
- Graceful error handling with detailed messages
- Rate limit handling with automatic retry
- Timezone-aware datetime handling (UTC)
- Support for both SVG and PNG output formats
- Configurable download chunk size for large files

### MVP Success Criteria Met
- ✅ Single visual generation via CLI works end-to-end
- ✅ All 15+ Napkin AI styles accessible
- ✅ Rich terminal interface with progress feedback
- ✅ Comprehensive error handling and retry logic
- ✅ Binary-safe file downloads with proper naming
- ✅ Full API integration with authentication
- ✅ Configuration via environment variables
- ✅ Cross-platform compatibility (Windows/macOS/Linux)