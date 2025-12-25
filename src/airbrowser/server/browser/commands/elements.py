"""Element interaction browser commands."""

import logging
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

# Map key names to Selenium Keys constants
KEY_MAP = {
    "ENTER": Keys.ENTER,
    "RETURN": Keys.RETURN,
    "TAB": Keys.TAB,
    "ESCAPE": Keys.ESCAPE,
    "BACKSPACE": Keys.BACKSPACE,
    "DELETE": Keys.DELETE,
    "SPACE": Keys.SPACE,
    "UP": Keys.UP,
    "DOWN": Keys.DOWN,
    "LEFT": Keys.LEFT,
    "RIGHT": Keys.RIGHT,
    "HOME": Keys.HOME,
    "END": Keys.END,
    "PAGE_UP": Keys.PAGE_UP,
    "PAGE_DOWN": Keys.PAGE_DOWN,
    "F1": Keys.F1,
    "F2": Keys.F2,
    "F3": Keys.F3,
    "F4": Keys.F4,
    "F5": Keys.F5,
    "F6": Keys.F6,
    "F7": Keys.F7,
    "F8": Keys.F8,
    "F9": Keys.F9,
    "F10": Keys.F10,
    "F11": Keys.F11,
    "F12": Keys.F12,
    "CONTROL": Keys.CONTROL,
    "CTRL": Keys.CONTROL,
    "ALT": Keys.ALT,
    "SHIFT": Keys.SHIFT,
    "META": Keys.META,
    "COMMAND": Keys.COMMAND,
}


# Map our 'by' values to Selenium's expected format
BY_MAP = {
    "css": "css selector",
    "xpath": "xpath",
    "id": "id",
    "name": "name",
}


def _get_selenium_by(by: str) -> str:
    """Convert our by value to Selenium's expected format."""
    return BY_MAP.get(by, "css selector")


def _find_element_by(driver, selector: str, by: str = "css"):
    """Find element using the specified selector strategy."""
    selenium_by = _get_selenium_by(by)
    return driver.find_element(selenium_by, selector)


def handle_click(driver, command: dict) -> dict:
    """Click on an element."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        # Find the element and click it
        selenium_by = _get_selenium_by(by)
        element = driver.find_element(selenium_by, selector)
        element.click()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"Click failed: {str(e)}"}


def handle_type(driver, command: dict) -> dict:
    """Type text into an element."""
    selector = command.get("selector")
    by = command.get("by", "css")
    text = command.get("text", "")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        driver.type(selector, text, by=_get_selenium_by(by))
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"Type failed: {str(e)}"}


def handle_wait(driver, command: dict) -> dict:
    """Wait for an element to appear."""
    selector = command.get("selector")
    by = command.get("by", "css")
    timeout = command.get("timeout", 10)
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        driver.wait_for_element_visible(selector, by=_get_selenium_by(by), timeout=timeout)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"Element not found: {str(e)}"}


def handle_click_if_visible(driver, command: dict) -> dict:
    """Click an element if it's visible."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        element = _find_element_by(driver, selector, by)
        if element and element.is_displayed():
            driver.uc_click(selector, by=_get_selenium_by(by))
            return {"status": "success", "clicked": True, "message": "Element clicked"}
        else:
            return {"status": "success", "clicked": False, "message": "Element not visible"}
    except Exception:
        return {"status": "success", "clicked": False, "message": "Element not found"}


def handle_wait_for_element_not_visible(driver, command: dict) -> dict:
    """Wait for an element to become invisible."""
    selector = command.get("selector")
    by = command.get("by", "css")
    timeout = command.get("timeout", 20)
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        driver.wait_for_element_not_visible(selector, by=_get_selenium_by(by), timeout=timeout)
        return {"status": "success", "message": "Element is not visible"}
    except Exception as e:
        return {"status": "error", "message": f"Element still visible: {str(e)}"}


def handle_press_keys(driver, command: dict) -> dict:
    """Press keys on an element.

    Supports special key names like ENTER, TAB, ESCAPE, etc.
    Multiple keys can be combined with + (e.g., "CTRL+a" for select all).
    """
    selector = command.get("selector")
    by = command.get("by", "css")
    keys_input = command.get("text", "")  # BrowserAction uses "text" field
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        element = _find_element_by(driver, selector, by)
    except Exception as e:
        return {"status": "error", "message": f"Element not found: {str(e)}"}

    # Convert key names to Selenium Keys constants
    # Support both single keys ("ENTER") and combinations ("CTRL+a")
    if "+" in keys_input:
        # Handle key combinations like "CTRL+a", "SHIFT+TAB"
        parts = keys_input.split("+")
        keys_to_send = []
        for part in parts:
            part_stripped = part.strip()
            part_upper = part_stripped.upper()
            if part_upper in KEY_MAP:
                keys_to_send.append(KEY_MAP[part_upper])
            else:
                # Regular character - preserve original case
                keys_to_send.append(part_stripped)

        # Send key combination using ActionChains for proper modifier key handling
        actions = ActionChains(driver)
        # Hold down modifier keys, press the final key, then release
        for key in keys_to_send[:-1]:
            actions.key_down(key, element)
        actions.send_keys_to_element(element, keys_to_send[-1])
        for key in reversed(keys_to_send[:-1]):
            actions.key_up(key, element)
        actions.perform()
    else:
        # Single key - check if it's a special key
        key_upper = keys_input.strip().upper()
        if key_upper in KEY_MAP:
            element.send_keys(KEY_MAP[key_upper])
        else:
            # Regular text, send as-is
            element.send_keys(keys_input)

    return {"status": "success", "message": f"Keys pressed: {keys_input}"}


def handle_get_text(driver, command: dict) -> dict:
    """Get text from an element."""
    selector = command.get("selector")
    by = command.get("by", "css")

    try:
        from selenium.common.exceptions import NoSuchElementException

        element = _find_element_by(driver, selector, by)

        if element:
            text = element.text
            return {
                "status": "success",
                "result": text,
                "data": {"text": text, "request_id": str(time.time()), "timestamp": time.time()},
            }
        else:
            return {"status": "error", "message": "Element not found"}

    except NoSuchElementException:
        return {"status": "error", "message": "Element not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get text: {str(e)}"}


def handle_find_element(driver, command: dict) -> dict:
    """Check if an element exists."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        from selenium.common.exceptions import NoSuchElementException

        element = _find_element_by(driver, selector, by)
        return {"status": "success", "found": element is not None, "selector": selector, "by": by}
    except NoSuchElementException:
        return {"status": "success", "found": False, "selector": selector, "by": by}
    except Exception as e:
        return {"status": "error", "message": f"Failed to find element: {str(e)}"}


def handle_is_element_visible(driver, command: dict) -> dict:
    """Check if an element is visible."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        from selenium.common.exceptions import NoSuchElementException

        element = _find_element_by(driver, selector, by)
        visible = element is not None and element.is_displayed()
        return {"status": "success", "visible": visible, "selector": selector, "by": by}
    except NoSuchElementException:
        return {"status": "success", "visible": False, "selector": selector, "by": by}
    except Exception as e:
        return {"status": "error", "message": f"Failed to check visibility: {str(e)}"}


def handle_get_elements(driver, command: dict) -> dict:
    """Get multiple elements matching a selector."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        elements = driver.find_elements(_get_selenium_by(by), selector)
        return {
            "status": "success",
            "count": len(elements),
            "elements": [{"text": el.text, "tag": el.tag_name} for el in elements[:10]],
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to find elements: {str(e)}"}


def handle_hover(driver, command: dict) -> dict:
    """Hover over an element."""
    selector = command.get("selector")
    by = command.get("by", "css")
    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        element = _find_element_by(driver, selector, by)
        if element:
            ActionChains(driver).move_to_element(element).perform()
            return {"status": "success", "message": "Hovered over element"}
        else:
            return {"status": "error", "message": "Element not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to hover: {str(e)}"}


def handle_drag(driver, command: dict) -> dict:
    """Drag element from source to target."""
    source_selector = command.get("source")
    target_selector = command.get("target")
    by = command.get("by", "css")

    if not source_selector or not target_selector:
        return {"status": "error", "message": "Source and target selectors are required"}

    try:
        source = _find_element_by(driver, source_selector, by)
        target = _find_element_by(driver, target_selector, by)

        if not source:
            return {"status": "error", "message": "Source element not found"}
        if not target:
            return {"status": "error", "message": "Target element not found"}

        ActionChains(driver).drag_and_drop(source, target).perform()
        return {"status": "success", "message": "Drag completed"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to drag: {str(e)}"}


def handle_fill_form(driver, command: dict) -> dict:
    """Fill multiple form fields at once."""
    fields = command.get("fields", [])
    by = command.get("by", "css")

    if not fields:
        return {"status": "error", "message": "Fields array is required"}

    filled = []
    errors = []

    for field in fields:
        selector = field.get("selector")
        value = field.get("value", "")

        if not selector:
            errors.append({"selector": selector, "error": "Missing selector"})
            continue

        try:
            element = _find_element_by(driver, selector, by)
            if element:
                element.clear()
                element.send_keys(value)
                filled.append(selector)
            else:
                errors.append({"selector": selector, "error": "Element not found"})
        except Exception as e:
            errors.append({"selector": selector, "error": str(e)})

    return {
        "status": "success" if not errors else "partial",
        "filled_count": len(filled),
        "filled": filled,
        "errors": errors,
    }


def handle_upload_file(driver, command: dict) -> dict:
    """Upload a file to a file input element."""
    selector = command.get("selector")
    file_path = command.get("file_path")
    by = command.get("by", "css")

    if not selector:
        return {"status": "error", "message": "Selector is required"}
    if not file_path:
        return {"status": "error", "message": "File path is required"}

    try:
        element = _find_element_by(driver, selector, by)
        if element:
            element.send_keys(file_path)
            return {"status": "success", "message": f"File uploaded: {file_path}"}
        else:
            return {"status": "error", "message": "File input element not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to upload file: {str(e)}"}


def handle_scroll(driver, command: dict) -> dict:
    """Scroll to element or coordinates."""
    selector = command.get("selector")
    by = command.get("by", "css")
    x = command.get("x")
    y = command.get("y")
    behavior = command.get("behavior", "smooth")  # smooth or instant

    try:
        if selector:
            # Scroll to element
            element = _find_element_by(driver, selector, by)
            if element:
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: arguments[1], block: 'center'});",
                    element,
                    behavior,
                )
                return {"status": "success", "message": "Scrolled to element"}
            else:
                return {"status": "error", "message": "Element not found"}
        elif x is not None or y is not None:
            # Scroll to coordinates
            scroll_x = x if x is not None else 0
            scroll_y = y if y is not None else 0
            driver.execute_script(
                f"window.scrollTo({{left: {scroll_x}, top: {scroll_y}, behavior: '{behavior}'}});"
            )
            return {"status": "success", "message": f"Scrolled to ({scroll_x}, {scroll_y})"}
        else:
            return {"status": "error", "message": "Either selector or coordinates (x, y) required"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to scroll: {str(e)}"}


def handle_scroll_by(driver, command: dict) -> dict:
    """Scroll by relative amount."""
    delta_x = command.get("delta_x", 0)
    delta_y = command.get("delta_y", 0)
    behavior = command.get("behavior", "smooth")

    try:
        driver.execute_script(
            f"window.scrollBy({{left: {delta_x}, top: {delta_y}, behavior: '{behavior}'}});"
        )
        return {"status": "success", "message": f"Scrolled by ({delta_x}, {delta_y})"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to scroll: {str(e)}"}


def handle_select(driver, command: dict) -> dict:
    """Select option from dropdown."""
    selector = command.get("selector")
    by = command.get("by", "css")
    value = command.get("value")
    text = command.get("text")
    index = command.get("index")

    if not selector:
        return {"status": "error", "message": "Selector is required"}
    if value is None and text is None and index is None:
        return {"status": "error", "message": "One of value, text, or index is required"}

    try:
        from selenium.webdriver.support.ui import Select

        element = _find_element_by(driver, selector, by)
        if not element:
            return {"status": "error", "message": "Select element not found"}

        select = Select(element)

        if value is not None:
            select.select_by_value(str(value))
            return {"status": "success", "message": f"Selected by value: {value}"}
        elif text is not None:
            select.select_by_visible_text(str(text))
            return {"status": "success", "message": f"Selected by text: {text}"}
        elif index is not None:
            select.select_by_index(int(index))
            return {"status": "success", "message": f"Selected by index: {index}"}

    except Exception as e:
        return {"status": "error", "message": f"Failed to select: {str(e)}"}


def handle_get_select_options(driver, command: dict) -> dict:
    """Get all options from a select dropdown."""
    selector = command.get("selector")
    by = command.get("by", "css")

    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        from selenium.webdriver.support.ui import Select

        element = _find_element_by(driver, selector, by)
        if not element:
            return {"status": "error", "message": "Select element not found"}

        select = Select(element)
        options = []
        for i, opt in enumerate(select.options):
            options.append({
                "index": i,
                "value": opt.get_attribute("value"),
                "text": opt.text,
                "selected": opt.is_selected(),
            })

        selected = [opt.text for opt in select.all_selected_options]

        return {
            "status": "success",
            "options": options,
            "selected": selected,
            "count": len(options),
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to get options: {str(e)}"}


def handle_get_attribute(driver, command: dict) -> dict:
    """Get attribute value from an element."""
    selector = command.get("selector")
    by = command.get("by", "css")
    attribute = command.get("attribute")

    if not selector:
        return {"status": "error", "message": "Selector is required"}
    if not attribute:
        return {"status": "error", "message": "Attribute name is required"}

    try:
        element = _find_element_by(driver, selector, by)
        if element:
            value = element.get_attribute(attribute)
            return {
                "status": "success",
                "attribute": attribute,
                "value": value,
            }
        else:
            return {"status": "error", "message": "Element not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get attribute: {str(e)}"}


def handle_get_property(driver, command: dict) -> dict:
    """Get DOM property value from an element."""
    selector = command.get("selector")
    by = command.get("by", "css")
    prop = command.get("property")

    if not selector:
        return {"status": "error", "message": "Selector is required"}
    if not prop:
        return {"status": "error", "message": "Property name is required"}

    try:
        element = _find_element_by(driver, selector, by)
        if element:
            value = element.get_property(prop)
            return {
                "status": "success",
                "property": prop,
                "value": value,
            }
        else:
            return {"status": "error", "message": "Element not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get property: {str(e)}"}
