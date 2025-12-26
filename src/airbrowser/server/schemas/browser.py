"""Browser-related request/response schemas for Swagger documentation."""

from flask_restx import fields


def register_browser_schemas(api):
    """Register browser-related schemas with the API."""

    schemas = {}

    # Request schemas
    # Note: UC (undetected chrome) + CDP mode are always enabled, browsers are always headful
    schemas["BrowserConfig"] = api.model(
        "BrowserConfig",
        {
            "profile_name": fields.String(
                description="Profile name for persistent data. Omit for fresh session.",
                example="dev-session",
            ),
            "proxy": fields.String(description="Proxy server URL"),
            "user_agent": fields.String(description="Custom user agent string"),
            "window_size": fields.List(fields.Integer, description="Browser window size [width, height]"),
            "disable_gpu": fields.Boolean(description="Disable GPU acceleration", default=False),
            "disable_images": fields.Boolean(description="Disable image loading", default=False),
            "disable_javascript": fields.Boolean(description="Disable JavaScript", default=False),
            "extensions": fields.List(fields.String, description="Chrome extension paths"),
            "custom_args": fields.List(fields.String, description="Custom Chrome arguments"),
        },
    )

    schemas["NavigateRequest"] = api.model(
        "NavigateRequest",
        {
            "url": fields.String(description="URL to navigate to", required=True),
            "timeout": fields.Integer(description="Navigation timeout in seconds", default=60),
        },
    )

    schemas["ClickRequest"] = api.model(
        "ClickRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "timeout": fields.Integer(description="Timeout in seconds", default=10),
            "if_visible": fields.Boolean(description="Only click if element is visible", default=False),
        },
    )

    schemas["TypeRequest"] = api.model(
        "TypeRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "text": fields.String(description="Text to type", required=True),
            "timeout": fields.Integer(description="Timeout in seconds", default=10),
        },
    )

    schemas["WaitRequest"] = api.model(
        "WaitRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "timeout": fields.Integer(description="Timeout in seconds", default=10),
        },
    )

    schemas["ExecuteRequest"] = api.model(
        "ExecuteRequest",
        {
            "script": fields.String(description="JavaScript code to execute", required=True),
            "timeout": fields.Integer(description="Timeout in seconds", default=120),
        },
    )

    schemas["GetTextRequest"] = api.model(
        "GetTextRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "timeout": fields.Integer(description="Timeout in seconds", default=10),
        },
    )

    schemas["ScalePool"] = api.model(
        "ScalePool",
        {"target_size": fields.Integer(description="New maximum number of browsers", required=True, min=1, max=200)},
    )

    schemas["GuiClickXYRequest"] = api.model(
        "GuiClickXYRequest",
        {
            "x": fields.Float(description="Screen X coordinate", required=True),
            "y": fields.Float(description="Screen Y coordinate", required=True),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
        },
    )

    schemas["GuiClickRequest"] = api.model(
        "GuiClickRequest",
        {
            "selector": fields.String(description="Element selector (CSS or XPath)", required=True),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
            "fx": fields.Float(description="Relative X (0..1) within element to click", required=False),
            "fy": fields.Float(description="Relative Y (0..1) within element to click", required=False),
        },
    )

    schemas["DetectCoordinatesRequest"] = api.model(
        "DetectCoordinatesRequest",
        {
            "prompt": fields.String(
                description="Natural language description of element to find",
                required=True,
                example="the search input field",
            )
        },
    )

    schemas["FindElementRequest"] = api.model(
        "FindElementRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
        },
    )

    schemas["IsVisibleRequest"] = api.model(
        "IsVisibleRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
        },
    )

    schemas["ClickIfVisibleRequest"] = api.model(
        "ClickIfVisibleRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
        },
    )

    schemas["WaitNotVisibleRequest"] = api.model(
        "WaitNotVisibleRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "timeout": fields.Integer(description="Timeout in seconds", default=20),
        },
    )

    schemas["PressKeysRequest"] = api.model(
        "PressKeysRequest",
        {
            "selector": fields.String(description="Element selector", required=True),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
            "keys": fields.String(description="Keys to press", required=True),
        },
    )

    schemas["MouseRequest"] = api.model(
        "MouseRequest",
        {
            "action": fields.String(description="Action: hover or drag", required=True),
            "selector": fields.String(description="Element selector (for hover)"),
            "source": fields.String(description="Source selector (for drag)"),
            "target": fields.String(description="Target selector (for drag)"),
            "by": fields.String(description="Selector type: css, id, name, xpath", default="css"),
        },
    )

    # Response schemas for specific endpoints
    schemas["DetectCoordinatesResult"] = api.model(
        "DetectCoordinatesResult",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Success message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "prompt": fields.String(description="Element description used"),
            "coordinates": fields.Raw(description="Full coordinate information"),
            "bounding_box": fields.Raw(description="Element bounding box {x, y, width, height}"),
            "click_point": fields.Raw(description="Recommended click point {x, y}"),
            "screenshot_path": fields.String(description="Path to screenshot analyzed"),
            "model_used": fields.String(description="Vision model used for detection"),
            "confidence": fields.Float(description="Detection confidence (0.0-1.0)"),
            "models_tried": fields.List(fields.String, description="Models attempted if detection failed"),
            "data": fields.Raw(description="Additional result data"),
            "error": fields.String(description="Error message if failed"),
        },
    )

    schemas["WhatIsVisibleResult"] = api.model(
        "WhatIsVisibleResult",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Success message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "analysis": fields.String(description="Comprehensive page state analysis"),
            "model": fields.String(description="AI model used for analysis"),
            "screenshot_url": fields.String(description="URL to the screenshot"),
            "screenshot_path": fields.String(description="Path to the screenshot file"),
            "error": fields.String(description="Error message if failed"),
        },
    )

    # Profile schemas
    schemas["ProfileInfo"] = api.model(
        "ProfileInfo",
        {
            "name": fields.String(description="Profile name"),
            "path": fields.String(description="Profile storage path"),
            "size_mb": fields.Float(description="Profile size in MB"),
            "last_used": fields.String(description="Last used timestamp (ISO format)"),
            "in_use": fields.Boolean(description="Whether profile is currently in use by a browser"),
        },
    )

    schemas["ProfileListData"] = api.model(
        "ProfileListData",
        {
            "profiles": fields.List(fields.Nested(schemas["ProfileInfo"]), description="List of profiles"),
        },
    )

    schemas["ProfileListResponse"] = api.model(
        "ProfileListResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["ProfileListData"]),
        },
    )

    schemas["CreateProfileRequest"] = api.model(
        "CreateProfileRequest",
        {
            "name": fields.String(description="Profile name", required=True, example="dev-session"),
        },
    )

    schemas["ProfileResponse"] = api.model(
        "ProfileResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["ProfileInfo"]),
        },
    )

    # Tab schemas
    schemas["TabInfo"] = api.model(
        "TabInfo",
        {
            "index": fields.Integer(description="Tab index"),
            "handle": fields.String(description="Tab window handle"),
            "url": fields.String(description="Tab URL"),
            "title": fields.String(description="Tab title"),
            "is_active": fields.Boolean(description="Whether this tab is active"),
        },
    )

    schemas["TabListData"] = api.model(
        "TabListData",
        {
            "tabs": fields.List(fields.Nested(schemas["TabInfo"]), description="List of tabs"),
            "count": fields.Integer(description="Number of tabs"),
            "current_index": fields.Integer(description="Index of current active tab"),
        },
    )

    schemas["TabListResponse"] = api.model(
        "TabListResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["TabListData"]),
        },
    )

    schemas["NewTabRequest"] = api.model(
        "NewTabRequest",
        {
            "url": fields.String(description="URL to open in new tab (optional)", example="https://example.com"),
        },
    )

    schemas["NewTabData"] = api.model(
        "NewTabData",
        {
            "handle": fields.String(description="New tab window handle"),
            "index": fields.Integer(description="New tab index"),
            "url": fields.String(description="Tab URL"),
            "title": fields.String(description="Tab title"),
        },
    )

    schemas["NewTabResponse"] = api.model(
        "NewTabResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["NewTabData"]),
        },
    )

    schemas["SwitchTabRequest"] = api.model(
        "SwitchTabRequest",
        {
            "index": fields.Integer(description="Tab index to switch to"),
            "handle": fields.String(description="Tab handle to switch to (alternative to index)"),
        },
    )

    schemas["SwitchTabData"] = api.model(
        "SwitchTabData",
        {
            "handle": fields.String(description="Current tab window handle"),
            "index": fields.Integer(description="Current tab index"),
            "url": fields.String(description="Tab URL"),
            "title": fields.String(description="Tab title"),
        },
    )

    schemas["SwitchTabResponse"] = api.model(
        "SwitchTabResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["SwitchTabData"]),
        },
    )

    schemas["CloseTabRequest"] = api.model(
        "CloseTabRequest",
        {
            "index": fields.Integer(description="Tab index to close"),
            "handle": fields.String(description="Tab handle to close (alternative to index)"),
        },
    )

    schemas["CloseTabData"] = api.model(
        "CloseTabData",
        {
            "closed_handle": fields.String(description="Handle of closed tab"),
            "remaining_tabs": fields.Integer(description="Number of remaining tabs"),
            "current_handle": fields.String(description="Handle of current tab"),
            "current_url": fields.String(description="URL of current tab"),
        },
    )

    schemas["CloseTabResponse"] = api.model(
        "CloseTabResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["CloseTabData"]),
        },
    )

    schemas["CurrentTabData"] = api.model(
        "CurrentTabData",
        {
            "handle": fields.String(description="Current tab window handle"),
            "index": fields.Integer(description="Current tab index"),
            "url": fields.String(description="Tab URL"),
            "title": fields.String(description="Tab title"),
            "total_tabs": fields.Integer(description="Total number of tabs"),
        },
    )

    schemas["CurrentTabResponse"] = api.model(
        "CurrentTabResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Nested(schemas["CurrentTabData"]),
        },
    )

    # ==================== Input Automation Schemas ====================

    schemas["HoverRequest"] = api.model(
        "HoverRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
        },
    )

    schemas["DragRequest"] = api.model(
        "DragRequest",
        {
            "source": fields.String(required=True, description="Source element selector"),
            "target": fields.String(required=True, description="Target element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
        },
    )

    schemas["FormField"] = api.model(
        "FormField",
        {
            "selector": fields.String(required=True, description="Field selector"),
            "value": fields.String(required=True, description="Value to fill"),
        },
    )

    schemas["FillFormRequest"] = api.model(
        "FillFormRequest",
        {
            "fields": fields.List(fields.Nested(schemas["FormField"]), required=True, description="Fields to fill"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
        },
    )

    schemas["UploadFileRequest"] = api.model(
        "UploadFileRequest",
        {
            "selector": fields.String(required=True, description="File input selector"),
            "file_path": fields.String(required=True, description="Path to file to upload"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
        },
    )

    schemas["HandleDialogRequest"] = api.model(
        "HandleDialogRequest",
        {
            "action": fields.String(required=True, description="Dialog action: accept or dismiss"),
            "text": fields.String(description="Text to enter for prompt dialogs"),
        },
    )

    # ==================== Page Schemas ====================

    schemas["ResizeRequest"] = api.model(
        "ResizeRequest",
        {
            "width": fields.Integer(required=True, description="Viewport width"),
            "height": fields.Integer(required=True, description="Viewport height"),
        },
    )

    schemas["SnapshotRequest"] = api.model(
        "SnapshotRequest",
        {
            "type": fields.String(description="Snapshot type: dom or accessibility", default="dom"),
        },
    )

    # ==================== Emulation Schemas ====================

    schemas["EmulateRequest"] = api.model(
        "EmulateRequest",
        {
            "device": fields.String(description="Device preset name (e.g., iPhone 14, iPad)"),
            "width": fields.Integer(description="Custom viewport width"),
            "height": fields.Integer(description="Custom viewport height"),
            "device_scale_factor": fields.Float(description="Device pixel ratio"),
            "mobile": fields.Boolean(description="Enable touch events"),
            "user_agent": fields.String(description="Custom user agent"),
        },
    )

    # ==================== Performance Schemas ====================

    schemas["StartTraceRequest"] = api.model(
        "StartTraceRequest",
        {
            "categories": fields.String(description="Comma-separated trace categories"),
        },
    )

    # ==================== Combined Request Schemas ====================

    schemas["HistoryRequest"] = api.model(
        "HistoryRequest",
        {
            "action": fields.String(
                required=True,
                description="History action: back, forward, or refresh",
                enum=["back", "forward", "refresh"],
            ),
        },
    )

    schemas["CheckElementRequest"] = api.model(
        "CheckElementRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "check": fields.String(
                required=True,
                description="Check type: exists or visible",
                enum=["exists", "visible"],
            ),
        },
    )

    schemas["WaitElementRequest"] = api.model(
        "WaitElementRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "until": fields.String(
                required=True,
                description="Wait until: visible or hidden",
                enum=["visible", "hidden"],
            ),
            "timeout": fields.Integer(description="Timeout in seconds", default=10),
        },
    )

    schemas["ElementDataRequest"] = api.model(
        "ElementDataRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "type": fields.String(
                required=True,
                description="Data type: text, attribute, or property",
                enum=["text", "attribute", "property"],
            ),
            "name": fields.String(description="Attribute/property name (required for attribute/property)"),
        },
    )

    schemas["CombinedScrollRequest"] = api.model(
        "CombinedScrollRequest",
        {
            "selector": fields.String(description="Element selector to scroll to"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "x": fields.Integer(description="X coordinate to scroll to (absolute)"),
            "y": fields.Integer(description="Y coordinate to scroll to (absolute)"),
            "delta_x": fields.Integer(description="Horizontal scroll amount (relative)"),
            "delta_y": fields.Integer(description="Vertical scroll amount (relative)"),
            "behavior": fields.String(description="Scroll behavior: smooth or instant", default="smooth"),
        },
    )

    schemas["CombinedGuiClickRequest"] = api.model(
        "CombinedGuiClickRequest",
        {
            "selector": fields.String(description="Element selector (for selector mode)"),
            "x": fields.Float(description="Screen X coordinate (for coordinate mode)"),
            "y": fields.Float(description="Screen Y coordinate (for coordinate mode)"),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
            "fx": fields.Float(description="Relative X (0..1) within element to click"),
            "fy": fields.Float(description="Relative Y (0..1) within element to click"),
        },
    )

    schemas["GuiTypeXyRequest"] = api.model(
        "GuiTypeXyRequest",
        {
            "x": fields.Float(required=True, description="Screen X coordinate"),
            "y": fields.Float(required=True, description="Screen Y coordinate"),
            "text": fields.String(required=True, description="Text to type"),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
        },
    )

    schemas["GuiHoverXyRequest"] = api.model(
        "GuiHoverXyRequest",
        {
            "x": fields.Float(required=True, description="Screen X coordinate"),
            "y": fields.Float(required=True, description="Screen Y coordinate"),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
        },
    )

    schemas["GuiPressKeysXyRequest"] = api.model(
        "GuiPressKeysXyRequest",
        {
            "x": fields.Float(required=True, description="Screen X coordinate"),
            "y": fields.Float(required=True, description="Screen Y coordinate"),
            "keys": fields.String(required=True, description="Keys to press (e.g., 'ENTER', 'TAB', 'CTRL+a')"),
            "timeframe": fields.Float(description="Mouse move duration (seconds)", default=0.25),
        },
    )

    schemas["ConsoleLogsRequest"] = api.model(
        "ConsoleLogsRequest",
        {
            "action": fields.String(
                required=True,
                description="Action: get or clear",
                enum=["get", "clear"],
            ),
            "limit": fields.Integer(description="Max number of logs to return (for get)", default=200),
        },
    )

    schemas["NetworkLogsRequest"] = api.model(
        "NetworkLogsRequest",
        {
            "action": fields.String(
                required=True,
                description="Action: get or clear",
                enum=["get", "clear"],
            ),
            "limit": fields.Integer(description="Max number of logs to return (for get)", default=200),
        },
    )

    schemas["TabsRequest"] = api.model(
        "TabsRequest",
        {
            "action": fields.String(
                required=True,
                description="Tab action: list, new, switch, close, or current",
                enum=["list", "new", "switch", "close", "current"],
            ),
            "url": fields.String(description="URL for new tab (for 'new' action)"),
            "index": fields.Integer(description="Tab index (for 'switch' or 'close' actions)"),
            "handle": fields.String(description="Tab handle (for 'switch' or 'close' actions)"),
        },
    )

    schemas["CombinedDialogRequest"] = api.model(
        "CombinedDialogRequest",
        {
            "action": fields.String(
                required=True,
                description="Dialog action: get, accept, or dismiss",
                enum=["get", "accept", "dismiss"],
            ),
            "text": fields.String(description="Text to enter for prompt dialogs (for 'accept' action)"),
        },
    )

    schemas["CombinedEmulateRequest"] = api.model(
        "CombinedEmulateRequest",
        {
            "action": fields.String(
                description="Emulation action: set, clear, or list_devices",
                enum=["set", "clear", "list_devices"],
                default="set",
            ),
            "device": fields.String(description="Device preset name (e.g., iPhone 14, iPad)"),
            "width": fields.Integer(description="Custom viewport width"),
            "height": fields.Integer(description="Custom viewport height"),
            "device_scale_factor": fields.Float(description="Device pixel ratio"),
            "mobile": fields.Boolean(description="Enable touch events"),
            "user_agent": fields.String(description="Custom user agent"),
        },
    )

    schemas["PerformanceRequest"] = api.model(
        "PerformanceRequest",
        {
            "action": fields.String(
                required=True,
                description="Performance action: start_trace, stop_trace, metrics, or analyze",
                enum=["start_trace", "stop_trace", "metrics", "analyze"],
            ),
            "categories": fields.String(description="Comma-separated trace categories (for start_trace)"),
        },
    )

    # Generic success response for simple operations
    schemas["SuccessResponse"] = api.model(
        "SuccessResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Success message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Raw(description="Additional result data"),
        },
    )

    # ==================== Scroll Schemas ====================

    schemas["ScrollRequest"] = api.model(
        "ScrollRequest",
        {
            "selector": fields.String(description="Element selector to scroll to"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "x": fields.Integer(description="X coordinate to scroll to"),
            "y": fields.Integer(description="Y coordinate to scroll to"),
            "behavior": fields.String(description="Scroll behavior: smooth or instant", default="smooth"),
        },
    )

    schemas["ScrollByRequest"] = api.model(
        "ScrollByRequest",
        {
            "delta_x": fields.Integer(description="Horizontal scroll amount", default=0),
            "delta_y": fields.Integer(description="Vertical scroll amount", default=0),
            "behavior": fields.String(description="Scroll behavior: smooth or instant", default="smooth"),
        },
    )

    # ==================== Select Schemas ====================

    schemas["SelectRequest"] = api.model(
        "SelectRequest",
        {
            "selector": fields.String(required=True, description="Select element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "action": fields.String(description="Action: select or options", default="select", enum=["select", "options"]),
            "value": fields.String(description="Option value to select"),
            "text": fields.String(description="Option text to select"),
            "index": fields.Integer(description="Option index to select"),
        },
    )

    schemas["SelectOption"] = api.model(
        "SelectOption",
        {
            "index": fields.Integer(description="Option index"),
            "value": fields.String(description="Option value"),
            "text": fields.String(description="Option text"),
            "selected": fields.Boolean(description="Whether option is selected"),
        },
    )

    schemas["SelectOptionsResponse"] = api.model(
        "SelectOptionsResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Raw(description="Options data"),
        },
    )

    # ==================== Attribute/Property Schemas ====================

    schemas["GetAttributeRequest"] = api.model(
        "GetAttributeRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "attribute": fields.String(required=True, description="Attribute name to get"),
        },
    )

    schemas["GetPropertyRequest"] = api.model(
        "GetPropertyRequest",
        {
            "selector": fields.String(required=True, description="Element selector"),
            "by": fields.String(description="Selector type (css, id, name, xpath)", default="css"),
            "property": fields.String(required=True, description="DOM property name to get"),
        },
    )

    schemas["AttributeResponse"] = api.model(
        "AttributeResponse",
        {
            "success": fields.Boolean(description="Operation success"),
            "message": fields.String(description="Status message"),
            "timestamp": fields.Float(description="Unix timestamp"),
            "data": fields.Raw(description="Attribute/property data"),
        },
    )

    return schemas
