"""Browser pool management routes for Airbrowser API."""

import time

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException


def success_response(data=None, message: str = "Success"):
    """Create success response."""
    response = {"success": True, "message": message, "timestamp": time.time()}
    if data is not None:
        response["data"] = data
    return response


def create_pool_namespace(api, browser_pool, schemas):
    """Create and configure the pool namespace."""

    pool_ns = Namespace("pool", description="Browser pool operations")

    @pool_ns.route("/scale")
    class ScalePool(Resource):
        @pool_ns.doc("scale_pool")
        @pool_ns.expect(schemas["ScalePool"])
        @pool_ns.response(200, "Success", schemas["PoolScaled"])
        @pool_ns.response(400, "Bad request", schemas["ErrorResponse"])
        def post(self):
            """Scale the browser pool to a new maximum size."""
            try:
                data = request.get_json(silent=True) or {}
                target_size = data.get("target_size")

                if target_size is None:
                    api.abort(400, "target_size is required")

                if target_size < 1 or target_size > 200:
                    api.abort(400, "target_size must be between 1 and 200")

                browser_pool.max_browsers = target_size

                return success_response({"new_max_browsers": target_size}, "Pool scaled successfully")

            except HTTPException:
                raise
            except Exception as e:
                api.abort(400, f"Failed to scale pool: {str(e)}")

    @pool_ns.route("/shutdown")
    class ShutdownServer(Resource):
        @pool_ns.doc("shutdown_server")
        @pool_ns.response(200, "Success", schemas["BaseResponse"])
        def post(self):
            """Gracefully shutdown the browser pool server."""
            try:
                browser_pool.close_all_browsers()

                import os
                import threading

                def shutdown():
                    time.sleep(2)
                    os._exit(0)

                thread = threading.Thread(target=shutdown)
                thread.daemon = True
                thread.start()

                return success_response(message="Server shutting down gracefully")

            except HTTPException:
                raise
            except Exception as e:
                api.abort(500, f"Failed to shutdown server: {str(e)}")

    return pool_ns
