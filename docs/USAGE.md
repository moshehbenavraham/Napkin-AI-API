# Usage Guide

Overview
This guide documents both the Web Interface (Streamlit) and CLI that are implemented today. Any commands not listed here are not available. Some features referenced in PRD (interactive TUI, batch engine, gallery) are roadmap items and not yet implemented.

Note: All examples below assume you're using Poetry. If you've activated the virtual environment with `source .venv/bin/activate`, you can omit `poetry run` from the commands.

Quick Reference

Available Interfaces:
- **Web Interface** - Interactive Streamlit application for visual generation
- **CLI** - Command-line interface with the following commands:
  - `napkin generate` - Create visuals from text
  - `napkin styles` - Browse and list visual styles  
  - `napkin config` - Manage configuration settings
  - `napkin version` - Show version information

## Web Interface (Streamlit)

### Starting the Web Interface
```bash
# Set your API token (get one from https://napkin.ai)
export NAPKIN_API_TOKEN="your_actual_token_here"

# Launch the web application
poetry run streamlit run streamlit_app.py

# The app will open in your browser at http://localhost:8501
```

### Using the Web Interface

1. **API Token Setup**
   - Set via environment variable (recommended): `export NAPKIN_API_TOKEN="your_token"`
   - Or enter directly in the sidebar password field

2. **Generate Visuals**
   - Enter your content in the main text area
   - Select a style category and specific style from the sidebar
   - Choose output format (SVG or PNG)
   - For PNG, set custom dimensions (100-4096 pixels)
   - Adjust number of variations (1-4)
   - Click "🚀 Generate Visual"

3. **Download Results**
   - View generated visuals directly in the browser
   - Click download buttons to save locally
   - Files are named with style and variation number

### Web Interface Features
- **Interactive Style Browser**: Browse 15+ styles organized by category
- **Real-time Generation**: See progress indicators during generation
- **Multiple Variations**: Generate up to 4 variations at once
- **Custom Dimensions**: Set PNG width/height with megapixel display
- **Direct Downloads**: One-click download for each generated visual
- **Multi-Language Support**: Generate visuals in 30+ languages
- **Context Options**: Add before/after text for better context
- **Advanced Options**: Transparency, color inversion controls
- **Visual Regeneration**: Update existing visuals or search types
- **Error Handling**: Clear error messages with troubleshooting details

### Troubleshooting Web Interface

**"StatusResponse" object has no field "downloaded_files" error**
- Fixed in v0.2.2 - update to latest version
- Run `git pull` to get the latest fixes

**Port already in use error**
```bash
# Try a different port
poetry run streamlit run streamlit_app.py --server.port 8502
```

**API token not working**
- Ensure token is correctly set: `echo $NAPKIN_API_TOKEN`
- Try entering token directly in the sidebar
- Verify token at https://napkin.ai

## CLI Basics

Basic Generation
```bash
# Simple generation
poetry run napkin generate "Your text content"

# With options
poetry run napkin generate "Machine Learning" \
  --style vibrant-strokes \
  --format png \
  --width 1200

# Multiple variations (1-4)
poetry run napkin generate "Data Pipeline" --variations 4

# With context
poetry run napkin generate "Neural Networks" \
  --context-before "Introduction to" \
  --context-after "for beginners"

# With transparency and color options
poetry run napkin generate "Workflow Diagram" \
  --transparent \
  --inverted-color

# With language specification
poetry run napkin generate "Architecture de système" \
  --language fr-FR

# Regenerate existing visual
poetry run napkin generate "Updated Content" \
  --visual-id "5UCQJLAV5S6NXEWS2PBJF54UYPW5NZ4G"

# Search for specific visual type
poetry run napkin generate "Project Roadmap" \
  --visual-query "timeline"

# With debug output
poetry run napkin generate "API Architecture" --debug
```

### New CLI Parameters (v0.3.0)

| Parameter | Description | Example |
|-----------|-------------|------|
| `--transparent` | Enable transparent background | `--transparent` |
| `--inverted-color` | Invert color scheme | `--inverted-color` |
| `--language` | Specify language (BCP 47) | `--language ja-JP` |
| `--visual-id` | Regenerate existing visual | `--visual-id ABC123` |
| `--visual-query` | Search visual type | `--visual-query mindmap` |

Commands Overview

1. Generate Command
```bash
# See all generation options
poetry run napkin generate --help

# Basic usage
poetry run napkin generate "Your content"
```

2. Styles Command
```bash
# List all available styles (15+ styles)
poetry run napkin styles --list

# Filter by category (colorful, casual, hand_drawn, formal, monochrome)
poetry run napkin styles --category colorful
```

3. Configuration Command
```bash
# Show current configuration
poetry run napkin config --show

# Validate configuration (checks API token)
poetry run napkin config --check
```

4. Version Command
```bash
# Show version and API information
poetry run napkin version
```

Notes
- Style argument maps to API field style_id. Known slugs resolve to IDs using the internal catalog; unknown values are treated as custom IDs.
- Variations maps to number_of_visuals.
- Context flags map to context_before/context_after.
- Width/height apply to PNG only and are validated.

Parameter Mapping Reference
```
--style                -> style_id
--variations           -> number_of_visuals
--context-before       -> context_before
--context-after        -> context_after
--width (PNG only)     -> width
--height (PNG only)    -> height
--transparent          -> transparent_background
--inverted             -> inverted_color
--language             -> language (BCP 47)
```

Examples

Generate SVG (default)
```bash
poetry run napkin generate "Architecture Overview"
```

Generate PNG with dimensions
```bash
poetry run napkin generate "Sequence Diagram" --format png --width 1920 --height 1080
```

Use a named style
```bash
poetry run napkin generate "Data Pipeline" --style elegant-outline
```

Save to custom directory
```bash
poetry run napkin generate "System Design" --output ./my-visuals
```

Generate with transparency and inverted colors
```bash
poetry run napkin generate "Network Topology" --transparent --inverted
```

Generate multiple variations with custom language
```bash
poetry run napkin generate "Database Schema" --variations 3 --language es-ES
```

Troubleshooting
- Authentication failed: Ensure NAPKIN_API_TOKEN is set in your environment or .env file.
- Invalid format: Only svg or png are supported.
- PNG dimensions rejected: width/height are only allowed when --format png is used.
- Rate limit exceeded: Wait for Retry-After seconds and try again.

FAQ

**Q: Which interface should I use - Web or CLI?**
A: Use the Web Interface for interactive exploration and visual feedback. Use the CLI for automation, scripting, or integration into workflows.

**Q: Where are files saved?**
A: CLI saves to the configured storage path (NAPKIN_STORAGE_PATH, defaults to ./data/visuals). Web Interface provides direct downloads to your browser's download folder.

**Q: How do I find available style names?**
A: Web Interface has an interactive style browser. For CLI, use `poetry run napkin styles --list` or consult the styles table in docs/NAPKIN_AI_API.md.

**Q: Can I pass a custom style ID?**
A: Yes in CLI, pass the raw style ID via --style. The Web Interface currently only supports built-in styles.

**Q: How many variations can I request?**
A: 1 to 4 in both interfaces.

**Q: Why use `poetry run` before every command?**
A: Poetry 2.0 requires this to run commands in the virtual environment. Alternatively, activate the environment first with `source .venv/bin/activate`.

**Q: Can I use without Poetry?**
A: Yes, use `python main.py` for CLI or `python -m streamlit run streamlit_app.py` for Web after installing dependencies with pip.

**Q: Can I run both Web and CLI at the same time?**
A: Yes, they are independent interfaces. The Web Interface runs on a local server while CLI runs in your terminal.

Accessibility and i18n
- Language is provided in BCP 47 format (e.g., en-US).
- Ensure terminal supports UTF-8 for non-Latin scripts.

Next Steps
- See API_REFERENCE.md for Python client usage.
- Review SETUP.md to configure environment variables.