"""Route helper utilities to reduce boilerplate."""

import time
from functools import wraps

from flask import request
from werkzeug.exceptions import HTTPException


def success_response(data=None, message: str = "Success"):
    """Create a standardized success response."""
    response = {"success": True, "message": message, "timestamp": time.time()}
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str, status_code: int = 400):
    """Create a standardized error response."""
    return {
        "success": False,
        "message": message,
        "timestamp": time.time(),
    }, status_code


def browser_op(api, success_msg="Success", error_prefix="Operation"):
    """
    Decorator for browser operation endpoints with browser_id.

    The decorated function should return a dict with 'success' key,
    or a tuple (response_dict, status_code) for errors.

    Usage:
        @browser_op(api, "Clicked", "Click")
        def post(self, browser_id):
            data = request.get_json(silent=True) or {}
            return browser_ops.click(browser_id, data.get("selector"))
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(self, browser_id, *args, **kwargs):
            try:
                result = fn(self, browser_id, *args, **kwargs)
                # Handle tuple returns (response, status_code)
                if isinstance(result, tuple):
                    return result
                # Handle dict returns
                if result.get("success"):
                    return success_response(result.get("data"), result.get("message", success_msg))
                else:
                    api.abort(400, result.get("error") or result.get("message") or f"{error_prefix} failed")
            except HTTPException:
                raise
            except ValueError as e:
                api.abort(400, str(e))
            except Exception as e:
                api.abort(400, f"{error_prefix} failed: {str(e)}")

        return wrapper

    return decorator


def pool_op(api, success_msg="Success", error_prefix="Operation"):
    """
    Decorator for pool-level operations without browser_id.

    Usage:
        @pool_op(api, "Browsers listed", "List")
        def get(self):
            return browser_pool.list_browsers()
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                result = fn(self, *args, **kwargs)
                if isinstance(result, tuple):
                    return result
                if result.get("success"):
                    return success_response(result.get("data"), result.get("message", success_msg))
                else:
                    api.abort(400, result.get("error") or result.get("message") or f"{error_prefix} failed")
            except HTTPException:
                raise
            except ValueError as e:
                api.abort(400, str(e))
            except Exception as e:
                api.abort(400, f"{error_prefix} failed: {str(e)}")

        return wrapper

    return decorator


def get_json():
    """Get JSON request body or empty dict."""
    return request.get_json(silent=True) or {}


def require_params(data: dict, *params):
    """
    Validate required parameters exist in data.

    Raises:
        ValueError if any required param is missing
    """
    missing = [p for p in params if not data.get(p)]
    if missing:
        raise ValueError(f"Missing required: {', '.join(missing)}")


def extract_selector(data: dict) -> tuple:
    """Extract selector, by, timeout from request data."""
    return data.get("selector"), data.get("by", "css"), data.get("timeout", 10)
