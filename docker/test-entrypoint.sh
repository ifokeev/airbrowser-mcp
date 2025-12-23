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
PYTEST_DEFAULT_ARGS="-v --tb=short"
PYTEST_EXTRA_ARGS="${PYTEST_ARGS:-}"

# If no command args provided, run in two phases
if [ $# -eq 0 ] && [ -z "$PYTEST_EXTRA_ARGS" ]; then
    echo "Phase 1: Running parallel tests (excluding close_all tests)..."
    echo "Running: pytest $PYTEST_DEFAULT_ARGS -k 'not close_all'"
    pytest $PYTEST_DEFAULT_ARGS -k "not close_all"
    PHASE1_EXIT=$?

    echo ""
    echo "Phase 2: Running close_all tests (sequential to avoid closing other tests' browsers)..."
    echo "Running: pytest $PYTEST_DEFAULT_ARGS -n0 -k 'close_all'"
    pytest $PYTEST_DEFAULT_ARGS -n0 -k "close_all"
    PHASE2_EXIT=$?

    # Exit with failure if either phase failed
    if [ $PHASE1_EXIT -ne 0 ] || [ $PHASE2_EXIT -ne 0 ]; then
        exit 1
    fi
    exit 0
elif [ -z "$PYTEST_EXTRA_ARGS" ]; then
    echo "Running: pytest $PYTEST_DEFAULT_ARGS"
    exec pytest $PYTEST_DEFAULT_ARGS
else
    echo "Running: pytest $PYTEST_DEFAULT_ARGS $PYTEST_EXTRA_ARGS"
    exec pytest $PYTEST_DEFAULT_ARGS $PYTEST_EXTRA_ARGS
fi
