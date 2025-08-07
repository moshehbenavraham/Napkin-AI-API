# GitHub Actions Failure Scripts

Simple tools to monitor GitHub Actions failures for this repository.

## 🚀 Quick Start

```bash
# Check last 5 failures (default)
bin/failures

# Check last 10 failures
bin/failures 10

# Export failures to JSON
python scripts/check_failures.py 10 --json failures.json

# Simple one-line format
python scripts/check_failures.py --simple
```

## 📁 Files

### User Tools
- **`bin/failures`** - Main command-line tool (wrapper for check_failures.py)
- **`scripts/check_failures.py`** - Core failure checking script with advanced features

### CI/CD Integration
- **`.github/scripts/error_reporter.py`** - Automated error reporting for GitHub Actions workflows
- **`.github/workflows/ci.yml`** - Main CI workflow with integrated failure notifications

## ⚙️ Setup

1. **Add GitHub Token to .env**:
```bash
echo "GITHUB_TOKEN=ghp_your_token_here" >> .env
```

2. **For CI/CD Notifications** (optional):
Add these secrets to your GitHub repository:
- `SLACK_WEBHOOK` - For Slack notifications
- `DISCORD_WEBHOOK` - For Discord notifications

## 📝 Features

### check_failures.py
- ✅ Automatic .env file loading
- ✅ Git repository detection
- ✅ Detailed or simple output formats
- ✅ JSON export capability
- ✅ Failure rate statistics
- ✅ Human-readable time formatting

### error_reporter.py (CI/CD)
- ✅ Slack notifications
- ✅ Discord notifications
- ✅ GitHub issue creation
- ✅ Custom API webhooks
- ✅ Detailed error context

## 🔧 Usage Examples

### Command Line

```bash
# Basic usage
bin/failures

# Check specific number of failures
bin/failures 20

# Export to JSON for analysis
python scripts/check_failures.py 50 --json analysis.json

# Quick overview with simple format
python scripts/check_failures.py 10 --simple
```

### CI/CD Integration

The CI workflow automatically reports failures when:
- Tests fail
- Linting fails
- Type checking fails
- Security checks fail

Notifications are sent to configured channels (Slack, Discord) and can create GitHub issues for main branch failures.

## 🔐 Security

- GitHub tokens are read from `.env` file (never commit this!)
- The `.env` file is gitignored for security
- CI/CD uses GitHub Secrets for sensitive data

## 📊 Output Examples

### Standard Output
```
✅ Using GitHub token from .env file
📂 Repository: moshehbenavraham/Napkin-AI-API
🔍 Fetching last 5 failures...

🚨 Last 5 failures:
------------------------------------------------------------
❌ CI #16 - 1h ago
   📅 2025-08-07 00:52 UTC
   🌿 Branch: main
   👤 Author: Mosheh Ben Avraham
   💬 Fix dependencies
   🔗 https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/16792301463

📊 Stats: 23.5% failure rate (last 50 runs)
```

### Simple Output
```
❌ 08/07 00:52 - CI - main
❌ 08/07 00:46 - CI - develop
❌ 08/07 00:38 - Tests - feature/new-api
```

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| No token found | Add `GITHUB_TOKEN=ghp_...` to `.env` file |
| 403 Error | Check token permissions or rate limit |
| 404 Error | Verify repository name and access rights |
| Can't detect repo | Run from git repository or set `GITHUB_REPOSITORY` env var |

## 📈 Best Practices

1. **Regular Monitoring**: Run `bin/failures` daily to catch patterns
2. **Export for Analysis**: Use JSON export for trend analysis
3. **CI/CD Alerts**: Configure webhooks for immediate notification
4. **Token Security**: Never commit tokens, use `.env` or GitHub Secrets

---

*Last updated: 2025-08-07*