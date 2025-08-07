#!/usr/bin/env python3
"""
GitHub Actions failure checker with advanced features
Reads token from .env file automatically
Usage: python scripts/check_failures.py [number] [--json output.json] [--simple]
"""

import sys
import json
import urllib.request
import urllib.error
import os
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

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

def get_repo() -> Optional[str]:
    """Get repository from environment or git"""
    repo = os.environ.get('GITHUB_REPOSITORY', '')
    if not repo:
        try:
            import subprocess
            url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
            repo = url.split('github.com')[-1].strip('/:').replace('.git', '')
        except Exception:
            return None
    return repo

def fetch_runs(repo: str, token: Optional[str] = None) -> Dict[str, Any]:
    """Fetch workflow runs from GitHub API"""
    headers = {'Authorization': f'token {token}'} if token else {}
    req = urllib.request.Request(
        f'https://api.github.com/repos/{repo}/actions/runs?status=completed&per_page=50',
        headers=headers
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def format_time_ago(date: datetime) -> str:
    """Format time difference as human-readable string"""
    time_ago = datetime.now(timezone.utc).replace(tzinfo=None) - date
    if time_ago.days > 0:
        return f"{time_ago.days}d ago"
    elif time_ago.seconds > 3600:
        return f"{time_ago.seconds // 3600}h ago"
    else:
        return f"{time_ago.seconds // 60}m ago"

def display_failures(failures: List[Dict[str, Any]], simple: bool = False):
    """Display failures in formatted output"""
    if not failures:
        print("✅ No recent failures! Great job! 🎉")
        return
    
    print(f"🚨 Last {len(failures)} failures:\n")
    print("-" * 60)
    
    for run in failures:
        date = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        time_str = format_time_ago(date)
        
        if simple:
            # Simple one-line format
            print(f"❌ {date.strftime('%m/%d %H:%M')} - {run['name'][:30]} - {run['head_branch'][:20]}")
        else:
            # Detailed format
            print(f"❌ {run['name']} #{run['run_number']} - {time_str}")
            print(f"   📅 {date.strftime('%Y-%m-%d %H:%M UTC')}")
            print(f"   🌿 Branch: {run['head_branch']}")
            print(f"   👤 Author: {run['head_commit']['author']['name']}")
            print(f"   💬 {run['head_commit']['message'].split(chr(10))[0][:50]}")
            print(f"   🔗 {run['html_url']}")
            print()

def export_json(failures: List[Dict[str, Any]], filename: str):
    """Export failures to JSON file"""
    data = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "count": len(failures),
        "failures": [
            {
                "id": run["id"],
                "name": run["name"],
                "run_number": run["run_number"],
                "created_at": run["created_at"],
                "branch": run["head_branch"],
                "author": run["head_commit"]["author"]["name"],
                "message": run["head_commit"]["message"],
                "url": run["html_url"],
                "commit_sha": run["head_sha"]
            }
            for run in failures
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Exported {len(failures)} failures to {filename}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Check GitHub Actions failures")
    parser.add_argument('count', nargs='?', type=int, default=5, help='Number of failures to show')
    parser.add_argument('--json', '-j', metavar='FILE', help='Export failures to JSON file')
    parser.add_argument('--simple', '-s', action='store_true', help='Simple one-line output format')
    args = parser.parse_args()
    
    # Load environment
    load_env()
    
    # Get repo
    repo = get_repo()
    if not repo:
        print("❌ Could not detect GitHub repository")
        print("Run from inside your git repo or set GITHUB_REPOSITORY")
        sys.exit(1)
    
    # Get token
    token = os.environ.get('GITHUB_TOKEN', '')
    if not token:
        print("⚠️  No GitHub token found in .env file")
        print("   Add GITHUB_TOKEN=ghp_yourtoken to .env file")
    else:
        print("✅ Using GitHub token from .env file")
    
    print(f"📂 Repository: {repo}")
    print(f"🔍 Fetching last {args.count} failures...\n")
    
    try:
        # Fetch and filter failures
        data = fetch_runs(repo, token)
        all_runs = data['workflow_runs']
        failures = [r for r in all_runs if r['conclusion'] == 'failure'][:args.count]
        
        # Export if requested
        if args.json:
            export_json(failures, args.json)
        
        # Display failures
        display_failures(failures, args.simple)
        
        # Show stats
        if failures and not args.simple:
            total_failures = len([r for r in all_runs if r['conclusion'] == 'failure'])
            if all_runs:
                failure_rate = (total_failures / len(all_runs)) * 100
                print("-" * 60)
                print(f"📊 Stats: {failure_rate:.1f}% failure rate (last {len(all_runs)} runs)")
                
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("❌ Error 403: API rate limit or bad token")
            print("   Check your GitHub token in .env file")
        elif e.code == 404:
            print("❌ Error 404: Repository not found or private")
            print(f"   Attempted repo: {repo}")
        else:
            print(f"❌ HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure your GitHub token is valid")
        sys.exit(1)

if __name__ == "__main__":
    main()