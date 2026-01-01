# Airbrowser

[![CI](https://github.com/ifokeev/airbrowser-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ifokeev/airbrowser-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Fair%20Source-blue.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white)](https://discord.gg/dP9PbTPHcN)

**AI Remote Browser** — Undetectable Chrome runtime for AI agents. REST API + MCP server + VNC debugging.

## Quick Start

### Cloud Hosted (no setup)

Use the managed cloud version - no installation required:

**[https://airbrowser.dev](https://airbrowser.dev)**

### Docker (one-liner)

```bash
docker run -d -p 18080:18080 --name airbrowser ghcr.io/ifokeev/airbrowser-mcp:latest
```

### Portable Downloads

Download and run - no Docker knowledge required:

| Platform | Download | Requirements |
|----------|----------|--------------|
| Linux | [airbrowser-linux.tar.gz](https://github.com/ifokeev/airbrowser-mcp/releases/latest/download/airbrowser-linux.tar.gz) | `uidmap` package or Docker |
| macOS | [airbrowser-mac.tar.gz](https://github.com/ifokeev/airbrowser-mcp/releases/latest/download/airbrowser-mac.tar.gz) | Colima, Docker Desktop, or Podman |
| Windows | [airbrowser-windows.zip](https://github.com/ifokeev/airbrowser-mcp/releases/latest/download/airbrowser-windows.zip) | Docker Desktop or Podman |

```bash
# Linux/macOS
tar -xzf airbrowser-*.tar.gz && cd airbrowser-* && ./airbrowser

# Windows: Extract zip and double-click airbrowser.bat
```

### From Source

```bash
git clone https://github.com/ifokeev/airbrowser-mcp.git
cd airbrowser-mcp
docker compose up --build
```

---

Open **http://localhost:18080** - all services available:

| Service | Path |
|---------|------|
| Dashboard | `/` |
| API Docs | `/docs/` |
| REST API | `/api/v1/` |
| MCP Server | `/mcp` |
| VNC Viewer | `/vnc/` |

## Features

- Undetected Chrome (SeleniumBase UC)
- 100+ concurrent browsers
- Persistent profiles & cookies
- Tab management
- Proxy per browser
- MCP for AI agents
- AI vision tools (optional)

## AI Vision (Recommended)

Enable AI-powered vision tools (`what_is_visible`, `detect_coordinates`) by setting your OpenRouter API key. Without it, these tools won't be available to AI agents.

```bash
# Docker run
docker run -d -p 18080:18080 -e OPENROUTER_API_KEY=sk-or-v1-xxx ghcr.io/ifokeev/airbrowser-mcp:latest

# Docker compose
OPENROUTER_API_KEY=sk-or-v1-xxx docker compose up
```

Get your API key at https://openrouter.ai/

## MCP Client Configuration

Add airbrowser to your AI coding assistant:

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add airbrowser --transport http http://localhost:18080/mcp
```
</details>

<details>
<summary><b>Cursor</b></summary>

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
</details>

<details>
<summary><b>VS Code / Copilot</b></summary>

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
</details>

<details>
<summary><b>Cline</b></summary>

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
</details>

<details>
<summary><b>Windsurf</b></summary>

Follow the [Windsurf MCP guide](https://docs.windsurf.com/windsurf/cascade/mcp) with the config above.
</details>

### Test your setup

```
Navigate to https://example.com and take a screenshot
```

Your AI assistant should create a browser, navigate to the URL, and return a screenshot.

## Generated Clients

Auto-generated from OpenAPI spec:

```bash
# Python
pip install airbrowser-client

# TypeScript
npm install airbrowser-client
```

## Docs

- [docs/](docs/) - Full documentation
- [examples/](examples/) - Code samples

## License

[Fair Source](LICENSE) - Free for up to 10 users. Cannot be offered as a hosted service. Commercial license required for larger deployments.
