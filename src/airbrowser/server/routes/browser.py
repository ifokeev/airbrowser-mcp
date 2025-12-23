"""Browser management routes for Airbrowser API."""

import time

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException

from ..models import BrowserConfig, get_window_size_from_env
from ..services.operations import (
    BrowsersAction,
    DialogAction,
    ElementCheck,
    ElementDataType,
    EmulateAction,
    HistoryAction,
    LogAction,
    MouseAction,
    PerformanceAction,
    SelectAction,
    TabAction,
    WaitUntil,
)
from .helpers import browser_op, get_json, pool_op, require_params, success_response


def create_browser_namespace(api, browser_pool, browser_ops, schemas):
    """Create and configure the browser namespace."""

    browser_ns = Namespace("browser", description="Browser management operations")

    # ==================== Browser Lifecycle ====================

    @browser_ns.route("/create")
    class CreateBrowser(Resource):
        @browser_ns.doc("create_browser")
        @browser_ns.expect(schemas["BrowserConfig"])
        @browser_ns.response(200, "Browser created", schemas["BrowserCreated"])
        @browser_ns.response(400, "Bad request", schemas["ErrorResponse"])
        def post(self):
            """Create a new browser instance."""
            try:
                data = get_json()
                config = BrowserConfig(
                    profile_name=data.get("profile_name"),
                    proxy=data.get("proxy"),
                    user_agent=data.get("user_agent"),
                    window_size=tuple(data.get("window_size", get_window_size_from_env())),
                    disable_gpu=data.get("disable_gpu", False),
                    disable_images=data.get("disable_images", False),
                    disable_javascript=data.get("disable_javascript", False),
                    extensions=data.get("extensions", []),
                    custom_args=data.get("custom_args", []),
                )
                browser_id = browser_pool.create_browser(config)
                return success_response(
                    {"browser_id": browser_id, "config": config.to_dict()},
                    "Browser created successfully",
                )
            except ValueError as e:
                return {"success": False, "message": str(e), "timestamp": time.time()}, 409
            except Exception as e:
                api.abort(400, f"Failed to create browser: {str(e)}")

    @browser_ns.route("/list")
    class BrowserList(Resource):
        @browser_ns.doc("list_browsers")
        @browser_ns.response(200, "Success", schemas["BrowserList"])
        def get(self):
            """List all active browser instances."""
            browsers = browser_pool.list_browsers()
            browser_dicts = [b.to_dict() for b in browsers]
            return success_response({"browsers": browser_dicts, "count": len(browser_dicts)})

    @browser_ns.route("/close_all")
    class CloseAllBrowsers(Resource):
        @browser_ns.doc("close_all_browsers")
        @browser_ns.response(200, "Success", schemas["BaseResponse"])
        @pool_op(api, "All browsers closed", "Close all")
        def post(self):
            """Close all active browser instances."""
            browser_pool.close_all_browsers()
            return {"success": True}

    @browser_ns.route("/pool/status")
    class PoolStatus(Resource):
        @browser_ns.doc("get_pool_status")
        @browser_ns.response(200, "Success", schemas["PoolStatus"])
        @pool_op(api, "Pool status retrieved", "Get pool status")
        def get(self):
            """Get browser pool status."""
            return browser_ops.get_pool_status()

    @browser_ns.route("/<string:browser_id>")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Browser(Resource):
        @browser_ns.doc("get_browser")
        @browser_ns.response(200, "Success", schemas["BrowserInfo"])
        @browser_ns.response(404, "Browser not found", schemas["ErrorResponse"])
        def get(self, browser_id):
            """Get browser instance details."""
            browser = browser_pool.get_browser(browser_id)
            if browser:
                return success_response(browser.to_dict(), "Browser found")
            api.abort(404, f"Browser {browser_id} not found")

        @browser_ns.doc("delete_browser")
        @browser_ns.response(200, "Success", schemas["BaseResponse"])
        @browser_op(api, "Browser closed", "Close browser")
        def delete(self, browser_id):
            """Close and remove a browser instance."""
            browser_pool.close_browser(browser_id)
            return {"success": True}

    @browser_ns.route("/<string:browser_id>/status")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class BrowserStatus(Resource):
        @browser_ns.doc("get_browser_status")
        @browser_ns.response(200, "Success", schemas["BrowserInfo"])
        def get(self, browser_id):
            """Get browser status."""
            browser = browser_pool.get_browser(browser_id)
            if browser:
                return success_response(browser.to_dict(), "Status retrieved")
            api.abort(404, f"Browser {browser_id} not found")

    @browser_ns.route("/<string:browser_id>/close")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class CloseBrowser(Resource):
        @browser_ns.doc("close_browser")
        @browser_ns.response(200, "Success", schemas["BaseResponse"])
        @browser_op(api, "Browser closed", "Close browser")
        def post(self, browser_id):
            """Close a browser instance."""
            browser_pool.close_browser(browser_id)
            return {"success": True}

    # ==================== Navigation ====================

    @browser_ns.route("/<string:browser_id>/navigate")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Navigate(Resource):
        @browser_ns.doc("navigate_browser")
        @browser_ns.expect(schemas["NavigateRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "Navigated successfully", "Navigate")
        def post(self, browser_id):
            """Navigate to a URL."""
            data = get_json()
            require_params(data, "url")
            return browser_ops.navigate_browser(browser_id, data["url"], data.get("timeout", 60))

    @browser_ns.route("/<string:browser_id>/url")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class GetUrl(Resource):
        @browser_ns.doc("get_url")
        @browser_ns.response(200, "Success", schemas["UrlResponse"])
        @browser_op(api, "URL retrieved", "Get URL")
        def get(self, browser_id):
            """Get current page URL."""
            return browser_ops.get_url(browser_id)

    @browser_ns.route("/<string:browser_id>/history")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class History(Resource):
        @browser_ns.doc("history")
        @browser_ns.expect(schemas["HistoryRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "History action completed", "History")
        def post(self, browser_id):
            """Execute history action: back, forward, or refresh."""
            data = get_json()
            require_params(data, "action")
            action = HistoryAction(data["action"])
            return browser_ops.history(browser_id, action)

    # ==================== Element Interactions ====================

    @browser_ns.route("/<string:browser_id>/click")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Click(Resource):
        @browser_ns.doc("click")
        @browser_ns.expect(schemas["ClickRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "Element clicked", "Click")
        def post(self, browser_id):
            """Click element. Use if_visible=true to only click if visible."""
            data = get_json()
            require_params(data, "selector")
            return browser_ops.click(
                browser_id, data["selector"], data.get("timeout", 10),
                data.get("by", "css"), data.get("if_visible", False)
            )

    @browser_ns.route("/<string:browser_id>/type")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Type(Resource):
        @browser_ns.doc("type_text")
        @browser_ns.expect(schemas["TypeRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "Text typed", "Type")
        def post(self, browser_id):
            """Type text into an element."""
            data = get_json()
            require_params(data, "selector", "text")
            return browser_ops.type_text(browser_id, data["selector"], data["text"], data.get("timeout", 10), data.get("by", "css"))

    @browser_ns.route("/<string:browser_id>/wait_element")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class WaitElement(Resource):
        @browser_ns.doc("wait_element")
        @browser_ns.expect(schemas["WaitElementRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "Wait completed", "Wait element")
        def post(self, browser_id):
            """Wait for element to become visible or hidden."""
            data = get_json()
            require_params(data, "selector", "until")
            until = WaitUntil(data["until"])
            return browser_ops.wait_element(
                browser_id, data["selector"], until, data.get("timeout", 10), data.get("by", "css")
            )

    @browser_ns.route("/<string:browser_id>/check_element")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class CheckElement(Resource):
        @browser_ns.doc("check_element")
        @browser_ns.expect(schemas["CheckElementRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Element checked", "Check element")
        def post(self, browser_id):
            """Check if element exists or is visible."""
            data = get_json()
            require_params(data, "selector", "check")
            check = ElementCheck(data["check"])
            return browser_ops.check_element(browser_id, data["selector"], check, data.get("by", "css"))

    @browser_ns.route("/<string:browser_id>/press_keys")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class PressKeys(Resource):
        @browser_ns.doc("press_keys")
        @browser_ns.expect(schemas["PressKeysRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "Keys pressed", "Press keys")
        def post(self, browser_id):
            """Press keys on an element."""
            data = get_json()
            require_params(data, "selector", "keys")
            return browser_ops.press_keys(browser_id, data["selector"], data["keys"], data.get("by", "css"))

    @browser_ns.route("/<string:browser_id>/mouse")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Mouse(Resource):
        @browser_ns.doc("mouse")
        @browser_ns.expect(schemas["MouseRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Mouse action completed", "Mouse")
        def post(self, browser_id):
            """Mouse action: hover or drag."""
            data = get_json()
            require_params(data, "action")
            action = MouseAction(data["action"])
            return browser_ops.mouse(
                browser_id, action, data.get("selector"), data.get("source"),
                data.get("target"), data.get("by", "css")
            )

    @browser_ns.route("/<string:browser_id>/fill_form")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class FillForm(Resource):
        @browser_ns.doc("fill_form")
        @browser_ns.expect(schemas["FillFormRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Form filled", "Fill form")
        def post(self, browser_id):
            """Fill multiple form fields."""
            data = get_json()
            require_params(data, "fields")
            return browser_ops.fill_form(browser_id, data["fields"], data.get("by", "css"))

    @browser_ns.route("/<string:browser_id>/upload_file")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class UploadFile(Resource):
        @browser_ns.doc("upload_file")
        @browser_ns.expect(schemas["UploadFileRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "File uploaded", "Upload file")
        def post(self, browser_id):
            """Upload a file."""
            data = get_json()
            require_params(data, "selector", "file_path")
            return browser_ops.upload_file(browser_id, data["selector"], data["file_path"], data.get("by", "css"))

    @browser_ns.route("/<string:browser_id>/scroll")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Scroll(Resource):
        @browser_ns.doc("scroll")
        @browser_ns.expect(schemas["CombinedScrollRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Scrolled", "Scroll")
        def post(self, browser_id):
            """Scroll to element/coordinates (absolute) or by delta (relative)."""
            data = get_json()
            return browser_ops.scroll(
                browser_id,
                data.get("selector"),
                data.get("x"),
                data.get("y"),
                data.get("delta_x"),
                data.get("delta_y"),
                data.get("behavior", "smooth"),
                data.get("by", "css"),
            )

    @browser_ns.route("/<string:browser_id>/select")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Select(Resource):
        @browser_ns.doc("select")
        @browser_ns.expect(schemas["SelectRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Select completed", "Select")
        def post(self, browser_id):
            """Select dropdown: select option or get options."""
            data = get_json()
            require_params(data, "selector")
            action = SelectAction(data.get("action", "select"))
            return browser_ops.select(
                browser_id, data["selector"], action, data.get("value"),
                data.get("text"), data.get("index"), data.get("by", "css")
            )

    @browser_ns.route("/<string:browser_id>/element_data")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class ElementData(Resource):
        @browser_ns.doc("get_element_data")
        @browser_ns.expect(schemas["ElementDataRequest"])
        @browser_ns.response(200, "Success", schemas["AttributeResponse"])
        @browser_op(api, "Element data retrieved", "Get element data")
        def post(self, browser_id):
            """Get element text, attribute, or property."""
            data = get_json()
            require_params(data, "selector", "type")
            data_type = ElementDataType(data["type"])
            return browser_ops.get_element_data(
                browser_id, data["selector"], data_type, data.get("name"), data.get("by", "css")
            )

    # ==================== GUI Interactions ====================

    @browser_ns.route("/<string:browser_id>/gui_click")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class GuiClick(Resource):
        @browser_ns.doc("gui_click")
        @browser_ns.expect(schemas["CombinedGuiClickRequest"])
        @browser_ns.response(200, "Success", schemas["ActionResult"])
        @browser_op(api, "GUI click completed", "GUI click")
        def post(self, browser_id):
            """Click using selector or screen coordinates."""
            data = get_json()
            return browser_ops.gui_click(
                browser_id,
                data.get("selector"),
                data.get("x"),
                data.get("y"),
                data.get("timeframe", 0.25),
                data.get("fx"),
                data.get("fy"),
            )

    # ==================== Page Content ====================

    @browser_ns.route("/<string:browser_id>/content")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class GetContent(Resource):
        @browser_ns.doc("get_content")
        @browser_ns.response(200, "Success", schemas["ContentResponse"])
        @browser_op(api, "Content retrieved", "Get content")
        def get(self, browser_id):
            """Get page HTML content."""
            return browser_ops.get_content(browser_id)

    @browser_ns.route("/<string:browser_id>/screenshot")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Screenshot(Resource):
        @browser_ns.doc("take_screenshot")
        @browser_ns.response(200, "Success", schemas["ScreenshotResponse"])
        @browser_op(api, "Screenshot taken", "Screenshot")
        def post(self, browser_id):
            """Take a screenshot."""
            return browser_ops.take_screenshot(browser_id)

    @browser_ns.route("/<string:browser_id>/execute")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class ExecuteScript(Resource):
        @browser_ns.doc("execute_script")
        @browser_ns.expect(schemas["ExecuteRequest"])
        @browser_ns.response(200, "Success", schemas["ExecuteResponse"])
        @browser_op(api, "Script executed", "Execute script")
        def post(self, browser_id):
            """Execute JavaScript."""
            data = get_json()
            require_params(data, "script")
            return browser_ops.execute_script(browser_id, data["script"])

    # ==================== Debugging ====================

    @browser_ns.route("/<string:browser_id>/console")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class ConsoleLogs(Resource):
        @browser_ns.doc("console_logs")
        @browser_ns.expect(schemas["ConsoleLogsRequest"])
        @browser_ns.response(200, "Success", schemas["LogsResponse"])
        @browser_op(api, "Console logs operation completed", "Console logs")
        def post(self, browser_id):
            """Get or clear console logs."""
            data = get_json()
            require_params(data, "action")
            action = LogAction(data["action"])
            return browser_ops.console_logs(browser_id, action, data.get("limit", 200))

    @browser_ns.route("/<string:browser_id>/network")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class NetworkLogs(Resource):
        @browser_ns.doc("network_logs")
        @browser_ns.expect(schemas["NetworkLogsRequest"])
        @browser_ns.response(200, "Success", schemas["LogsResponse"])
        @browser_op(api, "Network logs operation completed", "Network logs")
        def post(self, browser_id):
            """Get or clear network logs."""
            data = get_json()
            require_params(data, "action")
            action = LogAction(data["action"])
            return browser_ops.network_logs(browser_id, action, data.get("limit", 200))

    # ==================== AI Vision ====================

    @browser_ns.route("/<string:browser_id>/detect_coordinates")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class DetectCoordinates(Resource):
        @browser_ns.doc("detect_coordinates")
        @browser_ns.expect(schemas["DetectCoordinatesRequest"])
        @browser_ns.response(200, "Success", schemas["DetectCoordinatesResult"])
        @browser_op(api, "Coordinates detected", "Detect coordinates")
        def post(self, browser_id):
            """Detect element coordinates using AI vision."""
            data = get_json()
            require_params(data, "prompt")
            return browser_ops.detect_coordinates(browser_id, data["prompt"])

    @browser_ns.route("/<string:browser_id>/what_is_visible")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class WhatIsVisible(Resource):
        @browser_ns.doc("what_is_visible")
        @browser_ns.response(200, "Success", schemas["WhatIsVisibleResult"])
        @browser_op(api, "Analysis complete", "What is visible")
        def get(self, browser_id):
            """Analyze visible page content using AI."""
            return browser_ops.what_is_visible(browser_id)

    # ==================== Tabs ====================

    @browser_ns.route("/<string:browser_id>/tabs")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Tabs(Resource):
        @browser_ns.doc("tabs")
        @browser_ns.expect(schemas["TabsRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Tab operation completed", "Tabs")
        def post(self, browser_id):
            """Manage browser tabs: list, new, switch, close, or current."""
            data = get_json()
            require_params(data, "action")
            action = TabAction(data["action"])
            return browser_ops.tabs(
                browser_id, action, data.get("url"), data.get("index"), data.get("handle")
            )

    # ==================== Dialogs ====================

    @browser_ns.route("/<string:browser_id>/dialog")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Dialog(Resource):
        @browser_ns.doc("dialog")
        @browser_ns.expect(schemas["CombinedDialogRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Dialog operation completed", "Dialog")
        def post(self, browser_id):
            """Manage browser dialogs: get, accept, or dismiss."""
            data = get_json()
            require_params(data, "action")
            action = DialogAction(data["action"])
            return browser_ops.dialog(browser_id, action, data.get("text"))

    # ==================== Page Operations ====================

    @browser_ns.route("/<string:browser_id>/resize")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Resize(Resource):
        @browser_ns.doc("resize")
        @browser_ns.expect(schemas["ResizeRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Page resized", "Resize")
        def post(self, browser_id):
            """Resize viewport."""
            data = get_json()
            require_params(data, "width", "height")
            return browser_ops.resize(browser_id, data["width"], data["height"])

    @browser_ns.route("/<string:browser_id>/snapshot")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Snapshot(Resource):
        @browser_ns.doc("take_snapshot")
        @browser_ns.expect(schemas["SnapshotRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Snapshot taken", "Snapshot")
        def post(self, browser_id):
            """Take DOM/accessibility snapshot."""
            data = get_json()
            return browser_ops.snapshot(browser_id, data.get("type", "dom"))

    # ==================== Emulation ====================

    @browser_ns.route("/<string:browser_id>/emulate")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Emulate(Resource):
        @browser_ns.doc("emulate")
        @browser_ns.expect(schemas["CombinedEmulateRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Emulation operation completed", "Emulate")
        def post(self, browser_id):
            """Manage device emulation: set, clear, or list_devices."""
            data = get_json()
            action = EmulateAction(data.get("action", "set"))
            return browser_ops.emulate(
                browser_id,
                action,
                data.get("device"),
                data.get("width"),
                data.get("height"),
                data.get("device_scale_factor"),
                data.get("mobile"),
                data.get("user_agent"),
            )

    # ==================== Performance ====================

    @browser_ns.route("/<string:browser_id>/performance")
    @browser_ns.param("browser_id", "Unique browser identifier")
    class Performance(Resource):
        @browser_ns.doc("performance")
        @browser_ns.expect(schemas["PerformanceRequest"])
        @browser_ns.response(200, "Success", schemas["SuccessResponse"])
        @browser_op(api, "Performance operation completed", "Performance")
        def post(self, browser_id):
            """Manage performance: start_trace, stop_trace, metrics, or analyze."""
            data = get_json()
            require_params(data, "action")
            action = PerformanceAction(data["action"])
            return browser_ops.performance(browser_id, action, data.get("categories"))

    return browser_ns
