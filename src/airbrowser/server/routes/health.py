"""Health check routes for Airbrowser API."""

from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException


def create_health_namespace(api, browser_ops, schemas):
    """Create and configure the health namespace."""

    health_ns = Namespace("health", description="Health and monitoring")

    @health_ns.route("/")
    class HealthCheck(Resource):
        @health_ns.doc("health_check")
        @health_ns.response(200, "Success", schemas["HealthStatus"])
        def get(self):
            """Check the health status of the browser pool."""
            try:
                result = browser_ops.health_check()
                if result.get("success"):
                    data = result.get("data", {})
                    return {
                        "status": data.get("status", "unknown"),
                        "version": data.get("version", "0.0.0"),
                        "vision_enabled": data.get("vision_enabled", False),
                        "pool": data.get("pool_metrics", {}),
                        "timestamp": data.get("timestamp", 0),
                    }
                else:
                    api.abort(500, result.get("error", "Health check failed"))
            except HTTPException:
                raise
            except Exception as e:
                api.abort(500, f"Health check failed: {str(e)}")

    @health_ns.route("/metrics")
    class Metrics(Resource):
        @health_ns.doc("prometheus_metrics")
        def get(self):
            """Get Prometheus-style metrics for monitoring."""
            result = browser_ops.get_pool_status()
            if not result.get("success"):
                return "# Error getting pool status\n", 500, {"Content-Type": "text/plain"}

            data = result.get("data", {})
            total = data.get("total_browsers", 0)
            active = data.get("active_browsers", 0)
            available = data.get("available_browsers", 0)
            memory = data.get("memory_usage_mb", 0)
            cpu = data.get("cpu_usage_percent", 0)
            uptime = data.get("uptime_seconds", 0)

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
