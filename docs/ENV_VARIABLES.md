# Environment Variables

This document describes all environment variables used by Airbrowser.

## Quick Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_BROWSERS` | 10 | Maximum concurrent browser instances |
| `LOG_LEVEL` | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `OPENROUTER_API_KEY` | - | API key for AI vision features |
| `COMMAND_TIMEOUT_DEFAULT` | 20 | Default timeout for browser commands (seconds) |
| `NAVIGATE_TIMEOUT_DEFAULT` | 60 | Default timeout for page navigation (seconds) |
| `API_BASE_URL` | http://localhost:18080 | Base URL for the API server |

## Core Settings

### `MAX_BROWSERS`
- **Default:** 10
- **Description:** Maximum number of concurrent browser instances allowed in the pool.
- **Usage:** Set higher for production workloads, lower for development to save resources.

```bash
MAX_BROWSERS=20 docker compose up
```

### `LOG_LEVEL`
- **Default:** INFO
- **Description:** Controls logging verbosity.
- **Values:** DEBUG, INFO, WARNING, ERROR
- **Usage:** Use DEBUG for development, INFO for production.

```bash
LOG_LEVEL=DEBUG docker compose -f compose.local.yml up
```

## AI Vision

### `OPENROUTER_API_KEY`
- **Default:** None (vision features disabled)
- **Description:** API key for OpenRouter, enabling AI-powered vision tools.
- **Required for:** `what_is_visible`, `detect_coordinates` tools
- **Get a key:** https://openrouter.ai/

```bash
OPENROUTER_API_KEY=sk-or-v1-xxx docker compose up
```

### `OPENROUTER_COORD_MODEL`
- **Default:** google/gemini-3-flash-preview
- **Description:** Vision model used for `detect_coordinates` (element location).
- **Usage:** Override to use a different model for coordinate detection.

```bash
OPENROUTER_COORD_MODEL=anthropic/claude-3.5-sonnet docker compose up
```

### `OPENROUTER_ANALYSIS_MODEL`
- **Default:** google/gemini-3-flash-preview
- **Description:** Vision model used for `what_is_visible` (page analysis).
- **Usage:** Override to use a different model for page state analysis.

```bash
OPENROUTER_ANALYSIS_MODEL=anthropic/claude-3.5-sonnet docker compose up
```

## Timeouts

### `COMMAND_TIMEOUT_DEFAULT`
- **Default:** 20
- **Description:** Default timeout in seconds for browser commands (click, type, wait, etc.).
- **Usage:** Increase for slow connections or complex pages.

```bash
# Increase default command timeout to 30 seconds
COMMAND_TIMEOUT_DEFAULT=30 docker compose up
```

### `NAVIGATE_TIMEOUT_DEFAULT`
- **Default:** 60
- **Description:** Default timeout in seconds for page navigation.
- **Usage:** Increase for slow-loading pages or poor network conditions.

```bash
# Increase navigation timeout to 120 seconds
NAVIGATE_TIMEOUT_DEFAULT=120 docker compose up
```

### `IPC_TIMEOUT_SLACK`
- **Default:** 5
- **Description:** Additional seconds added to IPC timeouts for safety margin.

## Display & Screen

### `SCREEN_WIDTH` / `SCREEN_HEIGHT`
- **Default:** 1920 x 1080
- **Description:** Virtual display resolution for browser rendering.
- **Usage:** Set both together to override `SCREEN_RESOLUTION`.

```bash
SCREEN_WIDTH=1366 SCREEN_HEIGHT=768 docker compose up
```

### `SCREEN_RESOLUTION`
- **Default:** 1920x1080x24
- **Description:** Full resolution string (width x height x depth).
- **Note:** `SCREEN_WIDTH`/`SCREEN_HEIGHT` take precedence if set.

### `SCREEN_DPI`
- **Default:** 96
- **Description:** Display DPI for the virtual screen.

## API Settings

### `API_BASE_URL`
- **Default:** http://localhost:18080
- **Description:** Base URL for the API server. Used internally and passed to containers.
- **Usage:** Override when running behind a reverse proxy or with custom networking.

```bash
API_BASE_URL=https://api.example.com docker compose up
```

## Network Ports

### `NGINX_HTTP_PORT`
- **Default:** 18080
- **Description:** Main entry point port (nginx proxy).

### `MCP_PORT`
- **Default:** 3001
- **Description:** MCP server port (proxied via nginx at `/mcp`).

### `VNC_PORT`
- **Default:** 5900
- **Description:** VNC server port for remote viewing.

### `NOVNC_PORT`
- **Default:** 6080
- **Description:** noVNC web interface port (proxied via nginx at `/vnc/`).

### `PORT`
- **Default:** 8000
- **Description:** Flask REST API port.

## Directories

### `PROFILES_DIR`
- **Default:** /app/browser-profiles
- **Description:** Directory for persistent browser profiles.

### `SCREENSHOTS_DIR`
- **Default:** /tmp/screenshots
- **Description:** Directory for screenshot storage.

## Feature Flags

### `ENABLE_MCP`
- **Default:** true
- **Description:** Enable/disable MCP server.

```bash
ENABLE_MCP=false docker compose up  # Disable MCP
```

### `DISABLE_NGINX`
- **Default:** false
- **Description:** Disable nginx proxy (use direct ports instead).

## noVNC Settings

### `NOVNC_RESIZE`
- **Default:** scale
- **Description:** How noVNC handles display resizing.
- **Values:** off, scale, remote

### `NOVNC_AUTOCONNECT`
- **Default:** true
- **Description:** Automatically connect when opening noVNC web interface.

### `NOVNC_VIEW_ONLY`
- **Default:** false
- **Description:** Disable mouse/keyboard input in noVNC (view only mode).

### `NOVNC_RECONNECT`
- **Default:** true
- **Description:** Automatically reconnect on disconnect.

### `NOVNC_RECONNECT_DELAY`
- **Default:** 2
- **Description:** Seconds to wait before reconnecting.

## Compose File Defaults

Each compose file sets appropriate defaults for its use case:

| Variable | compose.yml | compose.local.yml | compose.test.yml |
|----------|-------------|-------------------|------------------|
| `MAX_BROWSERS` | 10 | 5 | 10 |
| `LOG_LEVEL` | INFO | DEBUG | INFO |
| `COMMAND_TIMEOUT_DEFAULT` | (default) | 90 | 90 |
| `SCREEN_WIDTH` | (default) | 1366 | 1366 |
| `SCREEN_HEIGHT` | (default) | 768 | 768 |

## Example .env File

```bash
# .env (copy from .env.example)

# Optional: enables AI-powered vision tools
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```
