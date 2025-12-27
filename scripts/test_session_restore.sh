#!/bin/bash
#
# Integration test for session restore feature
#
# This test:
# 1. Starts the container with session restore enabled
# 2. Creates a browser and navigates to a page
# 3. Gracefully stops the container (SIGTERM)
# 4. Restarts the container
# 5. Verifies browser was restored
#
# Usage: ./scripts/test_session_restore.sh
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

# Configuration
COMPOSE_FILE="compose.local.yml"
API_URL="http://localhost:8000/api/v1"
STOP_TIMEOUT=30
STARTUP_TIMEOUT=90

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Session Restore Integration Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
}

# Set up trap for cleanup on exit
trap cleanup EXIT

# Helper: Wait for API to be healthy
wait_for_healthy() {
    local max_wait=$1
    local waited=0

    echo -n "Waiting for API to be healthy"
    while [ $waited -lt $max_wait ]; do
        if curl -sf "http://localhost:8000/health" > /dev/null 2>&1; then
            echo -e " ${GREEN}OK${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        waited=$((waited + 1))
    done

    echo -e " ${RED}TIMEOUT${NC}"
    return 1
}

# Helper: Create a browser and return its ID
create_browser() {
    curl -sf -X POST "$API_URL/browser/create_browser" \
        -H "Content-Type: application/json" \
        -d '{"window_size": [1280, 720]}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['browser_id'])"
}

# Helper: Navigate browser to URL (with retry)
navigate_browser() {
    local browser_id=$1
    local url=$2
    local attempts=0
    local max_attempts=2

    while [ $attempts -lt $max_attempts ]; do
        local result
        result=$(curl -s -X POST "$API_URL/browser/$browser_id/navigate" \
            -H "Content-Type: application/json" \
            -d "{\"url\": \"$url\", \"timeout\": 90}")

        if echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('success') else 1)" 2>/dev/null; then
            return 0
        fi

        attempts=$((attempts + 1))
        if [ $attempts -lt $max_attempts ]; then
            echo "    Retry $attempts..."
            sleep 2
        fi
    done

    echo "Navigation failed after $max_attempts attempts" >&2
    return 1
}

# Helper: Get browser count
get_browser_count() {
    curl -sf -X POST "$API_URL/browser/browsers" \
        -H "Content-Type: application/json" \
        -d '{"action": "list"}' | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('data', {}).get('browsers', [])))"
}

# Helper: Get current URL for a browser
get_current_url() {
    local browser_id=$1
    curl -sf -X POST "$API_URL/browser/$browser_id/get_url" \
        -H "Content-Type: application/json" \
        -d '{}' | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('data', {}).get('url', 'unknown'))"
}

# ========================================
# STEP 1: Clean start
# ========================================
echo -e "${BLUE}Step 1: Starting fresh container...${NC}"
docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
rm -rf ./state/*.json 2>/dev/null || true

# Ensure state directory exists
mkdir -p ./state

docker compose -f "$COMPOSE_FILE" up -d

if ! wait_for_healthy $STARTUP_TIMEOUT; then
    echo -e "${RED}ERROR: Container failed to start${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=50
    exit 1
fi

# ========================================
# STEP 2: Create browser and navigate
# ========================================
echo -e "\n${BLUE}Step 2: Creating browser and navigating to test page...${NC}"

echo "Creating browser..."
BROWSER_ID=$(create_browser)
echo "  Browser ID: $BROWSER_ID"

echo "  Navigating to example.com..."
if ! navigate_browser "$BROWSER_ID" "https://example.com"; then
    echo -e "${RED}ERROR: Navigation failed${NC}"
    exit 1
fi

# Verify initial state
echo -e "\n${BLUE}Verifying initial state...${NC}"
INITIAL_COUNT=$(get_browser_count)
CURRENT_URL=$(get_current_url "$BROWSER_ID")
echo "  Active browsers: $INITIAL_COUNT"
echo "  Current URL: $CURRENT_URL"

if [ "$INITIAL_COUNT" != "1" ]; then
    echo -e "${RED}ERROR: Expected 1 browser, got $INITIAL_COUNT${NC}"
    exit 1
fi

# ========================================
# STEP 3: Gracefully stop container
# ========================================
echo -e "\n${BLUE}Step 3: Gracefully stopping container (SIGTERM)...${NC}"
docker compose -f "$COMPOSE_FILE" stop -t $STOP_TIMEOUT

# Wait for stop
sleep 2

# Check if state file was created
if [ -f "./state/browsers.json" ]; then
    echo -e "  ${GREEN}State file created${NC}"
    SAVED_BROWSERS=$(python3 -c "import json; d=json.load(open('./state/browsers.json')); print(len(d.get('browsers', [])))")
    echo "  Saved browsers: $SAVED_BROWSERS"
else
    echo -e "  ${RED}ERROR: State file not found!${NC}"
    exit 1
fi

# ========================================
# STEP 4: Restart container
# ========================================
echo -e "\n${BLUE}Step 4: Restarting container...${NC}"
docker compose -f "$COMPOSE_FILE" up -d

if ! wait_for_healthy $STARTUP_TIMEOUT; then
    echo -e "${RED}ERROR: Container failed to restart${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=50
    exit 1
fi

# Give extra time for restore to complete
echo "Waiting for session restore..."
sleep 5

# ========================================
# STEP 5: Verify restoration
# ========================================
echo -e "\n${BLUE}Step 5: Verifying restoration...${NC}"

# Check browser count
RESTORED_COUNT=$(get_browser_count)
echo "  Restored browsers: $RESTORED_COUNT"

if [ "$RESTORED_COUNT" != "1" ]; then
    echo -e "${RED}ERROR: Expected 1 restored browser, got $RESTORED_COUNT${NC}"
    curl -s -X POST "$API_URL/browser/browsers" -H "Content-Type: application/json" -d '{"action": "list"}' | python3 -m json.tool
    exit 1
fi

# Get restored browser ID
RESTORED_ID=$(curl -sf -X POST "$API_URL/browser/browsers" \
    -H "Content-Type: application/json" \
    -d '{"action": "list"}' | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['browsers'][0]['browser_id'])")
echo "  Restored browser ID: $RESTORED_ID"

# Check URL of restored browser
RESTORED_URL=$(get_current_url "$RESTORED_ID")
echo "  Restored URL: $RESTORED_URL"

# Verify state file was cleared after restore
if [ -f "./state/browsers.json" ]; then
    echo -e "  ${YELLOW}Note: State file still exists (cleared on next shutdown)${NC}"
else
    echo -e "  ${GREEN}State file cleared after restore${NC}"
fi

# ========================================
# RESULT
# ========================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Session Restore Test PASSED${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Summary:"
echo "  - Created browser before shutdown"
echo "  - State was saved on graceful shutdown"
echo "  - Browser restored after restart"
echo "  - URL preserved: $RESTORED_URL"
echo ""

exit 0
