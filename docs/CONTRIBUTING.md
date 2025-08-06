# Contributing Guide

## Development Setup

### Prerequisites

- Python 3.9+
- Poetry
- Git
- SQLite3

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/napkin-playground.git
cd napkin-playground

# Install with development dependencies
poetry install --with dev

# Activate virtual environment
poetry shell

# Install pre-commit hooks
# If pre-commit is not installed, install it first:
#   poetry add --group dev pre-commit
# or with pipx:
#   pipx install pre-commit
pre-commit install

# Run tests
pytest

# Start development
python main.py --debug
```

## Project Structure

```
src/
├── cli/         # CLI commands and interface
├── api/         # API client and models
├── core/        # Business logic
├── storage/     # Database and file handling
├── web/         # Streamlit application
└── utils/       # Shared utilities
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow these guidelines:
- Write clear, self-documenting code
- Add type hints to all functions
- Update tests for new functionality
- Follow existing patterns

### 3. Code Quality

```bash
# Format and lint code (Ruff replaces Black + isort)
ruff format src/ tests/

# Sort imports
ruff check --select I --fix src/ tests/

# Type checking
mypy src/

# Linting
ruff check src/

# Run all checks (if Makefile is present)
# Otherwise, run the individual commands above.
make lint || echo "No Makefile found; ran individual checks instead."
```

### 4. Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_api/test_client.py::TestClient

# Run with verbose output
pytest -v

# Run integration tests
pytest -m integration
```

### 5. Documentation

- Update docstrings for new functions
- Add examples to relevant docs
- Update README if adding features
- Include type hints

### 6. Submit PR

```bash
# Push changes
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Testing Guidelines

### Unit Tests

```python
# tests/test_api/test_client.py
import pytest
from napkin_playground import NapkinClient

@pytest.fixture
def client():
    return NapkinClient(token="test_token")

def test_generate_basic(client, mock_response):
    result = client.generate("Test content")
    assert result.status == "completed"
    assert len(result.files) > 0
```

### Integration Tests

```python
# tests/integration/test_workflow.py
@pytest.mark.integration
async def test_full_workflow():
    client = NapkinClient()
    result = await client.generate("Test")
    gallery = Gallery()
    item = gallery.add(result)
    assert item.id is not None
```

### Mocking

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_api_response():
    return Mock(
        status_code=200,
        json=lambda: {"id": "test-id", "status": "completed"}
    )
```

## Code Style

### Python Style

```python
# Good
async def generate_visual(
    content: str,
    style: Optional[str] = None,
    format: Literal["svg", "png"] = "svg"
) -> VisualResult:
    """Generate visual from text content.
    
    Args:
        content: Text to visualize
        style: Style ID or name
        format: Output format
        
    Returns:
        VisualResult with generated files
        
    Raises:
        APIError: If request fails
    """
    # Implementation
```

### Imports

```python
# Standard library
import os
from datetime import datetime
from typing import Optional, List

# Third party
import httpx
from rich.console import Console

# Local
from napkin_playground.api import NapkinClient
from napkin_playground.models import VisualRequest
```

### Error Handling

```python
# Good
try:
    result = await client.generate(content)
except RateLimitError as e:
    logger.warning(f"Rate limit hit, retry after {e.retry_after}s")
    raise
except APIError as e:
    logger.error(f"API error: {e}")
    return None
```

## Adding Features

### New CLI Command

1. Create command in `src/cli/commands.py`
2. Add to command group
3. Include help text
4. Add tests

```python
# src/cli/commands.py
import typer

@typer.command()
def new_command(
    style: str = typer.Option(None, help="Visual style")
):
    """Your new command description."""
    # Implementation
```

### New API Endpoint

1. Add method to `NapkinClient`
2. Create request/response models
3. Add error handling
4. Write tests

```python
# src/api/client.py
async def new_endpoint(self, param: str) -> Result:
    """Call new API endpoint."""
    response = await self._request(
        "POST",
        "/v1/new-endpoint",
        json={"param": param}
    )
    return Result.from_response(response)
```

## Debugging

### Enable Debug Logging

```bash
# Unix/macOS (bash/zsh)
export NAPKIN_LOG_LEVEL=DEBUG

# Windows (Command Prompt - current session)
set NAPKIN_LOG_LEVEL=DEBUG

# Windows (PowerShell - current session)
$env:NAPKIN_LOG_LEVEL="DEBUG"

# Windows (persist for user)
# Note: requires a new terminal to take effect
setx NAPKIN_LOG_LEVEL "DEBUG"
```

```python
# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug CLI

```bash
# Verbose output
napkin --debug generate "Test"

# Dry run
napkin generate "Test" --dry-run

# Show HTTP traffic
# Unix/macOS
export HTTPX_LOG_LEVEL=debug
# Windows CMD
set HTTPX_LOG_LEVEL=debug
# Windows PowerShell
$env:HTTPX_LOG_LEVEL="debug"
```

### Profile Performance

```python
# Using cProfile
python -m cProfile -o profile.stats main.py

# Analyze
import pstats
stats = pstats.Stats("profile.stats")
stats.sort_stats("cumulative").print_stats(10)
```

## Release Process

### Version Bump

```bash
# Patch version (0.1.0 -> 0.1.1)
poetry version patch

# Minor version (0.1.0 -> 0.2.0)
poetry version minor

# Major version (0.1.0 -> 1.0.0)
poetry version major
```

### Build & Publish

```bash
# Build package
poetry build

# Test on TestPyPI
poetry publish -r test-pypi

# Publish to PyPI
poetry publish
```

### Changelog

Update `CHANGELOG.md`:

```markdown
## [0.2.0] - 2024-01-15

### Added
- New feature X
- Support for Y

### Fixed
- Bug in Z

### Changed
- Improved performance of A
```

## Resources

### Documentation

- [Napkin API Docs](../napkin_ai_api.md)
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints](https://peps.python.org/pep-0484/)

### Tools

- [Poetry](https://python-poetry.org/)
- [pytest](https://pytest.org/)
- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)

## Getting Help

- Open an issue on GitHub
- Join discussions
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow project guidelines