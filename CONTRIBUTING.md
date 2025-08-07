# Contributing to Napkin AI API

Thank you for contributing to the Napkin AI API client!

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept responsibility and apologize when making mistakes

## Development Setup

### Prerequisites

- Python 3.10+
- Poetry (dependency management)
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/Napkin-AI-API.git
cd Napkin-AI-API

# Install dependencies
poetry install --with dev

# Activate virtual environment
poetry shell

# Set up environment
cp .env.example .env
# Edit .env and add your NAPKIN_API_TOKEN

# Run tests
pytest

# Try the CLI
python main.py generate "Test content"
```

## Project Structure

```
src/
├── api/          # API client and models
├── cli/          # CLI commands and display
├── core/         # Core business logic (generator)
├── storage/      # Data persistence (future)
└── utils/        # Constants, config, helpers

tests/
├── test_api/     # API client tests
├── test_cli/     # CLI tests
└── test_models/  # Model validation tests
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. Make Changes

- Follow existing code patterns
- Add type hints to all functions
- Write tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/

# Type checking
mypy src/

# Run tests
pytest --cov=src
```

### 4. Submit Pull Request

```bash
# Push changes
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear description of changes
- Reference to any related issues
- Test results

## Coding Standards

### Python Style

```python
# Use type hints and Google-style docstrings
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

### Import Order

```python
# Standard library
import os
from typing import Optional, List

# Third party
import httpx
from pydantic import BaseModel

# Local
from src.api.client import NapkinAPIClient
from src.api.models import VisualRequest
```

### Error Handling

```python
try:
    result = await client.generate(content)
except RateLimitError as e:
    logger.warning(f"Rate limit: retry after {e.retry_after}s")
    raise
except APIError as e:
    logger.error(f"API error: {e}")
    return None
```

## Testing Guidelines

### Write Tests For

- New features and bug fixes
- Edge cases and error conditions
- API client methods (with mocked responses)
- CLI commands and options
- Model validation

### CI/CD Monitoring

Before submitting a PR, check the CI status:

```bash
# Check recent CI failures
bin/gh-monitor

# Analyze any failures in detail
bin/gh-monitor analyze

# Ensure all tests pass locally
poetry run pytest
poetry run mypy src/
poetry run ruff check src/
```

### Example Test

```python
# tests/test_api/test_client.py
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
    assert result.status == "completed"
```

## Adding Features

### New CLI Command

1. Add command to `src/cli/commands.py`
2. Add display formatting to `src/cli/display.py`
3. Write tests in `tests/test_cli/`
4. Update README.md with usage examples

### New API Endpoint

1. Add method to `NapkinAPIClient` in `src/api/client.py`
2. Create models in `src/api/models.py`
3. Add tests with mocked responses
4. Update API_REFERENCE.md

### New Style or Feature

1. Add constants to `src/utils/constants.py`
2. Update relevant models
3. Add CLI support if user-facing
4. Write tests

## Commit Messages

Use conventional commits:

```
type(scope): description

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(cli): add batch processing from CSV

Implements ability to process multiple visuals from a CSV file
with progress tracking and error recovery.

Closes #45
```

## Debugging

```bash
# Enable debug logging
export NAPKIN_LOG_LEVEL=DEBUG
export NAPKIN_DEBUG_MODE=true

# Test with verbose output
python main.py generate "Test" --debug

# Check configuration
python main.py config --check
```

## Documentation

When contributing, update:

- **README.md**: User-facing features and examples
- **API_REFERENCE.md**: Library API changes
- **CLAUDE.md**: New patterns or conventions
- **TODO.md**: Mark completed items
- **Docstrings**: All public functions and classes

## Getting Help

- Check existing documentation in `docs/`
- Review similar code in the codebase
- Open a GitHub issue for questions
- Check the roadmap in `docs/PRD.md`

## Resources

- [Napkin API Docs](napkin_ai_api.md)
- [Project Roadmap](PRD.md)
- [Python Type Hints](https://peps.python.org/pep-0484/)
- [Pydantic v2 Docs](https://docs.pydantic.dev/)
- [Rich CLI Formatting](https://rich.readthedocs.io/)