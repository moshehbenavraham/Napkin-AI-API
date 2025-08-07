# Napkin AI Web Interface Features

## Overview

The Streamlit-based web interface provides an intuitive way to generate visuals using the Napkin AI API without writing code. Version 0.3.0 introduces comprehensive API feature support including multi-language generation, visual regeneration, and advanced customization options.

## Core Features

### 🎨 Visual Generation

- **Real-time generation** with progress indicators
- **Multiple variations** (1-4) in a single request
- **Instant preview** of generated visuals
- **Direct download** buttons for each visual
- **Context-aware generation** with before/after text fields
- **Visual regeneration** using existing visual IDs
- **Visual type search** for specific diagram types

### 🌍 Multi-Language Support

- **30+ languages** with proper BCP 47 tags
- **Regional variants** (e.g., en-US, en-GB, es-ES, es-MX)
- **RTL language support** (Arabic, Hebrew)
- **Asian languages** (Chinese, Japanese, Korean)
- **European languages** (French, German, Italian, Spanish, etc.)

### 🎯 Style Selection

- **15+ visual styles** organized by category
- **Category filtering** for easier navigation
- **Style descriptions** and use cases
- **Interactive style browser** with detailed information
- **Proper API ID mapping** for all styles

### 📐 Format Options

- **SVG support** for scalable vector graphics
- **PNG support** with custom dimensions
- **Resolution calculator** showing megapixels
- **16MP safety cap** to prevent excessive sizes
- **Responsive preview** that adapts to content
- **Transparent backgrounds** option
- **Color inversion** for alternate schemes

### 🔄 Visual Regeneration

- **Update existing visuals** with new content
- **Search visual types** (mindmap, flowchart, timeline, etc.)
- **15+ visual type queries** supported
- **Smart validation** for regeneration parameters

### 🎯 Advanced Options

- **Transparency control** for backgrounds
- **Color inversion** toggle
- **Context fields** for enhanced meaning
- **Language selection** dropdown
- **Collapsible panels** for better organization

### 🔐 Authentication

- **Environment variable support** for API tokens
- **Manual token input** via secure password field
- **Bearer token authentication** for file downloads
- **Secure token handling** without exposure

## Technical Implementation

### Architecture

```
┌─────────────────┐
│   Streamlit UI  │
├─────────────────┤
│  Worker Thread  │ <- Isolated async execution
├─────────────────┤
│ Visual Generator│ <- Core generation logic
├─────────────────┤
│   API Client    │ <- Authenticated requests
└─────────────────┘
```

### Key Components

#### Thread-Safe Execution

```python
def run_generation_in_worker():
    # Runs in dedicated thread with own event loop
    # Prevents blocking Streamlit's runtime
    # Handles async/await properly
```

#### File Download Handling

The app handles two types of file URLs:

1. **Direct CDN URLs** - Public URLs that don't need authentication
2. **API Endpoints** - Require Bearer token authentication

```python
# Automatic detection and handling
if '/v1/visual/' in url and '/file/' in url:
    # API endpoint - needs auth
    content = await client.download_file(request_id, file_id)
else:
    # CDN URL - direct fetch
    content = fetch_bytes(url)
```

#### Error Recovery

- Graceful fallback for failed downloads
- Individual file error handling
- Clear error messages for users
- Detailed error logs in expander

## User Interface

### Sidebar Configuration

- **API Token** - Secure input with environment variable support
- **Style Selection** - Category-based filtering with 15+ styles
- **Format Options** - SVG/PNG with dimension controls
- **Variations** - Slider for multiple outputs (1-4)
- **Advanced Options** - Transparency, color inversion
- **Language Selection** - 30+ language dropdown
- **Regeneration Options** - Visual ID or type search

### Main Content Area

- **Context Fields** - Optional before/after text (expandable)
- **Text Input** - Large text area with examples
- **Action Buttons** - Generate and Clear
- **Results Display** - Grid layout for multiple visuals
- **Download Options** - Individual download buttons
- **Generation Details** - Full parameter display

### Footer Information

- **Version display** - Current version and git commit
- **Update timestamp** - Last deployment time
- **Resource links** - Documentation and support

## Version History

### v0.3.0 (2025-08-07)
- Added multi-language support (30+ languages)
- Implemented context options (before/after fields)
- Added transparency and color inversion controls
- Implemented visual regeneration with ID
- Added visual type search functionality
- Enhanced UI with collapsible sections
- Improved generation details display
- Updated all API parameters support

### v0.2.2 (2025-08-07)
- Fixed Pydantic model field access issues
- Resolved StatusResponse attribute errors

### v0.2.1 (2025-08-07)
- Fixed 403 Forbidden errors with authenticated downloads
- Improved error handling and recovery
- Added version info in footer
- Code quality improvements

### v0.2.0 (2025-08-07)
- Initial web interface release
- Full API integration
- Support for all styles and formats

## Performance Optimizations

### Efficient File Handling

- **Pre-download in worker** - Files downloaded once in background
- **Byte streaming** - Direct memory handling without temp files
- **Parallel processing** - Multiple files handled concurrently

### Resource Management

- **Lazy loading** - Components load as needed
- **Memory cleanup** - Proper resource disposal
- **Thread pooling** - Controlled concurrent execution

## Browser Compatibility

- **Chrome/Edge** - Full support
- **Firefox** - Full support
- **Safari** - Full support
- **Mobile browsers** - Responsive design

## Accessibility

- **Keyboard navigation** - Full keyboard support
- **Screen reader compatible** - Proper ARIA labels
- **High contrast** - Works with system themes
- **Responsive design** - Adapts to screen sizes

## Security Features

### Token Protection

- Never displayed in UI
- Transmitted via HTTPS only
- Stored in session state
- No client-side storage

### Input Validation

- Content length limits
- Style validation
- Format verification
- Dimension constraints

### Error Handling

- No sensitive data in errors
- Sanitized file names
- Safe URL parsing
- Controlled external requests

## Future Enhancements

### Planned Features

- **Batch processing** - Multiple prompts at once
- **History tracking** - Previous generations
- **Style preview** - Sample images
- **Export options** - PDF, ZIP archives
- **Sharing** - Public links for visuals

### Under Consideration

- User accounts
- Team collaboration
- Custom style creation
- API usage analytics
- Webhook notifications

## Known Limitations

1. **File size** - Large PNG files may be slow
2. **Concurrent users** - Shared Streamlit instance limits
3. **Rate limiting** - 60 requests/minute API limit
4. **Session state** - Lost on page refresh
5. **Download method** - Browser-dependent behavior

## Tips for Users

### Best Practices

1. **Be descriptive** - More detail yields better visuals
2. **Try variations** - Generate multiple for options
3. **Use appropriate formats** - SVG for logos, PNG for complex
4. **Experiment with styles** - Each has unique characteristics

### Troubleshooting

1. **No visuals appear** - Check API token
2. **Slow generation** - Try fewer variations
3. **Download fails** - Try different browser
4. **Style not working** - Verify category selection

## Supported Languages

### European Languages
- English (en, en-US, en-GB)
- Spanish (es, es-ES, es-MX)
- French (fr, fr-FR)
- German (de, de-DE)
- Italian (it, it-IT)
- Portuguese (pt, pt-BR)
- Dutch (nl, nl-NL)
- Polish (pl, pl-PL)
- Swedish (sv, sv-SE)
- Danish (da, da-DK)
- Norwegian (no, no-NO)
- Finnish (fi, fi-FI)
- Turkish (tr, tr-TR)
- Russian (ru, ru-RU)

### Asian Languages
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- Japanese (ja, ja-JP)
- Korean (ko, ko-KR)
- Hindi (hi)

### Middle Eastern Languages
- Arabic (ar)

## Visual Type Queries

The following visual types can be searched for:
- mindmap
- flowchart
- timeline
- diagram
- infographic
- chart
- graph
- process
- hierarchy
- network
- venn
- matrix
- cycle
- pyramid
- funnel

---

Last updated: 2025-08-07