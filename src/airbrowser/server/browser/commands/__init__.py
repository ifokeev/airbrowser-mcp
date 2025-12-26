"""Command dispatcher for browser operations."""

import json
import logging

from . import cookies, debug, dialogs, elements, emulation, gui, navigation, page, performance, tabs, vision

logger = logging.getLogger(__name__)

# Map command types to handler functions
COMMAND_HANDLERS = {
    # Navigation
    "navigate": navigation.handle_navigate,
    "url": navigation.handle_get_url,
    "get_url": navigation.handle_get_url,
    "go_back": navigation.handle_go_back,
    "go_forward": navigation.handle_go_forward,
    "refresh": navigation.handle_refresh,
    # Elements
    "click": elements.handle_click,
    "type": elements.handle_type,
    "wait": elements.handle_wait,
    "wait_for_element": elements.handle_wait,
    "click_if_visible": elements.handle_click_if_visible,
    "wait_for_element_not_visible": elements.handle_wait_for_element_not_visible,
    "press_keys": elements.handle_press_keys,
    "get_text": elements.handle_get_text,
    "find_element": elements.handle_find_element,
    "is_element_visible": elements.handle_is_element_visible,
    "is_visible": elements.handle_is_element_visible,
    "get_elements": elements.handle_get_elements,
    "hover": elements.handle_hover,
    "drag": elements.handle_drag,
    "fill_form": elements.handle_fill_form,
    "upload_file": elements.handle_upload_file,
    "scroll": elements.handle_scroll,
    "scroll_by": elements.handle_scroll_by,
    "select": elements.handle_select,
    "get_select_options": elements.handle_get_select_options,
    "get_attribute": elements.handle_get_attribute,
    "get_property": elements.handle_get_property,
    # Dialogs
    "handle_dialog": dialogs.handle_dialog,
    "get_dialog": dialogs.handle_get_dialog,
    # GUI operations
    "gui_click": gui.handle_gui_click,
    "gui_click_xy": gui.handle_gui_click_xy,
    "gui_type_xy": gui.handle_gui_type_xy,
    "gui_hover_xy": gui.handle_gui_hover_xy,
    "gui_press_keys_xy": gui.handle_gui_press_keys_xy,
    # Page content
    "screenshot": page.handle_screenshot,
    "get_content": page.handle_get_content,
    "execute_script": page.handle_execute_script,
    "resize": page.handle_resize,
    "snapshot": page.handle_snapshot,
    # Emulation
    "emulate": emulation.handle_emulate,
    "list_devices": emulation.handle_list_devices,
    "clear_emulation": emulation.handle_clear_emulation,
    # Performance
    "start_trace": performance.handle_start_trace,
    "stop_trace": performance.handle_stop_trace,
    "get_metrics": performance.handle_get_metrics,
    "analyze_insight": performance.handle_analyze_insight,
    # Cookies
    "get_cookies": cookies.handle_get_cookies,
    "set_cookie": cookies.handle_set_cookie,
    "delete_cookies": cookies.handle_delete_cookies,
    # Debug/logging
    "get_console_logs": debug.handle_get_console_logs,
    "clear_console_logs": debug.handle_clear_console_logs,
    "get_performance_logs": debug.handle_get_performance_logs,
    "clear_performance_logs": debug.handle_clear_performance_logs,
    # Vision
    "detect_coordinates": vision.handle_detect_coordinates,
    "what_is_visible": vision.handle_what_is_visible,
    # Tabs
    "list_tabs": tabs.handle_list_tabs,
    "new_tab": tabs.handle_new_tab,
    "switch_tab": tabs.handle_switch_tab,
    "close_tab": tabs.handle_close_tab,
    "get_current_tab": tabs.handle_get_current_tab,
}

# Commands that need browser_id passed to them
COMMANDS_NEEDING_BROWSER_ID = {
    "screenshot",
    "detect_coordinates",
    "what_is_visible",
    "start_trace",
    "stop_trace",
}


def handle_command(driver, command, browser_id: str = "unknown") -> dict:
    """
    Dispatch a command to the appropriate handler.

    Args:
        driver: SeleniumBase driver instance
        command: Command dict or JSON string
        browser_id: Browser instance identifier

    Returns:
        Result dictionary with 'status' key
    """
    logger.debug(f"Received command: {command}")

    # Handle case where command might be a string
    if isinstance(command, str):
        try:
            command = json.loads(command)
        except json.JSONDecodeError:
            return {"status": "error", "message": f"Invalid command format: {command}"}

    cmd_type = command.get("type")
    logger.debug(f"Command type: {cmd_type}")

    # Handle close command specially
    if cmd_type == "close":
        return {"status": "success", "action": "close", "message": "Browser closing"}

    # Look up handler
    handler = COMMAND_HANDLERS.get(cmd_type)
    if not handler:
        return {"status": "error", "message": f"Unknown command type: {cmd_type}"}

    try:
        # Some commands need browser_id (for screenshot filenames, etc.)
        if cmd_type in COMMANDS_NEEDING_BROWSER_ID:
            return handler(driver, command, browser_id=browser_id)
        else:
            return handler(driver, command)

    except Exception as e:
        logger.error(f"Error handling command {cmd_type}: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
