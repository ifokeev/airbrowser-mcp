"""Shared response helpers for consistent API responses."""

from typing import Any


def success(data: dict | None = None, message: str = "Success") -> dict[str, Any]:
    """Create a success response with normalized format.

    All API responses follow the format: {success, message, data}
    """
    return {"success": True, "message": message, "data": data or {}}


def error(message: str) -> dict[str, Any]:
    """Create an error response with normalized format."""
    return {"success": False, "message": message, "data": None}
