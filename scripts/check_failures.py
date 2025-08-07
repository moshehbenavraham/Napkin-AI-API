#!/usr/bin/env python3
"""
Automated GitHub Actions failure checker
Reads token from .env file automatically
Usage: python scripts/check_failures.py [number]
"""

import sys
import json
import urllib.request
import os
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
def load_env():
    """Load variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Check for both GITHUB_API_TOKEN and the typo GITHUT_API_TOKEN
                    if key.strip() in ['GITHUB_API_TOKEN', 'GITHUT_API_TOKEN', 'GITHUB_TOKEN']:
                        os.environ['GITHUB_TOKEN'] = value.strip()

# Load env vars
load_env()

# Get number of failures to show
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# Get repo (try from git or use environment variable)
repo = os.environ.get('GITHUB_REPOSITORY', '')
if not repo:
    try:
        import subprocess
        url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
        repo = url.split('github.com')[-1].strip('/:').replace('.git', '')
    except:
        print("❌ Could not detect GitHub repository")
        print("Run from inside your git repo or set GITHUB_REPOSITORY")
        sys.exit(1)

# Get token (now automatically loaded from .env)
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    print("⚠️  No GitHub token found in .env file")
    print("   Add GITHUB_TOKEN=ghp_yourtoken to .env file")
else:
    print(f"✅ Using GitHub token from .env file")

# Make API request
headers = {'Authorization': f'token {token}'} if token else {}
req = urllib.request.Request(
    f'https://api.github.com/repos/{repo}/actions/runs?status=completed&per_page=50',
    headers=headers
)

print(f"📂 Repository: {repo}")
print(f"🔍 Fetching last {n} failures...\n")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        
    # Filter failures and show them
    failures = [r for r in data['workflow_runs'] if r['conclusion'] == 'failure'][:n]
    
    if not failures:
        print("✅ No recent failures! Great job! 🎉")
    else:
        print(f"🚨 Last {len(failures)} failures:\n")
        print("-" * 60)
        for run in failures:
            date = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            
            # Calculate time ago
            time_ago = datetime.utcnow() - date
            if time_ago.days > 0:
                time_str = f"{time_ago.days}d ago"
            elif time_ago.seconds > 3600:
                time_str = f"{time_ago.seconds // 3600}h ago"
            else:
                time_str = f"{time_ago.seconds // 60}m ago"
            
            print(f"❌ {run['name']} #{run['run_number']} - {time_str}")
            print(f"   📅 {date.strftime('%Y-%m-%d %H:%M UTC')}")
            print(f"   🌿 Branch: {run['head_branch']}")
            print(f"   👤 Author: {run['head_commit']['author']['name']}")
            print(f"   💬 {run['head_commit']['message'].split(chr(10))[0][:50]}")
            print(f"   🔗 {run['html_url']}")
            print()
        
        # Quick stats
        all_runs = data['workflow_runs'][:50]
        total_failures = len([r for r in all_runs if r['conclusion'] == 'failure'])
        if len(all_runs) > 0:
            failure_rate = (total_failures / len(all_runs)) * 100
            print("-" * 60)
            print(f"📊 Stats: {failure_rate:.1f}% failure rate (last {len(all_runs)} runs)")
            
except urllib.error.HTTPError as e:
    if e.code == 403:
        print(f"❌ Error 403: API rate limit or bad token")
        print("   Check your GitHub token in .env file")
    elif e.code == 404:
        print(f"❌ Error 404: Repository not found or private")
        print(f"   Attempted repo: {repo}")
    else:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Make sure your GitHub token is valid")