"""MCP integration for Airbrowser - auto-generates tools from BrowserOperations."""

import functools
import inspect
import os
import sys
import time
import traceback
from collections.abc import Callable
from typing import Any, get_type_hints

from fastmcp import FastMCP  # type: ignore

from ..services.browser_operations import BrowserOperations
from .tool_descriptions import TOOL_DESCRIPTIONS

# Methods that need start_time injected (not exposed to MCP clients)
_INJECT_START_TIME = {"get_pool_status", "health_check"}

# Methods to exclude from MCP (internal/private)
_EXCLUDED_METHODS = {"__init__", "__class__", "__repr__", "__str__"}

# Vision tools that require OPENROUTER_API_KEY
_VISION_TOOLS = {"what_is_visible", "detect_coordinates"}


class MCPIntegration:
    """Integrates MCP protocol with browser operations via auto-generation."""

    def __init__(self, browser_ops: BrowserOperations):
        self.browser_ops = browser_ops
        self.mcp = FastMCP("Airbrowser")
        self.start_time = time.time()
        self._register_tools()

    def _register_tools(self):
        """Auto-register all public BrowserOperations methods as MCP tools."""
        registered = []
        skipped_vision = []

        # Check if vision tools should be enabled
        # MCP_INCLUDE_ALL_TOOLS=true enables all tools (for doc generation)
        # OPENROUTER_API_KEY enables vision tools for actual use
        include_all_tools = os.environ.get("MCP_INCLUDE_ALL_TOOLS", "").lower() == "true"
        has_openrouter_key = bool(os.environ.get("OPENROUTER_API_KEY"))

        for name in dir(self.browser_ops):
            # Skip private/magic methods
            if name.startswith("_") or name in _EXCLUDED_METHODS:
                continue

            # Skip vision tools unless OPENROUTER_API_KEY is set or MCP_INCLUDE_ALL_TOOLS=true
            if name in _VISION_TOOLS and not (has_openrouter_key or include_all_tools):
                skipped_vision.append(name)
                continue

            method = getattr(self.browser_ops, name)

            # Only register callable methods
            if not callable(method):
                continue

            # Create MCP tool wrapper
            tool_func = self._create_tool_wrapper(name, method)
            if tool_func:
                self.mcp.tool(tool_func)
                registered.append(name)

        print(f"[MCP] Auto-registered {len(registered)} tools from BrowserOperations")
        if skipped_vision:
            print(f"[MCP] Vision tools disabled (set OPENROUTER_API_KEY to enable): {', '.join(skipped_vision)}")

    def _create_tool_wrapper(self, name: str, method: Callable) -> Callable | None:
        """Create an async MCP tool wrapper for a BrowserOperations method."""
        try:
            sig = inspect.signature(method)
            # Use enhanced description if available, otherwise fall back to method docstring
            doc = TOOL_DESCRIPTIONS.get(name) or inspect.getdoc(method) or f"Execute {name} operation."

            # Build parameter list excluding 'self' and special params
            params = []
            for param_name, param in sig.parameters.items():
                if param_name == "self":
                    continue
                # Skip start_time - we inject it internally
                if name in _INJECT_START_TIME and param_name == "start_time":
                    continue
                params.append((param_name, param))

            # Create the async wrapper function dynamically
            if name in _INJECT_START_TIME:
                # Special handling for methods needing start_time
                wrapper = self._create_start_time_wrapper(name, method, params, doc)
            else:
                wrapper = self._create_standard_wrapper(name, method, params, doc)

            return wrapper

        except Exception as e:
            print(f"[MCP] Warning: Could not register tool '{name}': {e}")
            return None

    def _create_standard_wrapper(self, name: str, method: Callable, params: list, doc: str) -> Callable:
        """Create a standard async wrapper for a method."""
        # Get type hints for better MCP schema generation
        try:
            hints = get_type_hints(method)
        except Exception:
            hints = {}

        # Create wrapper with correct signature
        @functools.wraps(method)
        async def wrapper(**kwargs) -> dict[str, Any]:
            return method(**kwargs)

        # Preserve original signature for FastMCP
        wrapper.__doc__ = doc
        wrapper.__name__ = name

        # Build new signature with only the exposed parameters
        new_params = []
        for param_name, param in params:
            # Preserve type annotation if available
            annotation = hints.get(param_name, param.annotation)
            new_param = inspect.Parameter(
                param_name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=param.default,
                annotation=annotation if annotation != inspect.Parameter.empty else Any,
            )
            new_params.append(new_param)

        # Set return type
        return_annotation = hints.get("return", dict[str, Any])
        wrapper.__signature__ = inspect.Signature(parameters=new_params, return_annotation=return_annotation)

        return wrapper

    def _create_start_time_wrapper(self, name: str, method: Callable, params: list, doc: str) -> Callable:
        """Create wrapper for methods that need start_time injected."""
        start_time = self.start_time

        @functools.wraps(method)
        async def wrapper(**kwargs) -> dict[str, Any]:
            return method(start_time=start_time, **kwargs)

        wrapper.__doc__ = doc
        wrapper.__name__ = name

        # These methods typically have no other params after excluding start_time
        wrapper.__signature__ = inspect.Signature(parameters=[], return_annotation=dict[str, Any])

        return wrapper

    def get_mcp_server(self):
        """Get the MCP server instance."""
        return self.mcp

    def run_mcp_server(self, host: str = "0.0.0.0", port: int = 3001, path: str = "/mcp", quiet: bool = False):
        """Run the MCP server independently."""
        try:
            if not quiet:
                print("🚀 Starting Airbrowser MCP Server")
                tool_count = len(self.mcp._tool_manager._tools) if hasattr(self.mcp, "_tool_manager") else "?"
                print(f"🔗 Available tools: {tool_count}")
                print("\n🎯 Ready to accept MCP tool calls from AI agents!")

            # Run the MCP server with HTTP transport
            self.mcp.run(transport="http", host=host, port=port, path=path)
        except Exception as e:
            print(f"[MCP] Fatal error starting MCP server: {e}", file=sys.stderr)
            traceback.print_exc()
