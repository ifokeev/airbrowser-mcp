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

# Run pytest with any additional args
cd /app/tests

# Combine default args with any user-provided args
# -n auto uses all CPU cores, -q for quiet output (faster)
PYTEST_DEFAULT_ARGS="--tb=short -q"
PYTEST_EXTRA_ARGS="${PYTEST_ARGS:-}"

# Run tests sequentially to avoid fixture conflicts with class-scoped browser fixtures
# Note: Parallelism can be achieved within tests using multiple browsers/tabs from the pool
if [ $# -eq 0 ] && [ -z "$PYTEST_EXTRA_ARGS" ]; then
    echo "Running tests sequentially (browser fixtures are class-scoped)..."
    exec pytest $PYTEST_DEFAULT_ARGS -n 1
elif [ -z "$PYTEST_EXTRA_ARGS" ]; then
    exec pytest $PYTEST_DEFAULT_ARGS -n 1
else
    exec pytest $PYTEST_DEFAULT_ARGS $PYTEST_EXTRA_ARGS
fi
