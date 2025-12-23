# MCP Integration

## Overview

Airbrowser provides MCP (Model Context Protocol) support for AI agent integration. MCP tools are auto-generated from the core `BrowserOperations` module, ensuring consistency with the REST API.

## Quick Start

```python
from fastmcp import Client

async with Client("http://localhost:18080/mcp") as client:
    # Create browser
    result = await client.call_tool("create_browser", {"uc": True})
    browser_id = result["browser_id"]

    # Navigate
    await client.call_tool("navigate_browser", {
        "browser_id": browser_id,
        "url": "https://example.com"
    })

    # Take screenshot
    await client.call_tool("take_screenshot", {"browser_id": browser_id})

    # Close browser
    await client.call_tool("close_browser", {"browser_id": browser_id})
```

## Configuration

MCP is **enabled by default**. To disable:

```bash
ENABLE_MCP=false
```

Check status:
```bash
curl http://localhost:18080/mcp/status
```

## MCP Client Configuration

### Claude Code

```bash
claude mcp add airbrowser --transport http http://localhost:18080/mcp
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "airbrowser": {
      "url": "http://localhost:18080/mcp",
      "transport": "http"
    }
  }
}
```

### Cursor

Go to `Cursor Settings` → `MCP` → `Add new MCP Server`:

```json
{
  "mcpServers": {
    "airbrowser": {
      "url": "http://localhost:18080/mcp",
      "transport": "http"
    }
  }
}
```

### VS Code / Copilot

Add to your MCP settings:

```json
{
  "mcpServers": {
    "airbrowser": {
      "url": "http://localhost:18080/mcp",
      "transport": "http"
    }
  }
}
```

### Cline

Follow [Cline MCP guide](https://docs.cline.bot/mcp/configuring-mcp-servers) with:

```json
{
  "mcpServers": {
    "airbrowser": {
      "url": "http://localhost:18080/mcp",
      "transport": "http"
    }
  }
}
```

### Windsurf

Follow the [Windsurf MCP guide](https://docs.windsurf.com/windsurf/cascade/mcp) with the config above.

## Available Tools

Tools are auto-generated from `BrowserOperations`. Key tools:

| Tool | Description |
|------|-------------|
| `create_browser` | Create browser instance |
| `navigate_browser` | Navigate to URL |
| `click` | Click element by selector |
| `type_text` | Type text into element |
| `take_screenshot` | Capture screenshot |
| `what_is_visible` | AI-powered page analysis |
| `detect_coordinates` | Vision-based element detection |
| `gui_click` | Undetectable GUI click |
| `dialog` | Handle browser dialogs |
| `console_logs` | Get/clear console logs |
| `close_browser` | Close browser instance |

List all tools programmatically:
```python
tools = await client.list_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")
```

## Architecture

```
┌─────────────────────────────────────────┐
│           nginx (:18080)                │
│  /mcp → MCP Server (:3001)              │
│  /api/v1 → Flask API (:8000)            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│          BrowserOperations              │
│  (shared by both MCP and REST API)      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│            Browser Pool                 │
└─────────────────────────────────────────┘
```

## Troubleshooting

**MCP Not Available**
- Verify `ENABLE_MCP=true` (default)
- Check `curl http://localhost:18080/mcp/status`
- Review container logs for MCP initialization errors

**Connection Issues**
- Ensure container is running: `docker compose ps`
- Check nginx is proxying correctly: `curl http://localhost:18080/`
