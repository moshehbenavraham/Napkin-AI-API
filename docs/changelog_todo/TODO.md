# TODO - Pending Tasks Only

> Completed tasks have been moved to CHANGELOG.md

## Immediate Priorities

### Testing
- [ ] Add unit tests for client (download flow, Content-Disposition parsing, MIME fallback, synthesized filenames)
- [ ] Add integration tests with mocked API (generated_files and legacy files; 401/404/410/429 paths; chunked streaming)
- [ ] Test retry logic with mocked responses
- [ ] Add integration tests for file downloads
- [ ] Establish coverage threshold (≥50%) for core modules

### Quality & Tooling
- [ ] Configure pre-commit hooks (.pre-commit-config.yaml) with ruff, mypy, pytest (quick), optional detect-secrets

### Code Quality Improvements
- [ ] **Unify OutputFormat enum**
  - Remove duplicate enum from src/utils/constants.py
  - Import from src/api/models.py everywhere
  - Update DEFAULTS to use models.OutputFormat
- [ ] **Datetime imports cleanup**
  - Replace dynamic `__import__` with normal imports in client.py
  - Ensure timezone-aware UTC consistently
- [ ] **Interactive CLI**
  - Either implement or remove src/cli/interactive.py stub
- [ ] **Pydantic v2 Compatibility**
  - Review remaining models/settings for full Pydantic v2 compatibility

### Documentation
- [ ] Update README inline docstrings and cross-references
- [ ] Keep API response format as the single source of truth in docs/API_REFERENCE.md
- [ ] Cross-link from docs/napkin_ai_api.md

### Optional Enhancements
- [ ] Optional file logging toggle and implementation (NAPKIN_FILE_LOGGING) with rolling, size-limited logs

## Pre-commit Hooks Configuration Guide

When implementing pre-commit hooks:
```bash
pipx install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml` with:
- ruff (format and check)
- mypy
- pytest (quick tests)
- detect-secrets (optional)

## Environment Variables Reference

### Required
- `NAPKIN_API_TOKEN`

### Optional (with defaults)
- `NAPKIN_DOWNLOAD_CHUNK_SIZE` (default: 65536)
- `NAPKIN_DOWNLOAD_OVERWRITE` (default: false)
- `NAPKIN_FILE_LOGGING` (default: false - to be implemented)

## Test Implementation Plan

### Unit Tests Priority
1. Content-Disposition parsing (filename*, filename, unicode, spaces)
2. MIME fallback from format when header missing
3. Filename synthesis logic

### Integration Tests (Mocked)
1. Status returns generated_files with url → download returns 200 with Content-Disposition
2. Legacy shape: files instead of generated_files
3. Fallback path when url missing → GET /v1/visual/:id/file/:file-id
4. Error paths: 401, 404, 410, 429 retry, unexpected content-type

### Performance Tests
- Streamed chunks validation
- Assert chunked writes occur (spy on write calls or count)