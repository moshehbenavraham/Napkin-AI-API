# Napkin AI API Playground - Product Requirements Document

## Executive Summary

The Napkin AI API Playground is a Python application that enables exploration and utilization of the Napkin AI API. It serves as both a developer testing environment and a production-ready client for generating visual content at scale. The application offers a command-line interface with an optional web UI, providing flexible access to API features while maintaining an excellent developer experience.

## Product Vision

Create a playground for the Napkin AI API that enables users to:
- Explore API capabilities without writing code
- Test visual generation with different parameters
- Manage and organize generated visuals efficiently
- Monitor API usage and optimize performance
- Automate workflows for batch visual generation
- Integrate with existing development workflows

## Core Features

### 1. Interactive Visual Generator
Description: Command-line and web interfaces for testing API parameters

Capabilities:
- Input text content with optional context_before and context_after
- Select from built-in styles and reference custom style IDs
- Choose output format (SVG or PNG) with dimension control for PNG
- Set language using BCP 47 tags
- Configure visual options: transparent_background and inverted_color
- Generate 1–4 variations per request
- Show real-time status with progress indicators

User Stories:
- As a developer, I want to test different visual styles quickly
- As a content creator, I want to generate multiple variations to choose from
- As a designer, I want precise control over output dimensions and formats

### 2. Style Explorer
Description: Interactive browser for available visual styles

Capabilities:
- Display style gallery with previews
- Filter styles by category: Colorful, Casual, Hand-drawn, Formal, Monochrome
- Save favorite styles for quick access
- Compare styles side-by-side
- Track custom style IDs from app.napkin.ai
- Provide non-AI style recommendations based on content type

User Stories:
- As a user, I want to see styles before choosing
- As a brand manager, I want to find styles that match guidelines
- As a developer, I want to copy style IDs for code

### 3. Batch Processing Engine
Description: Bulk visual generation

Capabilities:
- Process multiple text inputs from CSV or JSON files
- Apply different styles to the same content
- Generate variations for A/B testing
- Handle parallel requests with rate limit management
- Track progress with ETA
- Automatically retry on failures
- Export batch results into organized folders

User Stories:
- As a content team, we want to generate visuals for multiple articles
- As an educator, I want to create visual aids for entire courses
- As a marketer, I want to test different visual styles for campaigns

### 4. Visual Gallery & Management
Description: Local storage and organization for generated visuals

Capabilities:
- Store metadata in SQLite
- Automatically organize files by date, project, and style
- Search and filter by content, style, date, and format
- Tagging for categorization
- Generate thumbnails for quick preview
- Export collections as ZIP archives
- Clean up expired content
- Track versions for regenerated visuals

User Stories:
- As a user, I want to find previously generated visuals easily
- As a team, we want to share visual collections
- As a developer, I want to track visual generation history

### 5. API Monitor & Analytics
Description: API usage tracking and optimization

Capabilities:
- Monitor rate limits with visual indicators
- Track request and response times
- Analyze success and failure rates
- Estimate cost and usage
- Provide performance insights
- Export usage reports
- Alert when approaching rate limits
- Display historical usage graphs

User Stories:
- As a developer, I want to monitor API usage
- As a manager, I want to track costs and optimize usage
- As a user, I want to know when I’m approaching limits

### 6. Visual Search & Regeneration
Description: Visual discovery and modification

Capabilities:
- Search by visual type such as mindmap, flowchart, or timeline
- Regenerate existing visuals with new content
- Clone visuals with different parameters
- Provide type suggestions based on content
- Batch regeneration with parameter updates
- Compare regenerated versions side-by-side

User Stories:
- As a user, I want to find the right visual type for my content
- As a designer, I want to iterate on existing visuals
- As a content creator, I want to update visuals with new information

## Technical Architecture

### Technology Stack

Core:
- Python 3.10+ with async/await
- Poetry for dependency management
- python-dotenv for environment configuration (.env support; preferred key OPENAI_API_KEY, legacy API_KEY fallback)

CLI:
- Rich for terminal formatting and progress bars
- Typer for CLI framework
- Questionary for interactive prompts

Web Interface optional:
- Streamlit for web UI
- Plotly for analytics charts

API & Networking:
- HTTPX for async HTTP with retry logic
- Pydantic v2 for validation and settings
- Tenacity for exponential backoff

Storage:
- SQLite for metadata
- Pillow for image processing and thumbnails
- Pathlib for file management

Development:
- Pytest for testing
- Ruff for linting and formatting
- Mypy for type checking
- pre-commit for Git hooks

### Project Structure

```
napkin-api-playground/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py       # CLI command definitions
│   │   ├── interactive.py    # Interactive prompts
│   │   └── display.py        # Rich terminal output
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py         # API client with retry logic
│   │   ├── models.py         # Pydantic models
│   │   └── monitor.py        # Rate limit tracking
│   ├── core/
│   │   ├── __init__.py
│   │   ├── generator.py      # Visual generation logic
│   │   ├── batch.py          # Batch processing
│   │   ├── gallery.py        # Visual management
│   │   └── analytics.py      # Usage analytics
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py       # SQLite operations
│   │   ├── files.py          # File management
│   │   └── cache.py          # Caching layer
│   ├── web/
│   │   ├── __init__.py
│   │   ├── app.py            # Streamlit app
│   │   ├── pages/            # Web UI pages
│   │   └── components/       # Reusable components
│   └── utils/
│       ├── __init__.py
│       ├── config.py         # Configuration management
│       ├── helpers.py        # Utility functions
│       └── constants.py      # Style IDs, etc.
├── tests/
│   ├── test_api/
│   ├── test_core/
│   └── test_storage/
├── data/
│   ├── database/             # SQLite files
│   ├── visuals/              # Generated visuals
│   └── exports/              # Export archives
├── config/
│   ├── .env.example          # Environment template (set OPENAI_API_KEY)
│   └── styles.json           # Style definitions
├── docs/
│   ├── PRD.md                # This document
│   ├── API_GUIDE.md          # API usage guide
│   └── DEVELOPMENT.md        # Development guide
├── pyproject.toml            # Poetry configuration
├── README.md                 # Project overview
└── main.py                   # Entry point
```

### Data Models

The following fields must be captured for correct operation and align with the API documentation:

```python
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

class VisualRequest:
    id: UUID
    content: str
    context_before: Optional[str]
    context_after: Optional[str]
    format: Literal["svg", "png"]
    style_id: Optional[str]
    language: str = "en-US"
    number_of_visuals: int = 1
    transparent_background: bool = False
    inverted_color: bool = False
    width: Optional[int]  # PNG only; width takes precedence if both set
    height: Optional[int] # PNG only; ignored if width is set
    created_at: datetime
    status: Literal["pending", "processing", "completed", "failed"]
    error_message: Optional[str] = None

class GeneratedFile:
    id: str
    request_id: UUID
    file_url: str
    format: str
    file_size: Optional[int]
    downloaded: bool
    local_path: Optional[Path]
    created_at: datetime
    expires_at: datetime

class GalleryItem:
    id: UUID
    request_id: UUID
    content: str
    style_name: str
    style_id: str
    format: str
    file_path: Path
    thumbnail_path: Optional[Path]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    file_size: Optional[int]
```

## User Interface Design

### CLI Interface

- Provide interactive and direct command usage for generation, batch processing, gallery management, and monitoring.
- In interactive mode, prompt for content, optional context, style selection, format, variations, and language.
- Display progress bars and completion messages; store outputs under data/visuals by date.

### Web Interface optional

- Launch via `napkin-playground web`, opening `http://localhost:8501`.
- Pages:
  1. Generator with form-based inputs and preview
  2. Style Explorer with grid and filters
  3. Batch Processor for CSV upload and configuration
  4. Gallery for browsing and search
  5. Analytics for usage and performance charts
  6. Settings for API token and defaults

## Implementation Phases

Phase 1: Core Foundation (Week 1)
Priority: Critical
- Project setup with Poetry and pyproject.toml
- Basic API client using HTTPX with Tenacity-backed retries
- CLI structure with Typer
- Configuration management with Pydantic v2 settings
- Single visual generation command
- Structured logging with configurable log level
- Environment variable validation and .env support
- Basic error handling with user-friendly messages

Phase 2: Interactive Features (Week 2)
Priority: High
- Interactive CLI with Questionary prompts
- Style browser using Rich and preview logic
- Terminal UI with progress bars and spinners
- Async status polling with exponential backoff
- File management with automatic organization
- Download progress tracking and resume
- Rate limit detection and intelligent queuing

Phase 3: Storage & Gallery (Week 3)
Priority: High
- SQLite database with migrations
- Gallery management and metadata indexing
- Hierarchical file organization by date, project, and style
- Full-text search and advanced filters
- Thumbnail generation with caching
- Bulk export with compression
- Database backup and restore

Phase 4: Batch Processing (Week 4)
Priority: Medium
- CSV and JSON input parsing with validation
- Configurable parallel requests
- Rate limit management with backoff
- Real-time batch progress with ETA
- Result aggregation with success and failure reporting
- Bulk export with multiple formats
- Resume capability for interrupted batches
- Template support for common batch operations

Phase 5: Web Interface (Week 5)
Priority: Medium
- Streamlit app
- Generator page with preview
- Style explorer with filtering
- Gallery browser with infinite scroll
- Drag-and-drop file upload
- Real-time status updates
- Responsive layout
- Dark and light themes

Phase 6: Analytics & Monitoring (Week 6)
Priority: Low
- Usage tracking with privacy controls
- Trend analysis
- Cost estimation with alerts
- Performance metrics and suggestions
- Dashboards with customizable widgets
- Automated report generation and scheduling
- API health indicators

Phase 7: Advanced Features (Week 7)
Priority: Low
- Visual search by content and type
- One-click regeneration with parameter variations
- Side-by-side comparison tools
- Custom style tracking and management
- Workflow automation with triggers and actions
- Plugin system for extensions
- Integrations with design tools

Phase 8: Polish & Documentation (Week 8)
Priority: Critical
- Comprehensive testing suite (unit, integration, e2e)
- Performance optimization and memory profiling
- Complete documentation with examples
- Video tutorials and sample workflows
- Multi-platform installation guides
- Release preparation and CI/CD pipeline
- Security review
- Accessibility considerations

## Success Metrics

Technical Metrics
- API performance: p95 response time under 10 seconds for valid requests
- Reliability: success rate over 98 percent for valid requests
- Data integrity: zero data loss for generated visuals
- Code quality: 90 percent test coverage for core functionality
- API coverage: support documented API parameters
- Resource efficiency: memory usage under 500 MB during batch processing
- Scalability: handle 1000 concurrent requests in controlled tests

User Experience Metrics
- Onboarding: time to first visual under 30 seconds with valid token
- Batch operations: process 100 items without errors in a single run
- Search: gallery search results under 1 second on 10k items on a typical dev machine
- Preview speed: style preview load under 2 seconds
- CLI responsiveness: command startup under 100 ms
- Error recovery: clear error messages with actionable guidance

Business Metrics
- Feature completeness: support the set of built-in styles documented in napkin_ai_api
- API utilization: enable testing of all exposed API features
- Efficiency gains: reduce avoidable API calls via caching by at least 20 percent
- Throughput: capability to generate 1000 visuals per day on a single machine
- Export performance: export a 500-item collection in under 5 minutes
- User adoption: 90 percent task completion rate for new users in guided tests

## Risk Management

Technical Risks
- API rate limiting: Implement intelligent queuing, exponential backoff, and user notifications
- API changes: Pin versions, test thoroughly, degrade gracefully
- Large file handling: Stream downloads, track progress, monitor disk usage
- Database corruption: Backups, transactional safety, recovery procedures
- Memory leaks: Profiling, automated tests, resource cleanup

Business Risks
- API token revocation: Clear errors, validation, user guidance
- Competitive tools: Focus on UX and documentation quality
- User adoption: Improve docs, tutorials, and support materials

Operational Risks
- Dependency vulnerabilities: Automated scanning, updates, pinning
- Platform compatibility: Cross-platform testing, container options
- Support burden: Self-service docs, FAQ, and community channels

## Security & Privacy

API Token Management
- Store tokens in environment or config files securely
- Never log or display tokens; use masked previews only
- Validate tokens on startup
- Support encrypted configuration storage
- Provide clear errors for invalid tokens

Data Protection
- Local storage only
- Optional database encryption
- Secure file permissions
- No telemetry without explicit consent

Rate Limit Protection
- Back off automatically on 429
- Queue batch operations
- Warn users before hitting limits
- Provide daily usage summaries

## Error Handling

API Errors
- Handle HTTP status codes consistently
- Retry with exponential backoff when appropriate
- Provide actionable error messages
- Offer fallback options where feasible

File Management
- Handle expired URLs gracefully
- Clean temporary files automatically
- Monitor disk space
- Detect and recover from file corruption

User Input Validation
- Validate parameters prior to API calls
- Provide helpful error messages for invalid input
- Suggest corrections
- Sanitize inputs

## Future Enhancements
Note: The following roadmap outlines future releases beyond the current scope; no new scope is introduced for the current project.

Version 2.0: Collaboration & Cloud
- Multi-user support
- Cloud storage integrations
- Webhooks
- Custom style creator
- Content assistance
- Team analytics

Version 3.0: Enterprise & Integration
- Advanced collaboration
- Visual editor
- Template marketplace
- Design tool integrations
- Enterprise API proxy
- White-label options

Version 4.0: AI & Automation
- AI visual optimization
- Workflow automation
- Content intelligence
- Performance prediction
- Advanced analytics

## Appendix

Style ID Reference
Refer to docs/napkin_ai_api.md for the latest style IDs. Keep utils/constants.py in sync.

Sample Configuration / Environment

Environment variables:
- OPENAI_API_KEY: Preferred environment variable for OpenAI access
- API_KEY: Legacy fallback (still read but deprecated)

Local development:
- Use a project-root .env (gitignored). If python-dotenv is installed, it will be loaded automatically.
- Example .env:
  ```
  OPENAI_API_KEY=sk-...
  ```

See .env.example for environment variables relevant to configuration.
## Immediate Next Steps

Week 1 Priorities
1. Project Initialization
   - Set up Poetry project and pyproject.toml
   - Configure pre-commit hooks
   - Create project structure

2. Core API Client
   - Implement HTTPX client with authentication
   - Add Pydantic models for API requests and responses
   - Implement configuration management using environment variables

3. MVP CLI
   - Build Typer-based CLI with basic commands
   - Implement single visual generation workflow
   - Add basic error handling and logging

Success Criteria for Week 1
- User can install the package locally
- User can generate a single visual via CLI
- All API parameters used by MVP are supported
- Error messages are user-friendly

## Conclusion

The Napkin AI API Playground provides CLI and optional web interfaces, batch processing, local storage, and analytics to generate, manage, and optimize visual content creation at scale. The modular architecture and phased implementation support maintainability and iterative delivery. The plan centers on developer experience, clear risk mitigation, and measurable success criteria while staying within the defined scope.