# Airbrowser - Windows Launcher
# Uses WSL2 or Docker Desktop for container runtime

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataDir = "$env:LOCALAPPDATA\Airbrowser"
$ImageFile = "$ScriptDir\image.tar.gz"
$EnvFile = "$DataDir\.env"

function Write-Log { param($Message) Write-Host "[airbrowser] $Message" -ForegroundColor Green }
function Write-Warn { param($Message) Write-Host "[airbrowser] $Message" -ForegroundColor Yellow }
function Write-Err { param($Message) Write-Host "[airbrowser] $Message" -ForegroundColor Red }

# Check for Docker Desktop
function Test-DockerDesktop {
    try {
        $null = docker info 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Check for WSL2
function Test-WSL {
    try {
        $wslList = wsl --list --quiet 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Check for Podman
function Test-Podman {
    try {
        $null = podman info 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Load environment from .env file
function Import-EnvFile {
    if (Test-Path $EnvFile) {
        Write-Log "Loading environment from $EnvFile"
        Get-Content $EnvFile | ForEach-Object {
            if ($_ -match '^\s*([^#][^=]*)\s*=\s*(.*)$') {
                $name = $matches[1].Trim()
                $value = $matches[2].Trim()
                # Remove quotes if present
                $value = $value -replace '^["'']|["'']$', ''
                [Environment]::SetEnvironmentVariable($name, $value, "Process")
            }
        }
    }
}

# Environment variables to pass through to container
$EnvVars = @(
    "OPENROUTER_API_KEY",
    "OPENROUTER_COORD_MODEL",
    "OPENROUTER_ANALYSIS_MODEL",
    "MAX_BROWSERS",
    "LOG_LEVEL",
    "COMMAND_TIMEOUT_DEFAULT",
    "NAVIGATE_TIMEOUT_DEFAULT",
    "SCREEN_WIDTH",
    "SCREEN_HEIGHT"
)

# Build environment arguments for container
function Get-EnvArgs {
    $envArgs = @("-e", "API_BASE_URL=http://localhost:18080", "-e", "NGINX_HTTPS_PORT=18443")

    # Pass through all supported environment variables if set
    foreach ($var in $EnvVars) {
        $value = [Environment]::GetEnvironmentVariable($var, "Process")
        if ($value) {
            $envArgs += @("-e", "$var=$value")
        }
    }

    # Log if AI vision is enabled
    $apiKey = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "Process")
    if ($apiKey) {
        Write-Log "AI vision tools enabled"
    }

    return $envArgs
}

# Find available runtime
function Find-Runtime {
    if (Test-DockerDesktop) {
        return "docker"
    }
    if (Test-Podman) {
        return "podman"
    }
    if (Test-WSL) {
        return "wsl"
    }
    return $null
}

# Show install instructions
function Show-InstallInstructions {
    Write-Err "No container runtime found"
    Write-Host ""
    Write-Host "Install one of the following:"
    Write-Host ""
    Write-Host "  Docker Desktop (recommended):"
    Write-Host "    winget install Docker.DockerDesktop"
    Write-Host "    (Restart after installation)"
    Write-Host ""
    Write-Host "  Podman Desktop:"
    Write-Host "    winget install RedHat.Podman-Desktop"
    Write-Host ""
    Write-Host "  WSL2 + Docker:"
    Write-Host "    wsl --install"
    Write-Host "    (Then install Docker inside WSL)"
    Write-Host ""
    exit 1
}

# Load image into runtime
function Import-Image {
    param($Runtime)

    # Check if image already exists
    if ($Runtime -eq "wsl") {
        $exists = wsl docker image inspect airbrowser:latest 2>&1
    } else {
        $exists = & $Runtime image inspect airbrowser:latest 2>&1
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Log "Image already loaded"
        return
    }

    if (-not (Test-Path $ImageFile)) {
        Write-Err "Image file not found: $ImageFile"
        exit 1
    }

    Write-Log "Loading container image (this may take a moment)..."

    if ($Runtime -eq "wsl") {
        # Convert Windows path to WSL path
        $wslPath = wsl wslpath -u "$ImageFile"
        wsl bash -c "gunzip -c '$wslPath' | docker load"
    } else {
        # Use 7-zip or tar to extract, then load
        $tempTar = "$env:TEMP\airbrowser-image.tar"

        # Try to find gunzip/gzip
        if (Get-Command "gzip" -ErrorAction SilentlyContinue) {
            & gzip -d -c $ImageFile > $tempTar
        } elseif (Get-Command "7z" -ErrorAction SilentlyContinue) {
            & 7z e -so $ImageFile > $tempTar
        } else {
            Write-Err "Need gzip or 7-zip to extract image"
            Write-Host "Install with: winget install 7zip.7zip"
            exit 1
        }

        & $Runtime load -i $tempTar
        Remove-Item $tempTar -Force
    }

    Write-Log "Image loaded successfully"
}

# Start container
function Start-Container {
    param($Runtime)

    # Create data directories
    New-Item -ItemType Directory -Force -Path "$DataDir\profiles" | Out-Null
    New-Item -ItemType Directory -Force -Path "$DataDir\screenshots" | Out-Null
    New-Item -ItemType Directory -Force -Path "$DataDir\downloads" | Out-Null

    # Load environment from .env file if exists
    Import-EnvFile

    # Build environment arguments
    $envArgs = Get-EnvArgs

    Write-Log "Starting server..."
    Write-Host ""
    Write-Log "All services at https://localhost:18443 (or http://localhost:18080)"
    Write-Log "  Dashboard: /"
    Write-Log "  API Docs:  /docs/"
    Write-Log "  VNC:       /vnc/"
    Write-Log "  REST API:  /api/v1/"
    Write-Log "  MCP:       /mcp"
    Write-Host ""
    Write-Log "Press Ctrl+C to stop"
    Write-Host ""

    if ($Runtime -eq "wsl") {
        $wslDataDir = wsl wslpath -u "$DataDir"
        # Build WSL env args string
        $wslEnvStr = ($envArgs -join " ")
        wsl docker run --rm -it `
            --name airbrowser `
            -p 18080:18080 `
            -p 18443:18443 `
            -v "${wslDataDir}/profiles:/app/browser-profiles" `
            -v "${wslDataDir}/screenshots:/tmp/screenshots" `
            -v "${wslDataDir}/downloads:/app/downloads" `
            $wslEnvStr `
            airbrowser:latest
    } else {
        & $Runtime run --rm -it `
            --name airbrowser `
            -p 18080:18080 `
            -p 18443:18443 `
            -v "${DataDir}\profiles:/app/browser-profiles" `
            -v "${DataDir}\screenshots:/tmp/screenshots" `
            -v "${DataDir}\downloads:/app/downloads" `
            @envArgs `
            airbrowser:latest
    }
}

# Stop container
function Stop-Container {
    param($Runtime)

    if ($Runtime -eq "wsl") {
        wsl docker stop airbrowser 2>&1 | Out-Null
    } else {
        & $Runtime stop airbrowser 2>&1 | Out-Null
    }
    Write-Log "Stopped"
}

# Main
function Main {
    Write-Log "Starting Airbrowser..."

    $Runtime = Find-Runtime
    if (-not $Runtime) {
        Show-InstallInstructions
    }
    Write-Log "Using runtime: $Runtime"

    Import-Image $Runtime
    Start-Container $Runtime
}

# Handle arguments
switch ($args[0]) {
    "--help" {
        Write-Host "Airbrowser - Browser Automation Server"
        Write-Host ""
        Write-Host "Usage: .\launcher.ps1 [OPTIONS]"
        Write-Host ""
        Write-Host "Options:"
        Write-Host "  --help     Show this help"
        Write-Host "  --version  Show version"
        Write-Host "  --stop     Stop running instance"
        Write-Host ""
        Write-Host "All services available at https://localhost:18443 (or http://localhost:18080):"
        Write-Host "  Dashboard: /"
        Write-Host "  API Docs:  /docs/"
        Write-Host "  VNC:       /vnc/"
        Write-Host "  REST API:  /api/v1/"
        Write-Host "  MCP:       /mcp"
        Write-Host ""
        Write-Host "Environment Variables (set via .env file or environment):"
        Write-Host "  OPENROUTER_API_KEY       Enable AI vision tools (recommended)"
        Write-Host "  MAX_BROWSERS             Max concurrent browsers (default: 10)"
        Write-Host "  LOG_LEVEL                DEBUG, INFO, WARNING, ERROR (default: INFO)"
        Write-Host "  SCREEN_WIDTH/HEIGHT      Virtual display size (default: 1920x1080)"
        Write-Host ""
        Write-Host "  Create .env file in data directory:"
        Write-Host "    echo 'OPENROUTER_API_KEY=sk-or-v1-xxx' > `$env:LOCALAPPDATA\Airbrowser\.env"
    }
    "-h" {
        & $MyInvocation.MyCommand.Path --help
    }
    "--version" {
        Write-Host "Airbrowser v0.1.1"
    }
    "-v" {
        & $MyInvocation.MyCommand.Path --version
    }
    "--stop" {
        $Runtime = Find-Runtime
        if ($Runtime) {
            Stop-Container $Runtime
        }
    }
    default {
        Main
    }
}
