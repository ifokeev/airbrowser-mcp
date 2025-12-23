"""Health check routes for Airbrowser API."""

import time

from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException


def create_health_namespace(api, browser_pool, schemas):
    """Create and configure the health namespace."""

    health_ns = Namespace("health", description="Health and monitoring")

    @health_ns.route("/")
    class HealthCheck(Resource):
        @health_ns.doc("health_check")
        @health_ns.response(200, "Success", schemas["HealthStatus"])
        def get(self):
            """Check the health status of the browser pool."""
            try:
                pool_status = browser_pool.get_status()
                if isinstance(pool_status, dict):
                    is_healthy = pool_status.get("healthy", False)
                    status_dict = pool_status
                else:
                    is_healthy = pool_status.healthy
                    status_dict = pool_status.to_dict()

                return {
                    "status": "healthy" if is_healthy else "degraded",
                    "pool": status_dict,
                    "timestamp": time.time(),
                }
            except HTTPException:
                raise
            except Exception as e:
                api.abort(500, f"Health check failed: {str(e)}")

    @health_ns.route("/metrics")
    class Metrics(Resource):
        @health_ns.doc("prometheus_metrics")
        def get(self):
            """Get Prometheus-style metrics for monitoring."""
            pool_status = browser_pool.get_status()

            if isinstance(pool_status, dict):
                total = pool_status.get("total_browsers", 0)
                active = pool_status.get("active_browsers", 0)
                available = pool_status.get("available_browsers", 0)
                memory = pool_status.get("memory_usage_mb", 0)
                cpu = pool_status.get("cpu_usage_percent", 0)
                uptime = pool_status.get("uptime_seconds", 0)
            else:
                total = pool_status.total_browsers
                active = pool_status.active_browsers
                available = pool_status.available_browsers
                memory = pool_status.memory_usage_mb
                cpu = pool_status.cpu_usage_percent
                uptime = pool_status.uptime_seconds

            metrics = f"""# HELP browser_pool_total_browsers Total number of browsers
# TYPE browser_pool_total_browsers gauge
browser_pool_total_browsers {total}

# HELP browser_pool_active_browsers Number of active browsers
# TYPE browser_pool_active_browsers gauge
browser_pool_active_browsers {active}

# HELP browser_pool_available_browsers Number of available browsers
# TYPE browser_pool_available_browsers gauge
browser_pool_available_browsers {available}

# HELP browser_pool_memory_usage_mb Memory usage in MB
# TYPE browser_pool_memory_usage_mb gauge
browser_pool_memory_usage_mb {memory}

# HELP browser_pool_cpu_usage_percent CPU usage percentage
# TYPE browser_pool_cpu_usage_percent gauge
browser_pool_cpu_usage_percent {cpu}

# HELP browser_pool_uptime_seconds Uptime in seconds
# TYPE browser_pool_uptime_seconds gauge
browser_pool_uptime_seconds {uptime}
"""

            return metrics, 200, {"Content-Type": "text/plain"}

    return health_ns
