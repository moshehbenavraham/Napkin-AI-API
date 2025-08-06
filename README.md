# Napkin AI API Playground

A Python client for the Napkin AI Visual Generation API that transforms text into professional visual content (diagrams, illustrations, graphics).

## 🚀 Quick Start

### Installation

```bash
# Install dependencies with Poetry
poetry install

# Or if you prefer pip
pip install -r requirements.txt
```

### Configuration

1. **Get your API token**: Request one from api@napkin.ai
2. **Set up environment**:
   ```bash
   # Copy the example configuration
   cp .env.example .env
   
   # Edit .env and add your API token
   NAPKIN_API_TOKEN=your_token_here
   ```

### Basic Usage

```bash
# Generate a visual from text
napkin generate "Machine Learning Pipeline"

# Use a specific style
napkin generate "Data Flow Diagram" --style sketch-notes

# Generate PNG with custom dimensions
napkin generate "Architecture" --format png --width 1920 --height 1080

# Generate multiple variations
napkin generate "Workflow Process" --variations 3

# Save to specific directory
napkin generate "System Design" --output ./output
```

## 📋 Features

### Phase 1 (Completed) ✅
- **Single Visual Generation**: Generate visuals from text via CLI
- **15+ Built-in Styles**: Choose from vibrant, formal, hand-drawn, and more
- **Multiple Formats**: SVG (scalable) and PNG (with custom dimensions)
- **Async Processing**: Efficient API calls with retry logic
- **Rich CLI Interface**: Beautiful terminal output with progress indicators
- **Configuration Management**: Environment-based settings with validation
- **Error Handling**: User-friendly error messages and rate limit management

### Available Commands

```bash
# Generate visual from text
napkin generate "Your content" [OPTIONS]

# List available styles
napkin styles --list
napkin styles --category colorful

# Check configuration
napkin config --show
napkin config --check

# Show version
napkin version
```

### Command Options

#### `generate` command:
- `--style, -s`: Visual style name or ID
- `--format, -f`: Output format (svg/png)
- `--output, -o`: Output directory
- `--variations, -n`: Number of variations (1-4)
- `--language, -l`: Language code (e.g., en-US)
- `--context-before`: Context before main content
- `--context-after`: Context after main content
- `--width, -w`: Width in pixels (PNG only)
- `--height, -h`: Height in pixels (PNG only)
- `--transparent`: Enable transparent background
- `--inverted`: Invert colors
- `--debug`: Enable debug logging

## 🎨 Available Styles

### Colorful Styles
- `vibrant-strokes`: Vivid lines for bold notes
- `glowful-breeze`: Cheerful colors for laid-back planning
- `bold-canvas`: Lively shapes for dynamic content
- `radiant-blocks`: Bright solid colors for tasks
- `pragmatic-shades`: Blended hues for bold ideas

### Casual Styles
- `carefree-mist`: Calm tones for playful tasks
- `lively-layers`: Soft colors for bright ideas

### Hand-drawn Styles
- `artistic-flair`: Hand-drawn color for creative thinking
- `sketch-notes`: Free-flowing hand-drawn style

### Formal Styles
- `elegant-outline`: Refined black outline for clarity
- `subtle-accent`: Light color touch for documents
- `monochrome-pro`: Single-color focused presentations
- `corporate-clean`: Professional flat business diagrams

### Monochrome Styles
- `minimal-contrast`: Clean monochrome for focused work
- `silver-beam`: Grayscale with striking focus

## 🔧 Configuration

All settings can be configured via environment variables or `.env` file:

```bash
# Required
NAPKIN_API_TOKEN=your_token_here

# API Settings (with defaults)
NAPKIN_API_BASE_URL=https://api.napkin.ai
NAPKIN_API_VERSION=v1

# Generation Defaults
NAPKIN_DEFAULT_STYLE=vibrant-strokes
NAPKIN_DEFAULT_FORMAT=svg
NAPKIN_DEFAULT_LANGUAGE=en-US
NAPKIN_DEFAULT_VARIATIONS=1

# Storage
NAPKIN_STORAGE_PATH=./data/visuals
NAPKIN_DATABASE_PATH=./data/database/napkin.db

# Performance
NAPKIN_MAX_RETRIES=3
NAPKIN_TIMEOUT_SECONDS=30
NAPKIN_POLL_INTERVAL_SECONDS=2.0
```

## 📁 Project Structure

```
napkin-api-playground/
├── src/
│   ├── api/          # API client and models
│   ├── cli/          # CLI commands and display
│   ├── core/         # Core generation logic
│   ├── storage/      # Data persistence (future)
│   └── utils/        # Configuration and helpers
├── tests/            # Test suite
├── docs/             # Comprehensive documentation
├── data/             # Generated visuals storage
└── main.py           # Entry point
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_models.py
```

### Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## 📚 Documentation

See the `docs/` directory for comprehensive documentation:
- `PRD.md` - Product requirements and roadmap
- `API_REFERENCE.md` - Complete API documentation
- `SETUP.md` - Detailed setup instructions
- `USAGE.md` - Usage examples and guides
- `CONTRIBUTING.md` - Development guidelines

## 🔒 Security

- API tokens are never logged or displayed
- Secrets are masked in all output
- Environment variables are validated
- `.env` files are gitignored

## 📈 Future Phases

- **Phase 2**: Style explorer with preview
- **Phase 3**: Batch processing from CSV/JSON
- **Phase 4**: Visual gallery and management
- **Phase 5**: API monitoring and analytics
- **Phase 6**: Web UI (optional)
- **Phase 7**: Workflow automation
- **Phase 8**: Team collaboration features

## 🤝 Contributing

See `docs/CONTRIBUTING.md` for development guidelines.

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- Napkin AI for the amazing visual generation API
- Built with Python, Poetry, Typer, Rich, and httpx