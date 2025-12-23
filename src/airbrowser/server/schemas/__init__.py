"""API schemas for Swagger documentation."""

from .browser import register_browser_schemas
from .responses import register_response_schemas

__all__ = ["register_browser_schemas", "register_response_schemas"]
