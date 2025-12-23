"""Airbrowser server (REST + MCP).

This module provides both REST API and MCP (Model Context Protocol) interfaces
for browser automation.
"""

from .app import create_app, main
from .models import (
    ActionResult,
    BrowserAction,
    BrowserConfig,
    BrowserInfo,
    BrowserStatus,
    PoolStatus,
    get_window_size_from_env,
)

__all__ = [
    # App factory
    "create_app",
    "main",
    # Models
    "BrowserConfig",
    "BrowserInfo",
    "BrowserAction",
    "ActionResult",
    "PoolStatus",
    "BrowserStatus",
    "get_window_size_from_env",
]
