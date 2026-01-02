# Examples

Practical examples showing common Airbrowser workflows.

## Prerequisites

```bash
# Start Airbrowser
docker compose up --build

# Install the Python client
uv pip install -e generated-clients/python
```

## Examples

| File | Description |
|------|-------------|
| [`basic_navigation.py`](basic_navigation.py) | Create browser, navigate, screenshot, cleanup |
| [`form_automation.py`](form_automation.py) | Fill forms, click buttons, handle inputs |
| [`mcp_agent_example.py`](mcp_agent_example.py) | MCP integration for AI agents |
| [`parallel_browsers.py`](parallel_browsers.py) | Run multiple browsers concurrently |
| [`proxy_rotation.py`](proxy_rotation.py) | Different proxy per browser instance |
| [`what_is_visible.py`](what_is_visible.py) | AI vision analysis of page content |
| [`cloudflare_captcha_vision.py`](cloudflare_captcha_vision.py) | AI vision to detect and click captcha (requires OPENROUTER_API_KEY) |

## Running Examples

```bash
# Basic navigation
uv run python examples/basic_navigation.py

# Form automation
uv run python examples/form_automation.py

# MCP agent (requires: uv pip install fastmcp)
uv run python examples/mcp_agent_example.py

# Parallel browsers
uv run python examples/parallel_browsers.py

# Proxy rotation (edit PROXIES list first)
uv run python examples/proxy_rotation.py
```

### AI Vision Examples

These examples require `OPENROUTER_API_KEY` to be set in the container:

```bash
# Start with vision enabled
OPENROUTER_API_KEY=sk-or-... docker compose up

# AI vision analysis
uv run python examples/what_is_visible.py

# Cloudflare captcha detection and click
uv run python examples/cloudflare_captcha_vision.py
```

## API Reference

All services at http://localhost:18080:

- Dashboard: http://localhost:18080/
- REST API Docs: http://localhost:18080/docs/
- MCP Endpoint: http://localhost:18080/mcp
- VNC Viewer: http://localhost:18080/vnc/
