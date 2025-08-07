# Changelog

All notable changes to this project are documented in this file.
The format follows Keep a Changelog, and the project aims to follow Semantic Versioning.

## [0.3.3] - 2025-08-07

### Changed
- **Documentation**: Consolidated multiple documentation files into two main guides:
  - `API_GUIDE.md` - Complete API reference, usage examples, and styles
  - `PROJECT_GUIDE.md` - Development setup, testing, CI/CD, and contributing
- **Simplified Structure**: Reduced documentation redundancy while maintaining all essential information
- **README**: Updated to reference the new consolidated documentation structure

### Maintained
- All original documentation content preserved in consolidated format
- Official Napkin API documentation remains in `napkin_official/`
- FUNDING.yml, LICENSE.md, and CONTRIBUTING.md remain as required files

## [0.3.2] - 2025-08-07

### Fixed - Code Quality & CI/CD
- 🐛 **CI/CD Pipeline** - Fixed Python version compatibility
  - Updated CI workflow from Python 3.9 to 3.10+ to match project requirements
  - Fixed poetry.lock file synchronization issues
- 🔧 **Code Quality Improvements**
  - Fixed all ruff linting errors across the codebase
  - Replaced bare `except:` with `except Exception:` in all scripts
  - Removed unnecessary f-string placeholders
  - Fixed unused imports in test files
  - Formatted code with ruff to maintain consistency
- 🚨 **Deprecation Fixes**
  - Updated `datetime.utcnow()` to `datetime.now(timezone.utc)` to address deprecation warning
- 📝 **Script Improvements**
  - Fixed Windows line endings (CRLF to LF) in shell scripts
  - Fixed bash syntax errors in `scripts/failures.sh`
  - Improved error handling in GitHub failure monitoring scripts

### Improved
- ✅ **Testing & Validation**
  - All tests passing
  - Type checking clean with mypy
  - Linting clean with ruff
  - GitHub Actions workflows validated
- 📚 **Documentation Updates**
  - Added development section to README with testing commands
  - Updated version badge to 0.3.2
  - Changed status from "MVP Complete" to "Production Ready"
  - Added CI passing badge

## [0.3.1] - 2025-08-07

### Added - Developer Tools
- 🔍 **GitHub Actions Failure Monitoring** - Quick scripts to check CI failures
  - `bin/failures` command for instant failure checks
  - `scripts/check_failures.py` - Reads GitHub token from .env automatically
  - `scripts/get_github_failures.py` - Full-featured failure analysis with export
  - `scripts/quick_failures.py` - Ultra-simple one-file script
- 🔔 **CI/CD Error Notifications** - Automated error reporting workflows
  - `.github/workflows/error-notifications.yml` - Multi-channel notifications
  - `.github/workflows/error-monitor.yml` - Simple webhook monitor
  - `.github/scripts/error_reporter.py` - Advanced Python error reporter
  - Support for Slack, Discord, Email, GitHub Issues, PagerDuty
- 📚 **Enhanced Documentation**
  - `docs/GITHUB_ERROR_MONITORING.md` - Complete setup guide for error notifications
  - `scripts/README.md` - Guide for failure checking scripts
  - `scripts/SETUP.md` - Quick setup instructions

### Improved
- Added GITHUB_TOKEN to .env configuration
- Created convenient `bin/` directory for quick commands
- Enhanced documentation structure with new monitoring tools

### Fixed
- Corrected typo in .env file (GITHUT_API_TOKEN → GITHUB_TOKEN)

## [0.3.0] - 2025-08-07

### Added
- 🌍 **Multi-Language Support** - Generate visuals in 38 languages
  - Support for English, Spanish, French, German, Italian, Portuguese, Dutch, Russian
  - Chinese (Simplified/Traditional), Japanese, Korean, Arabic, Hindi, Turkish
  - Polish, Swedish, Danish, Norwegian, Finnish and regional variants
  - Proper BCP 47 language tag implementation
- 📋 **Context Options** - Enhanced visual generation with contextual information
  - `context_before` field for text appearing before main content
  - `context_after` field for text appearing after main content
  - Helps generate more meaningful and relevant visuals
- 🎯 **Advanced Options Panel** - New settings for fine-tuned control
  - Transparent background toggle (works best with PNG)
  - Color inversion option for alternate color schemes
  - Collapsible advanced options section in sidebar
- 🔄 **Visual Regeneration** - Update and modify existing visuals
  - Regenerate existing visuals with new content using visual ID
  - Search for specific visual types (mindmap, flowchart, timeline, etc.)
  - Support for 15+ visual type queries
- 🎨 **Enhanced Style Integration** - Complete API style support
  - All 16 styles properly mapped with official API IDs
  - Style categories: Colorful, Casual, Hand-drawn, Formal, Monochrome
  - Detailed style descriptions and metadata

### Improved
- Enhanced Streamlit UI with better organization and layout
- Added expandable sections for better space utilization
- Improved generation details panel with all parameters displayed
- Better error handling for visual regeneration modes
- Updated documentation with comprehensive feature list

### Changed
- Updated `VisualGenerator` to accept all new API parameters
- Modified `run_generation_in_worker` to handle extended parameter set
- Enhanced API models to support visual_id and visual_query parameters

## [0.2.2] - 2025-08-07

### Fixed
- 🐛 **Fixed Pydantic Model Field Access** - Resolved "StatusResponse object has no field downloaded_files" error
  - Changed from attempting to dynamically add attributes to Pydantic models (not allowed)
  - Now returns tuple (status_response, downloaded_files) from worker function
  - Properly handles tuple unpacking in main generation flow
  - Maintains backward compatibility with existing file display logic

### Improved
- Enhanced documentation with clearer local testing instructions
- Added explicit API token setup steps in README

## [0.2.1] - 2025-08-07

### Fixed
- 🔐 **Fixed Authorization Issue** - Resolved 403 Forbidden errors when fetching generated visuals
  - Added Bearer token authentication to image fetch requests
  - Implemented pre-download mechanism in worker thread for API endpoints
  - Properly parse and handle file download URLs that require authentication
  - Added fallback handling for both direct CDN URLs and authenticated API endpoints
- Fixed duplicate import statements and moved all imports to top of file
- Fixed bare except clause to use specific Exception handling
- Applied proper code formatting with ruff

### Improved
- Enhanced error handling with try-catch blocks for file downloads
- Better file URL extraction with support for multiple response formats
- Added version info display with git commit hash in footer
- Improved file_id parsing to handle suffixes properly

## [0.2.0] - 2025-08-07

### Added
- 🌐 **Streamlit Web Interface** - Interactive web application for visual generation
  - Real-time visual generation with progress indicators
  - Interactive style browser with categories and descriptions
  - Support for all 16 visual styles with filtering
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