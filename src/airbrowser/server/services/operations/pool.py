"""Pool management operations (status, health check)."""

import time
from typing import Any

from ..browser_pool import BrowserPoolAdapter


class PoolOperations:
    """Handles browser pool management operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def get_pool_status(self, start_time: float | None = None) -> dict[str, Any]:
        """Get the current status of the browser pool."""
        try:
            pool_status = self.browser_pool.get_status()

            # Handle both dict and object responses
            if isinstance(pool_status, dict):
                status_dict = pool_status
                is_healthy = pool_status.get("healthy", False)
            else:
                status_dict = pool_status.to_dict()
                is_healthy = getattr(pool_status, "healthy", False)

            result = {
                "success": True,
                "message": "Pool status retrieved successfully",
                "data": {
                    "status": "healthy" if is_healthy else "degraded",
                    "pool_metrics": status_dict,
                    "active_browsers": status_dict.get("active_browsers", 0) if isinstance(status_dict, dict) else 0,
                },
            }

            if start_time:
                result["uptime_seconds"] = time.time() - start_time

            return result

        except Exception as e:
            return {"success": False, "error": f"Failed to get pool status: {str(e)}"}

    def health_check(self, start_time: float | None = None) -> dict[str, Any]:
        """Perform a health check of the browser pool server."""
        try:
            pool_status = self.browser_pool.get_status()

            # Handle both dict and object responses
            if isinstance(pool_status, dict):
                active = pool_status.get("active_browsers", 0)
                total = pool_status.get("total_browsers", 0)
                is_healthy = pool_status.get("healthy", False)
            else:
                active = getattr(pool_status, "active_browsers", 0)
                total = getattr(pool_status, "total_browsers", 0)
                is_healthy = getattr(pool_status, "healthy", False)

            result = {
                "success": True,
                "status": "healthy" if is_healthy else "degraded",
                "server": "Airbrowser",
                "version": "1.0.0",
                "pool_metrics": {
                    "active_browsers": active,
                    "total_browsers": total,
                    "max_browsers": self.browser_pool.max_browsers,
                },
                "message": "Health check completed",
            }

            if start_time:
                result["uptime_seconds"] = time.time() - start_time

            return result

        except Exception as e:
            return {"success": False, "error": f"Health check failed: {str(e)}"}
