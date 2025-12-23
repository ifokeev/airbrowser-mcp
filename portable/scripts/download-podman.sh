#!/bin/bash
# Download static podman binary for bundling
# Source: https://github.com/mgoltzsche/podman-static
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${1:-$SCRIPT_DIR/../runtime}"

# Podman static release
PODMAN_VERSION="v5.3.1"
PODMAN_REPO="mgoltzsche/podman-static"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[download]${NC} $1"; }
info() { echo -e "${BLUE}[download]${NC} $1"; }

detect_arch() {
    local arch=$(uname -m)
    case "$arch" in
        x86_64)  echo "amd64" ;;
        aarch64) echo "arm64" ;;
        arm64)   echo "arm64" ;;
        *)       echo "amd64" ;;  # Default to amd64
    esac
}

download_linux() {
    local arch=$(detect_arch)
    local url="https://github.com/${PODMAN_REPO}/releases/download/${PODMAN_VERSION}/podman-linux-${arch}.tar.gz"
    local output_dir="$OUTPUT_DIR/linux-${arch}"

    log "Downloading podman static for linux-${arch}..."
    mkdir -p "$output_dir"

    curl -fsSL "$url" | tar -xz -C "$output_dir" --strip-components=1

    # We only need the core binaries
    log "Extracting essential binaries..."
    mkdir -p "$output_dir/bin"

    # Move essential binaries
    mv "$output_dir/podman-remote-static" "$output_dir/bin/podman" 2>/dev/null || \
    mv "$output_dir/usr/local/bin/podman" "$output_dir/bin/podman" 2>/dev/null || \
    find "$output_dir" -name "podman" -type f -executable -exec mv {} "$output_dir/bin/podman" \;

    # Clean up extras
    rm -rf "$output_dir/usr" "$output_dir/etc" 2>/dev/null || true

    chmod +x "$output_dir/bin/podman"

    local size=$(du -sh "$output_dir/bin/podman" | cut -f1)
    info "Downloaded podman binary: $size"
}

# Main
main() {
    log "Podman Static Downloader"
    log "Version: $PODMAN_VERSION"
    log "Output: $OUTPUT_DIR"
    echo ""

    mkdir -p "$OUTPUT_DIR"

    case "$(uname -s)" in
        Linux)
            download_linux
            ;;
        Darwin)
            log "macOS requires a VM-based solution (Lima/Colima)"
            log "Static podman not available for macOS"
            ;;
        *)
            log "Unsupported platform: $(uname -s)"
            exit 1
            ;;
    esac

    log "Done!"
}

main "$@"
