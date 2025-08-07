# Setup Guide for GitHub Failure Scripts

## 🔑 Step 1: Get GitHub Token (Recommended)

### Option A: Create a Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "CI Failure Checker"
4. Select scopes:
   - For PUBLIC repos: Check `public_repo`
   - For PRIVATE repos: Check `repo`
5. Click "Generate token"
6. **COPY THE TOKEN NOW** (you won't see it again!)

### Option B: Use GitHub CLI Token (if you have gh installed)
```bash
# If you have GitHub CLI installed and authenticated
gh auth status
# Your token is already configured!
```

## 🔧 Step 2: Set Up Environment

### Linux/Mac:
```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_YourTokenHere"
export GITHUB_REPOSITORY="YourUsername/YourRepo"  # Optional

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

### Windows (PowerShell):
```powershell
# Add to your PowerShell profile
$env:GITHUB_TOKEN = "ghp_YourTokenHere"
$env:GITHUB_REPOSITORY = "YourUsername/YourRepo"  # Optional
```

### Windows (Command Prompt):
```cmd
set GITHUB_TOKEN=ghp_YourTokenHere
set GITHUB_REPOSITORY=YourUsername/YourRepo
```

## 📦 Step 3: Install Requirements

### Check Python is installed:
```bash
python --version  # or python3 --version
# Should be 3.6 or higher
```

### No additional packages needed!
The scripts use only Python standard library.

## 🎯 Step 4: Test the Scripts

### 1. Navigate to your repo:
```bash
cd /path/to/your/napkin-api-repo
```

### 2. Try the simplest script:
```bash
python scripts/quick_failures.py
```

### Expected output:
```
🚨 Last 5 failures in YourUsername/YourRepo:

❌ 01/07 15:23 - CI Pipeline - main
   https://github.com/YourUsername/YourRepo/actions/runs/123456
   
(or "✅ No recent failures!" if no failures)
```

## 🐛 Troubleshooting

### Error: "Set GITHUB_REPOSITORY env var or run from a git repo"

**Solution 1**: Run from inside your git repository
```bash
cd /mnt/c/Projects/Napkin-AI-API
python scripts/quick_failures.py
```

**Solution 2**: Set the repository manually
```bash
export GITHUB_REPOSITORY="moshehbenavraham/Napkin-AI-API"
python scripts/quick_failures.py
```

### Error: "403 Forbidden" or "API rate limit exceeded"

**Solution**: You need a GitHub token
```bash
export GITHUB_TOKEN="ghp_YourActualTokenHere"
```

### Error: "python: command not found"

**Solution**: Use python3 instead
```bash
python3 scripts/quick_failures.py
```

### Error: "No module named 'requests'"

**Solution**: Use the quick_failures.py script instead (no dependencies)
```bash
python scripts/quick_failures.py
```

## ✅ Quick Test Commands

Copy and paste these to test quickly:

### Test without token (public repos only, limited):
```bash
cd /mnt/c/Projects/Napkin-AI-API
python scripts/quick_failures.py 3
```

### Test with token:
```bash
cd /mnt/c/Projects/Napkin-AI-API
export GITHUB_TOKEN="ghp_YourTokenHere"
python scripts/quick_failures.py 5
```

### Test with specific repo:
```bash
export GITHUB_REPOSITORY="facebook/react"  # Example public repo
python scripts/quick_failures.py 5
```

## 📝 Full Example Session

```bash
# 1. Set your token (one time)
export GITHUB_TOKEN="ghp_abc123..."

# 2. Go to your repo
cd /mnt/c/Projects/Napkin-AI-API

# 3. Check last 5 failures
python scripts/quick_failures.py 5

# 4. Get more details
python scripts/get_github_failures.py --last 3 --jobs

# 5. Export to file
python scripts/get_github_failures.py --export failures.json
```

## 🎉 Success Indicators

You know it's working when you see:
- ✅ "No recent failures!" - Your CI is perfect!
- ❌ List of failures with dates and links
- 📂 "Repository: YourUsername/YourRepo" message

## 💡 Pro Tips

1. **Add an alias** for quick access:
   ```bash
   echo 'alias failures="python ~/Projects/Napkin-AI-API/scripts/quick_failures.py"' >> ~/.bashrc
   source ~/.bashrc
   # Now just type: failures
   ```

2. **Check specific repos** without cd:
   ```bash
   GITHUB_REPOSITORY="vercel/next.js" python scripts/quick_failures.py
   ```

3. **Morning routine**:
   ```bash
   python scripts/quick_failures.py 10  # See overnight failures
   ```

## 🔒 Security Note

NEVER commit your token to git! Add to .gitignore:
```bash
echo "GITHUB_TOKEN=*" >> .gitignore
```