"""Shared browser operations coordinator for both REST API and MCP server.

This is a slim coordinator that delegates to specialized operations modules.
"""

from typing import Any

from .browser_pool import BrowserPoolAdapter
from .operations import (
    BrowsersAction,
    DebugOperations,
    DialogAction,
    DialogOperations,
    ElementCheck,
    ElementDataType,
    ElementOperations,
    EmulateAction,
    EmulationOperations,
    GuiOperations,
    HistoryAction,
    LifecycleOperations,
    LogAction,
    MouseAction,
    NavigationOperations,
    PageOperations,
    PerformanceAction,
    PerformanceOperations,
    PoolOperations,
    SelectAction,
    TabAction,
    TabOperations,
    VisionOperations,
    WaitUntil,
)


class BrowserOperations:
    """Browser operations coordinator. Each public method becomes an MCP tool."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool
        self._lifecycle = LifecycleOperations(browser_pool)
        self._navigation = NavigationOperations(browser_pool)
        self._elements = ElementOperations(browser_pool)
        self._gui = GuiOperations(browser_pool)
        self._vision = VisionOperations(browser_pool)
        self._page = PageOperations(browser_pool)
        self._debug = DebugOperations(browser_pool)
        self._pool = PoolOperations(browser_pool)
        self._tabs = TabOperations(browser_pool)
        self._dialogs = DialogOperations(browser_pool)
        self._emulation = EmulationOperations(browser_pool)
        self._performance = PerformanceOperations(browser_pool)

    # ==================== Lifecycle ====================

    def create_browser(
        self,
        uc: bool = True,
        proxy: str | None = None,
        window_size: list[int] | None = None,
        user_agent: str | None = None,
        disable_gpu: bool = False,
        disable_images: bool = False,
        disable_javascript: bool = False,
        extensions: list[str] | None = None,
        custom_args: list[str] | None = None,
        profile_name: str | None = None,
    ) -> dict[str, Any]:
        """Create browser instance with optional persistent profile."""
        return self._lifecycle.create_browser(
            uc=uc,
            proxy=proxy,
            window_size=window_size,
            user_agent=user_agent,
            disable_gpu=disable_gpu,
            disable_images=disable_images,
            disable_javascript=disable_javascript,
            extensions=extensions,
            custom_args=custom_args,
            profile_name=profile_name,
        )

    def close_browser(self, browser_id: str) -> dict[str, Any]:
        """Close browser instance."""
        return self._lifecycle.close_browser(browser_id)

    def browsers(self, action: BrowsersAction, browser_id: str | None = None) -> dict[str, Any]:
        """Admin: list all, get info, or close all browsers."""
        return self._lifecycle.browsers(action, browser_id)

    # ==================== Navigation ====================

    def navigate_browser(self, browser_id: str, url: str, timeout: int | None = None) -> dict[str, Any]:
        """Navigate to URL."""
        return self._navigation.navigate_browser(browser_id, url, timeout)

    def get_url(self, browser_id: str) -> dict[str, Any]:
        """Get current URL."""
        return self._navigation.get_url(browser_id)

    def history(self, browser_id: str, action: HistoryAction) -> dict[str, Any]:
        """History: back, forward, or refresh."""
        return self._navigation.history(browser_id, action)

    # ==================== Elements ====================

    def click(
        self, browser_id: str, selector: str, timeout: int | None = None, by: str = "css", if_visible: bool = False
    ) -> dict[str, Any]:
        """Click element. Use if_visible=True to only click if visible."""
        return self._elements.click(browser_id, selector, timeout, by, if_visible)

    def type_text(
        self, browser_id: str, selector: str, text: str, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Type text into element."""
        return self._elements.type_text(browser_id, selector, text, timeout, by)

    def press_keys(self, browser_id: str, selector: str, keys: str, by: str = "css") -> dict[str, Any]:
        """Press keyboard keys."""
        return self._elements.press_keys(browser_id, selector, keys, by)

    def check_element(self, browser_id: str, selector: str, check: ElementCheck, by: str = "css") -> dict[str, Any]:
        """Check if element exists or is visible."""
        return self._elements.check_element(browser_id, selector, check, by)

    def wait_element(
        self, browser_id: str, selector: str, until: WaitUntil, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Wait for element to be visible or hidden."""
        return self._elements.wait_element(browser_id, selector, until, timeout, by)

    def get_element_data(
        self, browser_id: str, selector: str, data_type: ElementDataType, name: str | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Get element text, attribute, or property."""
        return self._elements.get_element_data(browser_id, selector, data_type, name, by)

    def mouse(
        self,
        browser_id: str,
        action: MouseAction,
        selector: str | None = None,
        source: str | None = None,
        target: str | None = None,
        by: str = "css",
    ) -> dict[str, Any]:
        """Mouse: hover or drag."""
        return self._elements.mouse(browser_id, action, selector, source, target, by)

    def scroll(
        self,
        browser_id: str,
        selector: str | None = None,
        x: int | None = None,
        y: int | None = None,
        delta_x: int | None = None,
        delta_y: int | None = None,
        behavior: str = "smooth",
        by: str = "css",
    ) -> dict[str, Any]:
        """Scroll to element/coords or by delta."""
        return self._elements.scroll(browser_id, selector, x, y, delta_x, delta_y, behavior, by)

    # ==================== Forms ====================

    def fill_form(self, browser_id: str, fields: list[dict], by: str = "css") -> dict[str, Any]:
        """Fill multiple form fields."""
        return self._elements.fill_form(browser_id, fields, by)

    def select(
        self,
        browser_id: str,
        selector: str,
        action: SelectAction = SelectAction.SELECT,
        value: str | None = None,
        text: str | None = None,
        index: int | None = None,
        by: str = "css",
    ) -> dict[str, Any]:
        """Select dropdown: select option or get options."""
        return self._elements.select_action(browser_id, selector, action, value, text, index, by)

    def upload_file(self, browser_id: str, selector: str, file_path: str, by: str = "css") -> dict[str, Any]:
        """Upload file to input."""
        return self._elements.upload_file(browser_id, selector, file_path, by)

    # ==================== GUI/Vision ====================

    def gui_click(
        self,
        browser_id: str,
        selector: str | None = None,
        x: float | None = None,
        y: float | None = None,
        timeframe: float = 0.25,
        fx: float | None = None,
        fy: float | None = None,
    ) -> dict[str, Any]:
        """GUI click by selector or coordinates."""
        return self._gui.gui_click(browser_id, selector, x, y, timeframe, fx, fy)

    def gui_type_xy(self, browser_id: str, x: float, y: float, text: str, timeframe: float = 0.25) -> dict[str, Any]:
        """GUI type at coordinates - clicks then types text."""
        return self._gui.gui_type_xy(browser_id, x, y, text, timeframe)

    def gui_hover_xy(self, browser_id: str, x: float, y: float, timeframe: float = 0.25) -> dict[str, Any]:
        """GUI hover at coordinates."""
        return self._gui.gui_hover_xy(browser_id, x, y, timeframe)

    def gui_press_keys_xy(
        self, browser_id: str, x: float, y: float, keys: str, timeframe: float = 0.25
    ) -> dict[str, Any]:
        """Press keys at coordinates (click to focus, then send keys)."""
        return self._gui.gui_press_keys_xy(browser_id, x, y, keys, timeframe)

    def detect_coordinates(
        self, browser_id: str, prompt: str, fx: float | None = None, fy: float | None = None
    ) -> dict[str, Any]:
        """Detect element coordinates using vision.

        Args:
            browser_id: Browser instance identifier
            prompt: Natural language description of element to find
            fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right).
                If None, auto-bias is applied for wide elements (0.25 for aspect ratio > 10).
            fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom).
        """
        return self._vision.detect_coordinates(browser_id, prompt, fx, fy)

    def what_is_visible(self, browser_id: str) -> dict[str, Any]:
        """AI page analysis - what's visible."""
        return self._vision.what_is_visible(browser_id)

    # ==================== Page ====================

    def take_screenshot(self, browser_id: str, full_page: bool = False) -> dict[str, Any]:
        """Take screenshot."""
        return self._page.take_screenshot(browser_id, full_page)

    def get_content(self, browser_id: str) -> dict[str, Any]:
        """Get page HTML."""
        return self._page.get_content(browser_id)

    def execute_script(self, browser_id: str, script: str) -> dict[str, Any]:
        """Execute JavaScript."""
        return self._page.execute_script(browser_id, script)

    def resize(self, browser_id: str, width: int, height: int) -> dict[str, Any]:
        """Resize viewport."""
        return self._page.resize(browser_id, width, height)

    def snapshot(self, browser_id: str, snapshot_type: str = "dom") -> dict[str, Any]:
        """DOM or accessibility snapshot."""
        return self._page.snapshot(browser_id, snapshot_type)

    # ==================== Debug ====================

    def console_logs(self, browser_id: str, action: LogAction, limit: int = 200) -> dict[str, Any]:
        """Console logs: get or clear."""
        return self._debug.console_logs(browser_id, action, limit)

    def network_logs(self, browser_id: str, action: LogAction, limit: int = 500) -> dict[str, Any]:
        """Network logs: get or clear."""
        return self._debug.network_logs(browser_id, action, limit)

    def get_cdp_endpoint(self, browser_id: str) -> dict[str, Any]:
        """Get Chrome DevTools Protocol WebSocket URL for direct CDP access.

        Returns the WebSocket URL that external tools (Playwright, Puppeteer, etc.)
        can use to connect directly to Chrome's DevTools Protocol for advanced
        automation like network interception, performance profiling, or custom CDP commands.

        The returned URL format: ws://host:port/devtools/browser/{guid}

        Note: The URL uses the container's internal address. For external access,
        ensure the CDP port is exposed and use the appropriate host address.
        """
        return self._debug.get_cdp_endpoint(browser_id)

    # ==================== Tabs/Dialogs ====================

    def tabs(
        self,
        browser_id: str,
        action: TabAction,
        url: str | None = None,
        index: int | None = None,
        handle: str | None = None,
    ) -> dict[str, Any]:
        """Tabs: list, new, switch, close, current."""
        return self._tabs.tabs(browser_id, action, url, index, handle)

    def dialog(self, browser_id: str, action: DialogAction, text: str | None = None) -> dict[str, Any]:
        """Dialogs: get, accept, dismiss."""
        return self._dialogs.dialog(browser_id, action, text)

    # ==================== Emulation/Performance ====================

    def emulate(
        self,
        browser_id: str,
        action: EmulateAction = EmulateAction.SET,
        device: str | None = None,
        width: int | None = None,
        height: int | None = None,
        device_scale_factor: float | None = None,
        mobile: bool | None = None,
        user_agent: str | None = None,
    ) -> dict[str, Any]:
        """Emulation: set, clear, list_devices."""
        return self._emulation.emulate(
            browser_id, action, device, width, height, device_scale_factor, mobile, user_agent
        )

    def performance(self, browser_id: str, action: PerformanceAction, categories: str | None = None) -> dict[str, Any]:
        """Performance: start_trace, stop_trace, metrics, analyze."""
        return self._performance.performance(browser_id, action, categories)

    # ==================== Pool ====================

    def get_pool_status(self, start_time: float | None = None) -> dict[str, Any]:
        """Get pool status."""
        return self._pool.get_pool_status(start_time)

    def health_check(self, start_time: float | None = None) -> dict[str, Any]:
        """Health check."""
        return self._pool.health_check(start_time)
