# Setup Guide

Overview
This guide covers installation and configuration for the current CLI and client library. Any web UI or gallery/database configuration alluded to elsewhere is future scope and intentionally omitted here.

Prerequisites
- Python 3.9 or higher
- pip or Poetry
- Napkin API token

Install

Local development (recommended)
```bash
poetry install
```

Pip
```bash
pip install -r requirements.txt
```

Configuration

API token via environment
```bash
# macOS/Linux (bash/zsh)
export NAPKIN_API_TOKEN="your_token_here"

# Windows (Command Prompt)
set NAPKIN_API_TOKEN=your_token_here

# Windows (PowerShell)
$env:NAPKIN_API_TOKEN="your_token_here"

# Persist for user (requires new terminal)
setx NAPKIN_API_TOKEN "your_token_here"
```

Using .env (gitignored)
```bash
cp ../.env.example ../.env   # if running from docs/
# or
cp .env.example .env         # from project root
# then edit .env to set NAPKIN_API_TOKEN
```

Supported environment variables
- Required:
  - NAPKIN_API_TOKEN
- Common optional:
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

Verification
```bash
# Show version/help
napkin version
napkin --help

# Validate configuration
napkin config --check

# Generate a test visual
napkin generate "Hello Napkin"
```

Troubleshooting
- Command not found (Windows): open a new terminal after setting PATH or use python -m to invoke the CLI.
- Invalid token: ensure NAPKIN_API_TOKEN is exported or set in .env.
- Permissions: ensure the storage path is writable; defaults to ./data/visuals.
- Networking: verify outbound HTTPS to api.napkin.ai:443 is allowed.

Assumptions
- The project is used as a CLI from source while in development. Packaging to PyPI is out of scope at present. Remove this note when packaging is published and verified.