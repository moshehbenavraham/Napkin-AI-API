# Napkin AI Playground Documentation

## Quick Navigation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview, features, quick start |
| [SETUP.md](SETUP.md) | Installation, dependencies, configuration |
| [USAGE.md](USAGE.md) | CLI commands, examples, workflows |
| [API_REFERENCE.md](API_REFERENCE.md) | Python client library documentation |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development setup, testing, guidelines |

---

# Napkin AI Playground

Transform text into beautiful visuals using the Napkin AI API through an intuitive Python CLI and web interface.

## Features

- 🎨 **15+ Visual Styles** - From vibrant to minimal, plus custom styles
- ⚡ **Intelligent Batch Processing** - Parallel generation with smart rate limiting
- 🗂️ **Advanced Gallery** - Full-text search, tagging, and organization
- 📊 **Comprehensive Analytics** - Usage tracking, performance insights, and cost estimation
- 🔄 **Smart Retry Logic** - Exponential backoff with rate limit detection
- 🌐 **Modern Web UI** - Responsive Streamlit interface with real-time updates
- 🤖 **AI-Powered Features** - Visual recommendations and content optimization (in active development)
- 🔍 **Visual Search** - Find visuals by type, content, or similarity (in active development)

## Quick Start

```bash
# Install
pip install napkin-playground

# Configure API token
# Unix/macOS (bash/zsh)
export NAPKIN_API_TOKEN="your_token_here"
# Windows (CMD - current session)
set NAPKIN_API_TOKEN=your_token_here
# Windows (PowerShell - current session)
$env:NAPKIN_API_TOKEN="your_token_here"
# Windows (persist for user; requires a new terminal)
setx NAPKIN_API_TOKEN "your_token_here"

# Generate your first visual
napkin generate "Machine Learning Pipeline"

# Launch interactive mode
napkin interactive

# Explore visual styles
napkin styles explore

# Start web interface
napkin web

# If the 'napkin' command is not found, try a new terminal
# or invoke via Python:
#   python -m napkin_playground.cli --help
```

## Project Structure

```
napkin-playground/
├── src/
│   ├── cli/          # Command-line interface
│   ├── api/          # API client and models
│   ├── core/         # Business logic
│   ├── storage/      # Database and files
│   └── web/          # Streamlit app
├── docs/             # Documentation
├── tests/            # Test suite
└── examples/         # Usage examples
```

## Requirements

- Python 3.9+
- Napkin API token (request at api@napkin.ai)
- 1GB free disk space for visual storage

## License

MIT License - See LICENSE file for details