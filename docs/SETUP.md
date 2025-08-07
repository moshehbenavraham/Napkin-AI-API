# Setup Guide

Overview
This guide covers installation and configuration for the current CLI and client library. Any web UI or gallery/database configuration alluded to elsewhere is future scope and intentionally omitted here.

Prerequisites
- Python 3.10 or higher
- pip or Poetry
- Napkin API token

Install

Local development with Poetry (recommended)
```bash
# Install dependencies and the napkin CLI command
poetry install

# The napkin command is now available via poetry run
poetry run napkin --help
```

Pip (alternative)
```bash
pip install -r requirements.txt
# Then use python main.py instead of napkin command
python main.py --help
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

Running the CLI

With Poetry 2.0+, you have several options:

```bash
# Option 1: Use poetry run (recommended)
poetry run napkin --help
poetry run napkin generate "Your content"

# Option 2: Activate the virtual environment
source .venv/bin/activate  # Linux/Mac/WSL
# or
source $(poetry env info --path)/bin/activate
# Now use napkin directly
napkin --help

# Option 3: Use the full path
.venv/bin/napkin --help

# Option 4: Use Python directly
python main.py --help
```

Verification
```bash
# Show version/help
poetry run napkin version
poetry run napkin --help

# Validate configuration
poetry run napkin config --check

# Generate a test visual
poetry run napkin generate "Hello Napkin"
```

Troubleshooting
- Command not found: Use `poetry run napkin` or activate the virtual environment first with `source .venv/bin/activate`
- Poetry shell not working: Poetry 2.0 removed the shell command. Use `source .venv/bin/activate` or `poetry run` instead
- Invalid token: Ensure NAPKIN_API_TOKEN is exported or set in .env file
- Permissions: Ensure the storage path is writable; defaults to ./data/visuals
- Networking: Verify outbound HTTPS to api.napkin.ai:443 is allowed
- Windows issues: Open a new terminal after setting PATH or use `python main.py` to invoke the CLI

Assumptions
- The project is used as a CLI from source while in development. Packaging to PyPI is out of scope at present. Remove this note when packaging is published and verified.