#!/bin/bash
# Build and publish Python client to PyPI
# Usage:
#   ./scripts/publish_python.sh           # Publish to PyPI
#   ./scripts/publish_python.sh --test    # Publish to TestPyPI first
#   ./scripts/publish_python.sh --dry-run # Build only, don't publish

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLIENT_DIR="$PROJECT_ROOT/generated-clients/python"

# Parse arguments
TEST_PYPI=false
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --test)
            TEST_PYPI=true
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --test     Publish to TestPyPI instead of PyPI"
            echo "  --dry-run  Build only, don't publish"
            echo "  --help     Show this help message"
            echo ""
            echo "Prerequisites:"
            echo "  pip install build twine"
            echo ""
            echo "Authentication:"
            echo "  Option 1: Create ~/.pypirc with credentials"
            echo "  Option 2: Set TWINE_USERNAME and TWINE_PASSWORD env vars"
            echo "  Option 3: Use API token (recommended):"
            echo "            TWINE_USERNAME=__token__"
            echo "            TWINE_PASSWORD=pypi-xxxx..."
            exit 0
            ;;
    esac
done

echo "=== Publishing Python client to PyPI ==="
echo ""

cd "$CLIENT_DIR"

# Check prerequisites
if ! command -v python &> /dev/null; then
    echo "❌ Error: python not found"
    exit 1
fi

# Install build tools if needed
echo "📦 Installing build tools..."
pip install --quiet build twine

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build
echo "🔨 Building package..."
python -m build

echo ""
echo "📦 Built packages:"
ls -la dist/

if $DRY_RUN; then
    echo ""
    echo "✅ Dry run complete. Packages built but not published."
    exit 0
fi

# Upload
echo ""
if $TEST_PYPI; then
    echo "📤 Uploading to TestPyPI..."
    python -m twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Published to TestPyPI!"
    echo "   Install with: pip install -i https://test.pypi.org/simple/ airbrowser-client"
else
    echo "📤 Uploading to PyPI..."
    python -m twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo "   Install with: pip install airbrowser-client"
fi
