# ✅ GitHub Failures Script - All Set Up!

Your GitHub Actions failure checker is now fully configured and ready to use!

## 🚀 How to Use

### Quick Check (Recommended)
```bash
# From anywhere in the project:
python3 scripts/check_failures.py

# Or use the shortcut:
bin/failures

# Check last 10 failures:
bin/failures 10
```

### What's Configured

✅ **GitHub Token**: Automatically loaded from `.env` file
✅ **Repository**: Auto-detected from git
✅ **No setup needed**: Just run the commands above!

## 📊 Example Output

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
   💬 Update API endpoints
   🔗 https://github.com/moshehbenavraham/Napkin-AI-API/actions/runs/16792301463
------------------------------------------------------------
📊 Stats: 85.7% failure rate (last 21 runs)
```

## 🎯 Quick Commands

| Command | What it does |
|---------|-------------|
| `bin/failures` | Show last 5 failures |
| `bin/failures 10` | Show last 10 failures |
| `python3 scripts/check_failures.py 20` | Show last 20 failures |

## 🔧 How It Works

1. **Reads token from `.env`** - No need to export variables
2. **Auto-detects repository** - Works from any folder in the project
3. **Shows failure details** - Time, branch, author, message, link
4. **Calculates stats** - Shows failure rate percentage

## 💡 Pro Tips

### Add to your shell profile for global access:
```bash
echo 'alias failures="python3 /mnt/c/Projects/Napkin-AI-API/scripts/check_failures.py"' >> ~/.bashrc
source ~/.bashrc

# Now from anywhere:
failures
failures 10
```

### Morning routine:
```bash
# Check what failed overnight
bin/failures 10
```

### Click any URL to see full logs:
The script shows direct links to each failed run - just Ctrl+Click (or Cmd+Click on Mac) to open in browser.

## 🐛 Troubleshooting

### If you see "No GitHub token found":
- Check `.env` file has: `GITHUB_TOKEN=ghp_yourtoken`
- Make sure you're in the project directory

### If you see 403 errors:
- Your token might be expired
- Generate a new one at: https://github.com/settings/tokens

### If you see high failure rate:
- Click the URLs to investigate the actual failures
- Most recent failures show first

## 📁 Files Created

- `scripts/check_failures.py` - Main script (reads from .env)
- `bin/failures` - Convenient shortcut command
- `.env` - Contains your GitHub token (already configured)

## ✨ You're All Set!

Just run `bin/failures` anytime to check recent CI failures!