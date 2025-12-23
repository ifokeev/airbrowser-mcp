#!/bin/bash
# Build and publish generated clients to npm and PyPI
# Usage:
#   ./scripts/publish_clients.sh              # Publish both
#   ./scripts/publish_clients.sh python       # Publish Python only
#   ./scripts/publish_clients.sh npm          # Publish TypeScript only
#   ./scripts/publish_clients.sh --dry-run    # Build only, don't publish
#   ./scripts/publish_clients.sh --test       # Use TestPyPI for Python

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
TARGET="all"
EXTRA_ARGS=""

for arg in "$@"; do
    case $arg in
        python|py)
            TARGET="python"
            ;;
        npm|typescript|ts)
            TARGET="npm"
            ;;
        all)
            TARGET="all"
            ;;
        --dry-run|--test)
            EXTRA_ARGS="$EXTRA_ARGS $arg"
            ;;
        --help|-h)
            echo "Usage: $0 [target] [options]"
            echo ""
            echo "Targets:"
            echo "  all        Publish both Python and TypeScript (default)"
            echo "  python     Publish Python client to PyPI"
            echo "  npm        Publish TypeScript client to npm"
            echo ""
            echo "Options:"
            echo "  --dry-run  Build only, don't publish"
            echo "  --test     Use TestPyPI for Python client"
            echo "  --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Publish both to production"
            echo "  $0 python --test      # Publish Python to TestPyPI"
            echo "  $0 npm --dry-run      # Build TypeScript only"
            echo "  $0 --dry-run          # Build both without publishing"
            exit 0
            ;;
    esac
done

case $TARGET in
    python)
        "$SCRIPT_DIR/publish_python.sh" $EXTRA_ARGS
        ;;
    npm)
        "$SCRIPT_DIR/publish_npm.sh" $EXTRA_ARGS
        ;;
    all)
        echo "=========================================="
        echo "  Publishing all clients"
        echo "=========================================="
        echo ""
        "$SCRIPT_DIR/publish_python.sh" $EXTRA_ARGS
        echo ""
        echo "=========================================="
        echo ""
        "$SCRIPT_DIR/publish_npm.sh" $EXTRA_ARGS
        echo ""
        echo "=========================================="
        echo "✅ All clients published!"
        ;;
esac
