# GitHub Actions Error Monitoring Setup

This guide explains how to set up automated error notifications from GitHub Actions.

## 🚀 Quick Setup

### 1. Choose Your Notification Method

#### Option A: Slack Notifications

1. Create a Slack Webhook:
   - Go to https://api.slack.com/apps
   - Create new app → From scratch
   - Add "Incoming Webhooks" feature
   - Create webhook for your channel
   - Copy the webhook URL

2. Add to GitHub Secrets:
   ```
   Repository Settings → Secrets → Actions → New repository secret
   Name: SLACK_WEBHOOK
   Value: [Your Slack webhook URL]
   ```

#### Option B: Discord Notifications

1. Create Discord Webhook:
   - Server Settings → Integrations → Webhooks
   - New Webhook → Copy webhook URL

2. Add to GitHub Secrets:
   ```
   Name: DISCORD_WEBHOOK
   Value: [Your Discord webhook URL]
   ```

#### Option C: Email Notifications

1. For Gmail:
   - Enable 2FA on your Google account
   - Generate app-specific password
   - Add secrets:
     ```
     EMAIL_USERNAME: your-email@gmail.com
     EMAIL_PASSWORD: [app-specific password]
     NOTIFICATION_EMAIL: recipient@example.com
     ```

### 2. Enable the Workflow

Choose one of these workflows based on your needs:

#### Basic Error Monitor (Recommended)
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        run: |
          # Your test commands here
          poetry run pytest
      
      - name: Notify on Failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"❌ Build failed in ${{ github.repository }}"}'
```

#### Advanced Error Reporting
Use the provided `error-notifications.yml` for comprehensive error reporting with multiple notification channels.

### 3. Custom Error Reporter

For advanced error handling, use the Python error reporter:

```yaml
- name: Report Errors
  if: failure()
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    CREATE_GITHUB_ISSUE: true
  run: |
    python .github/scripts/error_reporter.py
```

## 📊 Monitoring Services Integration

### Datadog
```yaml
- name: Send to Datadog
  if: failure()
  run: |
    curl -X POST "https://api.datadoghq.com/api/v1/events" \
      -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
      -H "Content-Type: application/json" \
      -d '{
        "title": "GitHub Action Failed",
        "text": "Build failed in ${{ github.repository }}",
        "alert_type": "error",
        "tags": ["env:production", "service:ci"]
      }'
```

### PagerDuty (for critical failures)
```yaml
- name: PagerDuty Alert
  if: failure() && github.ref == 'refs/heads/main'
  uses: Entle/action-pagerduty-alert@v1
  with:
    pagerduty-integration-key: ${{ secrets.PAGERDUTY_KEY }}
```

### Sentry
```yaml
- name: Create Sentry Release
  if: failure()
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: your-org
    SENTRY_PROJECT: your-project
  run: |
    curl -X POST \
      "https://sentry.io/api/0/projects/${SENTRY_ORG}/${SENTRY_PROJECT}/events/" \
      -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
      -H "Content-Type: application/json" \
      -d '{
        "level": "error",
        "message": "GitHub Action failed",
        "tags": {
          "repository": "${{ github.repository }}",
          "workflow": "${{ github.workflow }}"
        }
      }'
```

## 🔧 Required Secrets

Add these secrets to your repository (Settings → Secrets → Actions):

| Secret Name | Description | Required |
|------------|-------------|----------|
| `SLACK_WEBHOOK` | Slack incoming webhook URL | For Slack |
| `DISCORD_WEBHOOK` | Discord webhook URL | For Discord |
| `EMAIL_USERNAME` | SMTP username | For Email |
| `EMAIL_PASSWORD` | SMTP password | For Email |
| `NOTIFICATION_EMAIL` | Recipient email | For Email |
| `ERROR_API_URL` | Custom API endpoint | For custom API |
| `ERROR_API_TOKEN` | API authentication token | For custom API |
| `DATADOG_API_KEY` | Datadog API key | For Datadog |
| `PAGERDUTY_KEY` | PagerDuty integration key | For PagerDuty |

## 📝 Message Formatting

### Slack Rich Messages
```json
{
  "blocks": [{
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*Build Failed* 🚨\n*Repo:* `${{ github.repository }}`"
    }
  }]
}
```

### Discord Embeds
```json
{
  "embeds": [{
    "title": "Build Failed",
    "color": 15158332,
    "fields": [
      {"name": "Repository", "value": "${{ github.repository }}"}
    ]
  }]
}
```

## 🎯 Best Practices

1. **Use Conditional Notifications**
   ```yaml
   if: failure() && github.ref == 'refs/heads/main'
   ```

2. **Group Related Errors**
   ```yaml
   - name: Collect All Errors
     if: always()
     run: |
       echo "Test: ${{ steps.test.outcome }}" >> errors.txt
       echo "Lint: ${{ steps.lint.outcome }}" >> errors.txt
   ```

3. **Rate Limit Notifications**
   - Use GitHub Issues for persistent tracking
   - Use Slack/Discord for immediate alerts
   - Use PagerDuty only for critical production issues

4. **Include Useful Context**
   - Commit SHA
   - Branch name
   - Author
   - Direct link to logs
   - Error messages

5. **Test Your Notifications**
   ```yaml
   - name: Test Notification
     run: |
       curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
         -d '{"text":"Test notification from GitHub Actions"}'
   ```

## 🔍 Debugging

### Check Webhook is Working
```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test message"}'
```

### View GitHub Context
```yaml
- name: Dump GitHub context
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
  run: echo "$GITHUB_CONTEXT"
```

### Common Issues

1. **Webhook not firing**: Check if condition is correct
2. **403 Forbidden**: Check webhook URL and permissions
3. **No notification**: Verify secrets are set correctly
4. **Rate limited**: Implement backoff or reduce frequency

## 📚 Examples

### Notify Only on Main Branch Failures
```yaml
if: failure() && github.ref == 'refs/heads/main'
```

### Notify Only for Push Events
```yaml
if: failure() && github.event_name == 'push'
```

### Different Channels for Different Branches
```yaml
- name: Notify Production
  if: failure() && github.ref == 'refs/heads/main'
  env:
    WEBHOOK: ${{ secrets.PROD_WEBHOOK }}
    
- name: Notify Development
  if: failure() && github.ref == 'refs/heads/develop'
  env:
    WEBHOOK: ${{ secrets.DEV_WEBHOOK }}
```

## 🔍 Monitoring Tools

### Quick Failure Check Scripts

The project includes convenient scripts for checking GitHub Actions failures:

#### Using bin/failures
```bash
# Check last 5 failures (default)
bin/failures

# Check last 10 failures
bin/failures 10
```

#### Python Scripts Available
- **scripts/check_failures.py** - Main failure checking script with .env support
- **scripts/get_github_failures.py** - Advanced analysis with export options
- **scripts/quick_failures.py** - Lightweight single-file script
- **scripts/failures.sh** - Bash alternative using GitHub CLI or curl

#### Setup Requirements
1. Add `GITHUB_TOKEN` to your `.env` file:
   ```
   GITHUB_TOKEN=ghp_yourtoken
   ```

2. Token permissions needed:
   - `repo` (for private repos)
   - `public_repo` (for public repos only)

### CI/CD Status
As of v0.3.2:
- ✅ Python 3.10+ compatibility fixed
- ✅ All tests passing
- ✅ Type checking clean
- ✅ Code formatting validated
- ✅ Security checks enabled

## 🔗 Resources

- [GitHub Actions Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitHub Actions Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Discord Embed Visualizer](https://autocode.com/tools/discord/embed-builder/)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)

---

Last updated: 2025-08-07 (v0.3.2)