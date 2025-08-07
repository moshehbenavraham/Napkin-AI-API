#!/usr/bin/env python3
"""
Unified GitHub Actions Monitor
Combines failure checking, log analysis, and error reporting in one tool.

Usage:
    gh_monitor                    # Show last 5 failures
    gh_monitor 10                 # Show last 10 failures
    gh_monitor analyze            # Analyze recent failures in detail
    gh_monitor report             # Generate error report for CI/CD context
    gh_monitor --json output.json # Export to JSON
    gh_monitor --webhook          # Send notifications to configured webhooks
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import requests  # type: ignore

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class GitHubMonitor:
    """Unified GitHub Actions monitoring tool"""

    def __init__(self):
        self.token = self._load_token()
        self.repo = self._get_repo()
        self.github_context = self._load_github_context()

    def _load_token(self) -> Optional[str]:
        """Load GitHub token from .env file"""
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip() in ["GITHUB_TOKEN", "GITHUB_API_TOKEN"]:
                            return value.strip().strip('"').strip("'")
        return os.environ.get("GITHUB_TOKEN")

    def _get_repo(self) -> Optional[str]:
        """Get repository from environment or git"""
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        if not repo:
            try:
                import subprocess

                url = subprocess.check_output(
                    ["git", "remote", "get-url", "origin"], text=True
                ).strip()
                repo = url.split("github.com")[-1].strip("/:").replace(".git", "")
            except Exception:
                return None
        return repo

    def _load_github_context(self) -> Dict[str, Any]:
        """Load GitHub Actions context from environment"""
        return {
            "repository": os.environ.get("GITHUB_REPOSITORY", self.repo or ""),
            "ref": os.environ.get("GITHUB_REF", ""),
            "sha": os.environ.get("GITHUB_SHA", ""),
            "actor": os.environ.get("GITHUB_ACTOR", ""),
            "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
            "run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "run_number": os.environ.get("GITHUB_RUN_NUMBER", ""),
            "event_name": os.environ.get("GITHUB_EVENT_NAME", ""),
            "server_url": os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
        }

    def _fetch(self, url: str) -> Any:
        """Fetch URL with authentication"""
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                if url.endswith("/logs"):
                    return response.read().decode("utf-8")
                else:
                    return json.loads(response.read())
        except urllib.error.HTTPError as e:
            if e.code != 403:  # Don't print for forbidden (logs often restricted)
                print(f"Error fetching {url}: {e.code}")
            return None

    def fetch_runs(self, per_page: int = 50) -> Dict[str, Any]:
        """Fetch workflow runs from GitHub API"""
        if not self.repo:
            raise ValueError("Repository not detected")
        url = f"https://api.github.com/repos/{self.repo}/actions/runs?status=completed&per_page={per_page}"
        return self._fetch(url)

    def format_time_ago(self, date: datetime) -> str:
        """Format time difference as human-readable string"""
        time_ago = datetime.now(timezone.utc).replace(tzinfo=None) - date
        if time_ago.days > 0:
            return f"{time_ago.days}d ago"
        elif time_ago.seconds > 3600:
            return f"{time_ago.seconds // 3600}h ago"
        else:
            return f"{time_ago.seconds // 60}m ago"

    def list_failures(self, count: int = 5, simple: bool = False) -> List[Dict]:
        """List recent failures"""
        print(f"📂 Repository: {self.repo}")
        print(f"🔍 Fetching last {count} failures...\n")

        data = self.fetch_runs()
        if not data:
            print("❌ Could not fetch workflow runs")
            return []

        all_runs = data["workflow_runs"]
        failures = [r for r in all_runs if r["conclusion"] == "failure"][:count]

        if not failures:
            print("✅ No recent failures! Great job! 🎉")
            return []

        print(f"🚨 Last {len(failures)} failures:\n")
        print("-" * 60)

        for run in failures:
            date = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            time_str = self.format_time_ago(date)

            if simple:
                print(
                    f"❌ {date.strftime('%m/%d %H:%M')} - {run['name'][:30]} - {run['head_branch'][:20]}"
                )
            else:
                print(f"❌ {run['name']} #{run['run_number']} - {time_str}")
                print(f"   📅 {date.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   🌿 Branch: {run['head_branch']}")
                print(f"   👤 Author: {run['head_commit']['author']['name']}")
                print(f"   💬 {run['head_commit']['message'].split(chr(10))[0][:50]}")
                print(f"   🔗 {run['html_url']}")
                print()

        # Show stats
        if failures and not simple:
            total_failures = len([r for r in all_runs if r["conclusion"] == "failure"])
            if all_runs:
                failure_rate = (total_failures / len(all_runs)) * 100
                print("-" * 60)
                print(
                    f"📊 Stats: {failure_rate:.1f}% failure rate (last {len(all_runs)} runs)"
                )

        return failures

    def analyze_failures(self, run_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        """Analyze specific workflow runs in detail"""
        if not run_ids:
            # Get recent failures
            data = self.fetch_runs(per_page=10)
            if not data:
                print("❌ Could not fetch workflow runs")
                return {}

            failures = [
                r for r in data["workflow_runs"] if r["conclusion"] == "failure"
            ][:3]
            run_ids = [r["id"] for r in failures]

        all_failures = []
        for run_id in run_ids:
            print(f"\n{'='*60}")
            print(f"Analyzing Run ID: {run_id}")
            print("=" * 60)

            # Get run details
            run_data = self._fetch(
                f"https://api.github.com/repos/{self.repo}/actions/runs/{run_id}"
            )
            if not run_data:
                continue

            print(f"Workflow: {run_data['name']}")
            print(f"Status: {run_data['status']}")
            print(f"Conclusion: {run_data['conclusion']}")
            print(f"Branch: {run_data['head_branch']}")
            print(f"Commit: {run_data['head_sha'][:8]}")

            # Get jobs
            jobs_data = self._fetch(
                f"https://api.github.com/repos/{self.repo}/actions/runs/{run_id}/jobs"
            )
            if not jobs_data:
                continue

            for job in jobs_data.get("jobs", []):
                if job["conclusion"] == "failure":
                    print(f"\n❌ Failed Job: {job['name']}")
                    all_failures.append(job)

                    # Show failed steps
                    for step in job.get("steps", []):
                        if step["conclusion"] == "failure":
                            print(f"   Failed Step: {step['name']}")

                    # Try to get logs
                    logs_url = f"https://api.github.com/repos/{self.repo}/actions/jobs/{job['id']}/logs"
                    logs = self._fetch(logs_url)

                    if logs:
                        error_lines = []
                        for line in logs.split("\n"):
                            if "error" in line.lower() or "failed" in line.lower():
                                error_lines.append(line.strip())

                        if error_lines:
                            print("\n   Key Error Messages:")
                            for error in error_lines[:5]:
                                if error:
                                    print(f"   > {error[:120]}")

        # Summary
        if all_failures:
            print(f"\n{'='*60}")
            print("SUMMARY OF FAILURES")
            print("=" * 60)

            job_names: Dict[str, int] = {}
            for job in all_failures:
                name = job["name"]
                job_names[name] = job_names.get(name, 0) + 1

            print("\nFailed Jobs by Frequency:")
            for name, count in sorted(
                job_names.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"  {name}: {count} failures")

        return {"failures": all_failures, "summary": job_names if all_failures else {}}

    def generate_report(self) -> Dict[str, Any]:
        """Generate error report for CI/CD context"""
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": self.github_context,
            "repository": self.repo,
        }

        if self.github_context["run_id"]:
            report[
                "run_url"
            ] = f"{self.github_context['server_url']}/{self.repo}/actions/runs/{self.github_context['run_id']}"

        report["environment"] = {
            "python_version": sys.version.split()[0],
            "runner_os": os.environ.get("RUNNER_OS", "local"),
            "runner_arch": os.environ.get("RUNNER_ARCH", "unknown"),
        }

        return report

    def send_webhook(self, webhook_url: str, webhook_type: str = "slack") -> bool:
        """Send notification to webhook"""
        if not HAS_REQUESTS:
            print("❌ requests library not available for webhooks")
            return False

        report = self.generate_report()

        if webhook_type == "slack":
            message = {
                "text": f"🚨 Build Failed in {self.repo}",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {"title": "Repository", "value": self.repo, "short": True},
                            {
                                "title": "Branch",
                                "value": self.github_context["ref"].replace(
                                    "refs/heads/", ""
                                ),
                                "short": True,
                            },
                            {
                                "title": "Author",
                                "value": self.github_context["actor"],
                                "short": True,
                            },
                            {
                                "title": "Workflow",
                                "value": self.github_context["workflow"],
                                "short": True,
                            },
                        ],
                        "actions": [
                            {
                                "type": "button",
                                "text": "View Logs",
                                "url": report.get("run_url", "#"),
                            }
                        ],
                    }
                ],
            }
        elif webhook_type == "discord":
            message = {
                "username": "GitHub Actions",
                "embeds": [
                    {
                        "title": "🚨 Build Failed",
                        "description": f"Build failed in **{self.repo}**",
                        "color": 15158332,
                        "fields": [
                            {
                                "name": "Branch",
                                "value": self.github_context["ref"].replace(
                                    "refs/heads/", ""
                                ),
                                "inline": True,
                            },
                            {
                                "name": "Author",
                                "value": self.github_context["actor"],
                                "inline": True,
                            },
                        ],
                        "timestamp": report["timestamp"],
                        "url": report.get("run_url", "#"),
                    }
                ],
            }
        else:
            message = report

        try:
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            print("✅ Webhook notification sent successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to send webhook: {e}")
            return False

    def export_json(self, failures: List[Dict], filename: str):
        """Export failures to JSON file"""
        data = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "repository": self.repo,
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
                    "commit_sha": run["head_sha"],
                }
                for run in failures
            ],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Exported {len(failures)} failures to {filename}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="GitHub Actions Monitor")

    # Check if first argument is a number (backward compatibility)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # Insert 'list' command before the number
        sys.argv.insert(1, "list")

    parser.add_argument(
        "command",
        nargs="?",
        default="list",
        choices=["list", "analyze", "report"],
        help="Command to run (default: list)",
    )
    parser.add_argument(
        "count",
        nargs="?",
        type=int,
        default=5,
        help="Number of failures to show (for list command)",
    )
    parser.add_argument("--json", "-j", metavar="FILE", help="Export to JSON file")
    parser.add_argument(
        "--simple", "-s", action="store_true", help="Simple one-line output format"
    )
    parser.add_argument(
        "--webhook", "-w", metavar="URL", help="Send notification to webhook"
    )
    parser.add_argument(
        "--webhook-type",
        choices=["slack", "discord", "custom"],
        default="slack",
        help="Type of webhook",
    )

    args = parser.parse_args()

    # Initialize monitor
    monitor = GitHubMonitor()

    if not monitor.repo:
        print("❌ Could not detect GitHub repository")
        print("Run from inside your git repo or set GITHUB_REPOSITORY")
        sys.exit(1)

    if not monitor.token:
        print("⚠️  No GitHub token found")
        print("   Add GITHUB_TOKEN to .env file for better API access")
    else:
        print("✅ Using GitHub token from .env file")

    # Handle commands
    if args.command == "analyze":
        monitor.analyze_failures()
    elif args.command == "report":
        report = monitor.generate_report()
        print(json.dumps(report, indent=2))
        if args.json:
            with open(args.json, "w") as f:
                json.dump(report, f, indent=2)
            print(f"✅ Report saved to {args.json}")
    else:  # list
        failures = monitor.list_failures(count=args.count, simple=args.simple)

        if args.json and failures:
            monitor.export_json(failures, args.json)

    # Send webhook if requested
    if args.webhook:
        monitor.send_webhook(args.webhook, args.webhook_type)


if __name__ == "__main__":
    main()
