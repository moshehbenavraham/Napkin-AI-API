# Napkin AI API Playground Documentation
- See [.github Directory Documentation](GITHUB_FOLDER.md) for CODEOWNERS, Dependabot, PR/Issue templates, and workflows maintenance.

Executive Overview
Napkin AI API Playground provides a production-ready Python CLI and async client for generating SVG/PNG visuals from text using the Napkin API. This documentation hub centralizes setup, usage, API reference, and security.

Quick Navigation
- Project Overview: ../README.md
- Setup & Installation: SETUP.md
- Usage (CLI): USAGE.md
- API Reference (Python): API_REFERENCE.md
- Security: SECURITY.md
- Contributing: CONTRIBUTING.md
- Changelog: CHANGELOG.md

System Architecture Overview
Components and responsibilities:
- CLI (src/cli/): Typer-based commands, Rich output, progress UX
- Core (src/core/): Orchestrates request, polling, downloads
- API Client (src/api/client.py): httpx + tenacity, auth, retries, rate limit parsing
- Models (src/api/models.py): Pydantic v2 models for requests/status/files/errors
- Config & Constants (src/utils/): Environment-backed settings and style catalog
High-level data flow:
1) CLI parses user input -> 2) Core builds VisualRequest -> 3) Client POST /visual -> 4) Client polls GET /visual/:id/status -> 5) Client downloads files by URL or file id -> 6) Files saved to storage_path

Prerequisites
- Python 3.9+
- Napkin API token (request at api@napkin.ai)

Quick Start
```bash
# Install with Poetry (recommended for local dev)
poetry install

# Or with pip
pip install -r ../requirements.txt
```

Configuration
Use environment variables or a .env file at project root:
```bash
# Copy template and set your token
cp ../.env.example ../.env
# then edit .env to set NAPKIN_API_TOKEN
```
On Windows CMD:
```bat
set NAPKIN_API_TOKEN=your_token_here
```
On PowerShell:
```powershell
$env:NAPKIN_API_TOKEN="your_token_here"
```

First Run
```bash
# Show version
python ../main.py --help
python ../main.py  # runs CLI entry
# or, using Typer app name:
# napkin --help  (if installed as a package/executable in PATH)
```

Generate a Visual
```bash
# Basic
napkin generate "Machine Learning Pipeline"

# With options
napkin generate "Data Flow Diagram" --style sketch-notes --format png --width 1920 --height 1080

# Save to custom directory
napkin generate "Architecture" --output ./data/visuals
```

Available Commands
```bash
napkin generate "Your content" [OPTIONS]
napkin styles --list
napkin styles --category colorful
napkin config --show
napkin config --check
napkin version
```

Project Structure
```
Napkin-AI-API/
├── src/
│   ├── api/          # API client and models
│   ├── cli/          # CLI commands and display
│   ├── core/         # Core generation logic
│   ├── storage/      # (reserved)
│   └── utils/        # Configuration and helpers
├── tests/            # Test suite
├── docs/             # Documentation
├── data/             # Generated visuals storage
└── main.py           # Entry point
```

Notes
- Security: API tokens are masked, never logged, and .env is gitignored.
- i18n: Language is BCP 47 compliant (e.g., en-US).
- Accessibility: Code blocks use explicit languages and examples include comments.