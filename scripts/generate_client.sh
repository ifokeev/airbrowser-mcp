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
SPEC_PATH="${SPEC_PATH:-openapi.json}"
SPEC_FILE="openapi_spec.json" # temp file used for generation

# Step 1: Acquire OpenAPI spec
if [ -f "$SPEC_PATH" ]; then
    echo "📋 Using OpenAPI spec from $SPEC_PATH..."
    cp "$SPEC_PATH" "$SPEC_FILE"
else
    echo "📋 Fetching latest OpenAPI spec from $API_URL/api/v1/swagger.json..."
    curl -s "$API_URL/api/v1/swagger.json" > "$SPEC_FILE"
fi

if [ ! -s "$SPEC_FILE" ]; then
    echo "❌ Error: Failed to fetch OpenAPI spec"
    exit 1
fi

echo "✅ OpenAPI spec saved to $SPEC_FILE"

# Step 2: Generate Python client using Docker
echo ""
echo "🔧 Generating Python client..."

# Ensure output directory exists with correct permissions
mkdir -p "$OUTPUT_DIR"

docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$(pwd):/local" \
  openapitools/openapi-generator-cli:latest generate \
  -i "/local/$SPEC_FILE" \
  -g python \
  -o "/local/$OUTPUT_DIR" \
  --skip-validate-spec \
  --git-user-id "$GITHUB_USER" \
  --git-repo-id "$GITHUB_REPO" \
  --additional-properties packageName=airbrowser_client,projectName=airbrowser-client,packageVersion="$VERSION" \
  2>&1 | grep -E "(INFO|WARN|ERROR|writing file)" || true

# Check if generation was successful
if [ -d "$OUTPUT_DIR/airbrowser_client" ]; then
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
TYPESCRIPT_OUTPUT_DIR="generated-clients/typescript"

# Clean and recreate directory with correct permissions
rm -rf "$TYPESCRIPT_OUTPUT_DIR"
mkdir -p "$TYPESCRIPT_OUTPUT_DIR"

docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$(pwd):/local" \
  openapitools/openapi-generator-cli:latest generate \
  -i "/local/$SPEC_FILE" \
  -g typescript-axios \
  -o "/local/$TYPESCRIPT_OUTPUT_DIR" \
  --skip-validate-spec \
  --git-user-id "$GITHUB_USER" \
  --git-repo-id "$GITHUB_REPO" \
  --additional-properties npmName=airbrowser-client,npmVersion="$VERSION",supportsES6=true \
  2>&1 | grep -E "(INFO|WARN|ERROR|writing file)" | tail -20 || true

if [ -f "$TYPESCRIPT_OUTPUT_DIR/api.ts" ]; then
    echo ""
    echo "✅ TypeScript client generated successfully in $TYPESCRIPT_OUTPUT_DIR"
else
    echo "⚠️ Warning: TypeScript client generation may have failed"
fi

# Step 4: Clean up the OpenAPI spec file
echo ""
echo "🧹 Cleaning up OpenAPI spec file..."
rm -f "$SPEC_FILE"
echo "✅ Removed $SPEC_FILE"

echo ""
echo "🎉 Done! Clients have been generated:"
echo "   Python:     $OUTPUT_DIR"
echo "   TypeScript: $TYPESCRIPT_OUTPUT_DIR"
