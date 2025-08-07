#!/bin/bash
# Super simple script to get recent GitHub Actions failures
# Usage: ./failures.sh [number_of_failures]

# Number of failures to fetch (default: 5)
LIMIT=${1:-5}

# Get repo from current directory
REPO=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

if [ -z "$REPO" ]; then
    echo "❌ Could not detect GitHub repository"
    exit 1
fi

echo "📂 Repository: $REPO"
echo "🔍 Fetching last $LIMIT failures..."
echo ""

# Use GitHub CLI if available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    gh run list --repo "$REPO" --status failure --limit "$LIMIT" --json conclusion,createdAt,displayTitle,headBranch,name,number,url,headSha | \
    jq -r '.[] | "❌ \(.name) #\(.number)\n   📅 \(.createdAt)\n   🌿 \(.headBranch)\n   🔗 \(.url)\n"'
else
    # Fallback to curl
    echo "Using GitHub API..."
    
    # Check for token
    if [ -z "$GITHUB_TOKEN" ]; then
        AUTH=""
        echo "⚠️  No GITHUB_TOKEN set, API rate limits will apply"
    else
        AUTH="-H \"Authorization: token $GITHUB_TOKEN\""
    fi
    
    # Fetch failures
    curl -s $AUTH \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$REPO/actions/runs?status=completed&per_page=50" | \
    jq -r --arg limit "$LIMIT" '
        .workflow_runs | 
        map(select(.conclusion == "failure")) | 
        .[:($limit | tonumber)] | 
        .[] | 
        "❌ \(.name) #\(.run_number)\n   📅 \(.created_at)\n   🌿 \(.head_branch)\n   👤 \(.head_commit.author.name)\n   💬 \(.head_commit.message | split("\n")[0][:50])\n   🔗 \(.html_url)\n"
    '
fi

echo ""
echo "To see more details, click on any URL above"