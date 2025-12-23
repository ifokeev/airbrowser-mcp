#!/bin/bash
# Airbrowser - macOS Launcher
# Uses Lima/Colima for lightweight Linux VM + container runtime
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$HOME/Library/Application Support/Airbrowser"
IMAGE_FILE="$SCRIPT_DIR/image.tar.gz"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[airbrowser]${NC} $1"; }
warn() { echo -e "${YELLOW}[airbrowser]${NC} $1"; }
error() { echo -e "${RED}[airbrowser]${NC} $1" >&2; }

# Find available runtime
find_runtime() {
    # Check for Docker Desktop
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        echo "docker"
        return
    fi

    # Check for Colima (lightweight Docker alternative)
    if command -v colima &> /dev/null; then
        if ! colima status &> /dev/null; then
            log "Starting Colima VM..."
            colima start --cpu 2 --memory 4 --network-address
        fi
        echo "docker"  # Colima provides docker CLI
        return
    fi

    # Check for Lima directly
    if command -v limactl &> /dev/null; then
        echo "lima"
        return
    fi

    # Check for Podman
    if command -v podman &> /dev/null; then
        if ! podman machine inspect &> /dev/null; then
            log "Initializing Podman machine..."
            podman machine init --cpus 2 --memory 4096
            podman machine start
        fi
        echo "podman"
        return
    fi

    echo ""
}

# Install runtime instructions
install_runtime() {
    error "No container runtime found"
    echo ""
    echo "Install one of the following:"
    echo ""
    echo "  Colima (recommended - lightweight):"
    echo "    brew install colima docker"
    echo "    colima start"
    echo ""
    echo "  Docker Desktop:"
    echo "    brew install --cask docker"
    echo ""
    echo "  Podman:"
    echo "    brew install podman"
    echo "    podman machine init && podman machine start"
    echo ""
    exit 1
}

# Load image
load_image() {
    local runtime=$1

    # Check if image exists
    if $runtime image inspect airbrowser:latest &>/dev/null; then
        log "Image already loaded"
        return 0
    fi

    if [[ ! -f "$IMAGE_FILE" ]]; then
        error "Image file not found: $IMAGE_FILE"
        exit 1
    fi

    log "Loading container image (this may take a moment)..."
    gunzip -c "$IMAGE_FILE" | $runtime load
    log "Image loaded successfully"
}

# Main
main() {
    log "Starting Airbrowser..."

    # Find runtime
    RUNTIME=$(find_runtime)
    if [[ -z "$RUNTIME" ]]; then
        install_runtime
    fi
    log "Using runtime: $RUNTIME"

    # Load image
    load_image "$RUNTIME"

    # Create data directories
    mkdir -p "$DATA_DIR"/{profiles,screenshots,downloads}

    # Run container
    # Note: macOS doesn't support --network=host, so we use port mapping
    log "Starting server..."
    echo ""
    log "All services at http://localhost:18080"
    log "  Dashboard: /"
    log "  API Docs:  /docs/"
    log "  VNC:       /vnc/"
    log "  REST API:  /api/v1/"
    log "  MCP:       /mcp"
    echo ""
    log "Press Ctrl+C to stop"
    echo ""

    exec $RUNTIME run --rm -it \
        --name airbrowser \
        -p 18080:18080 \
        -v "$DATA_DIR/profiles:/app/browser-profiles" \
        -v "$DATA_DIR/screenshots:/tmp/screenshots" \
        -v "$DATA_DIR/downloads:/app/downloads" \
        -e API_BASE_URL="http://localhost:18080" \
        airbrowser:latest
}

# Handle arguments
case "${1:-}" in
    --help|-h)
        echo "Airbrowser - Browser Automation Server"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help"
        echo "  --version, -v  Show version"
        echo "  --stop         Stop running instance"
        echo ""
        echo "All services available at http://localhost:18080:"
        echo "  Dashboard: http://localhost:18080"
        echo "  API Docs:  http://localhost:18080/docs/"
        echo "  VNC:       http://localhost:18080/vnc/"
        echo "  REST API:  http://localhost:18080/api/v1/"
        echo "  MCP:       http://localhost:18080/mcp"
        ;;
    --version|-v)
        echo "Airbrowser v0.1.1"
        ;;
    --stop)
        RUNTIME=$(find_runtime)
        if [[ -n "$RUNTIME" ]]; then
            $RUNTIME stop airbrowser 2>/dev/null || true
            log "Stopped"
        fi
        ;;
    *)
        main
        ;;
esac
