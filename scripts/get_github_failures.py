#!/usr/bin/env python3
"""
Simple script to fetch recent GitHub Actions failures
Usage: python get_github_failures.py [--last N] [--repo owner/name] [--token YOUR_TOKEN]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import requests


def get_workflow_runs(repo: str, token: str = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch recent workflow runs from GitHub"""
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Get all workflow runs (failed and successful)
    url = f"https://api.github.com/repos/{repo}/actions/runs"
    params = {
        "per_page": min(limit * 2, 100),  # Get extra to ensure we have enough failures
        "status": "completed"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("workflow_runs", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching workflow runs: {e}")
        sys.exit(1)


def filter_failures(runs: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    """Filter and return only failed runs"""
    failures = [run for run in runs if run.get("conclusion") == "failure"]
    return failures[:limit]


def get_job_details(repo: str, run_id: int, token: str = None) -> List[Dict[str, Any]]:
    """Get job details for a specific workflow run"""
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("jobs", [])
    except:
        return []


def format_failure(run: Dict[str, Any], repo: str, include_jobs: bool = False, token: str = None) -> str:
    """Format a failure for display"""
    
    # Parse timestamp
    created_at = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    time_ago = datetime.utcnow() - created_at
    
    if time_ago.days > 0:
        time_str = f"{time_ago.days}d ago"
    elif time_ago.seconds > 3600:
        time_str = f"{time_ago.seconds // 3600}h ago"
    else:
        time_str = f"{time_ago.seconds // 60}m ago"
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"❌ {run['name']} - {time_str}")
    output.append(f"{'='*60}")
    output.append(f"📅 Date: {created_at.strftime('%Y-%m-%d %H:%M UTC')}")
    output.append(f"🔢 Run: #{run['run_number']}")
    output.append(f"🌿 Branch: {run['head_branch']}")
    output.append(f"👤 Author: {run['head_commit']['author']['name']}")
    output.append(f"💬 Message: {run['head_commit']['message'].split(chr(10))[0][:50]}")
    output.append(f"🔗 URL: {run['html_url']}")
    
    if include_jobs:
        jobs = get_job_details(repo, run['id'], token)
        failed_jobs = [job for job in jobs if job.get('conclusion') == 'failure']
        if failed_jobs:
            output.append(f"\n  Failed Steps:")
            for job in failed_jobs:
                output.append(f"  • {job['name']}")
                for step in job.get('steps', []):
                    if step.get('conclusion') == 'failure':
                        output.append(f"    - {step['name']}")
    
    return "\n".join(output)


def format_simple(runs: List[Dict[str, Any]]) -> str:
    """Simple one-line format for each failure"""
    
    output = []
    output.append(f"\n🚨 Last {len(runs)} Failures:")
    output.append("-" * 60)
    
    for run in runs:
        created_at = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = created_at.strftime("%m/%d %H:%M")
        branch = run['head_branch'][:15].ljust(15)
        name = run['name'][:25].ljust(25)
        author = run['head_commit']['author']['name'].split()[0][:10]
        
        output.append(f"{date_str} | {branch} | {name} | by {author}")
    
    return "\n".join(output)


def export_json(runs: List[Dict[str, Any]], filename: str):
    """Export failures to JSON file"""
    
    data = {
        "exported_at": datetime.utcnow().isoformat(),
        "count": len(runs),
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
            for run in runs
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Exported {len(runs)} failures to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Fetch recent GitHub Actions failures")
    parser.add_argument("--last", "-n", type=int, default=5, help="Number of failures to fetch (default: 5)")
    parser.add_argument("--repo", "-r", help="Repository (owner/name). Defaults to current git repo")
    parser.add_argument("--token", "-t", help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--simple", "-s", action="store_true", help="Simple one-line output format")
    parser.add_argument("--jobs", "-j", action="store_true", help="Include failed job details")
    parser.add_argument("--export", "-e", help="Export to JSON file")
    parser.add_argument("--all", "-a", action="store_true", help="Show all runs, not just failures")
    
    args = parser.parse_args()
    
    # Get repository
    repo = args.repo
    if not repo:
        # Try to get from current git repository
        try:
            import subprocess
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True
            )
            url = result.stdout.strip()
            # Extract owner/repo from URL
            if "github.com" in url:
                if url.startswith("git@"):
                    repo = url.split(":")[-1].replace(".git", "")
                else:
                    repo = "/".join(url.split("/")[-2:]).replace(".git", "")
            else:
                print("❌ Could not detect GitHub repository. Please specify with --repo")
                sys.exit(1)
        except:
            print("❌ Could not detect GitHub repository. Please specify with --repo")
            sys.exit(1)
    
    # Get token
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("⚠️  No GitHub token provided. API rate limits will apply.")
        print("   Set GITHUB_TOKEN env var or use --token flag for better access.")
    
    print(f"📂 Repository: {repo}")
    print(f"🔍 Fetching last {args.last} {'runs' if args.all else 'failures'}...")
    
    # Fetch runs
    runs = get_workflow_runs(repo, token, args.last if args.all else args.last * 3)
    
    if not args.all:
        runs = filter_failures(runs, args.last)
    else:
        runs = runs[:args.last]
    
    if not runs:
        print("✅ No failures found! Great job! 🎉")
        return
    
    # Export if requested
    if args.export:
        export_json(runs, args.export)
    
    # Display results
    if args.simple:
        print(format_simple(runs))
    else:
        for run in runs:
            print(format_failure(run, repo, args.jobs, token))
    
    # Summary
    print(f"\n📊 Summary: {len(runs)} {'runs' if args.all else 'failures'} found")
    
    if not args.all:
        # Calculate failure rate
        all_runs = get_workflow_runs(repo, token, 50)
        failure_rate = (len([r for r in all_runs if r.get('conclusion') == 'failure']) / len(all_runs)) * 100
        print(f"📈 Failure rate: {failure_rate:.1f}% (last {len(all_runs)} runs)")


if __name__ == "__main__":
    main()