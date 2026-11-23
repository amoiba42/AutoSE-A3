#!/usr/bin/env bash
# Run the autose workflow for issues one at a time, so parallel runs never share the Gemini quota.
# Usage: scripts/run_issues.sh [-R owner/repo] [-g SECONDS] ISSUE [ISSUE...]
#   -g  gap in seconds between runs (default 60), lets per-minute quotas recover
set -u
repo=amoiba42/markdown; gap=60
while getopts "R:g:" o; do case $o in R) repo=$OPTARG;; g) gap=$OPTARG;; *) exit 2;; esac; done
shift $((OPTIND - 1))
[ $# -gt 0 ] || { echo "usage: $0 [-R owner/repo] [-g SECONDS] ISSUE..." >&2; exit 2; }

for issue in "$@"; do
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  gh workflow run autose -R "$repo" -f issue="$issue" || { echo "issue $issue: dispatch failed"; continue; }
  run=""
  for _ in $(seq 1 30); do   # dispatch takes a few seconds to show up
    sleep 4
    run=$(gh run list -R "$repo" --workflow autose --event workflow_dispatch --limit 5 \
          --json databaseId,createdAt --jq "[.[]|select(.createdAt>=\"$start\")][0].databaseId // empty")
    [ -n "$run" ] && break
  done
  [ -n "$run" ] || { echo "issue $issue: run not found"; continue; }
  echo "issue $issue: run $run started"
  while [ "$(gh run view "$run" -R "$repo" --json status --jq .status)" != completed ]; do sleep 20; done
  jobs=$(gh run view "$run" -R "$repo" --json jobs --jq '[.jobs[]|.name+"="+.conclusion]|join(" ")')
  echo "issue $issue: $jobs  https://github.com/$repo/actions/runs/$run"
  sleep "$gap"
done
