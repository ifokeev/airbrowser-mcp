# Portable Builds

This directory contains build scripts for creating cross-platform portable releases of Airbrowser.

## Quick Start

### Download from Releases

Download the pre-built package for your platform from [GitHub Releases](../../releases):

- **Linux**: `airbrowser-X.X.X-linux.tar.gz`
- **macOS**: `airbrowser-X.X.X-mac.tar.gz`
- **Windows**: `airbrowser-X.X.X-windows.zip`

### Build Locally

```bash
# Build all platforms
./build-release.sh

# Build specific platform
./build-release.sh --linux
./build-release.sh --mac
./build-release.sh --windows

# Set version
VERSION=1.0.0 ./build-release.sh
```

Output goes to `dist/`.

## Platform Requirements

| Platform | Container Runtime Options |
|----------|---------------------------|
| Linux | Podman (recommended) or Docker |
| macOS | Colima, Docker Desktop, or Podman |
| Windows | Docker Desktop or Podman Desktop |

### Linux

```bash
# Install Podman (recommended - rootless, no daemon)
sudo apt install podman     # Ubuntu/Debian
sudo dnf install podman     # Fedora
sudo pacman -S podman       # Arch

# Or install Docker
curl -fsSL https://get.docker.com | sh
```

### macOS

```bash
# Colima (recommended - lightweight)
brew install colima docker
colima start

# Or Docker Desktop
brew install --cask docker

# Or Podman
brew install podman
podman machine init && podman machine start
```

### Windows

```powershell
# Docker Desktop (recommended)
winget install Docker.DockerDesktop

# Or Podman Desktop
winget install RedHat.Podman-Desktop
```

## How It Works

The portable packages contain:

1. **Platform-specific launcher** (`airbrowser` / `airbrowser.bat`)
2. **Container image** (`image.tar.gz`) - the complete Airbrowser environment

When you run the launcher:

1. Detects available container runtime (Podman/Docker)
2. Loads the container image (first run only)
3. Starts the server with appropriate network settings
4. Exposes services on localhost

## Network Access

| Platform | localhost Access |
|----------|------------------|
| Linux | Full (`--network=host`) |
| macOS | Port-mapped (8000, 6080, 5900) |
| Windows | Port-mapped (8000, 6080, 5900) |

Linux uses `--network=host` for unrestricted localhost access. macOS and Windows use port mapping due to VM-based container runtimes.

## Creating a Release

1. Tag the version:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. GitHub Actions automatically:
   - Builds the Docker image
   - Creates platform packages
   - Uploads to GitHub Releases

Or manually trigger via Actions → "Build and Release" → "Run workflow".
