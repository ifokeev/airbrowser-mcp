#!/bin/bash
# Build and publish TypeScript client to npm
# Usage:
#   ./scripts/publish_npm.sh           # Publish to npm
#   ./scripts/publish_npm.sh --dry-run # Build only, don't publish

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLIENT_DIR="$PROJECT_ROOT/generated-clients/typescript"

# Parse arguments
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run  Build only, don't publish"
            echo "  --help     Show this help message"
            echo ""
            echo "Prerequisites:"
            echo "  npm login  # Authenticate with npm"
            exit 0
            ;;
    esac
done

echo "=== Publishing TypeScript client to npm ==="
echo ""

cd "$CLIENT_DIR"

# Check prerequisites
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm not found"
    exit 1
fi

# Check if logged in
if ! npm whoami &> /dev/null; then
    echo "❌ Error: Not logged in to npm. Run 'npm login' first."
    exit 1
fi

echo "👤 Logged in as: $(npm whoami)"
echo ""

# Clean and install
echo "🧹 Cleaning previous builds..."
rm -rf dist/ node_modules/

echo "📦 Installing dependencies..."
npm install

# Build
echo "🔨 Building package..."
npm run build

echo ""
echo "📦 Built files:"
ls -la dist/

if $DRY_RUN; then
    echo ""
    echo "✅ Dry run complete. Package built but not published."
    echo ""
    echo "To see what would be published:"
    npm pack --dry-run
    exit 0
fi

# Publish
echo ""
echo "📤 Publishing to npm..."
npm publish --access public

echo ""
echo "✅ Published to npm!"
echo "   Install with: npm install airbrowser-client"
