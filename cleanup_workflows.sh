#!/bin/bash

# GitHub repository bilgileri
REPO_OWNER="cemremete"
REPO_NAME="test-automation-project"

echo "Cleaning up old workflow runs..."

# GitHub API ile workflow runs listesini al ve sil
# Son 5 run'ı koru, geri kalanını sil
curl -s -H "Accept: application/vnd.github.v3+json" \
     "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs?per_page=100" | \
jq -r '.workflow_runs[] | select(.run_number > 5) | .id' | \
while read run_id; do
    echo "Deleting workflow run ID: $run_id"
    curl -X DELETE \
         -H "Accept: application/vnd.github.v3+json" \
         -H "Authorization: token $GITHUB_TOKEN" \
         "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/runs/$run_id"
    sleep 1  # Rate limiting
done

echo "Cleanup completed!"