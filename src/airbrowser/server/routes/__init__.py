"""Route blueprints for Airbrowser API."""

from .auto_browser_routes import generate_browser_routes
from .health import create_health_namespace
from .pool import create_pool_namespace
from .profiles import create_profile_namespace

__all__ = [
    "generate_browser_routes",
    "create_pool_namespace",
    "create_health_namespace",
    "create_profile_namespace",
]
