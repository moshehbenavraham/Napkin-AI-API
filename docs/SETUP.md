# Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip or Poetry package manager
- Napkin API token

## Installation

### Option 1: pip (Quick Start)

```bash
pip install napkin-playground
```

### Option 2: Poetry (Recommended)

```bash
git clone https://github.com/yourusername/napkin-playground.git
cd napkin-playground
poetry install
```

### Option 3: Development Setup

```bash
git clone https://github.com/yourusername/napkin-playground.git
cd napkin-playground
pip install -e ".[dev]"
```

## Configuration

### 1. API Token

```bash
# Environment variable (recommended)

# Unix/macOS (bash/zsh)
export NAPKIN_API_TOKEN="your_token_here"

# Windows (Command Prompt - current session)
set NAPKIN_API_TOKEN=your_token_here

# Windows (PowerShell - current session)
$env:NAPKIN_API_TOKEN="your_token_here"

# Windows (persist for user; requires new terminal)
setx NAPKIN_API_TOKEN "your_token_here"

# Or create .env file
echo "NAPKIN_API_TOKEN=your_token_here" > .env
```

### 2. Configuration File

Create the config file in your home directory:

- Unix/macOS: `~/.napkin/config.yaml`
- Windows: `%USERPROFILE%\.napkin\config.yaml`

Environment variables:
- The application reads configuration from environment variables with optional `.env` support for local development.
- Preferred key name for OpenAI access: `OPENAI_API_KEY` (legacy fallback `API_KEY` is still read but deprecated).
- To enable automatic loading from `.env`, install python-dotenv:
  ```bash
  pip install python-dotenv
  ```
- Example `.env` (project root, gitignored by default):
  ```
  OPENAI_API_KEY=sk-...
  ```

```yaml
api:
  token: ${NAPKIN_API_TOKEN}
  base_url: https://api.napkin.ai
  timeout: 30
  max_retries: 3

defaults:
  style: vibrant-strokes
  format: svg
  language: en-US
  number_of_visuals: 1

storage:
  path: ~/.napkin/visuals
  database: ~/.napkin/napkin.db
  cleanup_days: 30

cli:
  rich_output: true
  progress_bars: true
  
web:
  enabled: true
  port: 8501
  auto_open: true
```

### 3. Environment Variables

All configuration options can be set via environment:

```bash
# Unix/macOS
export NAPKIN_API_TOKEN=xxx
export NAPKIN_DEFAULT_STYLE=elegant-outline
export NAPKIN_DEFAULT_FORMAT=png
export NAPKIN_STORAGE_PATH=/custom/path
export NAPKIN_DATABASE_PATH=/custom/db.sqlite
export NAPKIN_WEB_PORT=8080
export NAPKIN_LOG_LEVEL=INFO
export NAPKIN_CACHE_ENABLED=true
export NAPKIN_MAX_RETRIES=3
export NAPKIN_TIMEOUT_SECONDS=30

# Windows (CMD - current session)
set NAPKIN_API_TOKEN=xxx
set NAPKIN_DEFAULT_STYLE=elegant-outline
set NAPKIN_DEFAULT_FORMAT=png
set NAPKIN_STORAGE_PATH=C:\custom\path
set NAPKIN_DATABASE_PATH=C:\custom\db.sqlite
set NAPKIN_WEB_PORT=8080
set NAPKIN_LOG_LEVEL=INFO
set NAPKIN_CACHE_ENABLED=true
set NAPKIN_MAX_RETRIES=3
set NAPKIN_TIMEOUT_SECONDS=30

# Windows (PowerShell - current session)
$env:NAPKIN_API_TOKEN="xxx"
$env:NAPKIN_DEFAULT_STYLE="elegant-outline"
$env:NAPKIN_DEFAULT_FORMAT="png"
$env:NAPKIN_STORAGE_PATH="C:\custom\path"
$env:NAPKIN_DATABASE_PATH="C:\custom\db.sqlite"
$env:NAPKIN_WEB_PORT="8080"
$env:NAPKIN_LOG_LEVEL="INFO"
$env:NAPKIN_CACHE_ENABLED="true"
$env:NAPKIN_MAX_RETRIES="3"
$env:NAPKIN_TIMEOUT_SECONDS="30"
```

## Verify Installation

```bash
# Check version
napkin --version

# Test API connection
napkin test-connection

# Generate test visual
napkin generate "Hello Napkin" --dry-run

# Note (Windows):
# If the 'napkin' command is not found after installation,
# try starting a new terminal or invoke via Python:
#   python -m napkin_playground.cli --help
```

## Troubleshooting

### Common Issues

1. **API Token Invalid**
   ```bash
   napkin config validate
   ```

2. **Permission Errors**
   ```bash
   # Fix storage permissions (Unix/macOS)
   chmod 755 ~/.napkin
   # Windows: ensure the user account has read/write permissions on %USERPROFILE%\.napkin
   ```

3. **Missing Dependencies**
   ```bash
   pip install --upgrade napkin-playground
   
   # If using Poetry:
   poetry update napkin-playground
   ```

## Next Steps

- Read [USAGE.md](USAGE.md) for command examples
- Check [API_REFERENCE.md](API_REFERENCE.md) for Python usage
- See [examples/](../examples/) for sample scripts