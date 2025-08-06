# Usage Guide

## CLI Commands

### Basic Generation

```bash
# Simple generation
napkin generate "Your text content"

# With options
napkin generate "Machine Learning" \
  --style vibrant-strokes \
  --format png \
  --width 1200

# Multiple variations
napkin generate "Data Pipeline" --variations 4

# With context
napkin generate "Neural Networks" \
  --context-before "Introduction to" \
  --context-after "for beginners"
```

### Interactive Mode

```bash
# Launch interactive prompt
napkin interactive

# Quick style exploration
napkin styles explore

# Skip style selection
napkin interactive --style elegant-outline

# Auto-download results
napkin interactive --auto-download
```

### Batch Processing

```bash
# Process CSV file
napkin batch input.csv --output results/

# CSV format:
# content,style,format,variations
# "Text 1","vibrant-strokes","svg",2
# "Text 2","minimal-contrast","png",1

# Process with single style
napkin batch content.txt --style corporate-clean

# Parallel processing
napkin batch large.csv --parallel 5
```

### Gallery Management

```bash
# List all visuals
napkin gallery list

# Filter by style
napkin gallery list --style formal

# Search content
napkin gallery search "machine learning"

# Add tags
napkin gallery tag <visual-id> --add "presentation,slides"

# Export collection
napkin gallery export --tag slides --output export.zip

# Clean old files
napkin gallery clean --older-than 30d
```

### Style Explorer

```bash
# List all styles
napkin styles list

# Show style details
napkin styles show vibrant-strokes

# Preview with sample text
napkin styles preview "Sample Text"

# Compare styles
napkin styles compare vibrant-strokes elegant-outline
```

Notes:
- CLI style argument names map to API fields:
  - --style -> style_id (the CLI accepts known aliases like 'vibrant-strokes' and resolves to the corresponding style ID)
  - --variations -> number_of_visuals
  - --context-before/--context-after -> context_before/context_after

### Monitoring

```bash
# Show current usage
napkin monitor

# Usage history
napkin monitor history --days 7

# Export analytics
napkin monitor export --format csv

# Real-time monitoring
napkin monitor live

# Performance insights
napkin monitor performance
```

## Advanced Features

### Regeneration

```bash
# Regenerate with same style
napkin regenerate <request-id>

# Change content
napkin regenerate <request-id> --content "New text"

# Try different style
napkin regenerate <request-id> --style minimal-contrast
```

### Experimental/Planned Options

The following options are experimental or planned and may require a feature flag or a pre-release build. Availability can change.

```bash
# AI-powered visual recommendations (experimental)
napkin recommend --content "Technical Architecture"

# Visual similarity search (experimental)
napkin similar <visual-id>

# Social square format convenience flag (planned)
napkin generate "Content" --format png --width 1080 --square

# Scheduling batch generation (planned)
napkin batch social.csv --schedule daily
```

### Visual Search

```bash
# Search by type
napkin search mindmap --content "Project Plan"

# Multiple types
napkin search "flowchart,timeline" --content "Process"

# AI-powered visual recommendations
napkin recommend --content "Technical Architecture"

# Visual similarity search
napkin similar <visual-id>
```

### Configuration

```bash
# Show current config
napkin config show

# Set default style
napkin config set default.style elegant-outline

# Validate setup
napkin config validate

# Reset to defaults
napkin config reset
```

## Workflow Examples

### 1. Presentation Visuals

```bash
# Generate all slides
napkin batch presentation.csv --tag slides

# Review in gallery
napkin gallery list --tag slides

# Export for PowerPoint
napkin gallery export --tag slides --format png --width 1920
```

### 2. Documentation Graphics

```bash
# Generate from markdown headers
napkin generate --from-markdown docs.md

# Apply consistent style
napkin batch docs.txt --style corporate-clean

# Organize by chapter
napkin gallery organize --by-tag chapter
```

### 3. Social Media Content

```bash
# Generate variations
napkin generate "Quote" --variations 4 --style vibrant

# Optimize for platforms
napkin generate "Content" --format png --width 1080 --square

# Batch schedule
napkin batch social.csv --schedule daily
```

## Tips & Tricks

### Performance

```bash
# Use caching for repeated content
napkin generate "Text" --cache

# Batch similar requests
napkin batch --group-by style

# Limit concurrent requests
napkin batch large.csv --parallel 3
```

### Organization

```bash
# Auto-tag by date
napkin generate "Text" --auto-tag date

# Project folders
napkin generate "Text" --project "Q1-Campaign"

# Template system
napkin template create "weekly-report"
napkin generate --template weekly-report
```

### Debugging

```bash
# Verbose output
napkin generate "Text" -v

# Dry run
napkin generate "Text" --dry-run

# Debug API calls
napkin generate "Text" --debug
```

## Parameter Mapping Reference

CLI flags to API parameters:

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

## Keyboard Shortcuts

In interactive mode:

- `Ctrl+S` - Quick save
- `Ctrl+R` - Regenerate
- `Ctrl+G` - Open gallery
- `Ctrl+C` - Cancel/Exit
- `Tab` - Auto-complete
- `↑/↓` - Navigate history

## Output Formats

### File Naming

```
<timestamp>_<style>_<hash>.<format>
2024-01-15_143022_vibrant-strokes_a3f2d1.svg
```

### Directory Structure

```
~/.napkin/visuals/
├── 2024-01-15/
│   ├── morning-session/
│   └── afternoon-batch/
├── projects/
│   ├── marketing/
│   └── documentation/
└── exports/
```

## Next Steps

- Check [API_REFERENCE.md](API_REFERENCE.md) for Python library usage
- See [examples/](../examples/) for complete scripts
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to extend functionality