"""Common response schemas for Swagger documentation."""

from flask_restx import fields


def register_response_schemas(api):
    """Register common response schemas with the API."""

    schemas = {}

    # Base response model that most endpoints inherit from
    schemas["BaseResponse"] = api.model(
        "BaseResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
        },
    )

    # Generic action result with data field
    schemas["ActionResult"] = api.model(
        "ActionResult",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Raw(description="Action result data"),
        },
    )

    # Health check response
    schemas["HealthStatus"] = api.model(
        "HealthStatus",
        {
            "status": fields.String(description="Health status"),
            "pool": fields.Raw(description="Pool status information"),
            "timestamp": fields.Float(description="Unix timestamp"),
        },
    )

    # Browser creation response
    browser_creation_data = api.model(
        "BrowserCreationData",
        {
            "browser_id": fields.String(description="Unique browser identifier", required=True),
            "config": fields.Raw(description="Browser configuration used"),
        },
    )

    schemas["BrowserCreated"] = api.model(
        "BrowserCreated",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(browser_creation_data, description="Browser creation data"),
        },
    )

    # Browser list response
    browser_list_data = api.model(
        "BrowserListData",
        {
            "browsers": fields.List(fields.Raw, description="List of active browsers"),
            "count": fields.Integer(description="Total browser count"),
        },
    )

    schemas["BrowserList"] = api.model(
        "BrowserList",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(browser_list_data, description="Browser list data"),
        },
    )

    # Browser info response
    schemas["BrowserInfo"] = api.model(
        "BrowserInfoResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Raw(description="Browser information"),
        },
    )

    # Browser deleted response
    schemas["BrowserDeleted"] = api.model(
        "BrowserDeleted",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
        },
    )

    # Browser status response
    browser_status_data = api.model(
        "BrowserStatusData",
        {
            "browser_id": fields.String(description="Browser identifier"),
            "status": fields.String(description="Browser status"),
            "session_id": fields.String(description="Session identifier"),
            "created_at": fields.Float(description="Creation timestamp"),
        },
    )

    schemas["BrowserStatus"] = api.model(
        "BrowserStatusResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(browser_status_data, description="Browser status data"),
        },
    )

    # URL response
    url_data = api.model("UrlData", {"url": fields.String(description="Current URL")})

    schemas["UrlResponse"] = api.model(
        "UrlResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(url_data, description="URL data"),
        },
    )

    # Text response
    text_data = api.model(
        "TextData",
        {
            "text": fields.String(description="Element text content"),
            "result": fields.String(description="Result value"),
        },
    )

    schemas["TextResponse"] = api.model(
        "TextResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(text_data, description="Text data"),
        },
    )

    # Find element response
    find_element_data = api.model(
        "FindElementData",
        {
            "found": fields.Boolean(description="Whether element was found"),
            "selector": fields.String(description="Selector used"),
            "by": fields.String(description="Selector type used"),
        },
    )

    schemas["FindElementResponse"] = api.model(
        "FindElementResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(find_element_data, description="Find element result"),
        },
    )

    # Is visible response
    is_visible_data = api.model(
        "IsVisibleData",
        {
            "visible": fields.Boolean(description="Whether element is visible"),
            "selector": fields.String(description="Selector used"),
            "by": fields.String(description="Selector type used"),
        },
    )

    schemas["IsVisibleResponse"] = api.model(
        "IsVisibleResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(is_visible_data, description="Visibility result"),
        },
    )

    # Screenshot response
    screenshot_data = api.model(
        "ScreenshotData",
        {
            "screenshot_url": fields.String(description="URL to screenshot"),
            "screenshot_path": fields.String(description="Path to screenshot file"),
        },
    )

    schemas["ScreenshotResponse"] = api.model(
        "ScreenshotResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(screenshot_data, description="Screenshot data"),
        },
    )

    # Execute script response
    execute_data = api.model("ExecuteData", {"result": fields.Raw(description="Script execution result")})

    schemas["ExecuteResponse"] = api.model(
        "ExecuteResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(execute_data, description="Execution result"),
        },
    )

    # Content response (visible text, title, etc.)
    content_data = api.model(
        "ContentData",
        {
            "text": fields.String(description="Visible text content (no HTML tags)"),
            "title": fields.String(description="Page title"),
            "url": fields.String(description="Current URL"),
            "truncated": fields.Boolean(description="Whether text was truncated"),
        },
    )

    schemas["ContentResponse"] = api.model(
        "ContentResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(content_data, description="Page content data"),
        },
    )

    # Pool status response
    schemas["PoolStatus"] = api.model(
        "PoolStatusResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Raw(description="Pool status information"),
        },
    )

    # Pool scaled response
    scale_data = api.model("ScaleData", {"new_max_browsers": fields.Integer(description="New maximum browser count")})

    schemas["PoolScaled"] = api.model(
        "PoolScaled",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Nested(scale_data, description="Scale result"),
        },
    )

    # Console/Network logs response
    schemas["LogsResponse"] = api.model(
        "LogsResponse",
        {
            "success": fields.Boolean(description="Operation success", required=True),
            "message": fields.String(description="Status message", required=True),
            "timestamp": fields.Float(description="Unix timestamp", required=True),
            "data": fields.Raw(description="Log entries"),
        },
    )

    # Error response (fields are optional since Flask-RESTX abort() may not include all)
    schemas["ErrorResponse"] = api.model(
        "ErrorResponse",
        {
            "success": fields.Boolean(description="Operation success (false)", default=False),
            "message": fields.String(description="Error message"),
            "timestamp": fields.Float(description="Unix timestamp"),
        },
    )

    return schemas
