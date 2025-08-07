#!/usr/bin/env python3
"""
GitHub Actions Error Reporter
Sends detailed error reports to various services
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import requests


class ErrorReporter:
    """Handle error reporting from GitHub Actions"""
    
    def __init__(self):
        self.github_context = self._load_github_context()
        self.error_data = self._collect_error_data()
    
    def _load_github_context(self) -> Dict[str, Any]:
        """Load GitHub Actions context from environment"""
        return {
            'repository': os.environ.get('GITHUB_REPOSITORY', ''),
            'ref': os.environ.get('GITHUB_REF', ''),
            'sha': os.environ.get('GITHUB_SHA', ''),
            'actor': os.environ.get('GITHUB_ACTOR', ''),
            'workflow': os.environ.get('GITHUB_WORKFLOW', ''),
            'run_id': os.environ.get('GITHUB_RUN_ID', ''),
            'run_number': os.environ.get('GITHUB_RUN_NUMBER', ''),
            'event_name': os.environ.get('GITHUB_EVENT_NAME', ''),
            'server_url': os.environ.get('GITHUB_SERVER_URL', 'https://github.com'),
        }
    
    def _collect_error_data(self) -> Dict[str, Any]:
        """Collect error data from environment and logs"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'context': self.github_context,
            'run_url': f"{self.github_context['server_url']}/{self.github_context['repository']}/actions/runs/{self.github_context['run_id']}",
            'environment': {
                'python_version': sys.version,
                'runner_os': os.environ.get('RUNNER_OS', ''),
                'runner_arch': os.environ.get('RUNNER_ARCH', ''),
            }
        }
    
    def send_to_slack(self, webhook_url: str) -> bool:
        """Send error notification to Slack"""
        if not webhook_url:
            print("No Slack webhook URL provided")
            return False
        
        message = {
            "text": f"🚨 Build Failed in {self.github_context['repository']}",
            "attachments": [{
                "color": "danger",
                "fields": [
                    {"title": "Repository", "value": self.github_context['repository'], "short": True},
                    {"title": "Branch", "value": self.github_context['ref'].replace('refs/heads/', ''), "short": True},
                    {"title": "Author", "value": self.github_context['actor'], "short": True},
                    {"title": "Workflow", "value": self.github_context['workflow'], "short": True},
                    {"title": "Commit", "value": self.github_context['sha'][:7], "short": True},
                    {"title": "Run Number", "value": self.github_context['run_number'], "short": True},
                ],
                "actions": [{
                    "type": "button",
                    "text": "View Logs",
                    "url": self.error_data['run_url']
                }]
            }]
        }
        
        try:
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            print("✅ Slack notification sent successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to send Slack notification: {e}")
            return False
    
    def send_to_discord(self, webhook_url: str) -> bool:
        """Send error notification to Discord"""
        if not webhook_url:
            print("No Discord webhook URL provided")
            return False
        
        message = {
            "username": "GitHub Actions",
            "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "embeds": [{
                "title": "🚨 Build Failed",
                "description": f"Build failed in **{self.github_context['repository']}**",
                "color": 15158332,  # Red color
                "fields": [
                    {"name": "Branch", "value": self.github_context['ref'].replace('refs/heads/', ''), "inline": True},
                    {"name": "Author", "value": self.github_context['actor'], "inline": True},
                    {"name": "Workflow", "value": self.github_context['workflow'], "inline": True},
                    {"name": "Commit", "value": f"`{self.github_context['sha'][:7]}`", "inline": True},
                ],
                "footer": {
                    "text": f"Run #{self.github_context['run_number']}"
                },
                "timestamp": self.error_data['timestamp'],
                "url": self.error_data['run_url']
            }]
        }
        
        try:
            response = requests.post(webhook_url, json=message)
            response.raise_for_status()
            print("✅ Discord notification sent successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to send Discord notification: {e}")
            return False
    
    def send_to_api(self, api_url: str, api_token: Optional[str] = None) -> bool:
        """Send error data to custom API endpoint"""
        if not api_url:
            print("No API URL provided")
            return False
        
        headers = {"Content-Type": "application/json"}
        if api_token:
            headers["Authorization"] = f"Bearer {api_token}"
        
        try:
            response = requests.post(api_url, json=self.error_data, headers=headers)
            response.raise_for_status()
            print("✅ Error data sent to API successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to send to API: {e}")
            return False
    
    def create_github_issue(self, token: str) -> bool:
        """Create a GitHub issue for the failure"""
        if not token:
            print("No GitHub token provided")
            return False
        
        repo_parts = self.github_context['repository'].split('/')
        if len(repo_parts) != 2:
            print(f"Invalid repository format: {self.github_context['repository']}")
            return False
        
        owner, repo = repo_parts
        api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        
        issue_data = {
            "title": f"🚨 Build Failed: {self.github_context['sha'][:7]}",
            "body": f"""## Build Failure Report

**Workflow:** {self.github_context['workflow']}
**Run ID:** {self.github_context['run_id']}
**Branch:** {self.github_context['ref'].replace('refs/heads/', '')}
**Commit:** {self.github_context['sha']}
**Author:** @{self.github_context['actor']}

### Environment
- **Event:** {self.github_context['event_name']}
- **Runner OS:** {self.error_data['environment']['runner_os']}
- **Python Version:** {self.error_data['environment']['python_version'].split()[0]}

[View Logs]({self.error_data['run_url']})

---
*This issue was automatically created by GitHub Actions*""",
            "labels": ["bug", "ci-failure", "automated"]
        }
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.post(api_url, json=issue_data, headers=headers)
            response.raise_for_status()
            issue_url = response.json().get('html_url', '')
            print(f"✅ GitHub issue created: {issue_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to create GitHub issue: {e}")
            return False
    
    def save_to_file(self, filepath: str = "error_report.json") -> bool:
        """Save error data to a file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.error_data, f, indent=2)
            print(f"✅ Error report saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to save error report: {e}")
            return False


def main():
    """Main entry point for error reporting"""
    reporter = ErrorReporter()
    
    # Get configuration from environment
    slack_webhook = os.environ.get('SLACK_WEBHOOK')
    discord_webhook = os.environ.get('DISCORD_WEBHOOK')
    api_url = os.environ.get('ERROR_API_URL')
    api_token = os.environ.get('ERROR_API_TOKEN')
    github_token = os.environ.get('GITHUB_TOKEN')
    create_issue = os.environ.get('CREATE_GITHUB_ISSUE', 'false').lower() == 'true'
    
    # Send notifications
    success = False
    
    if slack_webhook:
        success |= reporter.send_to_slack(slack_webhook)
    
    if discord_webhook:
        success |= reporter.send_to_discord(discord_webhook)
    
    if api_url:
        success |= reporter.send_to_api(api_url, api_token)
    
    if create_issue and github_token:
        success |= reporter.create_github_issue(github_token)
    
    # Always save to file for debugging
    reporter.save_to_file()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()