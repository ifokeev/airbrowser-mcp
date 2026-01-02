#!/bin/bash

# Airbrowser Entrypoint Script

set -e

# Set default environment variables
export DISPLAY=${DISPLAY:-:99}
export BROWSER_POOL_HOST=${BROWSER_POOL_HOST:-0.0.0.0}
export BROWSER_POOL_PORT=${BROWSER_POOL_PORT:-8000}
export MAX_BROWSERS=${MAX_BROWSERS:-10}
export BROWSER_TIMEOUT=${BROWSER_TIMEOUT:-300}
export CLEANUP_INTERVAL=${CLEANUP_INTERVAL:-60}
export LOG_LEVEL=${LOG_LEVEL:-INFO}
# Ports (configurable). Note: with host networking these bind directly on the host.
export VNC_PORT=${VNC_PORT:-5900}
export NOVNC_PORT=${NOVNC_PORT:-6080}
export NGINX_HTTP_PORT=${NGINX_HTTP_PORT:-18080}
export NGINX_HTTPS_PORT=${NGINX_HTTPS_PORT:-18443}
export DISABLE_NGINX=${DISABLE_NGINX:-false}

# Create necessary directories (ignore errors if they exist)
mkdir -p /app/browser-profiles 2>/dev/null || true
mkdir -p /app/screenshots 2>/dev/null || true
mkdir -p /app/downloads 2>/dev/null || true
mkdir -p /app/certs 2>/dev/null || true
mkdir -p /app/state 2>/dev/null || true
mkdir -p /tmp/.X11-unix 2>/dev/null || true
mkdir -p /home/browseruser/.fluxbox 2>/dev/null || true
mkdir -p /home/browseruser/.local/share/applications 2>/dev/null || true

# Set proper permissions (ignore errors)
chmod 1777 /tmp/.X11-unix 2>/dev/null || true
chmod 777 /tmp 2>/dev/null || true

# Ensure browseruser owns the app directories
chown -R browseruser:browseruser /app/browser-profiles /app/screenshots /app/downloads /app/certs /app/state 2>/dev/null || true
chown -R browseruser:browseruser /home/browseruser 2>/dev/null || true

# Create mimeapps.list file if it doesn't exist
touch /home/browseruser/.local/share/applications/mimeapps.list 2>/dev/null || true

# Generate SSL certificates for nginx HTTPS
echo "🔐 Checking SSL certificates for nginx..."

if [ ! -f /app/certs/cert.pem ] || [ ! -f /app/certs/key.pem ]; then
    echo "🔒 Generating self-signed SSL certificates..."
    
    # Generate self-signed certificate
    openssl req -x509 -newkey rsa:2048 \
        -keyout /app/certs/key.pem \
        -out /app/certs/cert.pem \
        -days 365 -nodes \
        -subj "/CN=localhost/O=Airbrowser/C=US" 2>/dev/null || {
        echo "❌ Failed to generate SSL certificates"
        exit 1
    }
    
    echo "✅ SSL certificates generated successfully"
    chmod 600 /app/certs/key.pem 2>/dev/null || true
    chmod 644 /app/certs/cert.pem 2>/dev/null || true
else
    echo "✅ SSL certificates already exist"
fi

# Print startup information
echo "========================================="
echo "Airbrowser Starting"
echo "========================================="
echo "Display: $DISPLAY"
echo "Host: $BROWSER_POOL_HOST"
echo "Port: $BROWSER_POOL_PORT"
echo "Max Browsers: $MAX_BROWSERS"
echo "Browser Timeout: $BROWSER_TIMEOUT"
echo "Cleanup Interval: $CLEANUP_INTERVAL"
echo "Log Level: $LOG_LEVEL"
echo "HTTP (nginx): Port $NGINX_HTTP_PORT"
echo "HTTPS (nginx): Port $NGINX_HTTPS_PORT"
echo "========================================="

# Verify Chrome installation
if command -v google-chrome >/dev/null 2>&1; then
    echo "Chrome version: $(google-chrome --version)"
else
    echo "ERROR: Chrome not found!"
    exit 1
fi

# Verify Python dependencies
echo "Verifying Python dependencies..."
python -c "import seleniumbase; print(f'SeleniumBase version: {seleniumbase.__version__}')" || {
    echo "ERROR: SeleniumBase not properly installed!"
    exit 1
}

python -c "import flask; print(f'Flask version: {flask.__version__}')" || {
    echo "ERROR: Flask not properly installed!"
    exit 1
}

# Start Xvfb and VNC services
echo "==========================================="
echo "🖥️  Starting Display and VNC Services"
echo "==========================================="

# Clean up any existing X server more thoroughly
echo "Cleaning up existing display..."
pkill -f "Xvfb" || true
pkill -f "fluxbox" || true  
pkill -f "x11vnc" || true
pkill -f "websockify" || true

# Wait for processes to terminate
sleep 2

# Force remove lock files and sockets (ignore permission errors)
rm -f /tmp/.X*-lock 2>/dev/null || true
rm -f /tmp/.X11-unix/X* 2>/dev/null || true
rm -f /tmp/.X99-lock 2>/dev/null || true

# Ensure X11 directory exists and has correct permissions
mkdir -p /tmp/.X11-unix 2>/dev/null || true
chmod 1777 /tmp/.X11-unix 2>/dev/null || true

# Start Xvfb with configurable screen resolution
# Allow overriding via SCREEN_WIDTH/SCREEN_HEIGHT/SCREEN_DEPTH for convenience
if [[ -n "$SCREEN_WIDTH" && -n "$SCREEN_HEIGHT" ]]; then
  export SCREEN_DEPTH=${SCREEN_DEPTH:-24}
  export SCREEN_RESOLUTION="${SCREEN_WIDTH}x${SCREEN_HEIGHT}x${SCREEN_DEPTH}"
fi

export SCREEN_RESOLUTION=${SCREEN_RESOLUTION:-1600x900x24}
export SCREEN_DPI=${SCREEN_DPI:-96}
echo "🚀 Starting Xvfb on display $DISPLAY with resolution $SCREEN_RESOLUTION (DPI: $SCREEN_DPI)..."
Xvfb $DISPLAY -screen 0 $SCREEN_RESOLUTION -dpi $SCREEN_DPI -ac +extension GLX +render -noreset -nolisten tcp &
XVFB_PID=$!

# Wait for Xvfb to initialize
sleep 3

# Verify Xvfb is running
if ! pgrep -f "Xvfb" > /dev/null; then
    echo "❌ ERROR: Xvfb failed to start!"
    exit 1
fi

echo "✅ Xvfb started successfully (PID: $XVFB_PID)"

# Start window manager
echo "🪟 Starting Fluxbox window manager..."
# Configure Fluxbox to use a single workspace by default (configurable)
FLUXBOX_WORKSPACES=${FLUXBOX_WORKSPACES:-1}

# Prepare Fluxbox init with desired workspace count
FLUXBOX_INIT="/home/browseruser/.fluxbox/init"
touch "$FLUXBOX_INIT" 2>/dev/null || true
chown browseruser:browseruser "$FLUXBOX_INIT" 2>/dev/null || true

# Update or append workspace settings
if grep -q "^session.screen0.workspaces:" "$FLUXBOX_INIT" 2>/dev/null; then
  sed -i "s/^session.screen0.workspaces:.*/session.screen0.workspaces: $FLUXBOX_WORKSPACES/" "$FLUXBOX_INIT" || true
else
  echo "session.screen0.workspaces: $FLUXBOX_WORKSPACES" >> "$FLUXBOX_INIT"
fi

# Some Fluxbox versions use workspaceCount; set it too for compatibility
if grep -q "^session.screen0.workspaceCount:" "$FLUXBOX_INIT" 2>/dev/null; then
  sed -i "s/^session.screen0.workspaceCount:.*/session.screen0.workspaceCount: $FLUXBOX_WORKSPACES/" "$FLUXBOX_INIT" || true
else
  echo "session.screen0.workspaceCount: $FLUXBOX_WORKSPACES" >> "$FLUXBOX_INIT"
fi

# Ensure the workspace name list matches the count (avoid extra tabs/pager entries)
if [ "$FLUXBOX_WORKSPACES" = "1" ]; then
  if grep -q "^session.screen0.workspaceNames:" "$FLUXBOX_INIT" 2>/dev/null; then
    sed -i "s/^session.screen0.workspaceNames:.*/session.screen0.workspaceNames: Workspace/" "$FLUXBOX_INIT" || true
  else
    echo "session.screen0.workspaceNames: Workspace" >> "$FLUXBOX_INIT"
  fi
fi

fluxbox -display $DISPLAY 2>/dev/null &
FLUXBOX_PID=$!

# Wait for window manager
sleep 2

echo "✅ Fluxbox started successfully (PID: $FLUXBOX_PID)"

# Start VNC server
echo "📺 Starting VNC server..."
x11vnc -display $DISPLAY -forever -shared -nopw -noxdamage -noxfixes -noxrandr -wait 10 -xkb -noxrecord -rfbport "$VNC_PORT" &
VNC_PID=$!

# Wait for VNC server to start
sleep 2

if ! pgrep -f "x11vnc" > /dev/null; then
    echo "⚠️  WARNING: x11vnc failed to start, but continuing..."
else
    echo "✅ VNC server started successfully (PID: $VNC_PID)"
fi

# Start noVNC websocket proxy
echo "🌐 Starting noVNC web interface..."
websockify --web=/opt/noVNC "$NOVNC_PORT" "localhost:$VNC_PORT" &
WEBSOCKIFY_PID=$!

# Wait for websockify to start
sleep 2

if ! pgrep -f "websockify" > /dev/null; then
    echo "⚠️  WARNING: websockify failed to start, but continuing..."
else
    echo "✅ noVNC web interface started successfully (PID: $WEBSOCKIFY_PID)"
fi

# Configure noVNC default behavior via environment variables
# Allow users to set scaling/resizing mode without using the UI each time
NOVNC_RESIZE=${NOVNC_RESIZE:-scale}         # off | scale | remote
NOVNC_AUTOCONNECT=${NOVNC_AUTOCONNECT:-true} # true | false
NOVNC_VIEW_ONLY=${NOVNC_VIEW_ONLY:-false}    # true | false
NOVNC_RECONNECT=${NOVNC_RECONNECT:-true}     # true | false
NOVNC_RECONNECT_DELAY=${NOVNC_RECONNECT_DELAY:-2} # seconds

# Replace default index.html symlink with a small redirector that applies defaults
if [ -L /opt/noVNC/index.html ]; then
  rm -f /opt/noVNC/index.html || true
fi
cat > /opt/noVNC/index.html <<EOF
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>noVNC</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script>
      (function() {
        var params = new URLSearchParams(window.location.search);
        if (!params.has('autoconnect')) params.set('autoconnect', '${NOVNC_AUTOCONNECT}');
        if (!params.has('resize')) params.set('resize', '${NOVNC_RESIZE}');
        if (!params.has('view_only')) params.set('view_only', '${NOVNC_VIEW_ONLY}');
        if (!params.has('reconnect')) params.set('reconnect', '${NOVNC_RECONNECT}');
        if (!params.has('reconnect_delay')) params.set('reconnect_delay', '${NOVNC_RECONNECT_DELAY}');
        var url = 'vnc.html?' + params.toString();
        window.location.replace(url);
      })();
    </script>
  </head>
  <body>
    <noscript>
      <meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=${NOVNC_AUTOCONNECT}&resize=${NOVNC_RESIZE}&view_only=${NOVNC_VIEW_ONLY}&reconnect=${NOVNC_RECONNECT}&reconnect_delay=${NOVNC_RECONNECT_DELAY}">
    </noscript>
  </body>
</html>
EOF

echo "==========================================="
echo "🎯 VNC Access Information:"
echo "   VNC Viewer: localhost:5900"
echo "   Web Browser: http://localhost:6080"
echo "==========================================="

# Cleanup function
cleanup() {
    echo "🛑 Shutting down browser pool and VNC services..."
    
    # Kill VNC and web services
    if [ -n "$VNC_PID" ]; then
        kill $VNC_PID 2>/dev/null || true
    fi
    
    if [ -n "$WEBSOCKIFY_PID" ]; then
        kill $WEBSOCKIFY_PID 2>/dev/null || true
    fi
    
    # Kill window manager and display server
    if [ -n "$FLUXBOX_PID" ]; then
        kill $FLUXBOX_PID 2>/dev/null || true
    fi
    
    if [ -n "$XVFB_PID" ]; then
        kill $XVFB_PID 2>/dev/null || true
    fi
    
    # Kill any remaining processes
    pkill -f "websockify" || true
    pkill -f "x11vnc" || true
    pkill -f "fluxbox" || true
    pkill -f "Xvfb" || true
    
    echo "✅ Cleanup completed"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start nginx for HTTPS support
if [ "${DISABLE_NGINX,,}" != "true" ]; then
    echo "🌐 Rendering nginx config and starting nginx..."
    if [ -f /etc/nginx/nginx.conf.template ]; then
        python - <<'PY'
import os
from pathlib import Path

template_path = Path("/etc/nginx/nginx.conf.template")
out_path = Path("/etc/nginx/nginx.conf")

text = template_path.read_text(encoding="utf-8")
replacements = {
    "${NGINX_HTTP_PORT}": os.environ.get("NGINX_HTTP_PORT", "18080"),
    "${NGINX_HTTPS_PORT}": os.environ.get("NGINX_HTTPS_PORT", "18443"),
    "${NOVNC_PORT}": os.environ.get("NOVNC_PORT", "6080"),
}
for k, v in replacements.items():
    text = text.replace(k, v)
out_path.write_text(text, encoding="utf-8")
PY
    fi

    nginx
    if pgrep -f "nginx" > /dev/null; then
        echo "✅ nginx started successfully (HTTP: $NGINX_HTTP_PORT, HTTPS: $NGINX_HTTPS_PORT)"
    else
        echo "⚠️  WARNING: nginx failed to start"
    fi
else
    echo "ℹ️  nginx disabled (DISABLE_NGINX=true)"
fi

# Default mode - run both Flask API and MCP server
echo "Starting browser pool services..."
echo ""
echo "🌐 All services available at http://localhost:$NGINX_HTTP_PORT"
echo "   Dashboard: /"
echo "   REST API:  /api/v1/"
echo "   MCP:       /mcp"
echo "   VNC:       /vnc/"
echo "   API Docs:  /docs/"
echo ""
cd /app

# Start supervisord (allow dev override via bind-mounted config)
SUPERVISOR_CONFIG=${SUPERVISOR_CONFIG:-/etc/supervisor/conf.d/supervisord.conf}
if [ "${FLASK_ENV:-}" = "development" ] && [ -f "/app/docker/supervisord.dev.conf" ]; then
  SUPERVISOR_CONFIG="/app/docker/supervisord.dev.conf"
fi

exec supervisord -c "$SUPERVISOR_CONFIG"
