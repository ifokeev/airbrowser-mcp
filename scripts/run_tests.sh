#!/bin/bash
#
# Run all tests in Docker environment
#
# Usage:
#   ./scripts/run_tests.sh                    # Run all tests
#   ./scripts/run_tests.sh -k "test_health"   # Run specific tests
#   ./scripts/run_tests.sh --build            # Force rebuild
#   ./scripts/run_tests.sh --logs             # Show browser-pool logs on failure
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
FORCE_BUILD=""
SHOW_LOGS_ON_FAILURE=false
PYTEST_ARGS=""
CLEANUP=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --build|-b)
            FORCE_BUILD="--build"
            shift
            ;;
        --logs|-l)
            SHOW_LOGS_ON_FAILURE=true
            shift
            ;;
        --no-cleanup)
            CLEANUP=false
            shift
            ;;
        -k|-m|--tb|--maxfail|-x|-v|-vv)
            PYTEST_ARGS="$PYTEST_ARGS $1 $2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS] [PYTEST_ARGS]"
            echo ""
            echo "Options:"
            echo "  --build, -b        Force rebuild of Docker images"
            echo "  --logs, -l         Show browser-pool logs on test failure"
            echo "  --no-cleanup       Don't stop containers after tests"
            echo "  -k EXPRESSION      Only run tests matching expression"
            echo "  -x                 Stop on first failure"
            echo "  -v, -vv            Increase verbosity"
            echo "  --help, -h         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Run all tests"
            echo "  $0 -k test_health            # Run only health tests"
            echo "  $0 --build -x                # Rebuild and stop on first failure"
            echo "  $0 -k 'not chatgpt' -v       # Skip chatgpt tests, verbose"
            exit 0
            ;;
        *)
            PYTEST_ARGS="$PYTEST_ARGS $1"
            shift
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Airbrowser Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Cleanup function
cleanup() {
    if [ "$CLEANUP" = true ]; then
        echo -e "\n${YELLOW}Cleaning up...${NC}"
        docker compose -f compose.test.yml down -v --remove-orphans 2>/dev/null || true
    else
        echo -e "\n${YELLOW}Leaving containers running (--no-cleanup)${NC}"
        echo "To stop: docker compose -f compose.test.yml down -v"
    fi
}

# Set up trap for cleanup
trap cleanup EXIT

# Export pytest args for docker-compose
export PYTEST_ARGS

# Build and start services
echo -e "${BLUE}Building and starting services...${NC}"
docker compose -f compose.test.yml up $FORCE_BUILD -d browser-pool

# Wait for browser-pool to be healthy
echo -e "${BLUE}Waiting for browser-pool to be healthy...${NC}"
MAX_WAIT=120
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if docker compose -f compose.test.yml ps browser-pool | grep -q "healthy"; then
        echo -e "${GREEN}Browser-pool is healthy!${NC}"
        break
    fi
    echo -n "."
    sleep 2
    WAITED=$((WAITED + 2))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    echo -e "\n${RED}ERROR: Browser-pool did not become healthy in ${MAX_WAIT}s${NC}"
    echo -e "${YELLOW}Browser-pool logs:${NC}"
    docker compose -f compose.test.yml logs browser-pool
    exit 1
fi

echo ""

# Run tests
echo -e "${BLUE}Running tests...${NC}"
echo ""

# Run test-runner and capture exit code
set +e
docker compose -f compose.test.yml up $FORCE_BUILD --abort-on-container-exit test-runner
TEST_EXIT_CODE=$?
set -e

# Show browser-pool logs on failure if requested
if [ $TEST_EXIT_CODE -ne 0 ] && [ "$SHOW_LOGS_ON_FAILURE" = true ]; then
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  Browser-pool logs (test failure):${NC}"
    echo -e "${YELLOW}========================================${NC}"
    docker compose -f compose.test.yml logs browser-pool --tail=100
fi

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  All tests passed!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  Tests failed (exit code: $TEST_EXIT_CODE)${NC}"
    echo -e "${RED}========================================${NC}"
fi

exit $TEST_EXIT_CODE
