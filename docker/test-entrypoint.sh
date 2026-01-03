#!/bin/bash
set -e

# Test entrypoint - waits for browser-pool and runs tests

BROWSER_POOL_URL="${BROWSER_POOL_URL:-http://browser-pool:8000}"
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "=== Airbrowser Test Runner ==="
echo "Browser Pool URL: $BROWSER_POOL_URL"
echo ""

# Wait for browser-pool to be healthy
echo "Waiting for browser-pool to be ready..."
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
    if curl -sf "${BROWSER_POOL_URL}/health" > /dev/null 2>&1; then
        echo "Browser-pool is ready!"
        break
    fi
    retry_count=$((retry_count + 1))
    echo "  Attempt $retry_count/$MAX_RETRIES - waiting ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

if [ $retry_count -eq $MAX_RETRIES ]; then
    echo "ERROR: Browser-pool did not become ready in time"
    exit 1
fi

echo ""
echo "=== Running Tests ==="
echo ""

# Update conftest to use the Docker service URL
export API_BASE_URL="${BROWSER_POOL_URL}/api/v1"

# Run pytest - uses settings from pytest.ini
cd /app/tests

PYTEST_EXTRA_ARGS="${PYTEST_ARGS:-}"

echo "Running tests with 4 parallel workers..."

# Base marker filter from pytest.ini
BASE_MARKERS="not slow and not external"

# Allow pytest to return non-zero without exiting the script.
set +e

# Run parallel tests first (excluding isolated tests that use close_all/kill_all)
echo "=== Phase 1: Parallel tests ==="
pytest -m "$BASE_MARKERS and not isolated" $PYTEST_EXTRA_ARGS
PARALLEL_EXIT=$?
if [ $PARALLEL_EXIT -eq 5 ]; then
    echo "No parallel tests selected."
    PARALLEL_EXIT=0
fi

# Run isolated tests sequentially (they use close_all/kill_all)
echo ""
echo "=== Phase 2: Isolated tests (sequential) ==="
pytest -m "$BASE_MARKERS and isolated" -n 1 $PYTEST_EXTRA_ARGS
ISOLATED_EXIT=$?
if [ $ISOLATED_EXIT -eq 5 ]; then
    echo "No isolated tests selected."
    ISOLATED_EXIT=0
fi

# Re-enable exit-on-error for any subsequent commands.
set -e

# Exit with failure if either phase failed
if [ $PARALLEL_EXIT -ne 0 ] || [ $ISOLATED_EXIT -ne 0 ]; then
    exit 1
fi
