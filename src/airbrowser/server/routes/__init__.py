"""Route blueprints for Airbrowser API."""

from .browser import create_browser_namespace
from .health import create_health_namespace
from .pool import create_pool_namespace
from .profiles import create_profile_namespace

__all__ = [
    "create_browser_namespace",
    "create_pool_namespace",
    "create_health_namespace",
    "create_profile_namespace",
]
