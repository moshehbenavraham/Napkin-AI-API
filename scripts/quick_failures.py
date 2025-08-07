#!/usr/bin/env python3
"""
Ultra-simple GitHub Actions failure checker
Usage: python quick_failures.py [number]
"""

import sys
import json
import urllib.request
import os
from datetime import datetime

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
        print("Set GITHUB_REPOSITORY env var or run from a git repo")
        sys.exit(1)

# Make API request
token = os.environ.get('GITHUB_TOKEN', '')
headers = {'Authorization': f'token {token}'} if token else {}
req = urllib.request.Request(
    f'https://api.github.com/repos/{repo}/actions/runs?status=completed&per_page=50',
    headers=headers
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        
    # Filter failures and show them
    failures = [r for r in data['workflow_runs'] if r['conclusion'] == 'failure'][:n]
    
    if not failures:
        print("✅ No recent failures!")
    else:
        print(f"\n🚨 Last {len(failures)} failures in {repo}:\n")
        for run in failures:
            date = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            print(f"❌ {date.strftime('%m/%d %H:%M')} - {run['name'][:30]} - {run['head_branch'][:20]}")
            print(f"   {run['html_url']}\n")
            
except Exception as e:
    print(f"Error: {e}")
    print("Make sure GITHUB_TOKEN is set for private repos")