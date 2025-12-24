#!/bin/bash
# Generate static documentation from OpenAPI spec and source code
# Usage: ./scripts/generate_docs.sh
#        VERSION=1.2.3 ./scripts/generate_docs.sh
#
# Requires: running server at localhost:8000 OR docker compose up

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_OUTPUT="$PROJECT_ROOT/landing/docs"

# Get version from env, git tag, or default
if [[ -z "$VERSION" ]]; then
    VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//' || echo "latest")
fi
echo "📚 Generating documentation (v$VERSION)..."

# Create docs directory
mkdir -p "$DOCS_OUTPUT"

# Check if server is running, if not start it
SERVER_URL="${BROWSER_POOL_URL:-http://localhost:8000}"
if ! curl -sf "$SERVER_URL/health" > /dev/null 2>&1; then
    echo "⏳ Starting server..."
    cd "$PROJECT_ROOT"
    docker compose up -d browser-pool

    # Wait for server
    for i in {1..30}; do
        if curl -sf "$SERVER_URL/health" > /dev/null 2>&1; then
            echo "✅ Server ready"
            break
        fi
        echo "Waiting for server... ($i/30)"
        sleep 2
    done
fi

# Fetch OpenAPI spec
echo "📥 Fetching OpenAPI spec..."
curl -sf "$SERVER_URL/api/v1/swagger.json" > "$DOCS_OUTPUT/openapi.json"

# Generate docs using Python script
python3 "$SCRIPT_DIR/generate_docs.py" \
    --openapi "$DOCS_OUTPUT/openapi.json" \
    --mcp-tools "$PROJECT_ROOT/src/airbrowser/server/mcp/tool_descriptions.py" \
    --output "$DOCS_OUTPUT/index.html" \
    --version "$VERSION"

echo "✅ Documentation generated at $DOCS_OUTPUT/index.html"
