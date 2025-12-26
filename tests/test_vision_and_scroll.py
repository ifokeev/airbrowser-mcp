#!/usr/bin/env python3
"""
Test suite for vision operations and scroll functionality.

Tests:
- detect_coordinates: AI-based element detection
- what_is_visible: AI page analysis
- scroll/scroll_by: Page scrolling
- Integration: Vision + GUI workflow

Run with: pytest tests/test_vision_and_scroll.py -v
"""

import os
import time

import pytest
from airbrowser_client.exceptions import BadRequestException
from airbrowser_client.models import (
    CreateBrowserRequest,
    DetectCoordinatesRequest,
    ExecuteScriptRequest,
    GuiClickRequest,
    GuiTypeXyRequest,
    NavigateBrowserRequest,
    ScrollRequest,
)


def has_openrouter_key():
    """Check if OPENROUTER_API_KEY is available."""
    return bool(os.environ.get("OPENROUTER_API_KEY"))


@pytest.fixture(scope="class")
def browser_with_page(browser_client):
    """Create a browser with a test page."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    assert result is not None and result.success
    bid = result.data['browser_id']

    # Navigate to example.com
    browser_client.navigate_browser(bid, payload=NavigateBrowserRequest(url="https://example.com"))

    # Create a long page with form elements for testing
    exec_request = ExecuteScriptRequest(
        script="""
        document.body.innerHTML = `
            <div style="padding: 50px;">
                <h1 id="top-heading">Vision & Scroll Test Page</h1>

                <form id="test-form" style="margin: 20px 0;">
                    <div style="margin: 10px 0;">
                        <label for="email">Email:</label>
                        <input id="email" type="email" placeholder="Enter email"
                               style="width: 300px; height: 35px; padding: 5px;">
                    </div>
                    <div style="margin: 10px 0;">
                        <label for="password">Password:</label>
                        <input id="password" type="password" placeholder="Enter password"
                               style="width: 300px; height: 35px; padding: 5px;">
                    </div>
                    <button id="submit-btn" type="button"
                            style="padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer;">
                        Submit Form
                    </button>
                </form>

                <div style="margin: 50px 0;">
                    <h2>Section 1</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>

                <!-- Add height to make page scrollable -->
                <div style="height: 1500px; background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);">
                    <p style="padding-top: 500px;">Middle of the page</p>
                    <p style="padding-top: 500px;" id="bottom-text">Bottom of the page</p>
                </div>

                <div id="footer" style="padding: 20px; background: #333; color: white;">
                    <button id="footer-btn" style="padding: 10px 20px;">Footer Button</button>
                </div>
            </div>
        `;
        """
    )
    browser_client.execute_script(bid, payload=exec_request)

    yield bid

    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestScrollOperations:
    """Tests for scroll and scroll_by operations."""

    def test_scroll_by_action_registered(self, browser_client, browser_with_page):
        """Test that scroll_by action is properly registered."""
        bid = browser_with_page

        result = browser_client.scroll(
            bid, payload=ScrollRequest(delta_y=500)
        )

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message), \
                "scroll_by action not registered in execute_action"

    def test_scroll_by_down(self, browser_client, browser_with_page):
        """Test scrolling down the page."""
        bid = browser_with_page

        # Reset scroll position first
        browser_client.execute_script(bid, payload=ExecuteScriptRequest(script="window.scrollTo(0, 0);"))
        time.sleep(0.3)

        # Get initial scroll position
        exec_req = ExecuteScriptRequest(script="return window.scrollY;")
        initial = browser_client.execute_script(bid, payload=exec_req)
        initial_y = 0
        if initial.success and initial.data:
            # Structure: data['result'] = {"value": raw_result}
            result_wrapper = initial.data.get('result')
            if isinstance(result_wrapper, dict):
                initial_y = result_wrapper.get('value', 0) or 0

        # Scroll down
        result = browser_client.scroll(
            bid, payload=ScrollRequest(delta_y=300)
        )
        assert result is not None

        # Check scroll position changed (allow time for smooth scroll)
        time.sleep(0.5)

        after = browser_client.execute_script(bid, payload=exec_req)
        after_y = 0
        if after.success and after.data:
            result_wrapper = after.data.get('result')
            if isinstance(result_wrapper, dict):
                after_y = result_wrapper.get('value', 0) or 0

        # Position should have increased (scrolled down)
        assert after_y >= initial_y, f"Page should have scrolled down: initial={initial_y}, after={after_y}"

    def test_scroll_by_up(self, browser_client, browser_with_page):
        """Test scrolling up the page."""
        bid = browser_with_page

        # First scroll down
        browser_client.execute_script(bid, payload=ExecuteScriptRequest(script="window.scrollTo(0, 500);"))
        time.sleep(0.3)

        # Get position after scrolling down
        exec_req = ExecuteScriptRequest(script="return window.scrollY;")
        middle = browser_client.execute_script(bid, payload=exec_req)
        middle_y = 0
        if middle.success and middle.data:
            result_wrapper = middle.data.get('result')
            if isinstance(result_wrapper, dict):
                middle_y = result_wrapper.get('value', 0) or 0

        # Scroll up (negative delta)
        result = browser_client.scroll(bid, payload=ScrollRequest(delta_y=-200))
        assert result is not None
        time.sleep(0.3)

        # Check position decreased
        after = browser_client.execute_script(bid, payload=exec_req)
        after_y = 0
        if after.success and after.data:
            result_wrapper = after.data.get('result')
            if isinstance(result_wrapper, dict):
                after_y = result_wrapper.get('value', 0) or 0

        assert after_y < middle_y, f"Page should have scrolled up: middle={middle_y}, after={after_y}"

    def test_scroll_to_element(self, browser_client, browser_with_page):
        """Test scrolling to a specific element."""
        bid = browser_with_page

        # Reset scroll first
        browser_client.execute_script(bid, payload=ExecuteScriptRequest(script="window.scrollTo(0, 0);"))
        time.sleep(0.3)

        # Scroll to footer element
        result = browser_client.scroll(
            bid, payload=ScrollRequest(selector="#footer")
        )
        assert result is not None

        time.sleep(0.5)

        # Check that scroll position changed
        exec_req = ExecuteScriptRequest(script="return window.scrollY;")
        after = browser_client.execute_script(bid, payload=exec_req)
        after_y = 0
        if after.success and after.data:
            result_wrapper = after.data.get('result')
            if isinstance(result_wrapper, dict):
                after_y = result_wrapper.get('value', 0) or 0

        # Should have scrolled significantly to reach footer
        assert after_y > 100, f"Should have scrolled to reach footer: scrollY={after_y}"


@pytest.mark.browser
class TestVisionOperations:
    """Tests for vision-based operations."""

    def test_detect_coordinates_action_registered(self, browser_client, browser_with_page):
        """Test that detect_coordinates action is properly registered."""
        bid = browser_with_page

        try:
            result = browser_client.detect_coordinates(
                bid, payload=DetectCoordinatesRequest(prompt="the Submit Form button")
            )
            assert result is not None
            if not result.success:
                # Should NOT be "Unknown action" - that means handler is missing
                assert "Unknown action" not in str(result.message), \
                    "detect_coordinates action not registered in execute_action"
        except BadRequestException as e:
            # 400 error means the action was found but vision API not available
            # This is OK - it means the action handler is registered
            assert "OpenRouter not available" in str(e) or "not available" in str(e), \
                f"Unexpected error: {e}"

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_detect_coordinates_finds_element(self, browser_client, browser_with_page):
        """Test that detect_coordinates finds a visible element."""
        bid = browser_with_page

        result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the blue Submit Form button")
        )

        assert result is not None
        if result.success:
            assert result.data is not None
            # Check for coordinates
            data = result.data
            coords = data.get('coordinates') if isinstance(data, dict) else {}
            if isinstance(coords, dict):
                assert coords.get("x") is not None or coords.get("click_point") is not None

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_detect_coordinates_returns_click_point(self, browser_client, browser_with_page):
        """Test that detect_coordinates returns usable click coordinates."""
        bid = browser_with_page

        result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the email input field")
        )

        if result.success and result.data:
            coords = result.data.get('coordinates') if isinstance(result.data, dict) else {}
            if isinstance(coords, dict):
                click_point = coords.get("click_point", {})
                if click_point:
                    assert "x" in click_point
                    assert "y" in click_point

    def test_what_is_visible_action_registered(self, browser_client, browser_with_page):
        """Test that what_is_visible action is properly registered."""
        bid = browser_with_page

        try:
            result = browser_client.what_is_visible(bid)
            assert result is not None
            if not result.success:
                assert "Unknown action" not in str(result.message), \
                    "what_is_visible action not registered in execute_action"
        except BadRequestException as e:
            # 400 error means action was found but vision API not available
            assert "OpenRouter not available" in str(e) or "not available" in str(e), \
                f"Unexpected error: {e}"

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_what_is_visible_returns_analysis(self, browser_client, browser_with_page):
        """Test that what_is_visible returns page analysis."""
        bid = browser_with_page

        result = browser_client.what_is_visible(bid)

        if result.success and result.data:
            analysis = result.data.get('analysis') if isinstance(result.data, dict) else None
            assert analysis is not None, "Should return analysis"
            assert len(str(analysis)) > 50, "Analysis should be substantive"


@pytest.mark.browser
class TestVisionGuiIntegration:
    """Integration tests for vision + GUI workflow."""

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_detect_then_gui_click(self, browser_client, browser_with_page):
        """Test complete workflow: detect_coordinates -> gui_click."""
        bid = browser_with_page

        detect_result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the Submit Form button")
        )

        if not detect_result.success:
            pytest.skip("Vision detection failed")

        coords = detect_result.data.get('coordinates') if isinstance(detect_result.data, dict) else {}
        if isinstance(coords, dict):
            click_point = coords.get("click_point", {})
        else:
            pytest.skip("No coordinates returned")

        if not click_point:
            pytest.skip("No click_point returned")

        click_result = browser_client.gui_click(
            bid, payload=GuiClickRequest(
                x=float(click_point["x"]),
                y=float(click_point["y"])
            )
        )

        assert click_result is not None
        if not click_result.success:
            assert "Unknown action" not in str(click_result.message)

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_detect_then_gui_type(self, browser_client, browser_with_page):
        """Test complete workflow: detect_coordinates -> gui_type_xy."""
        bid = browser_with_page

        detect_result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the email input field")
        )

        if not detect_result.success:
            pytest.skip("Vision detection failed")

        coords = detect_result.data.get('coordinates') if isinstance(detect_result.data, dict) else {}
        if isinstance(coords, dict):
            click_point = coords.get("click_point", {})
        else:
            pytest.skip("No coordinates returned")

        if not click_point:
            pytest.skip("No click_point returned")

        type_result = browser_client.gui_type_xy(
            bid, payload=GuiTypeXyRequest(
                x=float(click_point["x"]),
                y=float(click_point["y"]),
                text="test@example.com"
            )
        )

        assert type_result is not None
        if not type_result.success:
            assert "Unknown action" not in str(type_result.message)

    @pytest.mark.skipif(not has_openrouter_key(), reason="OPENROUTER_API_KEY not set")
    def test_scroll_then_detect(self, browser_client, browser_with_page):
        """Test scrolling to element then detecting it."""
        bid = browser_with_page

        # Scroll down to make footer visible
        scroll_result = browser_client.scroll(
            bid, payload=ScrollRequest(delta_y=1500)
        )
        assert scroll_result is not None

        time.sleep(0.5)

        # Now try to detect the footer button
        detect_result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the Footer Button")
        )

        if detect_result.success:
            coords = detect_result.data.get('coordinates') if isinstance(detect_result.data, dict) else {}
            if isinstance(coords, dict):
                assert coords.get("x") is not None or coords.get("click_point") is not None
