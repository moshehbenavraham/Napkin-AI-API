# Usage Guide

Overview
This guide documents the CLI that is implemented today. Any commands not listed here are not available. Some features referenced in PRD (interactive TUI, batch engine, gallery, web UI) are roadmap items and not yet part of the CLI.

CLI Basics

Basic Generation
```bash
# Simple generation
napkin generate "Your text content"

# With options
napkin generate "Machine Learning" \
  --style vibrant-strokes \
  --format png \
  --width 1200

# Multiple variations (1-4)
napkin generate "Data Pipeline" --variations 4

# With context
napkin generate "Neural Networks" \
  --context-before "Introduction to" \
  --context-after "for beginners"
```

Styles and Configuration
```bash
# List available styles
napkin styles --list

# Filter by category
napkin styles --category colorful

# Show current configuration
napkin config --show

# Validate configuration
napkin config --check
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
napkin generate "Architecture Overview"
```

Generate PNG with dimensions
```bash
napkin generate "Sequence Diagram" --format png --width 1920 --height 1080
```

Use a named style
```bash
napkin generate "Data Pipeline" --style elegant-outline
```

Save to custom directory
```bash
napkin generate "System Design" --output ./data/visuals
```

Troubleshooting
- Authentication failed: Ensure NAPKIN_API_TOKEN is set in your environment or .env file.
- Invalid format: Only svg or png are supported.
- PNG dimensions rejected: width/height are only allowed when --format png is used.
- Rate limit exceeded: Wait for Retry-After seconds and try again.

FAQ
Q: Where are files saved?
A: By default under the configured storage path (see NAPKIN_STORAGE_PATH). You can override with --output.

Q: How do I find available style names?
A: Use napkin styles --list or consult the styles table in docs/NAPKIN_AI_API.md. Named styles are mapped to API IDs internally.

Q: Can I pass a custom style ID?
A: Yes, pass the raw style ID via --style; it will be used as-is.

Q: How many variations can I request?
A: 1 to 4. The CLI validates the range.

Accessibility and i18n
- Language is provided in BCP 47 format (e.g., en-US).
- Ensure terminal supports UTF-8 for non-Latin scripts.

Next Steps
- See API_REFERENCE.md for Python client usage.
- Review SETUP.md to configure environment variables.