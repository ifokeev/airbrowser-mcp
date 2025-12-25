#!/bin/bash
# Airbrowser - Linux Launcher
# Portable package with bundled podman (requires uidmap package)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/airbrowser"
IMAGE_FILE="$SCRIPT_DIR/image.tar.gz"
PODMAN_DIR="$SCRIPT_DIR/podman"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[airbrowser]${NC} $1"; }
warn() { echo -e "${YELLOW}[airbrowser]${NC} $1"; }
error() { echo -e "${RED}[airbrowser]${NC} $1" >&2; }

# Setup bundled podman configuration
setup_bundled_podman() {
    local podman_bin="$PODMAN_DIR/usr/local/bin/podman"
    local helper_dir="$PODMAN_DIR/usr/local/lib/podman"

    if [[ ! -x "$podman_bin" ]]; then
        return 1
    fi

    # Check for uidmap (required for rootless containers)
    if ! command -v newuidmap &> /dev/null; then
        return 1
    fi

    # Create config directory
    local config_dir="$DATA_DIR/config"
    mkdir -p "$config_dir" "$DATA_DIR/run" "$DATA_DIR/storage"

    # Create containers.conf with helper paths
    cat > "$config_dir/containers.conf" << EOF
[engine]
cgroup_manager = "cgroupfs"
events_logger = "file"
conmon_path = ["$helper_dir/conmon"]
helper_binaries_dir = ["$helper_dir"]

[network]
network_backend = "netavark"
netavark_plugin_dirs = ["$helper_dir"]
EOF

    # Create storage.conf
    local fuse_overlayfs="$PODMAN_DIR/usr/local/bin/fuse-overlayfs"
    cat > "$config_dir/storage.conf" << EOF
[storage]
driver = "overlay"
runroot = "$DATA_DIR/run"
graphroot = "$DATA_DIR/storage"

[storage.options.overlay]
mount_program = "$fuse_overlayfs"
EOF

    # Export environment for podman
    export CONTAINERS_CONF="$config_dir/containers.conf"
    export CONTAINERS_STORAGE_CONF="$config_dir/storage.conf"
    export CONTAINERS_REGISTRIES_CONF="$PODMAN_DIR/etc/containers/registries.conf"

    # Add bundled binaries to PATH
    export PATH="$PODMAN_DIR/usr/local/bin:$PATH"

    # Verify podman actually works
    if ! "$podman_bin" info &>/dev/null; then
        return 1
    fi

    return 0
}

# Find container runtime
find_runtime() {
    # Try bundled podman first (requires uidmap package)
    if setup_bundled_podman; then
        echo "$PODMAN_DIR/usr/local/bin/podman"
        return
    fi

    # Fall back to docker (most reliable)
    if command -v docker &> /dev/null; then
        echo "docker"
        return
    fi

    # Fall back to system podman (may also need uidmap)
    if command -v podman &> /dev/null; then
        # Verify system podman works
        if podman info &>/dev/null; then
            echo "podman"
            return
        fi
    fi

    echo ""
}

# Show install instructions
install_runtime() {
    error "No container runtime found"
    echo ""
    if [[ -d "$PODMAN_DIR" ]]; then
        echo "Bundled podman requires the uidmap package:"
        echo "  Ubuntu/Debian: sudo apt install uidmap"
        echo "  Fedora/RHEL:   sudo dnf install shadow-utils"
        echo "  Arch:          sudo pacman -S shadow"
        echo ""
        echo "Or install Docker: https://docs.docker.com/engine/install/"
    else
        echo "Install Docker: https://docs.docker.com/engine/install/"
        echo "Or Podman:      sudo apt install podman"
    fi
    exit 1
}

# Load image if not already loaded
load_image() {
    local runtime=$1

    # Check if image exists
    if $runtime image exists airbrowser:latest 2>/dev/null; then
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

# Load environment from .env file
load_env() {
    local env_file="$DATA_DIR/.env"
    if [[ -f "$env_file" ]]; then
        log "Loading environment from $env_file"
        set -a
        source "$env_file"
        set +a
    fi
}

# Environment variables to pass through to container
ENV_VARS=(
    "OPENROUTER_API_KEY"
    "OPENROUTER_COORD_MODEL"
    "OPENROUTER_ANALYSIS_MODEL"
    "MAX_BROWSERS"
    "LOG_LEVEL"
    "COMMAND_TIMEOUT_DEFAULT"
    "NAVIGATE_TIMEOUT_DEFAULT"
    "SCREEN_WIDTH"
    "SCREEN_HEIGHT"
)

# Build environment args for docker/podman
build_env_args() {
    local args=""
    args="-e API_BASE_URL=http://localhost:18080 -e NGINX_HTTPS_PORT=18443"

    # Pass through all supported environment variables if set
    for var in "${ENV_VARS[@]}"; do
        if [[ -n "${!var:-}" ]]; then
            args="$args -e $var=${!var}"
        fi
    done

    # Log if AI vision is enabled
    if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
        log "AI vision tools enabled"
    fi

    echo "$args"
}

# Main
main() {
    log "Starting Airbrowser..."

    # Find runtime
    RUNTIME=$(find_runtime)
    if [[ -z "$RUNTIME" ]]; then
        install_runtime
    fi

    # Show which runtime we're using
    if [[ "$RUNTIME" == *"podman"* && "$RUNTIME" != "podman" ]]; then
        log "Using: bundled podman"
    else
        log "Using: $RUNTIME"
    fi

    # Load image
    load_image "$RUNTIME"

    # Create data directories
    mkdir -p "$DATA_DIR"/{profiles,screenshots,downloads}

    # Load environment from .env file if exists
    load_env

    # Build environment arguments
    ENV_ARGS=$(build_env_args)

    # Run container with host network for full localhost access
    log "Starting server..."
    echo ""
    log "All services at https://localhost:18443 (or http://localhost:18080)"
    log "  Dashboard: /"
    log "  API Docs:  /docs/"
    log "  VNC:       /vnc/"
    log "  REST API:  /api/v1/"
    log "  MCP:       /mcp"
    echo ""

    # Determine run mode based on TTY and flags
    if [[ "${DETACHED:-}" == "true" ]]; then
        log "Starting in background mode..."
        $RUNTIME run -d --rm \
            --network=host \
            --name airbrowser \
            -v "$DATA_DIR/profiles:/app/browser-profiles" \
            -v "$DATA_DIR/screenshots:/tmp/screenshots" \
            -v "$DATA_DIR/downloads:/app/downloads" \
            $ENV_ARGS \
            airbrowser:latest
        log "Container started. Use '$0 --stop' to stop."
    elif [[ -t 0 ]]; then
        # TTY available - run interactively
        log "Press Ctrl+C to stop"
        echo ""
        exec $RUNTIME run --rm -it \
            --network=host \
            --name airbrowser \
            -v "$DATA_DIR/profiles:/app/browser-profiles" \
            -v "$DATA_DIR/screenshots:/tmp/screenshots" \
            -v "$DATA_DIR/downloads:/app/downloads" \
            $ENV_ARGS \
            airbrowser:latest
    else
        # No TTY - run in detached mode
        log "No TTY detected, starting in background mode..."
        $RUNTIME run -d --rm \
            --network=host \
            --name airbrowser \
            -v "$DATA_DIR/profiles:/app/browser-profiles" \
            -v "$DATA_DIR/screenshots:/tmp/screenshots" \
            -v "$DATA_DIR/downloads:/app/downloads" \
            $ENV_ARGS \
            airbrowser:latest
        log "Container started. Use '$0 --stop' to stop."
    fi
}

# Handle arguments
case "${1:-}" in
    --help|-h)
        echo "Airbrowser - Browser Automation Server"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help"
        echo "  --version, -v   Show version"
        echo "  -d, --detach    Run in background (detached mode)"
        echo "  --stop          Stop running instance"
        echo "  --logs          Show container logs"
        echo ""
        echo "All services available at https://localhost:18443 (or http://localhost:18080):"
        echo "  Dashboard: /"
        echo "  API Docs:  /docs/"
        echo "  VNC:       /vnc/"
        echo "  REST API:  /api/v1/"
        echo "  MCP:       /mcp"
        echo ""
        echo "Environment Variables (set via .env file or environment):"
        echo "  OPENROUTER_API_KEY       Enable AI vision tools (recommended)"
        echo "  MAX_BROWSERS             Max concurrent browsers (default: 10)"
        echo "  LOG_LEVEL                DEBUG, INFO, WARNING, ERROR (default: INFO)"
        echo "  SCREEN_WIDTH/HEIGHT      Virtual display size (default: 1920x1080)"
        echo ""
        echo "  Create .env file in data directory:"
        echo "    echo 'OPENROUTER_API_KEY=sk-or-v1-xxx' > ~/.local/share/airbrowser/.env"
        echo "    echo 'MAX_BROWSERS=20' >> ~/.local/share/airbrowser/.env"
        echo ""
        echo "Requirements:"
        echo "  - uidmap package (for bundled podman)"
        echo "  - OR Docker/Podman installed on system"
        ;;
    --version|-v)
        echo "Airbrowser v0.1.1"
        ;;
    -d|--detach)
        DETACHED=true main
        ;;
    --stop)
        RUNTIME=$(find_runtime)
        if [[ -n "$RUNTIME" ]]; then
            $RUNTIME stop airbrowser 2>/dev/null || true
            log "Stopped"
        fi
        ;;
    --logs)
        RUNTIME=$(find_runtime)
        if [[ -n "$RUNTIME" ]]; then
            $RUNTIME logs -f airbrowser
        fi
        ;;
    *)
        main
        ;;
esac
