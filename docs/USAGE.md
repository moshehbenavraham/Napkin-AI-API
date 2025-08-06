# Usage Guide

Overview
This guide documents the CLI that is implemented today. Any commands not listed here are not available. Some features referenced in PRD (interactive TUI, batch engine, gallery, web UI) are roadmap items and not yet part of the CLI.

Note: All examples below assume you're using Poetry. If you've activated the virtual environment with `source .venv/bin/activate`, you can omit `poetry run` from the commands.

Quick Reference

Available Commands:
- `napkin generate` - Create visuals from text
- `napkin styles` - Browse and list visual styles  
- `napkin config` - Manage configuration settings
- `napkin version` - Show version information

CLI Basics

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

# With debug output
poetry run napkin generate "API Architecture" --debug
```

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
Q: Where are files saved?
A: By default under the configured storage path (see NAPKIN_STORAGE_PATH, defaults to ./data/visuals). You can override with --output.

Q: How do I find available style names?
A: Use `poetry run napkin styles --list` or consult the styles table in docs/NAPKIN_AI_API.md. Named styles are mapped to API IDs internally.

Q: Can I pass a custom style ID?
A: Yes, pass the raw style ID via --style; it will be used as-is.

Q: How many variations can I request?
A: 1 to 4. The CLI validates the range.

Q: Why use `poetry run` before every command?
A: Poetry 2.0 requires this to run commands in the virtual environment. Alternatively, activate the environment first with `source .venv/bin/activate`.

Q: Can I use the CLI without Poetry?
A: Yes, use `python main.py` instead of `napkin` after installing dependencies with pip.

Accessibility and i18n
- Language is provided in BCP 47 format (e.g., en-US).
- Ensure terminal supports UTF-8 for non-Latin scripts.

Next Steps
- See API_REFERENCE.md for Python client usage.
- Review SETUP.md to configure environment variables.