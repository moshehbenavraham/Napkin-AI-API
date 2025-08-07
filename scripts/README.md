# GitHub Actions Failure Scripts

Simple scripts to quickly check recent GitHub Actions failures.

## 🚀 Quick Start

### Option 1: Ultra Simple (Python one-liner)
```bash
# Show last 5 failures
python scripts/quick_failures.py

# Show last 10 failures
python scripts/quick_failures.py 10
```

### Option 2: Bash Script (uses gh CLI or curl)
```bash
# Show last 5 failures
./scripts/failures.sh

# Show last 10 failures
./scripts/failures.sh 10
```

### Option 3: Full Featured (Python)
```bash
# Basic usage
python scripts/get_github_failures.py

# Show last 10 failures with job details
python scripts/get_github_failures.py --last 10 --jobs

# Simple one-line format
python scripts/get_github_failures.py --simple

# Export to JSON
python scripts/get_github_failures.py --export failures.json

# Specific repository
python scripts/get_github_failures.py --repo owner/repo --last 20
```

## 🔑 Setup

### Set GitHub Token (Optional but recommended)
```bash
export GITHUB_TOKEN="your_github_token"
```

Without a token, you'll hit API rate limits quickly (60 requests/hour).

### Get a GitHub Token
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `repo` scope for private repos, or `public_repo` for public only
4. Copy token and set as environment variable

## 📊 Examples

### Quick Check
```bash
$ python scripts/quick_failures.py 3

🚨 Last 3 failures in moshehbenavraham/Napkin-AI-API:

❌ 01/07 15:23 - CI Pipeline - main
   https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/123456

❌ 01/07 14:10 - Test Suite - feature/new-api
   https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/123455

❌ 01/06 22:45 - Deploy - main
   https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/123454
```

### Detailed View
```bash
$ python scripts/get_github_failures.py --last 1 --jobs

📂 Repository: moshehbenavraham/Napkin-AI-API
🔍 Fetching last 1 failures...

============================================================
❌ CI Pipeline - 2h ago
============================================================
📅 Date: 2025-01-07 15:23 UTC
🔢 Run: #42
🌿 Branch: main
👤 Author: John Doe
💬 Message: Fix API endpoint validation
🔗 URL: https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/123456

  Failed Steps:
  • Run Tests
    - Run pytest
  • Type Check
    - Run mypy

📊 Summary: 1 failures found
📈 Failure rate: 15.2% (last 50 runs)
```

### Export for Analysis
```bash
$ python scripts/get_github_failures.py --last 50 --export failures.json
✅ Exported 50 failures to failures.json

$ jq '.failures[0]' failures.json
{
  "id": 123456,
  "name": "CI Pipeline",
  "run_number": 42,
  "created_at": "2025-01-07T15:23:00Z",
  "branch": "main",
  "author": "John Doe",
  "message": "Fix API endpoint validation",
  "url": "https://github.com/...",
  "commit_sha": "abc123..."
}
```

## 🎯 Use Cases

1. **Morning Check**: See what failed overnight
   ```bash
   python scripts/quick_failures.py 10
   ```

2. **Debug Session**: Get detailed failure info
   ```bash
   python scripts/get_github_failures.py --jobs --last 5
   ```

3. **Weekly Report**: Export failures for analysis
   ```bash
   python scripts/get_github_failures.py --last 100 --export weekly_failures.json
   ```

4. **CI Integration**: Add to your CI pipeline
   ```yaml
   - name: Check Recent Failures
     run: |
       python scripts/quick_failures.py 5
   ```

## 🛠️ Troubleshooting

### "Could not detect GitHub repository"
Run the script from inside a git repository, or specify the repo:
```bash
python scripts/get_github_failures.py --repo owner/repo
```

### "API rate limit exceeded"
Set a GitHub token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### "No failures found"
Great! Your CI is working perfectly! 🎉

## 📝 Script Comparison

| Script | Language | Features | Best For |
|--------|----------|----------|----------|
| `quick_failures.py` | Python | Minimal, fast | Quick checks |
| `failures.sh` | Bash | Uses gh CLI if available | Terminal users |
| `get_github_failures.py` | Python | Full featured, export | Detailed analysis |

---

Pro tip: Add an alias to your shell config:
```bash
alias failures="python ~/path/to/scripts/quick_failures.py"
```

Then just type `failures` to check recent CI failures!