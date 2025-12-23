#!/usr/bin/env bash
set -euo pipefail

if ! command -v git >/dev/null 2>&1; then
  echo "git not found; skipping generated client check."
  exit 0
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository; skipping generated client check."
  exit 0
fi

echo "Regenerating clients to check for staleness..."
./scripts/generate_client.sh

if ! git diff --exit-code -- generated-clients >/dev/null; then
  echo "Generated clients are stale. Re-run ./scripts/generate_client.sh and commit changes in generated-clients/."
  exit 1
fi

echo "Generated clients are up to date."

