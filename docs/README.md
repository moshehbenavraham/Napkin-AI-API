# Napkin AI API Playground Documentation

Overview
A cohesive documentation hub for the Napkin AI API Playground. This consolidates project navigation and aligns with the current CLI-only scope. Any web UI, batch engine, or gallery features referenced elsewhere are roadmap items and explicitly marked as future work to avoid confusion.

Quick Navigation
- README (root): Project overview, quick start, features
- SETUP: Installation and configuration
- USAGE: CLI commands and examples
- API_REFERENCE: Python client and high-level generator API
- SECURITY: Security policy and reporting
- CONTRIBUTING: Contributing guidelines
- CHANGELOG: Notable changes

Scope Clarification
Current scope is a Python CLI and client library:
- Implemented: CLI commands (generate, styles, config, version), async API client with retries, configuration via environment/.env, style constants, and basic single visual generation.
- Not implemented yet (roadmap): Interactive TUI, batch CSV engine, local gallery/SQLite, Streamlit web UI, analytics dashboards, similarity search. These are retained in PRD as future phases.

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