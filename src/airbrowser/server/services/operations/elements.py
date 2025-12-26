"""Element interaction operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import ElementCheck, ElementDataType, MouseAction, SelectAction, WaitUntil
from .response import error as _error
from .response import success as _success


def _make_result(result, error_prefix: str = "Operation") -> dict[str, Any]:
    """Create standardized result dict from action result."""
    if result.success:
        return _success(data=result.data, message=result.message)
    return _error(result.message)


class ElementOperations:
    """Handles element interaction operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def _execute(self, browser_id: str, action: BrowserAction, error_prefix: str = "Operation") -> dict[str, Any]:
        """Execute action and return standardized result."""
        try:
            result = self.browser_pool.execute_action(browser_id, action)
            return _make_result(result, error_prefix)
        except Exception as e:
            return _error(f"{error_prefix} failed: {str(e)}")

    def type_text(
        self, browser_id: str, selector: str, text: str, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Type text into an element in the browser."""
        try:
            action = BrowserAction(
                action="type",
                selector=selector,
                text=text,
                timeout=timeout,
                by=by,
            )
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Type operation failed: {str(e)}")

    def click_element(
        self, browser_id: str, selector: str, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Click on an element in the browser."""
        try:
            action = BrowserAction(
                action="click",
                selector=selector,
                timeout=timeout,
                by=by,
            )
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Click operation failed: {str(e)}")

    def get_text(self, browser_id: str, selector: str, timeout: int | None = None, by: str = "css") -> dict[str, Any]:
        """Get text content from an element."""
        try:
            action = BrowserAction(
                action="get_text",
                selector=selector,
                timeout=timeout,
                by=by,
            )
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            text_value = None
            if isinstance(result.data, dict):
                text_value = result.data.get("result") or (
                    (result.data.get("data") or {}).get("text") if isinstance(result.data.get("data"), dict) else None
                )

            data = result.data or {}
            data["text"] = text_value
            return _success(data=data, message=result.message)

        except Exception as e:
            return _error(f"Get text failed: {str(e)}")

    def wait_for_element(
        self, browser_id: str, selector: str, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Wait for an element to appear on the page."""
        try:
            action = BrowserAction(
                action="wait",
                selector=selector,
                timeout=timeout,
                by=by,
            )
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Wait operation failed: {str(e)}")

    def click_if_visible(self, browser_id: str, selector: str, by: str = "css") -> dict[str, Any]:
        """Click an element if it's visible."""
        try:
            action = BrowserAction(action="click_if_visible", selector=selector, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"click_if_visible failed: {str(e)}")

    def wait_not_visible(self, browser_id: str, selector: str, timeout: int = 20, by: str = "css") -> dict[str, Any]:
        """Wait for an element to become invisible."""
        try:
            action = BrowserAction(action="wait_for_element_not_visible", selector=selector, timeout=timeout, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"wait_for_element_not_visible failed: {str(e)}")

    def press_keys(self, browser_id: str, selector: str, keys: str, by: str = "css") -> dict[str, Any]:
        """Press keys on an element."""
        try:
            action = BrowserAction(action="press_keys", selector=selector, text=keys, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"press_keys failed: {str(e)}")

    def hover(self, browser_id: str, selector: str, by: str = "css") -> dict[str, Any]:
        """Hover over an element."""
        try:
            action = BrowserAction(action="hover", selector=selector, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"hover failed: {str(e)}")

    def drag(self, browser_id: str, source: str, target: str, by: str = "css") -> dict[str, Any]:
        """Drag element from source to target."""
        try:
            action = BrowserAction(action="drag", options={"source": source, "target": target}, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"drag failed: {str(e)}")

    def fill_form(self, browser_id: str, fields: list[dict], by: str = "css") -> dict[str, Any]:
        """Fill multiple form fields at once."""
        try:
            action = BrowserAction(action="fill_form", options={"fields": fields}, by=by)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"fill_form failed: {str(e)}")

    def upload_file(self, browser_id: str, selector: str, file_path: str, by: str = "css") -> dict[str, Any]:
        """Upload a file to a file input element."""
        action = BrowserAction(action="upload_file", selector=selector, options={"file_path": file_path}, by=by)
        return self._execute(browser_id, action, "upload_file")

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
        """Scroll to element/coordinates or by relative amount.

        Args:
            browser_id: The browser instance ID
            selector: CSS/XPath selector to scroll to
            x: Absolute X coordinate to scroll to
            y: Absolute Y coordinate to scroll to
            delta_x: Relative X scroll amount (for scroll_by mode)
            delta_y: Relative Y scroll amount (for scroll_by mode)
            behavior: Scroll behavior ("smooth" or "auto")
            by: Selector type ("css" or "xpath")

        If delta_x or delta_y is provided, performs relative scroll.
        Otherwise, scrolls to element or absolute coordinates.
        """
        # If delta values provided, use relative scroll
        if delta_x is not None or delta_y is not None:
            action = BrowserAction(
                action="scroll_by",
                options={"delta_x": delta_x or 0, "delta_y": delta_y or 0, "behavior": behavior},
            )
            return self._execute(browser_id, action, "scroll_by")

        # Otherwise, absolute scroll
        action = BrowserAction(
            action="scroll",
            selector=selector,
            by=by,
            options={"x": x, "y": y, "behavior": behavior},
        )
        return self._execute(browser_id, action, "scroll")

    def scroll_by(
        self, browser_id: str, delta_x: int = 0, delta_y: int = 0, behavior: str = "smooth"
    ) -> dict[str, Any]:
        """Scroll by relative amount. (Legacy - use scroll with delta_x/delta_y instead)"""
        action = BrowserAction(
            action="scroll_by",
            options={"delta_x": delta_x, "delta_y": delta_y, "behavior": behavior},
        )
        return self._execute(browser_id, action, "scroll_by")

    def select(
        self,
        browser_id: str,
        selector: str,
        value: str | None = None,
        text: str | None = None,
        index: int | None = None,
        by: str = "css",
    ) -> dict[str, Any]:
        """Select option from dropdown."""
        action = BrowserAction(
            action="select",
            selector=selector,
            by=by,
            options={"value": value, "text": text, "index": index},
        )
        return self._execute(browser_id, action, "select")

    def get_select_options(self, browser_id: str, selector: str, by: str = "css") -> dict[str, Any]:
        """Get all options from a select dropdown."""
        action = BrowserAction(action="get_select_options", selector=selector, by=by)
        return self._execute(browser_id, action, "get_select_options")

    def get_attribute(self, browser_id: str, selector: str, attribute: str, by: str = "css") -> dict[str, Any]:
        """Get attribute value from an element."""
        action = BrowserAction(
            action="get_attribute",
            selector=selector,
            by=by,
            options={"attribute": attribute},
        )
        return self._execute(browser_id, action, "get_attribute")

    def get_property(self, browser_id: str, selector: str, prop: str, by: str = "css") -> dict[str, Any]:
        """Get DOM property value from an element."""
        action = BrowserAction(
            action="get_property",
            selector=selector,
            by=by,
            options={"property": prop},
        )
        return self._execute(browser_id, action, "get_property")

    def find_element(self, browser_id: str, selector: str, by: str = "css") -> dict[str, Any]:
        """Check if an element exists on the page."""
        action = BrowserAction(action="find_element", selector=selector, by=by)
        return self._execute(browser_id, action, "find_element")

    def is_visible(self, browser_id: str, selector: str, by: str = "css") -> dict[str, Any]:
        """Check if an element is visible."""
        action = BrowserAction(action="is_visible", selector=selector, by=by)
        return self._execute(browser_id, action, "is_visible")

    # ==================== Combined Methods ====================

    def check_element(self, browser_id: str, selector: str, check: ElementCheck, by: str = "css") -> dict[str, Any]:
        """Check element state.

        Args:
            browser_id: The browser instance ID
            selector: CSS/XPath selector
            check: ElementCheck enum (EXISTS or VISIBLE)
            by: Selector type ("css" or "xpath")
        """
        if check == ElementCheck.EXISTS:
            return self.find_element(browser_id, selector, by)
        elif check == ElementCheck.VISIBLE:
            return self.is_visible(browser_id, selector, by)
        else:
            return _error(f"Invalid check type: {check}")

    def wait_element(
        self, browser_id: str, selector: str, until: WaitUntil, timeout: int | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Wait for element state.

        Args:
            browser_id: The browser instance ID
            selector: CSS/XPath selector
            until: WaitUntil enum (VISIBLE or HIDDEN)
            timeout: Wait timeout in seconds
            by: Selector type ("css" or "xpath")
        """
        if until == WaitUntil.VISIBLE:
            return self.wait_for_element(browser_id, selector, timeout, by)
        elif until == WaitUntil.HIDDEN:
            return self.wait_not_visible(browser_id, selector, timeout, by)
        else:
            return _error(f"Invalid until value: {until}")

    def get_element_data(
        self, browser_id: str, selector: str, data_type: ElementDataType, name: str | None = None, by: str = "css"
    ) -> dict[str, Any]:
        """Get element text, attribute, or property.

        Args:
            browser_id: The browser instance ID
            selector: CSS/XPath selector
            data_type: ElementDataType enum (TEXT, ATTRIBUTE, or PROPERTY)
            name: Name of the attribute/property (required for ATTRIBUTE/PROPERTY)
            by: Selector type ("css" or "xpath")
        """
        if data_type == ElementDataType.TEXT:
            return self.get_text(browser_id, selector, by=by)
        elif data_type == ElementDataType.ATTRIBUTE:
            if not name:
                return _error("name required for attribute")
            return self.get_attribute(browser_id, selector, name, by)
        elif data_type == ElementDataType.PROPERTY:
            if not name:
                return _error("name required for property")
            return self.get_property(browser_id, selector, name, by)
        else:
            return _error(f"Invalid data_type: {data_type}")

    def click(
        self, browser_id: str, selector: str, timeout: int | None = None, by: str = "css", if_visible: bool = False
    ) -> dict[str, Any]:
        """Click on element. Use if_visible=True to only click if element is visible."""
        if if_visible:
            return self.click_if_visible(browser_id, selector, by)
        return self.click_element(browser_id, selector, timeout, by)

    def mouse(
        self,
        browser_id: str,
        action: MouseAction,
        selector: str | None = None,
        source: str | None = None,
        target: str | None = None,
        by: str = "css",
    ) -> dict[str, Any]:
        """Mouse operations: hover or drag."""
        if action == MouseAction.HOVER:
            if not selector:
                return _error("selector required for hover")
            return self.hover(browser_id, selector, by)
        elif action == MouseAction.DRAG:
            if not source or not target:
                return _error("source and target required for drag")
            return self.drag(browser_id, source, target, by)
        return _error(f"Invalid mouse action: {action}")

    def select_action(
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
        if action == SelectAction.OPTIONS:
            return self.get_select_options(browser_id, selector, by)
        return self.select(browser_id, selector, value, text, index, by)
