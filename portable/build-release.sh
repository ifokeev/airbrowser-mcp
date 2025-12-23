#!/bin/bash
# Build portable releases for all platforms
# Outputs: dist/airbrowser-{linux,mac,windows}.{tar.gz,zip}
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
VERSION="${VERSION:-0.1.0}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[build]${NC} $1"; }
info() { echo -e "${BLUE}[build]${NC} $1"; }
warn() { echo -e "${YELLOW}[build]${NC} $1"; }
error() { echo -e "${RED}[build]${NC} $1" >&2; }

# Clean previous builds
clean() {
    log "Cleaning previous builds..."
    rm -rf "$DIST_DIR"
    mkdir -p "$DIST_DIR"
}

# Build and export Docker image
build_image() {
    log "Building Docker image..."
    cd "$ROOT_DIR"
    docker build -t airbrowser:latest .

    log "Exporting image..."
    docker save airbrowser:latest | gzip > "$DIST_DIR/image.tar.gz"

    IMAGE_SIZE=$(du -h "$DIST_DIR/image.tar.gz" | cut -f1)
    info "Image size: $IMAGE_SIZE"
}

# Download static podman for Linux
download_podman_linux() {
    local arch=$1
    local output_dir=$2
    local podman_version="v5.3.1"
    local url="https://github.com/mgoltzsche/podman-static/releases/download/${podman_version}/podman-linux-${arch}.tar.gz"

    log "Downloading static podman ${podman_version} for linux-${arch}..."

    # Download and extract
    curl -fsSL "$url" -o "/tmp/podman-linux-${arch}.tar.gz"
    mkdir -p "$output_dir"
    tar -xzf "/tmp/podman-linux-${arch}.tar.gz" -C "$output_dir"
    rm "/tmp/podman-linux-${arch}.tar.gz"

    # The archive extracts to podman-linux-${arch}/
    # Rename to just 'podman'
    mv "$output_dir/podman-linux-${arch}" "$output_dir/podman"

    # Remove unnecessary files (man pages, systemd units) to reduce size
    rm -rf "$output_dir/podman/usr/local/share/man" 2>/dev/null || true
    rm -rf "$output_dir/podman/usr/lib/systemd" 2>/dev/null || true

    local podman_size=$(du -sh "$output_dir/podman" | cut -f1)
    info "Podman bundle size: $podman_size"
}

# Build Linux package
build_linux() {
    log "Building Linux package (with bundled podman)..."

    local arch="amd64"  # Default to amd64, can be parameterized
    local pkg_dir="$DIST_DIR/airbrowser-linux"
    mkdir -p "$pkg_dir"

    # Download static podman
    download_podman_linux "$arch" "$pkg_dir"

    # Copy launcher
    cp "$SCRIPT_DIR/linux/launcher.sh" "$pkg_dir/airbrowser"
    chmod +x "$pkg_dir/airbrowser"

    # Copy image
    cp "$DIST_DIR/image.tar.gz" "$pkg_dir/"

    # Create README
    cat > "$pkg_dir/README.txt" << 'EOF'
Airbrowser - Linux (Portable)

Quick Start:
  ./airbrowser           # Run interactively
  ./airbrowser -d        # Run in background
  ./airbrowser --stop    # Stop the server
  ./airbrowser --logs    # View logs

The server runs at:
  API:       http://localhost:8000
  Docs:      http://localhost:8000/docs
  Dashboard: http://localhost:18080
  VNC:       http://localhost:6080

This package includes:
  - Bundled podman (no Docker installation needed!)
  - Pre-built container image
  - All dependencies

Requirements:
  - uidmap package (one-time install):
      Ubuntu/Debian: sudo apt install uidmap
      Fedora/RHEL:   sudo dnf install shadow-utils
      Arch:          sudo pacman -S shadow

  OR if you prefer Docker:
  - Docker: https://docs.docker.com/engine/install/
EOF

    # Create tarball
    cd "$DIST_DIR"
    tar -czf "airbrowser-${VERSION}-linux.tar.gz" "airbrowser-linux"
    rm -rf "airbrowser-linux"

    local pkg_size=$(du -h "airbrowser-${VERSION}-linux.tar.gz" | cut -f1)
    info "Created: airbrowser-${VERSION}-linux.tar.gz ($pkg_size)"
}

# Build macOS package
build_mac() {
    log "Building macOS package..."

    local pkg_dir="$DIST_DIR/airbrowser-mac"
    mkdir -p "$pkg_dir"

    # Copy launcher
    cp "$SCRIPT_DIR/mac/launcher.sh" "$pkg_dir/airbrowser"
    chmod +x "$pkg_dir/airbrowser"

    # Copy image
    cp "$DIST_DIR/image.tar.gz" "$pkg_dir/"

    # Create README
    cat > "$pkg_dir/README.txt" << 'EOF'
Airbrowser - macOS

Quick Start:
  ./airbrowser

Requirements (install one):
  - Colima (recommended): brew install colima docker && colima start
  - Docker Desktop:       brew install --cask docker
  - Podman:               brew install podman

The server runs at:
  API:  http://localhost:8000
  Docs: http://localhost:8000/docs
  VNC:  http://localhost:6080

Options:
  ./airbrowser --help    Show help
  ./airbrowser --stop    Stop the server
EOF

    # Create tarball
    cd "$DIST_DIR"
    tar -czf "airbrowser-${VERSION}-mac.tar.gz" "airbrowser-mac"
    rm -rf "airbrowser-mac"

    info "Created: airbrowser-${VERSION}-mac.tar.gz"
}

# Build Windows package
build_windows() {
    log "Building Windows package..."

    local pkg_dir="$DIST_DIR/airbrowser-windows"
    mkdir -p "$pkg_dir"

    # Copy launchers
    cp "$SCRIPT_DIR/windows/launcher.ps1" "$pkg_dir/"
    cp "$SCRIPT_DIR/windows/airbrowser.bat" "$pkg_dir/"

    # Copy image
    cp "$DIST_DIR/image.tar.gz" "$pkg_dir/"

    # Create README
    cat > "$pkg_dir/README.txt" << 'EOF'
Airbrowser - Windows

Quick Start:
  Double-click: airbrowser.bat
  Or run in PowerShell: .\launcher.ps1

Requirements (install one):
  - Docker Desktop: winget install Docker.DockerDesktop
  - Podman Desktop: winget install RedHat.Podman-Desktop

The server runs at:
  API:  http://localhost:8000
  Docs: http://localhost:8000/docs
  VNC:  http://localhost:6080

Options:
  .\launcher.ps1 --help    Show help
  .\launcher.ps1 --stop    Stop the server
EOF

    # Create zip (Windows users expect .zip)
    cd "$DIST_DIR"
    if command -v zip &> /dev/null; then
        zip -rq "airbrowser-${VERSION}-windows.zip" "airbrowser-windows"
    else
        # Fallback to tar if zip not available
        tar -czf "airbrowser-${VERSION}-windows.tar.gz" "airbrowser-windows"
    fi
    rm -rf "airbrowser-windows"

    info "Created: airbrowser-${VERSION}-windows.zip"
}

# Generate checksums
generate_checksums() {
    log "Generating checksums..."
    cd "$DIST_DIR"

    # Remove temporary image file
    rm -f image.tar.gz

    # Generate SHA256 checksums
    sha256sum airbrowser-* > checksums.sha256

    info "Created: checksums.sha256"
}

# Create version-less copies for "latest" download links
create_latest_links() {
    log "Creating version-less copies for latest links..."
    cd "$DIST_DIR"

    # Create copies without version in filename (for GitHub /releases/latest/download/ URLs)
    cp "airbrowser-${VERSION}-linux.tar.gz" "airbrowser-linux.tar.gz"
    cp "airbrowser-${VERSION}-mac.tar.gz" "airbrowser-mac.tar.gz"
    cp "airbrowser-${VERSION}-windows.zip" "airbrowser-windows.zip"

    info "Created: airbrowser-{linux,mac,windows}.{tar.gz,zip}"
}

# Main
main() {
    echo ""
    echo "=========================================="
    echo "  Airbrowser - Release Builder"
    echo "  Version: $VERSION"
    echo "=========================================="
    echo ""

    clean
    build_image
    build_linux
    build_mac
    build_windows
    generate_checksums
    create_latest_links

    echo ""
    echo "=========================================="
    echo "  Build Complete!"
    echo "=========================================="
    echo ""
    log "Output directory: $DIST_DIR"
    ls -lh "$DIST_DIR"
    echo ""
    echo "Upload these files to GitHub Releases:"
    ls "$DIST_DIR"/*.{tar.gz,zip} 2>/dev/null || true
}

# Handle arguments
case "${1:-}" in
    --help|-h)
        echo "Build portable releases for all platforms"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help"
        echo "  --linux         Build only Linux package"
        echo "  --mac           Build only macOS package"
        echo "  --windows       Build only Windows package"
        echo ""
        echo "Environment:"
        echo "  VERSION         Release version (default: 0.1.0)"
        ;;
    --linux)
        clean
        build_image
        build_linux
        ;;
    --mac)
        clean
        build_image
        build_mac
        ;;
    --windows)
        clean
        build_image
        build_windows
        ;;
    *)
        main
        ;;
esac
