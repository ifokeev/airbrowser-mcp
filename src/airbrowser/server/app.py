"""Flask application factory for Airbrowser API."""

import os
import time

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_restx import Api
from werkzeug.exceptions import HTTPException

from .mcp.integration import MCPIntegration
from .services.browser_operations import BrowserOperations
from .services.browser_pool import BrowserPoolAdapter


def _env_truthy(name: str, default: bool = False) -> bool:
    """Check if environment variable is truthy."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def create_app():
    """Create and configure the Flask application."""

    # Initialize Flask app with static folder
    app = Flask(__name__, static_folder="static")
    CORS(app)

    # Set APPLICATION_ROOT for subpath routing (used by url_for)
    base_path = os.environ.get("BASE_PATH", "")
    if base_path:
        app.config["APPLICATION_ROOT"] = base_path

    # Initialize API with Swagger documentation
    # Disable built-in docs when using BASE_PATH (we serve custom docs)
    doc_path = False if base_path else "/docs/"
    api = Api(
        app,
        version="1.0",
        title="Airbrowser API",
        description="Undetectable Chrome-in-Docker for developers and agents (REST + MCP)",
        doc=doc_path,
        prefix="/api/v1",
    )

    # Initialize browser pool
    browser_pool = BrowserPoolAdapter(max_browsers=int(os.environ.get("MAX_BROWSERS", 50)))

    # Initialize shared browser operations
    browser_ops = BrowserOperations(browser_pool)

    # Initialize MCP integration (enabled by default)
    mcp_integration = None
    if os.environ.get("ENABLE_MCP", "true").lower() != "false":
        mcp_integration = MCPIntegration(browser_ops)

    # Store in app context
    app.browser_pool = browser_pool
    app.browser_ops = browser_ops
    app.mcp_integration = mcp_integration
    app.start_time = time.time()

    # Register schemas
    from .schemas.browser import register_browser_schemas
    from .schemas.responses import register_response_schemas

    browser_schemas = register_browser_schemas(api)
    response_schemas = register_response_schemas(api)

    app.schemas = {**browser_schemas, **response_schemas}

    # Register routes
    from .routes.auto_browser_routes import generate_browser_routes
    from .routes.health import create_health_namespace
    from .routes.pool import create_pool_namespace
    from .routes.profiles import create_profile_namespace

    # Auto-generated routes for all browser operations (from BrowserOperations class)
    browser_ns = generate_browser_routes(api, browser_ops, app.schemas)
    pool_ns = create_pool_namespace(api, browser_pool, app.schemas)
    health_ns = create_health_namespace(api, browser_ops, app.schemas)
    profiles_ns = create_profile_namespace(api, browser_pool, app.schemas)

    api.add_namespace(browser_ns, path="/browser")
    api.add_namespace(pool_ns, path="/pool")
    api.add_namespace(health_ns, path="/health")
    api.add_namespace(profiles_ns, path="/profiles")

    # CDP WebSocket proxy for external CDP access
    from .routes.cdp_proxy import init_cdp_proxy

    init_cdp_proxy(app)

    # Dashboard route
    @app.route("/dashboard")
    def dashboard():
        """Serve the browser pool dashboard with BASE_PATH injected."""
        base_path = os.environ.get("BASE_PATH", "")
        # Read the dashboard HTML and inject BASE_PATH
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        with open(os.path.join(static_dir, "dashboard.html")) as f:
            html = f.read()
        # Inject BASE_PATH script before closing </head> tag
        inject_script = f'<script>window.BASE_PATH = "{base_path}";</script>\n</head>'
        html = html.replace("</head>", inject_script)
        return html

    # Custom Swagger UI docs route with BASE_PATH support
    @app.route("/docs/")
    @app.route("/docs")
    def custom_docs():
        """Serve Swagger UI with BASE_PATH for subpath routing."""
        base_path = os.environ.get("BASE_PATH", "")
        swagger_ui_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Airbrowser API - Swagger UI</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="{base_path}/swaggerui/swagger-ui.css">
    <link rel="icon" type="image/png" href="{base_path}/swaggerui/favicon-32x32.png" sizes="32x32"/>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="{base_path}/swaggerui/swagger-ui-bundle.js"></script>
    <script src="{base_path}/swaggerui/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            SwaggerUIBundle({{
                url: "{base_path}/api/v1/swagger.json",
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "StandaloneLayout"
            }});
        }};
    </script>
</body>
</html>"""
        return swagger_ui_html

    # Screenshots route - serve screenshots publicly
    SCREENSHOT_DIR = "/tmp/screenshots"
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    @app.route("/screenshots/<path:filename>")
    def serve_screenshot(filename):
        """Serve screenshot files."""
        return send_from_directory(SCREENSHOT_DIR, filename)

    # Simple health endpoint for Docker healthcheck
    @app.route("/health")
    def docker_health():
        """Simple health check endpoint for Docker healthcheck."""
        try:
            pool_status = browser_pool.get_status()
            if isinstance(pool_status, dict):
                is_healthy = pool_status.get("healthy", False)
                status_dict = pool_status
            else:
                is_healthy = pool_status.healthy
                status_dict = pool_status.to_dict()

            return {"status": "healthy" if is_healthy else "degraded", "pool": status_dict, "timestamp": time.time()}
        except Exception as e:
            return {"status": "error", "message": str(e), "timestamp": time.time()}, 500

    # MCP status endpoint
    @app.route("/mcp/status")
    def mcp_status():
        """Get MCP server status."""
        if not mcp_integration:
            return jsonify({"success": False, "message": "MCP is not enabled. Set ENABLE_MCP=true to enable."}), 404

        # Check tool count via FastMCP's internal tool manager
        tool_count = 0
        if hasattr(mcp_integration.mcp, "_tool_manager"):
            tool_count = len(mcp_integration.mcp._tool_manager._tools)

        return jsonify(
            {
                "success": True,
                "message": "MCP server is integrated",
                "tools_available": tool_count > 0,
                "tool_count": tool_count,
                "info": "MCP tools are auto-generated from BrowserOperations",
            }
        )

    # Error handlers
    @api.errorhandler(HTTPException)
    def http_exception_handler(error):
        """Return clean JSON for HTTP exceptions."""
        return {"message": getattr(error, "description", str(error))}, getattr(error, "code", 400)

    @api.errorhandler
    def default_error_handler(error):
        """Fallback error handler for unexpected exceptions."""
        return {"message": str(error)}, 500

    return app, mcp_integration


def run_mcp_server_thread(mcp_integration):
    """Run MCP server in a background thread."""
    if mcp_integration:
        import threading

        mcp_port = int(os.environ.get("MCP_PORT", 3001))
        mcp_thread = threading.Thread(
            target=mcp_integration.run_mcp_server,
            kwargs={"host": "0.0.0.0", "port": mcp_port, "path": "/mcp", "quiet": True},
            daemon=True,
        )
        mcp_thread.start()
        print(f"MCP server integrated and running on port {mcp_port}")


def main():
    """Main entry point for the API server."""
    print("Starting Airbrowser API (REST + MCP)")

    app, mcp_integration = create_app()

    print(f"Max browsers: {app.browser_pool.max_browsers}")
    print("Using subprocess-based browser creation")
    print("Swagger UI available at: http://localhost:8000/docs/")

    # Start MCP server if enabled
    # Only start in the reloader child process (WERKZEUG_RUN_MAIN=true) or when not using reloader
    # This prevents the MCP server from starting twice in debug mode
    is_reloader_child = os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    debug_mode = _env_truthy("DEBUG", False)
    should_start_mcp = not debug_mode or is_reloader_child

    if mcp_integration and should_start_mcp:
        run_mcp_server_thread(mcp_integration)
    elif not mcp_integration:
        print("MCP server is disabled. Set ENABLE_MCP=true to enable.")

    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=debug_mode, threaded=True)


if __name__ == "__main__":
    main()
