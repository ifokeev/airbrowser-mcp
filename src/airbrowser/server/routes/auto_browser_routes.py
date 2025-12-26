"""Auto-generate REST routes from BrowserOperations methods.

This module generates Flask-RESTX routes by introspecting BrowserOperations class methods,
similar to how MCP tools are auto-generated. This ensures consistency between MCP and REST APIs.
"""

import inspect
import logging
from typing import Any, get_origin, get_type_hints

from flask import request
from flask_restx import Namespace, Resource, fields

logger = logging.getLogger(__name__)

# Methods to exclude from auto-generation (in separate namespaces)
EXCLUDE_METHODS = {
    "health_check",  # Health endpoint (separate /health namespace)
    "get_pool_status",  # Pool status (separate /pool namespace)
}

# Path overrides for specific methods (method_name -> custom_path)
PATH_OVERRIDES = {
    "navigate_browser": "navigate",
    "click_element": "click",
    "type_text": "type",
    "get_page_content": "content",
    "take_screenshot": "screenshot",
    "execute_js": "execute",
}


# Type hint to Flask-RESTX field mapping
def _get_field_for_type(annotation: Any, param_name: str) -> fields.Raw:
    """Convert Python type annotation to Flask-RESTX field."""
    import types
    from typing import get_args

    origin = get_origin(annotation)

    # Handle Union types (e.g., str | None, list[int] | None)
    if origin is types.UnionType:
        # Get the non-None type from the union
        args = get_args(annotation)
        non_none_types = [t for t in args if t is not type(None)]
        if non_none_types:
            # Recursively process the actual type
            return _get_field_for_type(non_none_types[0], param_name)
        return fields.String(description=param_name)

    # Handle Optional types (Union[X, None])
    if origin is type(None):
        return fields.String(description=param_name)

    # Basic types
    if annotation is str:
        return fields.String(description=param_name)
    elif annotation is int:
        return fields.Integer(description=param_name)
    elif annotation is float:
        return fields.Float(description=param_name)
    elif annotation is bool:
        return fields.Boolean(description=param_name)
    elif origin is list or annotation is list:
        # Get the item type from list[X]
        args = get_args(annotation)
        if args:
            item_type = args[0]
            if item_type is int:
                return fields.List(fields.Integer, description=param_name)
            elif item_type is str:
                return fields.List(fields.String, description=param_name)
            elif item_type is float:
                return fields.List(fields.Float, description=param_name)
            elif item_type is bool:
                return fields.List(fields.Boolean, description=param_name)
        return fields.List(fields.Raw, description=param_name)
    elif origin is dict or annotation is dict:
        return fields.Raw(description=param_name)
    else:
        # For enums and complex types, use String
        return fields.String(description=param_name)


def _get_http_method(name: str) -> str:
    """Determine HTTP method from method name using conventions."""
    if name.startswith(("get_", "list_", "is_", "check_")):
        return "GET"
    if name.startswith(("close_", "delete_", "clear_")):
        return "DELETE"
    return "POST"


def _has_browser_id_param(sig: inspect.Signature) -> bool:
    """Check if method has browser_id as first parameter."""
    params = [p for p in sig.parameters if p != "self"]
    return len(params) > 0 and params[0] == "browser_id"


def _get_path_name(method_name: str) -> str:
    """Get URL path segment for a method."""
    return PATH_OVERRIDES.get(method_name, method_name)


def _generate_request_schema(api, method_name: str, sig: inspect.Signature, hints: dict):
    """Generate Flask-RESTX request model from method signature."""
    schema_fields = {}

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "browser_id"):
            continue

        annotation = hints.get(param_name, param.annotation)
        required = param.default is inspect.Parameter.empty

        # Create field with appropriate type
        field = _get_field_for_type(annotation, param_name)
        field.required = required

        # Set default if available
        if param.default is not inspect.Parameter.empty:
            field.default = param.default

        schema_fields[param_name] = field

    if not schema_fields:
        return None

    # Generate schema name from method name
    schema_name = "".join(word.title() for word in method_name.split("_")) + "Request"
    return api.model(schema_name, schema_fields)


def _create_resource_class(
    method_name: str,
    method: callable,
    http_method: str,
    has_browser_id: bool,
    request_schema,
    ns: Namespace,
    response_schema=None,
) -> type:
    """Create a Flask-RESTX Resource class for a BrowserOperations method."""

    def create_handler(method_ref, needs_browser_id, route_name):
        """Create handler function with proper closure."""

        def handler(self, browser_id=None):
            data = request.get_json(silent=True) or {}

            # For GET requests, also check query params
            if request.method == "GET":
                for key, value in request.args.items():
                    if key not in data:
                        data[key] = value

            try:
                if needs_browser_id:
                    result = method_ref(browser_id, **data)
                else:
                    result = method_ref(**data)
                return result
            except TypeError as e:
                # Handle missing required parameters
                return {"success": False, "error": f"Invalid parameters: {str(e)}"}, 400
            except Exception as e:
                logger.error(f"Auto-route {route_name} error: {e}", exc_info=True)
                return {"success": False, "error": str(e)}, 400

        return handler

    handler = create_handler(method, has_browser_id, method_name)
    handler.__doc__ = inspect.getdoc(method) or f"Auto-generated endpoint for {method_name}"
    handler.__name__ = method_name

    # Apply decorators for swagger documentation
    handler = ns.doc(method_name)(handler)

    # Add response schema
    if response_schema:
        handler = ns.response(200, "Success", response_schema)(handler)

    # Apply schema decorator for POST/PUT/PATCH requests
    if request_schema and http_method in ("POST", "PUT", "PATCH"):
        handler = ns.expect(request_schema)(handler)

    # For GET/DELETE requests, add query parameter documentation
    if http_method in ("GET", "DELETE") and request_schema:
        # Extract fields from schema and add as params
        for field_name, field_obj in request_schema.items():
            required = getattr(field_obj, "required", False)
            description = getattr(field_obj, "description", field_name)
            handler = ns.param(field_name, description, required=required)(handler)

    # Create Resource class with handler in class dict (required for swagger generation)
    class_name = f"Auto{''.join(word.title() for word in method_name.split('_'))}"
    class_dict = {http_method.lower(): handler}

    return type(class_name, (Resource,), class_dict)


def generate_browser_routes(api, browser_ops, existing_schemas: dict = None) -> Namespace:
    """Auto-generate Flask-RESTX routes from BrowserOperations methods.

    Args:
        api: Flask-RESTX Api instance
        browser_ops: BrowserOperations instance
        existing_schemas: Optional dict of existing schemas to reuse

    Returns:
        Namespace with auto-generated routes
    """
    ns = Namespace("browser", description="Browser operations")

    # Create a generic response model for all auto-generated endpoints
    generic_response = api.model(
        "GenericResponse",
        {
            "success": fields.Boolean(description="Whether the operation succeeded"),
            "message": fields.String(description="Response message"),
            "data": fields.Raw(description="Response data"),
        },
    )

    registered = []
    skipped = []

    for method_name in dir(browser_ops):
        # Skip private methods and excluded methods
        if method_name.startswith("_") or method_name in EXCLUDE_METHODS:
            continue

        method = getattr(browser_ops, method_name)
        if not callable(method):
            continue

        try:
            sig = inspect.signature(method)
        except (ValueError, TypeError):
            skipped.append(method_name)
            continue

        # Get type hints
        try:
            hints = get_type_hints(method)
        except Exception:
            hints = {}

        http_method = _get_http_method(method_name)
        has_browser_id = _has_browser_id_param(sig)
        path_name = _get_path_name(method_name)

        # Generate path
        if has_browser_id:
            path = f"/<string:browser_id>/{path_name}"
        else:
            path = f"/{path_name}"

        # Generate request schema
        request_schema = _generate_request_schema(api, method_name, sig, hints)

        # Create resource class
        resource_class = _create_resource_class(
            method_name, method, http_method, has_browser_id, request_schema, ns, generic_response
        )

        # Register route
        ns.add_resource(resource_class, path)
        registered.append(f"{http_method} {path} -> {method_name}")

    logger.info(f"[Auto-Routes] Registered {len(registered)} routes, skipped {len(skipped)}")
    for route in registered:
        logger.debug(f"  {route}")

    return ns
