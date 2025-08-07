# Napkin AI API Project Guide

## Development

### Project Structure

```
napkin-api-playground/
├── streamlit_app.py        # Web interface
├── main.py                 # CLI entry point
├── src/
│   ├── api/               # API client & models
│   ├── cli/               # CLI commands
│   ├── core/              # Business logic
│   └── utils/             # Helpers & config
├── tests/                 # Test suite
├── scripts/               # Utilities
│   └── gh_monitor.py      # CI/CD monitoring
└── bin/
    └── gh-monitor         # GitHub Actions tool
```

### Setup for Development

```bash
# Install with dev dependencies
poetry install --with dev

# Run quality checks
ruff format src/ tests/
ruff check src/
mypy src/
pytest

# Monitor CI/CD
bin/gh-monitor            # Recent failures
bin/gh-monitor analyze    # Detailed analysis
bin/gh-monitor report     # Error report
```

### Key Commands

```bash
# Development
poetry run pytest --cov=src            # Run tests with coverage
poetry run mypy src/                   # Type checking
poetry run ruff check src/             # Linting
poetry run bandit -r src/              # Security scan

# Application
poetry run streamlit run streamlit_app.py  # Web UI
python main.py generate "Content"          # CLI

# CI/CD Monitoring
bin/gh-monitor                         # Show failures
bin/gh-monitor analyze                 # Analyze errors
bin/gh-monitor report                  # Generate report
```

## Features

### Phase 1 & 2 (Complete)
- ✅ Full API integration with retry logic
- ✅ 16 visual styles + custom styles
- ✅ Streamlit web interface
- ✅ CLI with rich terminal output
- ✅ Multi-language support (38 languages)
- ✅ Advanced options (transparency, dimensions)
- ✅ GitHub Actions CI/CD

### Upcoming (Phase 3-5)
- 🚧 Batch processing from CSV/JSON
- 🚧 SQLite storage and gallery
- 🚧 Team collaboration features
- 🚧 Cloud storage integration
- 🚧 API webhooks

## Environment Variables

```bash
# Required
NAPKIN_API_TOKEN=your_token_here

# Optional
NAPKIN_DEFAULT_STYLE=vibrant-strokes
NAPKIN_DEFAULT_FORMAT=svg
NAPKIN_STORAGE_PATH=./data/visuals
NAPKIN_DEBUG_MODE=false
NAPKIN_LOG_LEVEL=INFO

# GitHub Monitoring (optional)
GITHUB_TOKEN=ghp_your_token
GITHUB_REPOSITORY=owner/repo
```

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific module
pytest tests/test_api/

# With verbose output
pytest -vv
```

### Writing Tests

```python
# Example test with fixture
import pytest
from src.api.client import NapkinAPIClient

@pytest.fixture
def client():
    return NapkinAPIClient(api_token="test_token")

@pytest.mark.asyncio
async def test_generate_visual(client, httpx_mock):
    httpx_mock.add_response(
        json={"id": "123", "status": "completed"}
    )
    
    async with client:
        result = await client.generate("Test")
    
    assert result.id == "123"
```

## CI/CD Pipeline

### GitHub Actions Workflow

- **Python versions**: 3.10, 3.11, 3.12
- **Checks**: Linting, type checking, tests, security
- **Notifications**: Slack, Discord, Email, GitHub Issues

### Monitoring Tools

```bash
# Check recent failures
bin/gh-monitor

# Detailed error analysis
bin/gh-monitor analyze

# Generate error report
bin/gh-monitor report

# Export to JSON
bin/gh-monitor 10 --json failures.json
```

## Contributing

### Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Make changes following code standards
4. Run quality checks (`ruff`, `mypy`, `pytest`)
5. Submit pull request

### Code Standards

- Type hints required
- Google-style docstrings
- Async/await for API calls
- Pydantic v2 models
- Error handling with proper logging

### Commit Convention

```
type(scope): description

Examples:
feat(cli): add batch processing
fix(api): handle rate limit errors
docs: update API reference
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Rate limit errors | Auto-retry with backoff (60 req/min) |
| Token errors | Check `NAPKIN_API_TOKEN` in `.env` |
| Import errors | Run `poetry install` |
| Type errors | Run `poetry run mypy src/` |
| Test failures | Ensure valid API token |

### Debug Mode

```bash
# Enable debug logging
export NAPKIN_DEBUG_MODE=true
export NAPKIN_LOG_LEVEL=DEBUG

# Check configuration
python main.py config --check
```

## Resources

- [API Guide](API_GUIDE.md)
- [Official Napkin API Docs](napkin_official/NAPKIN_AI_API.md)
- [GitHub Repository](https://github.com/moshehbenavraham/Napkin-AI-API)
- [Report Issues](https://github.com/moshehbenavraham/Napkin-AI-API/issues)

## License

Unlicense (Public Domain) - see [LICENSE.md](../LICENSE.md)