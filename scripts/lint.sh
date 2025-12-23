#!/bin/bash
# Run ruff linter and formatter

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Parse arguments
FIX=false
FORMAT=false
CHECK_ONLY=false

for arg in "$@"; do
    case $arg in
        --fix)
            FIX=true
            ;;
        --format)
            FORMAT=true
            ;;
        --check)
            CHECK_ONLY=true
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --fix      Auto-fix linting issues"
            echo "  --format   Format code with ruff"
            echo "  --check    Check only (for CI), exit non-zero if changes needed"
            echo "  --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0              # Run lint check only"
            echo "  $0 --fix        # Run lint and auto-fix issues"
            echo "  $0 --format     # Format code"
            echo "  $0 --fix --format  # Fix lint issues and format"
            echo "  $0 --check      # CI mode: check lint and format, fail if issues"
            exit 0
            ;;
    esac
done

if $CHECK_ONLY; then
    echo "=== Checking lint (ruff check) ==="
    ruff check src/ tests/

    echo ""
    echo "=== Checking format (ruff format --check) ==="
    ruff format --check src/ tests/

    echo ""
    echo "All checks passed!"
    exit 0
fi

echo "=== Running ruff linter ==="
if $FIX; then
    ruff check --fix src/ tests/
else
    ruff check src/ tests/ || true
fi

if $FORMAT; then
    echo ""
    echo "=== Running ruff formatter ==="
    ruff format src/ tests/
fi

echo ""
echo "Done!"
