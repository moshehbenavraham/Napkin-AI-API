# .github Directory Documentation

This document explains the purpose, structure, and maintenance of the `.github` directory for the Napkin AI API repository. It covers review ownership via CODEOWNERS, dependency automation via Dependabot, the Pull Request template, Issue templates (how to add or modify), and GitHub Actions workflows (how to organize and maintain).

## Overview

GitHub treats `.github/` as a special directory for repository-level configuration and community health files. These influence contributor experience and automation across the project:

- CODEOWNERS: review routing and ownership rules
- Dependabot: automated dependency updates and security fixes
- Pull Request template: standardized information for PRs
- Issue templates: standardized issue creation (bugs/features/etc.)
- Workflows: CI/CD and automation via GitHub Actions

Current tree:
```
.github/
├── CODEOWNERS
├── dependabot.yml
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml
│   ├── config.yml
│   └── feature_request.yml
├── pull_request_template.md
└── workflows/
    ├── ci.yml
    └── release.yml
```

---

## CODEOWNERS

File: `.github/CODEOWNERS`

Purpose: Automatically assigns reviewers and defines ownership for paths in the repository. Owners are responsible for reviews and stewardship of their areas.

Current rules (summary):
- Global default owner: `@moshehbenavraham`
- API client and core: `/src/api/`, `/src/core/` → `@moshehbenavraham`
- CLI: `/src/cli/` → `@moshehbenavraham`
- Documentation: `/docs/`, `*.md` → `@moshehbenavraham`
- Configuration and CI/CD: `/.github/`, `/pyproject.toml`, `/.env.example` → `@moshehbenavraham`
- Tests: `/tests/` → `@moshehbenavraham`

How matching works:
- The last matching pattern in the file takes precedence if multiple match.
- Patterns behave like `.gitignore`:
  - `*` matches anything
  - `**` matches across directories
  - A leading `/` anchors to repo root
  - A trailing `/` matches directories
- For a PR to be mergeable, required reviews may include codeowners depending on branch protection rules.

Common operations:
- Add a new owned area:
  - Example: assign storage code to two owners:
    ```
    /src/storage/ @owner1 @owner2
    ```
- Narrow ownership for a subpath:
  - Example to override a parent rule:
    ```
    /src/ @parentowner
    /src/utils/ @utilsowner  # wins for utils
    ```

Validation and testing tips:
- Use a feature branch PR touching files in the target path to observe auto-assignment.
- Use the “Files changed” tab to see if owners were requested.
- Ensure owners are members or have read access; otherwise GitHub cannot request them.

Maintenance SOP:
- Review quarterly or when code areas/teams change.
- Keep patterns minimal and specific; avoid overlapping rules unless required.
- Ensure there is always a sane fallback (global `*` rule).

---

## Dependabot

File: `.github/dependabot.yml`

Purpose: Automates dependency and GitHub Actions updates via PRs.

Current config highlights:
- Python (pip) ecosystem at repository root (`directory: "/"`)
  - Weekly schedule: Monday 03:00 UTC
  - Open PR limit: 5
  - Labels: `dependencies`, `python`
  - Assignees: `moshehbenavraham`
  - Commit message: `chore(scope): ...`
  - Groups:
    - `dev-dependencies`: development-only tools (pytest*, ruff, mypy, black)
    - `minor-updates`: only minor and patch update types
- GitHub Actions ecosystem
  - Monthly schedule: Monday 03:00 UTC
  - Open PR limit: 3
  - Labels: `dependencies`, `github-actions`
  - Commit message: `ci(scope): ...`

Operational guidance:
- Grouping reduces PR noise; additional groups can be added for families of packages.
- To ignore/snooze a dependency, use Dependabot’s PR UI “Dismiss” with a reason or add `ignore` rules in the YAML:
  ```
  ignore:
    - dependency-name: "package-name"
      versions: [">=2.0.0 < 3"]
  ```
- Security updates:
  - Enable “Dependabot security updates” in the repository settings to auto-open PRs for vulnerabilities.
- Branch protection:
  - Ensure Dependabot PRs can pass required checks (CI workflows) to merge.

Maintenance SOP:
- Quarterly review schedules and open PR caps based on team bandwidth.
- Add/remove labels or assignees to reflect current triage process.
- Consider pinning critical tooling to avoid unexpected breaks; let Dependabot propose vetted bumps.

---

## Pull Request Template

File: `.github/pull_request_template.md`

Purpose: Standardizes PR authoring to improve review quality and reduce back-and-forth.

Key sections:
- Description: concise summary of the change
- Type of Change: check one or more categories
- Related Issues: auto-closing syntax, e.g. `Fixes #123`
- Changes Made: bullet summary
- Testing: local verification checklist
  - pytest
  - ruff format/check
  - mypy type-checking
  - docs update
  - new tests for new features
- Test Coverage: paste `pytest --cov=src --cov-report=term-missing` output
- Screenshots: for UI-facing changes (if applicable)
- Additional Notes: edge-cases, roll-back plan, migration notes

Usage:
- The template auto-populates on new PRs to default branches.
- Keep checkboxes accurate; reviewers use them to gate merges.
- Include coverage output for visibility into untested lines.

Maintenance SOP:
- Update when new project-wide checks or conventions are introduced.
- Keep it concise to avoid template fatigue.

---

## Issue Templates

Folder: `.github/ISSUE_TEMPLATE/`

Purpose: Guides consistent issue reporting for faster triage.

Current templates:
- `bug_report.yml`: Bug report template with fields for description, expected behavior, steps to reproduce, environment, and logs
- `feature_request.yml`: Feature request template with problem statement, proposed solution, and alternatives
- `config.yml`: Configuration for issue template chooser

Create or modify templates:
1. Add YAML files under `.github/ISSUE_TEMPLATE/`:
   - `bug_report.yml`
   - `feature_request.yml`
   - `documentation.yml`
2. Optional: Add `.github/ISSUE_TEMPLATE/config.yml` to control blank issues and contact links.
3. Validate via the “New issue” button to ensure templates render.

Example skeleton (bug report):
```yaml
name: Bug report
description: Report a problem to help us improve
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear and concise description of the bug.
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Provide steps and minimal code if possible.
  - type: input
    id: environment
    attributes:
      label: Environment
      placeholder: OS, Python version, etc.
  - type: textarea
    id: logs
    attributes:
      label: Logs
      render: shell
```

Maintenance SOP:
- Adjust fields as triage needs evolve.
- Keep labels aligned with repo label taxonomy.

---

## Workflows (GitHub Actions)

Folder: `.github/workflows/`

Purpose: Contains CI/CD and automation pipelines. Examples include linting, tests, type checks, packaging, release, and security scans.

Current workflows:
- `ci.yml`: Main CI pipeline with linting, type checking, and tests across Python versions
- `release.yml`: Release automation for tagged versions

Best practices:
- Naming: `ci.yml`, `tests.yml`, `release.yml`, `lint.yml` for clarity.
- Triggers: prefer `pull_request` and `push` on active branches; add manual `workflow_dispatch` when useful.
- Concurrency: prevent duplicate runs on the same branch:
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```
- Permissions: least-privilege by default:
  ```yaml
  permissions:
    contents: read
  ```
  Elevate only where required (e.g., `packages: write` for publishing).
- Caching: Poetry/pip cache and pytest cache to speed CI.
- Matrix: test against supported Python versions.
- Secrets: reference via `secrets.*`; never commit secrets.
- Required checks: align with branch protection.

Maintenance SOP:
- Periodically bump action versions (e.g., `actions/checkout@v4`).
- Validate breaking changes in actions on a branch before merging.
- Keep workflows fast and deterministic; split heavy jobs to separate files.

---

## Maintenance Schedule and Ownership

- Owner: `@moshehbenavraham` (as per CODEOWNERS)
- Quarterly checklist:
  - Review CODEOWNERS scope against current code structure.
  - Review Dependabot schedules, groups, ignore lists.
  - Ensure PR and Issue templates reflect current engineering practices.
  - Audit workflows for action version updates, permissions, and caching.
  - Verify branch protection rules align with required checks and ownership.

---

## FAQ

Q: Which CODEOWNERS rule takes precedence?
A: The last rule matching the path in the file takes precedence.

Q: How do I skip the PR template for a one-off admin change?
A: You can keep the template minimal but do not remove required checks; alternatively, push directly if you have permissions and the change is exempt per policy.

Q: Can Dependabot group additional packages?
A: Yes. Add `groups` entries with `patterns` or `update-types` to consolidate PRs.

Q: How do workflows interact with labels or automations?
A: Use `if:` conditions with `github.event.pull_request.labels` to gate jobs by labels, or add a lightweight labeling bot if necessary.

Q: Do Issue Templates support required fields?
A: Yes, via `validations.required: true` in YAML.

---

## Change Log

Document notable changes to `.github/` here to aid future maintainers:
- 2025-01-07: Updated documentation to reflect actual file structure, added specific workflow and template details
- Initial documentation created: explains CODEOWNERS, Dependabot, PR and Issue templates, and Workflows; adds SOPs and FAQs.