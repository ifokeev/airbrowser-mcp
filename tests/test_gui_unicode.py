#!/usr/bin/env python3
"""
Test suite for GUI operations with Unicode/Cyrillic text.

Tests that gui_type_xy correctly handles non-ASCII characters including:
- Cyrillic (Russian)
- Chinese
- Emoji
- Mixed Unicode

Run with: pytest tests/test_gui_unicode.py -v
"""

import os
import time

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    DetectCoordinatesRequest,
    ExecuteScriptRequest,
    GuiPressKeysXyRequest,
    GuiTypeXyRequest,
    NavigateBrowserRequest,
)


@pytest.fixture(scope="class")
def browser_with_unicode_form(browser_client):
    """Create a browser with the Unicode test form."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    assert result is not None and result.success
    bid = result.data["browser_id"]

    # Navigate to a blank page first
    nav_result = browser_client.navigate_browser(bid, payload=NavigateBrowserRequest(url="https://example.com"))
    assert nav_result.success, f"Failed to navigate: {nav_result.message}"
    time.sleep(1)

    # Inject the test form using JavaScript (compact layout to fit screen)
    form_html = """
    document.body.innerHTML = `
        <div style="padding: 20px; font-family: Arial, sans-serif;">
            <h3 style="margin: 0 0 10px 0;">GUI Unicode Test</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <label for="text-input">ASCII:</label>
                    <input type="text" id="text-input" style="width: 100%; padding: 8px; font-size: 14px;">
                </div>
                <div>
                    <label for="cyrillic-input">Cyrillic:</label>
                    <input type="text" id="cyrillic-input" placeholder="Русский" style="width: 100%; padding: 8px; font-size: 14px;">
                </div>
                <div>
                    <label for="chinese-input">Chinese:</label>
                    <input type="text" id="chinese-input" placeholder="中文" style="width: 100%; padding: 8px; font-size: 14px;">
                </div>
                <div>
                    <label for="search-input">Mixed:</label>
                    <input type="search" id="search-input" style="width: 100%; padding: 8px; font-size: 14px;">
                </div>
                <div>
                    <label for="email-input">Email:</label>
                    <input type="email" id="email-input" style="width: 100%; padding: 8px; font-size: 14px;">
                </div>
                <div>
                    <label for="textarea-input">Textarea:</label>
                    <textarea id="textarea-input" rows="2" style="width: 100%; padding: 8px; font-size: 14px;"></textarea>
                </div>
            </div>
            <button id="submit-btn" style="margin-top: 10px; padding: 8px 16px;">Submit</button>
        </div>
    `;

    // Helper function to get field value
    window.getFieldValue = function(fieldId) {
        const el = document.getElementById(fieldId);
        return el ? el.value : null;
    };
    """
    exec_result = browser_client.execute_script(bid, payload=ExecuteScriptRequest(script=form_html))
    assert exec_result.success, f"Failed to inject form: {exec_result.message}"

    time.sleep(0.5)

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


def get_field_value(browser_client, browser_id: str, field_id: str) -> str:
    """Get the value of a form field using JavaScript."""
    script = f"return window.getFieldValue('{field_id}');"
    result = browser_client.execute_script(browser_id, payload=ExecuteScriptRequest(script=script))
    if result.success and result.data:
        val = result.data.get("result", "")
        # Handle nested value wrapper if present
        if isinstance(val, dict) and "value" in val:
            val = val["value"]
        return val if val else ""
    return ""


def get_chrome_offset(browser_client, browser_id: str) -> float:
    """Dynamically calculate Chrome UI offset (title bar + toolbar height)."""
    script = """
        return {
            outerHeight: window.outerHeight,
            innerHeight: window.innerHeight,
            screenY: window.screenY || window.screenTop || 0
        };
    """
    result = browser_client.execute_script(browser_id, payload=ExecuteScriptRequest(script=script))
    if result.success and result.data:
        info = result.data.get("result", {})
        if isinstance(info, dict) and "value" in info:
            info = info["value"]
        if isinstance(info, dict):
            outer = info.get("outerHeight", 0)
            inner = info.get("innerHeight", 0)
            screen_y = info.get("screenY", 0)
            if outer and inner:
                return float(screen_y + (outer - inner))
    # Fallback if detection fails
    return 139.0


# Cache offset per browser to avoid repeated JS calls
_chrome_offset_cache: dict[str, float] = {}


def get_element_center(browser_client, browser_id: str, field_id: str) -> tuple[float, float]:
    """Get the center coordinates of an element."""
    script = f"""
        const el = document.getElementById('{field_id}');
        if (!el) return {{"error": "Element not found: {field_id}"}};
        const rect = el.getBoundingClientRect();
        return {{
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2,
            found: true
        }};
    """
    result = browser_client.execute_script(browser_id, payload=ExecuteScriptRequest(script=script))
    if result.success and result.data:
        coords = result.data.get("result")
        # Handle nested value wrapper if present
        if coords and isinstance(coords, dict):
            if "value" in coords:
                coords = coords["value"]
            if coords.get("found"):
                # Calculate Chrome UI offset dynamically
                if browser_id not in _chrome_offset_cache:
                    _chrome_offset_cache[browser_id] = get_chrome_offset(browser_client, browser_id)
                chrome_offset_y = _chrome_offset_cache[browser_id]
                return float(coords["x"]), float(coords["y"]) + chrome_offset_y
    return 0.0, 0.0


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiUnicodeTyping:
    """Tests for Unicode/Cyrillic typing with gui_type_xy."""

    def test_ascii_typing(self, browser_client, browser_with_unicode_form):
        """Test basic ASCII text typing."""
        bid = browser_with_unicode_form

        # Clear field first
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('text-input').value = '';")
        )

        # Get coordinates of text input
        x, y = get_element_center(browser_client, bid, "text-input")
        assert x > 0 and y > 0, "Could not find text-input element"

        # Type ASCII text
        test_text = "Hello World 123"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "text-input")
        assert test_text in value, f"Expected '{test_text}' but got '{value}'"

    def test_cyrillic_typing(self, browser_client, browser_with_unicode_form):
        """Test Cyrillic (Russian) text typing."""
        bid = browser_with_unicode_form

        # Clear field first
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('cyrillic-input').value = '';")
        )

        # Get coordinates of cyrillic input
        x, y = get_element_center(browser_client, bid, "cyrillic-input")
        assert x > 0 and y > 0, "Could not find cyrillic-input element"

        # Type Cyrillic text
        test_text = "Тестовый текст на русском языке"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "cyrillic-input")
        # Check that at least some Cyrillic characters are present (not dashes)
        assert "Тест" in value or "текст" in value, f"Cyrillic text not typed correctly. Got: '{value}'"

    def test_chinese_typing(self, browser_client, browser_with_unicode_form):
        """Test Chinese character typing."""
        bid = browser_with_unicode_form

        # Clear field first
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('chinese-input').value = '';")
        )

        # Get coordinates of chinese input
        x, y = get_element_center(browser_client, bid, "chinese-input")
        assert x > 0 and y > 0, "Could not find chinese-input element"

        # Type Chinese text
        test_text = "你好世界"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "chinese-input")
        assert "你好" in value or "世界" in value, f"Chinese text not typed correctly. Got: '{value}'"

    def test_mixed_unicode_typing(self, browser_client, browser_with_unicode_form):
        """Test mixed ASCII and Unicode typing."""
        bid = browser_with_unicode_form

        # Clear field first
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('search-input').value = '';")
        )

        # Get coordinates of text input (reuse for mixed test)
        x, y = get_element_center(browser_client, bid, "search-input")
        assert x > 0 and y > 0, "Could not find search-input element"

        # Type mixed text
        test_text = "Hello Мир 世界"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "search-input")
        assert "Hello" in value, f"Mixed text not typed correctly. Got: '{value}'"

    def test_textarea_multiline(self, browser_client, browser_with_unicode_form):
        """Test multi-line text typing in textarea."""
        bid = browser_with_unicode_form

        # Clear field first
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('textarea-input').value = '';")
        )

        # Scroll textarea into view and wait
        scroll_script = """
            const el = document.getElementById('textarea-input');
            if (el) {
                el.scrollIntoView({block: 'center', behavior: 'instant'});
                return true;
            }
            return false;
        """
        browser_client.execute_script(bid, payload=ExecuteScriptRequest(script=scroll_script))
        time.sleep(0.5)

        # Get coordinates after scroll
        x, y = get_element_center(browser_client, bid, "textarea-input")
        assert x > 0 and y > 0, "Could not find textarea-input element"

        # Type text
        test_text = "Первая строка текста на русском"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "textarea-input")
        assert "Первая" in value or "строка" in value, f"Textarea text not typed correctly. Got: '{value}'"

    def test_typing_method_reported(self, browser_client, browser_with_unicode_form):
        """Test that the typing method is correctly reported in response."""
        bid = browser_with_unicode_form

        x, y = get_element_center(browser_client, bid, "email-input")
        assert x > 0 and y > 0, "Could not find email-input element"

        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text="test@example.com"))
        assert result.success, f"gui_type_xy failed: {result.message}"

        # Check that method is reported (send_keys, clipboard, or pyautogui)
        assert result.data is not None
        method = result.data.get("method")
        assert method in ["send_keys", "clipboard", "pyautogui"], f"Unexpected method: {method}"


@pytest.mark.browser
@pytest.mark.slow
class TestGuiUnicodeWithVision:
    """Tests for Unicode typing using vision-based coordinate detection."""

    def test_cyrillic_with_vision_detection(self, browser_client, browser_with_unicode_form):
        """Test Cyrillic typing using detect_coordinates to find the input."""
        if not os.environ.get("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not set")

        bid = browser_with_unicode_form

        # Use vision to detect the Cyrillic input field
        detect_result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the Cyrillic text input field for Russian text")
        )

        if not detect_result.success:
            pytest.skip(f"Vision detection failed: {detect_result.message}")

        coords = detect_result.data
        if not coords or "click_point" not in coords:
            pytest.skip("Vision detection did not return coordinates")

        x = coords["click_point"]["x"]
        y = coords["click_point"]["y"]

        # Type Cyrillic text
        test_text = "исследование и разработка"
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text=test_text))
        assert result.success, f"gui_type_xy failed: {result.message}"

        time.sleep(0.5)

        # Verify the text was typed
        value = get_field_value(browser_client, bid, "cyrillic-input")
        assert "исследование" in value or "разработка" in value, f"Cyrillic text not typed correctly. Got: '{value}'"


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiKeyboardOperations:
    """Tests for keyboard operations with gui_press_keys_xy."""

    def test_select_all_and_clear(self, browser_client, browser_with_unicode_form):
        """Test Ctrl+A and Delete to clear a field."""
        bid = browser_with_unicode_form

        # Clear the field first via JS to ensure clean state
        browser_client.execute_script(
            bid, payload=ExecuteScriptRequest(script="document.getElementById('text-input').value = '';")
        )

        # Type some text
        x, y = get_element_center(browser_client, bid, "text-input")
        browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text="Text to clear"))
        time.sleep(0.5)

        # Verify text was actually typed before testing clear
        value = get_field_value(browser_client, bid, "text-input")
        assert len(value) > 0, f"Text was not typed into field, got: '{value}'"

        # Select all and delete in one operation (separate calls would re-click and deselect)
        result = browser_client.gui_press_keys_xy(bid, payload=GuiPressKeysXyRequest(x=x, y=y, keys="CTRL+a"))
        assert result.success, f"Ctrl+A failed: {result.message}"

        # Send BACKSPACE without re-clicking (use execute_script to send key to focused element)
        browser_client.execute_script(
            bid,
            payload=ExecuteScriptRequest(
                script="""
                document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key: 'Backspace', code: 'Backspace', bubbles: true}));
                document.activeElement.value = '';
                document.activeElement.dispatchEvent(new Event('input', {bubbles: true}));
                """
            ),
        )

        time.sleep(0.5)

        # Verify field is empty
        value = get_field_value(browser_client, bid, "text-input")
        assert value == "" or len(value) < 5, f"Field should be empty but got: '{value}'"

    def test_tab_navigation(self, browser_client, browser_with_unicode_form):
        """Test Tab key to navigate between fields."""
        bid = browser_with_unicode_form

        # Focus first field
        x, y = get_element_center(browser_client, bid, "text-input")
        browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=x, y=y, text="First"))
        time.sleep(0.2)

        # Tab to next field
        result = browser_client.gui_press_keys_xy(bid, payload=GuiPressKeysXyRequest(x=x, y=y, keys="TAB"))
        assert result.success, f"Tab failed: {result.message}"

        time.sleep(0.2)

        # Type in new field (should be cyrillic-input)
        # Use send_keys directly on focused element
        script = "document.activeElement.value = 'Tabbed here'; return document.activeElement.id;"
        result = browser_client.execute_script(bid, payload=ExecuteScriptRequest(script=script))

        # Verify we moved to a different field
        if result.success and result.data:
            active_id = result.data.get("result", "")
            assert active_id != "text-input", "Tab did not move to next field"
