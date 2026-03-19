#!/usr/bin/env bash

# Script to generate Python and TypeScript clients from OpenAPI spec
# Usage:
#   ./scripts/generate_client.sh
#   VERSION=1.2.3 ./scripts/generate_client.sh
#   SPEC_PATH=openapi.json ./scripts/generate_client.sh

set -euo pipefail

echo "🚀 Generating Python and TypeScript clients from OpenAPI spec..."
echo "==========================================="

# Always run from repo root for consistent paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Configuration (allow override via env)
API_URL="${API_URL:-http://localhost:8000}"
VERSION="${VERSION:-1.0.0}"
GITHUB_USER="${GITHUB_USER:-ifokeev}"
GITHUB_REPO="${GITHUB_REPO:-airbrowser-mcp}"
OUTPUT_DIR="generated-clients/python"
TYPESCRIPT_OUTPUT_DIR="generated-clients/typescript"
SPEC_PATH="${SPEC_PATH:-openapi.json}"
SPEC_FILE="openapi_spec.json" # temp file used for generation
PYTHON_OUTPUT_DIR_TMP=""
TYPESCRIPT_OUTPUT_DIR_TMP=""
PYTHON_LOG=""
TYPESCRIPT_LOG=""

cleanup() {
    if [ -n "$SPEC_FILE" ] && [ -f "$SPEC_FILE" ]; then
        rm -f "$SPEC_FILE"
    fi
    if [ -n "$PYTHON_OUTPUT_DIR_TMP" ] && [ -d "$PYTHON_OUTPUT_DIR_TMP" ]; then
        rm -rf "$PYTHON_OUTPUT_DIR_TMP"
    fi
    if [ -n "$TYPESCRIPT_OUTPUT_DIR_TMP" ] && [ -d "$TYPESCRIPT_OUTPUT_DIR_TMP" ]; then
        rm -rf "$TYPESCRIPT_OUTPUT_DIR_TMP"
    fi
    if [ -n "$PYTHON_LOG" ] && [ -f "$PYTHON_LOG" ]; then
        rm -f "$PYTHON_LOG"
    fi
    if [ -n "$TYPESCRIPT_LOG" ] && [ -f "$TYPESCRIPT_LOG" ]; then
        rm -f "$TYPESCRIPT_LOG"
    fi
}

trap cleanup EXIT

validate_spec() {
    local spec_path="$1"

    uv run python - "$spec_path" <<'PY'
import json
import sys
from pathlib import Path

spec_path = Path(sys.argv[1])

try:
    payload = json.loads(spec_path.read_text())
except Exception as exc:  # noqa: BLE001
    raise SystemExit(f"❌ Error: Invalid OpenAPI JSON in {spec_path}: {exc}")

if not isinstance(payload, dict):
    raise SystemExit(f"❌ Error: OpenAPI spec in {spec_path} must be a JSON object")

if not payload.get("swagger") and not payload.get("openapi"):
    raise SystemExit(f"❌ Error: OpenAPI spec in {spec_path} is missing a swagger/openapi version")

paths = payload.get("paths")
if not isinstance(paths, dict):
    raise SystemExit(f"❌ Error: OpenAPI spec in {spec_path} is missing a valid paths object")
PY
}

print_filtered_log() {
    local log_path="$1"

    grep -E "(INFO|WARN|ERROR|writing file)" "$log_path" || true
}

sanitize_generated_tree() {
    local target_dir="$1"

    uv run python - "$target_dir" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])

for path in root.rglob("*"):
    if not path.is_file():
        continue

    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue

    normalized = original.replace("\r\n", "\n")
    lines = [line.rstrip() for line in normalized.splitlines()]
    while lines and lines[-1] == "":
        lines.pop()

    cleaned = "\n".join(lines)
    if cleaned:
        cleaned += "\n"

    if cleaned != normalized:
        path.write_text(cleaned, encoding="utf-8")
PY
}

# Step 1: Acquire OpenAPI spec
if [ -f "$SPEC_PATH" ]; then
    echo "📋 Using OpenAPI spec from $SPEC_PATH..."
    cp "$SPEC_PATH" "$SPEC_FILE"
else
    echo "📋 Fetching latest OpenAPI spec from $API_URL/api/v1/swagger.json..."
    curl -fsS "$API_URL/api/v1/swagger.json" > "$SPEC_FILE"
fi

if [ ! -s "$SPEC_FILE" ]; then
    echo "❌ Error: Failed to fetch OpenAPI spec"
    exit 1
fi

echo "✅ OpenAPI spec saved to $SPEC_FILE"
validate_spec "$SPEC_FILE"
echo "✅ OpenAPI spec validated"

# Step 2: Generate Python client using Docker
echo ""
echo "🔧 Generating Python client..."

PYTHON_OUTPUT_DIR_TMP="$(mktemp -d "$REPO_ROOT/generated-clients/python.tmp.XXXXXX")"
PYTHON_LOG="$(mktemp "$REPO_ROOT/generated-clients/python.generate.XXXXXX.log")"

if ! docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$(pwd):/local" \
  openapitools/openapi-generator-cli:latest generate \
  -i "/local/$SPEC_FILE" \
  -g python \
  -o "/local/${PYTHON_OUTPUT_DIR_TMP#$REPO_ROOT/}" \
  --skip-validate-spec \
  --git-user-id "$GITHUB_USER" \
  --git-repo-id "$GITHUB_REPO" \
  --additional-properties packageName=airbrowser_client,projectName=airbrowser-client,packageVersion="$VERSION" \
  >"$PYTHON_LOG" 2>&1; then
    print_filtered_log "$PYTHON_LOG"
    echo "❌ Error: Failed to generate Python client"
    exit 1
fi

print_filtered_log "$PYTHON_LOG"

if [ -f "$PYTHON_OUTPUT_DIR_TMP/airbrowser_client/api_client.py" ]; then
    sanitize_generated_tree "$PYTHON_OUTPUT_DIR_TMP"
    rm -rf "$OUTPUT_DIR"
    mv "$PYTHON_OUTPUT_DIR_TMP" "$OUTPUT_DIR"
    PYTHON_OUTPUT_DIR_TMP=""
    echo ""
    echo "✅ Python client generated successfully in $OUTPUT_DIR"
    echo ""
    echo "📦 To install the client:"
    echo "  1. Create/activate a virtual environment:"
    echo "     uv venv && source .venv/bin/activate"
    echo "  2. Install dependencies:"
    echo "     uv pip install -r $OUTPUT_DIR/requirements.txt"
    echo "  3. Install the client:"
    echo "     uv pip install -e $OUTPUT_DIR"
    echo ""
    echo "📚 Example usage:"
    echo "  import airbrowser_client"
    echo "  from airbrowser_client.api import browser_api, health_api"
    echo "  "
    echo "  config = airbrowser_client.Configuration()"
    echo "  config.host = \"$API_URL\""
    echo "  "
    echo "  health_client = health_api.HealthApi(airbrowser_client.ApiClient(config))"
    echo "  health = health_client.health_check()"
else
    echo "❌ Error: Failed to generate Python client"
    exit 1
fi

# Step 3: Generate TypeScript client
echo ""
echo "🔧 Generating TypeScript client..."

TYPESCRIPT_OUTPUT_DIR_TMP="$(mktemp -d "$REPO_ROOT/generated-clients/typescript.tmp.XXXXXX")"
TYPESCRIPT_LOG="$(mktemp "$REPO_ROOT/generated-clients/typescript.generate.XXXXXX.log")"

if ! docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$(pwd):/local" \
  openapitools/openapi-generator-cli:latest generate \
  -i "/local/$SPEC_FILE" \
  -g typescript-axios \
  -o "/local/${TYPESCRIPT_OUTPUT_DIR_TMP#$REPO_ROOT/}" \
  --skip-validate-spec \
  --git-user-id "$GITHUB_USER" \
  --git-repo-id "$GITHUB_REPO" \
  --additional-properties npmName=airbrowser-client,npmVersion="$VERSION",supportsES6=true \
  >"$TYPESCRIPT_LOG" 2>&1; then
    print_filtered_log "$TYPESCRIPT_LOG"
    echo "❌ Error: Failed to generate TypeScript client"
    exit 1
fi

print_filtered_log "$TYPESCRIPT_LOG"

if [ -f "$TYPESCRIPT_OUTPUT_DIR_TMP/api.ts" ]; then
    sanitize_generated_tree "$TYPESCRIPT_OUTPUT_DIR_TMP"
    rm -rf "$TYPESCRIPT_OUTPUT_DIR"
    mv "$TYPESCRIPT_OUTPUT_DIR_TMP" "$TYPESCRIPT_OUTPUT_DIR"
    TYPESCRIPT_OUTPUT_DIR_TMP=""
    echo ""
    echo "✅ TypeScript client generated successfully in $TYPESCRIPT_OUTPUT_DIR"
else
    echo "❌ Error: Failed to generate TypeScript client"
    exit 1
fi

# Step 4: Clean up the OpenAPI spec file
echo ""
echo "🧹 Cleaning up OpenAPI spec file..."
echo "✅ Removed $SPEC_FILE"
rm -f "$SPEC_FILE"
SPEC_FILE=""

echo ""
echo "🎉 Done! Clients have been generated:"
echo "   Python:     $OUTPUT_DIR"
echo "   TypeScript: $TYPESCRIPT_OUTPUT_DIR"
