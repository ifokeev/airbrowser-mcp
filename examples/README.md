# Examples

Practical examples showing common Airbrowser workflows.

## Prerequisites

```bash
# Start Airbrowser
docker compose up --build

# Install the Python client
pip install -e generated-clients/python
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

## Running Examples

```bash
# Basic navigation
python examples/basic_navigation.py

# Form automation
python examples/form_automation.py

# MCP agent (requires: pip install fastmcp)
python examples/mcp_agent_example.py

# Parallel browsers
python examples/parallel_browsers.py

# Proxy rotation (edit PROXIES list first)
python examples/proxy_rotation.py
```

## API Reference

All services at http://localhost:18080:

- Dashboard: http://localhost:18080/
- REST API Docs: http://localhost:18080/docs/
- MCP Endpoint: http://localhost:18080/mcp
- VNC Viewer: http://localhost:18080/vnc/
