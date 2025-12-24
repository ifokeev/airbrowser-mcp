#!/usr/bin/env python3
"""Generate static documentation from OpenAPI spec and MCP tools."""

import argparse
import json
import re
import html
from pathlib import Path


def parse_openapi(openapi_path: str) -> dict:
    """Parse OpenAPI spec and extract endpoints."""
    with open(openapi_path) as f:
        spec = json.load(f)

    endpoints = []
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method in ("get", "post", "put", "delete", "patch"):
                endpoints.append({
                    "method": method.upper(),
                    "path": path,
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "tags": details.get("tags", []),
                    "parameters": details.get("parameters", []),
                    "request_body": details.get("requestBody", {}),
                })

    # Group by tag
    grouped = {}
    for ep in endpoints:
        tag = ep["tags"][0] if ep["tags"] else "Other"
        if tag not in grouped:
            grouped[tag] = []
        grouped[tag].append(ep)

    return {"endpoints": grouped, "info": spec.get("info", {})}


def parse_mcp_tools(tools_path: str) -> list:
    """Parse MCP tools from BrowserOperations class + enhanced descriptions."""
    from pathlib import Path

    # Get project root from tools_path
    project_root = Path(tools_path).parent.parent.parent.parent.parent
    browser_ops_path = project_root / "src/airbrowser/server/services/browser_operations.py"

    # Parse BrowserOperations for all public methods (these become MCP tools)
    tools = []
    with open(browser_ops_path) as f:
        content = f.read()

    # Find all method definitions with docstrings (handles multiline signatures)
    # Use a two-step approach: find method names, then find their docstrings
    method_pattern = r'^\s{4}def (\w+)\('
    method_names = re.findall(method_pattern, content, re.MULTILINE)

    # For each method, find its docstring
    methods = []
    for name in method_names:
        # Find the docstring after the method definition (handles multiline params)
        doc_pattern = rf'def {name}\([\s\S]*?\)(?:\s*->[^:]+)?:\s*"""([^"]+)"""'
        match = re.search(doc_pattern, content)
        if match:
            methods.append((name, match.group(1)))

    # Parse enhanced descriptions from tool_descriptions.py
    enhanced = {}
    with open(tools_path) as f:
        desc_content = f.read()
    desc_pattern = r'"(\w+)":\s*"""(.*?)"""'
    desc_matches = re.findall(desc_pattern, desc_content, re.DOTALL)
    for name, description in desc_matches:
        desc_lines = description.strip().split("\n")
        title = desc_lines[0].replace("**", "").strip() if desc_lines else ""
        body = "\n".join(desc_lines[1:]).strip() if len(desc_lines) > 1 else ""
        enhanced[name] = {"title": title, "description": body}

    # Build tools list: all BrowserOperations methods, enhanced where available
    for name, docstring in methods:
        if name.startswith("_"):
            continue

        if name in enhanced:
            tools.append({
                "name": name,
                "title": enhanced[name]["title"],
                "description": enhanced[name]["description"],
            })
        else:
            tools.append({
                "name": name,
                "title": docstring.strip(),
                "description": "",
            })

    return tools


def get_mcp_section_html(tools_json: str, tools_count: int) -> str:
    """Generate MCP tools section from template."""
    from pathlib import Path

    # Read the template
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "landing" / "docs" / "mcp-tools-section.html"

    with open(template_path) as f:
        template = f.read()

    # Inject the tools JSON data
    html = template.replace("{{MCP_TOOLS_JSON}}", tools_json)

    # Update tool count in the header badge and footer
    html = html.replace('>33 tools<', f'>{tools_count} tools<')
    html = html.replace('"countAll">33<', f'"countAll">{tools_count}<')
    html = html.replace('"visibleCount">33<', f'"visibleCount">{tools_count}<')
    html = html.replace('of <span>33<', f'of <span>{tools_count}<')

    return html


def generate_html(openapi_data: dict, mcp_tools: list, version: str) -> str:
    """Generate HTML documentation page."""

    def method_color(method: str) -> str:
        colors = {
            "GET": "#40B66B",
            "POST": "#4C82FB",
            "PUT": "#FF6B00",
            "DELETE": "#FF5757",
            "PATCH": "#FC72FF",
        }
        return colors.get(method, "#888")

    # Build REST API section
    api_sections = []
    for tag, endpoints in openapi_data["endpoints"].items():
        rows = []
        for ep in endpoints:
            color = method_color(ep["method"])
            desc = html.escape(ep["summary"] or ep["description"][:100])
            rows.append(f'''
                <tr>
                    <td><span class="method" style="background: {color}">{ep["method"]}</span></td>
                    <td><code>{html.escape(ep["path"])}</code></td>
                    <td>{desc}</td>
                </tr>''')

        api_sections.append(f'''
            <div class="api-group">
                <h4>{html.escape(tag)}</h4>
                <table class="endpoint-table">
                    <tbody>{"".join(rows)}</tbody>
                </table>
            </div>''')

    # Build MCP tools JSON for the terminal-style interface
    import json
    mcp_tools_json = json.dumps([{
        "name": tool["name"],
        "title": tool["title"],
        "description": tool["description"]
    } for tool in mcp_tools])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airbrowser Documentation</title>
    <meta name="description" content="API documentation for Airbrowser - REST endpoints, MCP tools, and client libraries.">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Satoshi:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-deep: #131313;
            --bg-card: #1b1b1b;
            --bg-elevated: #232323;
            --border: rgba(255, 255, 255, 0.08);
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.6);
            --text-muted: rgba(255, 255, 255, 0.4);
            --pink: #FC72FF;
            --blue: #4C82FB;
            --green: #40B66B;
            --orange: #FF6B00;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-deep);
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        nav {{
            position: sticky; top: 0; z-index: 100;
            padding: 16px 0;
            background: rgba(19, 19, 19, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
        }}
        .nav-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--text-primary); }}
        .logo img {{ width: 32px; height: 32px; }}
        .logo-text {{ font-weight: 700; font-size: 18px; }}
        .nav-links {{ display: flex; gap: 24px; }}
        .nav-links a {{ color: var(--text-secondary); text-decoration: none; font-size: 14px; font-weight: 500; }}
        .nav-links a:hover {{ color: var(--text-primary); }}

        .hero {{
            padding: 80px 0 60px;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }}
        .hero h1 {{ font-size: 48px; font-weight: 900; letter-spacing: -1px; margin-bottom: 16px; }}
        .hero p {{ font-size: 18px; color: var(--text-secondary); }}
        .version {{ display: inline-block; padding: 4px 12px; background: var(--bg-card); border-radius: 100px; font-size: 13px; color: var(--pink); margin-top: 16px; }}

        .section {{ padding: 60px 0; border-bottom: 1px solid var(--border); }}
        .section:last-child {{ border-bottom: none; }}
        .section-title {{
            font-size: 28px; font-weight: 700; margin-bottom: 32px;
            display: flex; align-items: center; gap: 12px;
        }}
        .section-title span {{ font-size: 24px; }}

        /* API Endpoints */
        .api-group {{ margin-bottom: 32px; }}
        .api-group h4 {{ font-size: 16px; font-weight: 600; margin-bottom: 12px; color: var(--pink); }}
        .endpoint-table {{ width: 100%; border-collapse: collapse; }}
        .endpoint-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }}
        .endpoint-table tr:hover {{ background: var(--bg-card); }}
        .endpoint-table td:first-child {{ width: 80px; }}
        .endpoint-table td:nth-child(2) {{ width: 300px; }}
        .endpoint-table code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: var(--text-primary);
        }}
        .method {{
            display: inline-block; padding: 4px 8px;
            border-radius: 4px; font-size: 11px; font-weight: 700;
            color: white; text-transform: uppercase;
        }}


        /* Code Examples */
        .code-tabs {{ display: flex; gap: 4px; margin-bottom: 0; }}
        .code-tab {{
            padding: 10px 20px; background: var(--bg-card);
            border: 1px solid var(--border); border-bottom: none;
            border-radius: 8px 8px 0 0; font-size: 13px; font-weight: 500;
            color: var(--text-muted); cursor: pointer;
        }}
        .code-tab.active {{ background: var(--bg-elevated); color: var(--text-primary); }}
        .code-block {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 0 8px 8px 8px;
            padding: 20px; overflow-x: auto;
        }}
        .code-block pre {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px; line-height: 1.6; margin: 0;
        }}
        .code-block .comment {{ color: var(--text-muted); }}
        .code-block .keyword {{ color: var(--pink); }}
        .code-block .string {{ color: var(--green); }}
        .code-block .function {{ color: var(--blue); }}

        footer {{ padding: 40px 0; text-align: center; color: var(--text-muted); font-size: 14px; }}
        footer a {{ color: var(--pink); text-decoration: none; }}

        @media (max-width: 768px) {{
            .tools-grid {{ grid-template-columns: 1fr; }}
            .endpoint-table td:nth-child(2) {{ width: auto; }}
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container nav-inner">
            <a href="../" class="logo">
                <img src="../logo.svg" alt="Airbrowser">
                <span class="logo-text">Airbrowser</span>
            </a>
            <div class="nav-links">
                <a href="#api">REST API</a>
                <a href="#mcp">MCP Tools</a>
                <a href="#clients">Clients</a>
                <a href="https://github.com/ifokeev/airbrowser-mcp" target="_blank">GitHub</a>
            </div>
        </div>
    </nav>

    <main>
        <section class="hero">
            <div class="container">
                <h1>Documentation</h1>
                <p>REST API, MCP tools, and client libraries for Airbrowser</p>
                <div class="version">v{version}</div>
            </div>
        </section>

        <section class="section" id="api">
            <div class="container">
                <h2 class="section-title"><span>🔌</span> REST API</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">
                    All endpoints are prefixed with <code>/api/v1</code>. Base URL: <code>http://localhost:18080/api/v1</code>
                </p>
                {"".join(api_sections)}
            </div>
        </section>

        <section class="section" id="mcp">
            <div class="container">
                <h2 class="section-title"><span>🤖</span> MCP Tools</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">
                    Model Context Protocol tools for AI agents. Connect via <code>http://localhost:18080/mcp</code>
                </p>
                {get_mcp_section_html(mcp_tools_json, len(mcp_tools))}
            </div>
        </section>

        <section class="section" id="clients">
            <div class="container">
                <h2 class="section-title"><span>📦</span> Client Libraries</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">
                    Auto-generated from OpenAPI spec. Install and start automating in minutes.
                </p>

                <div class="code-tabs">
                    <button class="code-tab active" onclick="showTab('python')">Python</button>
                    <button class="code-tab" onclick="showTab('typescript')">TypeScript</button>
                </div>
                <div class="code-block" id="python-code">
<pre><span class="comment"># Install</span>
pip install airbrowser-client

<span class="comment"># Usage</span>
<span class="keyword">from</span> airbrowser_client <span class="keyword">import</span> ApiClient, Configuration, BrowserApi

config = Configuration(host=<span class="string">"http://localhost:18080/api/v1"</span>)
<span class="keyword">with</span> ApiClient(config) <span class="keyword">as</span> client:
    api = BrowserApi(client)

    <span class="comment"># Create browser</span>
    response = api.<span class="function">create_browser</span>()
    browser_id = response.data.browser_id

    <span class="comment"># Navigate</span>
    api.<span class="function">navigate_browser</span>(browser_id, {{"url": <span class="string">"https://example.com"</span>}})

    <span class="comment"># Screenshot</span>
    screenshot = api.<span class="function">take_screenshot</span>(browser_id)

    <span class="comment"># Cleanup</span>
    api.<span class="function">close_browser</span>(browser_id)</pre>
                </div>
                <div class="code-block" id="typescript-code" style="display: none;">
<pre><span class="comment">// Install</span>
npm install airbrowser-client

<span class="comment">// Usage</span>
<span class="keyword">import</span> {{ BrowserApi, Configuration }} <span class="keyword">from</span> <span class="string">'airbrowser-client'</span>;

<span class="keyword">const</span> config = <span class="keyword">new</span> <span class="function">Configuration</span>({{{{
  basePath: <span class="string">'http://localhost:18080/api/v1'</span>
}}}});

<span class="keyword">const</span> api = <span class="keyword">new</span> <span class="function">BrowserApi</span>(config);

<span class="comment">// Create browser</span>
<span class="keyword">const</span> {{ data }} = <span class="keyword">await</span> api.<span class="function">createBrowser</span>();
<span class="keyword">const</span> browserId = data.data.browser_id;

<span class="comment">// Navigate</span>
<span class="keyword">await</span> api.<span class="function">navigateBrowser</span>(browserId, {{{{ url: <span class="string">'https://example.com'</span> }}}});

<span class="comment">// Screenshot</span>
<span class="keyword">const</span> screenshot = <span class="keyword">await</span> api.<span class="function">takeScreenshot</span>(browserId);

<span class="comment">// Cleanup</span>
<span class="keyword">await</span> api.<span class="function">closeBrowser</span>(browserId);</pre>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>Generated from <a href="https://github.com/ifokeev/airbrowser-mcp">source code</a>. Run <code>./scripts/generate_docs.sh</code> to regenerate.</p>
        </div>
    </footer>

    <script>
        function showTab(tab) {{
            document.querySelectorAll('.code-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.code-block[id$="-code"]').forEach(b => b.style.display = 'none');
            event.target.classList.add('active');
            document.getElementById(tab + '-code').style.display = 'block';
        }}
    </script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="Generate documentation")
    parser.add_argument("--openapi", required=True, help="Path to OpenAPI JSON")
    parser.add_argument("--mcp-tools", required=True, help="Path to MCP tools file")
    parser.add_argument("--output", required=True, help="Output HTML file")
    parser.add_argument("--template", help="Landing page template (unused, for reference)")
    parser.add_argument("--version", default="latest", help="Version string")
    args = parser.parse_args()

    # Parse sources
    openapi_data = parse_openapi(args.openapi)
    mcp_tools = parse_mcp_tools(args.mcp_tools)

    # Get version from args (preferred) or OpenAPI info
    version = args.version if args.version != "latest" else openapi_data["info"].get("version", "latest")

    # Generate HTML
    html_content = generate_html(openapi_data, mcp_tools, version)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)

    print(f"Generated: {output_path}")
    print(f"  - {sum(len(eps) for eps in openapi_data['endpoints'].values())} API endpoints")
    print(f"  - {len(mcp_tools)} MCP tools")


if __name__ == "__main__":
    main()
