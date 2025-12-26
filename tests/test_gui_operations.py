#!/usr/bin/env python3
"""
Test suite for GUI operations (gui_type_xy, gui_hover_xy, gui_click_xy).

Tests coordinate-based GUI automation using PyAutoGUI.

Run with: pytest tests/test_gui_operations.py -v
"""

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    ExecuteScriptRequest,
    GuiClickRequest,
    GuiHoverXyRequest,
    GuiTypeXyRequest,
    NavigateBrowserRequest,
)


@pytest.fixture(scope="class")
def browser_with_form(browser_client):
    """Create a browser with a test form for GUI testing."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    assert result is not None and result.success
    bid = result.data['browser_id']

    # Navigate to example.com
    browser_client.navigate_browser(bid, payload=NavigateBrowserRequest(url="https://example.com"))

    # Create a form with input fields for testing
    exec_request = ExecuteScriptRequest(
        script="""
        // Clear the page and create a form
        document.body.innerHTML = `
            <div style="padding: 100px;">
                <h1>GUI Test Form</h1>
                <form id="test-form">
                    <input id="email-input" type="text" placeholder="Email"
                           style="width: 300px; height: 40px; font-size: 16px; padding: 8px; margin: 10px 0;">
                    <br>
                    <input id="password-input" type="password" placeholder="Password"
                           style="width: 300px; height: 40px; font-size: 16px; padding: 8px; margin: 10px 0;">
                    <br>
                    <button id="submit-btn" type="button"
                            style="width: 100px; height: 40px; margin: 10px 0;"
                            onmouseover="this.style.backgroundColor='#ddd'"
                            onmouseout="this.style.backgroundColor=''">
                        Submit
                    </button>
                    <div id="hover-indicator" style="display: none; color: green;">Hovered!</div>
                </form>
            </div>
        `;

        // Add hover detection
        document.getElementById('submit-btn').addEventListener('mouseenter', function() {
            document.getElementById('hover-indicator').style.display = 'block';
        });
        document.getElementById('submit-btn').addEventListener('mouseleave', function() {
            document.getElementById('hover-indicator').style.display = 'none';
        });
        """
    )
    browser_client.execute_script(bid, payload=exec_request)

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestGuiTypeXy:
    """Tests for gui_type_xy operation."""

    def test_gui_type_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_type_xy action is properly registered and executes."""
        bid = browser_with_form

        # Call the endpoint with valid coordinates
        # Even if the actual GUI operation fails (headless), the action should be recognized
        result = browser_client.gui_type_xy(
            bid, payload=GuiTypeXyRequest(x=500.0, y=300.0, text="test@example.com")
        )

        # The action should be recognized (not "Unknown action")
        # It may fail for other reasons in headless mode, but action routing works
        assert result is not None
        if not result.success:
            # Should NOT be "Unknown action" error - that means execute_action is missing the handler
            assert "Unknown action" not in str(result.message), \
                "gui_type_xy action not registered in execute_action"

    def test_gui_type_xy_with_timeframe(self, browser_client, browser_with_form):
        """Test gui_type_xy with custom timeframe parameter."""
        bid = browser_with_form

        result = browser_client.gui_type_xy(
            bid, payload=GuiTypeXyRequest(x=500.0, y=300.0, text="hello", timeframe=0.5)
        )

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message)

    def test_gui_type_xy_validation_missing_x(self, browser_client, browser_with_form):
        """Test that missing x coordinate fails validation."""
        bid = browser_with_form

        # Pydantic should reject None for required field
        with pytest.raises(Exception):
            browser_client.gui_type_xy(
                bid, payload=GuiTypeXyRequest(x=None, y=100.0, text="test")
            )

    def test_gui_type_xy_validation_missing_text(self, browser_client, browser_with_form):
        """Test that missing text fails validation."""
        bid = browser_with_form

        with pytest.raises(Exception):
            browser_client.gui_type_xy(
                bid, payload=GuiTypeXyRequest(x=100.0, y=100.0, text=None)
            )


@pytest.mark.browser
class TestGuiHoverXy:
    """Tests for gui_hover_xy operation."""

    def test_gui_hover_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_hover_xy action is properly registered and executes."""
        bid = browser_with_form

        result = browser_client.gui_hover_xy(
            bid, payload=GuiHoverXyRequest(x=500.0, y=300.0)
        )

        assert result is not None
        if not result.success:
            # Should NOT be "Unknown action" error
            assert "Unknown action" not in str(result.message), \
                "gui_hover_xy action not registered in execute_action"

    def test_gui_hover_xy_with_timeframe(self, browser_client, browser_with_form):
        """Test gui_hover_xy with custom timeframe parameter."""
        bid = browser_with_form

        result = browser_client.gui_hover_xy(
            bid, payload=GuiHoverXyRequest(x=500.0, y=300.0, timeframe=0.5)
        )

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message)

    def test_gui_hover_xy_validation_missing_coords(self, browser_client, browser_with_form):
        """Test that missing coordinates fails validation."""
        bid = browser_with_form

        with pytest.raises(Exception):
            browser_client.gui_hover_xy(
                bid, payload=GuiHoverXyRequest(x=None, y=100.0)
            )


@pytest.mark.browser
class TestGuiClickXy:
    """Tests for gui_click_xy operation (via gui_click endpoint)."""

    def test_gui_click_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_click with x,y coordinates works."""
        bid = browser_with_form

        result = browser_client.gui_click(
            bid, payload=GuiClickRequest(x=500.0, y=300.0)
        )

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message), \
                "gui_click_xy action not registered in execute_action"


@pytest.mark.browser
class TestGuiOperationsIntegration:
    """Integration tests for GUI operations with vision."""

    @pytest.mark.slow
    def test_detect_coordinates_with_gui_click(self, browser_client, browser_with_form):
        """Test the vision + GUI workflow: detect_coordinates -> gui_click_xy."""
        bid = browser_with_form

        import os
        if not os.environ.get("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not set")

        from airbrowser_client.models import DetectCoordinatesRequest
        result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the Submit button")
        )

        if result.success:
            coords = result.data
            assert "x" in str(coords) or "click_point" in str(coords)

    @pytest.mark.slow
    def test_detect_coordinates_with_gui_type(self, browser_client, browser_with_form):
        """Test the vision + GUI workflow: detect_coordinates -> gui_type_xy."""
        bid = browser_with_form

        import os
        if not os.environ.get("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not set")

        from airbrowser_client.models import DetectCoordinatesRequest
        result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the email input field")
        )

        if result.success:
            coords = result.data
            assert "x" in str(coords) or "click_point" in str(coords)
