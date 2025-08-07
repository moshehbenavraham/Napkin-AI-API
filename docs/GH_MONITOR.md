# GitHub Actions Monitor

Unified tool for monitoring GitHub Actions workflows, analyzing failures, and sending notifications.

## Installation

The tool is already installed in `scripts/gh_monitor.py` with a wrapper at `bin/gh-monitor`.

## Usage

### Quick Commands

```bash
# Show last 5 failures (default)
bin/gh-monitor

# Show last 10 failures
bin/gh-monitor 10

# Analyze recent failures in detail
bin/gh-monitor analyze

# Generate error report (useful in CI/CD)
bin/gh-monitor report

# Export failures to JSON
bin/gh-monitor 5 --json failures.json

# Simple one-line format
bin/gh-monitor 10 --simple
```

### Commands

- **list** (default): Show recent workflow failures
- **analyze**: Detailed analysis of failed runs with error messages
- **report**: Generate error report with GitHub Actions context

### Options

- `--json FILE`: Export results to JSON file
- `--simple`: Use simple one-line output format
- `--webhook URL`: Send notification to webhook
- `--webhook-type TYPE`: Webhook type (slack, discord, custom)

## Features

### 1. Failure Listing
Shows recent workflow failures with:
- Workflow name and run number
- Time since failure
- Branch and author
- Commit message
- Direct link to logs
- Overall failure rate statistics

### 2. Failure Analysis
Analyzes specific workflow runs to identify:
- Failed jobs and steps
- Error messages from logs
- Frequency of specific job failures
- Pattern detection across failures

### 3. Error Reporting
Generates comprehensive error reports for CI/CD contexts including:
- GitHub Actions environment variables
- Repository and workflow context
- Python version and runner information
- Timestamp and run URLs

### 4. Webhook Notifications
Send failure notifications to:
- **Slack**: Formatted message with action buttons
- **Discord**: Embedded message with failure details
- **Custom**: Raw JSON report

## Configuration

### GitHub Token
Add your GitHub token to `.env`:
```
GITHUB_TOKEN=ghp_yourtoken
```

### Webhook Setup
For Slack/Discord notifications in CI:
```yaml
- name: Send Notification
  run: |
    python3 scripts/gh_monitor.py report --webhook ${{ secrets.SLACK_WEBHOOK }}
```

## CI/CD Integration

### In GitHub Actions Workflow
```yaml
notify-on-failure:
  needs: [test, lint]
  if: failure()
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Report Failure
      run: |
        python3 scripts/gh_monitor.py report --json error.json
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Send Slack Notification
      if: env.SLACK_WEBHOOK
      run: |
        python3 scripts/gh_monitor.py report --webhook ${{ secrets.SLACK_WEBHOOK }}
```

## Examples

### Check Recent Failures
```bash
$ bin/gh-monitor 3
✅ Using GitHub token from .env file
📂 Repository: owner/repo
🔍 Fetching last 3 failures...

🚨 Last 3 failures:
------------------------------------------------------------
❌ CI #42 - 2h ago
   📅 2025-08-07 10:30 UTC
   🌿 Branch: main
   👤 Author: John Doe
   💬 Fix critical bug
   🔗 https://github.com/owner/repo/actions/runs/123456
```

### Analyze Failures
```bash
$ bin/gh-monitor analyze
Analyzing Run ID: 123456
============================================================
Workflow: CI
Status: completed
Conclusion: failure
Branch: main

❌ Failed Job: test
   Failed Step: Run tests
   
   Key Error Messages:
   > ImportError: No module named 'requests'
```

### Export to JSON
```bash
$ bin/gh-monitor 10 --json failures.json
✅ Exported 10 failures to failures.json
```

## Comparison with Previous Tools

This unified tool replaces:
- `scripts/check_failures.py` - Basic failure listing
- `analyze_ci_logs.py` - Log analysis
- `.github/scripts/error_reporter.py` - Error reporting for CI
- `bin/failures` and `failures` - Shell wrappers

All functionality is now consolidated into a single, maintainable tool.