# Airbrowser

[![CI](https://github.com/ifokeev/airbrowser-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ifokeev/airbrowser-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/airbrowser-client?label=PyPI&logo=python&logoColor=white)](https://pypi.org/project/airbrowser-client/)
[![npm](https://img.shields.io/npm/v/airbrowser-client?label=npm&logo=npm)](https://www.npmjs.com/package/airbrowser-client)
[![License](https://img.shields.io/badge/License-Fair%20Source-blue.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white)](https://discord.gg/dP9PbTPHcN)

**Open-source browser automation API with anti-detection** — Undetectable Chrome for AI agents, web scraping, and automation. REST API + MCP server + VNC debugging. Selenium/Playwright alternative that bypasses Cloudflare.

## Quick Start

### Cloud Hosted (no setup)

Use the managed cloud version - no installation required:

**[https://airbrowser.dev](https://airbrowser.dev)**

### Docker (one-liner)

```bash
docker run -d -p 18080:18080 --name airbrowser ghcr.io/ifokeev/airbrowser-mcp:latest

# With NVIDIA GPU (recommended for anti-detection)
docker run -d -p 18080:18080 --gpus all --device /dev/dri:/dev/dri --name airbrowser ghcr.io/ifokeev/airbrowser-mcp:latest
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

# With NVIDIA GPU
docker compose -f compose.gpu.yml up --build
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
- Proxy per browser ([DataImpulse](https://dataimpulse.com/?aff=250254) recommended)
- MCP for AI agents
- AI vision tools (optional)

## GPU Passthrough (Recommended)

GPU passthrough enables hardware-accelerated WebGL rendering via Vulkan, making the browser fingerprint match a real desktop machine. Without it, Chrome falls back to software rendering (SwiftShader) which is easily detected by anti-bot systems.

**Requirements:** NVIDIA GPU + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

```bash
# Docker Compose (recommended)
docker compose -f compose.gpu.yml up

# Docker run
docker run -d -p 18080:18080 \
  --gpus all \
  --device /dev/dri:/dev/dri \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  ghcr.io/ifokeev/airbrowser-mcp:latest

# Portable launcher
./airbrowser --gpu
```

Without a GPU, Chrome uses `--use-gl=swiftshader` automatically. With GPU passthrough, it uses `--use-gl=angle --use-angle=vulkan` for real GPU rendering.

## AI Vision (Optional)

Enable AI-powered vision tools (`what_is_visible`, `detect_coordinates`) with any OpenAI-compatible vision backend. Vision turns on only when `VISION_API_BASE_URL`, `VISION_API_KEY`, and `VISION_MODEL` are all set.

When smart targeting is enabled per request, `detect_coordinates` can validate a raw vision point, optionally snap to a nearby clickable target, and return both the original `click_point` and a `resolved_click_point` with an `outcome_status` that tells you whether the result was confirmed, corrected, or needs inspection before clicking. Pair that with `gui_click` or MCP-compatible `gui_click_xy` to re-check coordinate clicks and request post-click feedback.

```bash
# Docker run
docker run -d -p 18080:18080 \
  -e VISION_API_BASE_URL=https://your-openai-compatible-endpoint/v1 \
  -e VISION_API_KEY=your-api-key \
  -e VISION_MODEL=your-vision-model \
  ghcr.io/ifokeev/airbrowser-mcp:latest

# Docker compose
VISION_API_BASE_URL=https://your-openai-compatible-endpoint/v1 \
VISION_API_KEY=your-api-key \
VISION_MODEL=your-vision-model \
docker compose up
```

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

## Community

Join our [Discord server](https://discord.gg/dP9PbTPHcN) for support, feature requests, and discussion.

## Docs

- [docs/](docs/) - Full documentation
- [examples/](examples/) - Code samples

## License

[Fair Source](LICENSE) - Free for up to 10 users. Cannot be offered as a hosted service. Commercial license required for larger deployments.
