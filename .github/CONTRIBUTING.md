# Contributing to Napkin AI API

Thank you for your interest in contributing to the Napkin AI API client! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept responsibility and apologize when making mistakes

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue templates provided
- Include as much detail as possible
- Provide steps to reproduce bugs

### Suggesting Features

- Check the roadmap in `docs/PRD.md` for planned features
- Open a feature request issue using the template
- Explain the use case and benefits
- Consider how it fits with existing functionality

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/xamgibson/Napkin-AI-API.git
   cd Napkin-AI-API
   ```

2. **Set Up Development Environment**
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry install --with dev
   
   # Activate virtual environment
   poetry shell
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

4. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Keep commits focused and atomic

5. **Run Quality Checks**
   ```bash
   # Format code
   ruff format src/ tests/
   
   # Run linter
   ruff check src/
   
   # Type checking
   mypy src/
   
   # Run tests
   pytest --cov=src
   ```

6. **Submit Pull Request**
   - Use the PR template
   - Reference any related issues
   - Ensure all CI checks pass
   - Request review from maintainers

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write descriptive variable names
- Keep functions focused and small
- Add docstrings (Google style) for public APIs

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Use pytest fixtures for common setups
- Mock external API calls
- Test edge cases and error conditions

### Documentation

- Update README.md for user-facing changes
- Update API_REFERENCE.md for API changes
- Add inline comments for complex logic
- Update CLAUDE.md if adding new patterns

### Commit Messages

Follow conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes
- `perf`: Performance improvements

Example:
```
feat(cli): add interactive mode for style selection

Implements an interactive CLI mode that allows users to browse
and select styles visually before generating content.

Closes #123
```

## Project Structure

```
src/
├── api/          # API client and models
├── cli/          # CLI commands and display
├── core/         # Core business logic
├── storage/      # Data persistence (future)
└── utils/        # Utilities and helpers

tests/
├── unit/         # Unit tests
├── integration/  # Integration tests
└── fixtures/     # Test fixtures
```

## Getting Help

- Check the documentation in `docs/`
- Look at existing code for examples
- Ask questions in GitHub Discussions
- Reach out to maintainers for guidance

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing!