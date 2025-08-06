# Napkin AI API Playground

Executive Overview
Napkin AI API Playground is a Python CLI and client library that turns text into professional visuals via the Napkin API. It provides a robust async client, a friendly CLI, strong validation, and production-ready defaults to generate SVG/PNG artifacts quickly and reliably.

Key Capabilities
- Single Visual Generation via CLI
- 15+ Curated Styles with IDs and categories
- SVG/PNG Outputs with optional PNG dimensions
- Async Client with retries and rate-limit awareness
- Clear Errors and progress messaging
- Environment-based Configuration with .env support

Installation
```bash
# Local development
poetry install

# Or with pip
pip install -r requirements.txt
```

Configuration
Request a token at api@napkin.ai. Then:
```bash
cp .env.example .env
# edit .env
#   NAPKIN_API_TOKEN=your_token_here
```
Windows (CMD):
```bat
set NAPKIN_API_TOKEN=your_token_here
```
Windows (PowerShell):
```powershell
$env:NAPKIN_API_TOKEN="your_token_here"
```

Quick Start
```bash
# Generate a visual
napkin generate "Machine Learning Pipeline"

# With options
napkin generate "Data Flow Diagram" --style sketch-notes --format png --width 1920 --height 1080

# Multiple variations
napkin generate "Workflow Process" --variations 3

# Output directory
napkin generate "System Design" --output ./data/visuals
```

CLI Commands
```bash
napkin generate "Your content" [OPTIONS]
napkin styles --list
napkin styles --category colorful
napkin config --show
napkin config --check
napkin version
```

Generate Options
- --style, -s: Visual style name or ID
- --format, -f: svg or png
- --output, -o: Output directory
- --variations, -n: 1-4
- --language, -l: BCP 47 code (e.g., en-US)
- --context-before / --context-after
- --width, -w / --height, -h (PNG only)
- --transparent / --inverted
- --debug

Architecture Overview
- CLI (Typer + Rich): Commands, UX, progress bars
- API Client (httpx + tenacity): Auth, requests, retries, rate-limit parsing
- Models (Pydantic v2): Request/response validation
- Core (Generator): Orchestrates request, polling, downloads
- Constants/Config: Style catalog, endpoints, environment-backed settings

Project Structure
```
Napkin-AI-API/
├── src/
│   ├── api/          # API client and models
│   ├── cli/          # CLI commands and display
│   ├── core/         # Core generation logic
│   ├── storage/      # Reserved for future persistence
│   └── utils/        # Config and helpers
├── tests/            # Test suite
├── docs/             # Documentation
├── data/             # Generated visuals
└── main.py
```

Security
- Tokens masked and never logged
- .env is gitignored
- Validations guard against misuse

License
MIT (or your chosen license). See docs/SECURITY.md for security practices.

Further Reading
- docs/SETUP.md
- docs/USAGE.md
- docs/API_REFERENCE.md
- docs/README.md (docs hub)