#!/usr/bin/env python3
"""
Test suite for GUI operations (gui_type_xy, gui_hover_xy, gui_click_xy).

Tests coordinate-based GUI automation using PyAutoGUI.

Run with: pytest tests/test_gui_operations.py -v
"""

import os
from types import SimpleNamespace

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    ExecuteScriptRequest,
    GuiClickRequest,
    GuiHoverXyRequest,
    GuiTypeXyRequest,
    NavigateBrowserRequest,
)
from pydantic import ValidationError


def result_to_dict(value):
    """Normalize generated-client models and dict payloads."""
    if value is None or isinstance(value, dict):
        return value
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if hasattr(value, "model_dump"):
        return value.model_dump(by_alias=True)
    return value


def execute_script_value(browser_client, browser_id, script: str):
    """Return the raw value from execute_script responses."""
    result = browser_client.execute_script(browser_id, payload=ExecuteScriptRequest(script=script))
    assert result is not None and result.success
    payload = result.data.get("result") if isinstance(result.data, dict) else None
    if isinstance(payload, dict):
        return payload.get("value")
    return payload


def screen_point_for_selector(browser_client, browser_id, selector: str, fx: float = 0.5, fy: float = 0.5):
    """Compute public screen coordinates for a selector before CDP mode is enabled."""
    value = execute_script_value(
        browser_client,
        browser_id,
        f"""
        const el = document.querySelector({selector!r});
        if (!el) return null;
        el.scrollIntoView({{block: 'center', inline: 'nearest'}});
        const rect = el.getBoundingClientRect();
        const vv = window.visualViewport || {{scale: 1, offsetLeft: 0, offsetTop: 0}};
        return {{
            x: window.screenX + (rect.left + rect.width * {fx} + (vv.offsetLeft || 0)) * (vv.scale || 1),
            y: window.screenY + (window.outerHeight - window.innerHeight)
                + (rect.top + rect.height * {fy} + (vv.offsetTop || 0)) * (vv.scale || 1),
        }};
        """,
    )
    assert value is not None, f"selector not found: {selector}"
    return float(value["x"]), float(value["y"])


class CapturingIPCClient:
    instances = []

    def __init__(self):
        self.calls = []
        type(self).instances.append(self)

    def execute_command(self, browser_id: str, command: str, **kwargs):
        self.calls.append((browser_id, command, kwargs))
        return {"status": "success", "message": "ok", "success": True}


@pytest.fixture
def browser_pool_adapter(monkeypatch):
    pytest.importorskip("flask")
    import airbrowser.server.services.browser_pool as browser_pool_module

    CapturingIPCClient.instances.clear()
    monkeypatch.setattr(browser_pool_module, "BrowserIPCClient", CapturingIPCClient)
    adapter = browser_pool_module.BrowserPoolAdapter(max_browsers=1)
    return adapter, CapturingIPCClient.instances[-1]


def has_vision_config() -> bool:
    """Check if AI vision is configured."""
    return all(os.environ.get(name) for name in ("VISION_API_BASE_URL", "VISION_API_KEY", "VISION_MODEL"))


def test_handle_gui_click_preserves_precheck_recommended_next_action(monkeypatch):
    pytest.importorskip("flask")
    import airbrowser.server.browser.commands.gui as gui_commands
    from airbrowser.server.browser.smart_targeting import Point

    monkeypatch.setattr(
        gui_commands,
        "resolve_click_target",
        lambda **kwargs: SimpleNamespace(
            success=False,
            outcome_status="click_failed_precheck",
            reason="hit_iframe_boundary",
            reason_detail="hit iframe boundary",
            recommended_next_action="switch_to_iframe_context",
            original_screen_point=Point(325, 403),
            original_viewport_point=Point(20, 20),
            resolved_screen_point=Point(325, 403),
            resolved_viewport_point=Point(20, 20),
            hit_test_result=None,
            snap_candidate=None,
        ),
    )

    result = gui_commands.handle_gui_click(
        object(),
        {"x": 325, "y": 403, "pre_click_validate": "strict", "auto_snap": "nearest_clickable"},
    )

    assert result["status"] == "success"
    assert result["success"] is False
    assert result["outcome_status"] == "click_failed_precheck"
    assert result["recommended_next_action"] == "switch_to_iframe_context"


def test_handle_gui_click_uses_click_failed_postcheck_when_snapshot_capture_fails(monkeypatch):
    pytest.importorskip("flask")
    import airbrowser.server.browser.commands.gui as gui_commands
    from airbrowser.server.browser.smart_targeting import Point

    monkeypatch.setattr(
        gui_commands,
        "resolve_click_target",
        lambda **kwargs: SimpleNamespace(
            success=True,
            outcome_status="clicked_exact",
            reason="hit_interactive_element",
            reason_detail=None,
            recommended_next_action="proceed",
            original_screen_point=Point(325, 403),
            original_viewport_point=Point(20, 20),
            resolved_screen_point=Point(325, 403),
            resolved_viewport_point=Point(20, 20),
            hit_test_result=None,
            snap_candidate=None,
        ),
    )
    monkeypatch.setattr(
        gui_commands,
        "capture_postclick_snapshot",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("snapshot failed")),
    )
    monkeypatch.setattr(gui_commands, "_gui_click_at", lambda *args, **kwargs: None)
    monkeypatch.setattr(gui_commands, "_ensure_cdp_mode", lambda *args, **kwargs: None)
    monkeypatch.setattr(gui_commands, "_bring_window_to_front", lambda *args, **kwargs: None)

    result = gui_commands.handle_gui_click(
        object(),
        {"x": 325, "y": 403, "post_click_feedback": "auto"},
    )

    assert result["status"] == "success"
    assert result["success"] is False
    assert result["outcome_status"] == "click_failed_postcheck"
    assert result["postcheck"]["status"] == "postcheck_unavailable"


def test_gui_click_unexpected_backend_fault_bubbles_up():
    pytest.importorskip("flask")
    from airbrowser.server.services.operations.gui import GuiOperations

    browser_pool = SimpleNamespace(
        execute_action=lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("browser service exploded"))
    )

    with pytest.raises(RuntimeError, match="browser service exploded"):
        GuiOperations(browser_pool).gui_click("browser-123", x=325, y=403)


def test_selector_hit_match_rejects_unrelated_overlapping_interactive_hit():
    pytest.importorskip("flask")
    import airbrowser.server.browser.commands.gui as gui_commands
    from airbrowser.server.browser.smart_targeting import HitTestResult, Point, Rect

    target = gui_commands.SelectorTarget(
        tag="BUTTON",
        text="Primary action",
        rect=Rect(0, 0, 100, 40),
        viewport_point=Point(50, 20),
        screen_point=Point(150, 120),
        element_path="HTML[0]>BODY[0]>DIV[0]>BUTTON[0]",
    )
    hit = HitTestResult(
        viewport_point=Point(50, 20),
        target_rect=Rect(40, 0, 100, 40),
        tag="A",
        text="Overlay link",
        interactive=True,
        reason="hit_interactive_element",
        reason_detail=None,
        element_path="HTML[0]>BODY[0]>A[0]",
    )

    assert gui_commands._selector_hit_matches(target, hit) is False


def test_browser_pool_gui_click_xy_forwards_smart_options_to_ipc(browser_pool_adapter):
    from airbrowser.server.models import BrowserAction

    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(
            action="gui_click_xy",
            options={
                "x": 325,
                "y": 403,
                "timeframe": 0.4,
                "pre_click_validate": "strict",
                "auto_snap": "nearest_clickable",
                "snap_radius": 96,
                "post_click_feedback": "auto",
                "post_click_timeout_ms": 1500,
                "return_content": True,
                "content_limit_chars": 800,
                "include_debug": True,
            },
        ),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "gui_click_xy",
        {
            "x": 325,
            "y": 403,
            "timeframe": 0.4,
            "pre_click_validate": "strict",
            "auto_snap": "nearest_clickable",
            "snap_radius": 96,
            "post_click_feedback": "auto",
            "post_click_timeout_ms": 1500,
            "return_content": True,
            "content_limit_chars": 800,
            "include_debug": True,
        },
    )


def test_browser_pool_gui_click_selector_forwards_smart_options_to_ipc(browser_pool_adapter):
    from airbrowser.server.models import BrowserAction

    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(
            action="gui_click",
            selector="#submit",
            options={
                "timeframe": 0.4,
                "fx": 0.2,
                "fy": 0.6,
                "pre_click_validate": "warn",
                "auto_snap": "off",
                "snap_radius": 96,
                "post_click_feedback": "visible",
                "post_click_timeout_ms": 750,
                "return_content": False,
                "content_limit_chars": 4000,
                "include_debug": True,
            },
        ),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "gui_click",
        {
            "selector": "#submit",
            "timeframe": 0.4,
            "fx": 0.2,
            "fy": 0.6,
            "pre_click_validate": "warn",
            "auto_snap": "off",
            "snap_radius": 96,
            "post_click_feedback": "visible",
            "post_click_timeout_ms": 750,
            "return_content": False,
            "content_limit_chars": 4000,
            "include_debug": True,
        },
    )


@pytest.fixture(scope="class")
def browser_with_form(browser_client):
    """Create a browser with a test form for GUI testing."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    if result is None or not result.success:
        message = None if result is None else result.message
        pytest.skip(f"Browser environment unavailable for GUI tests: {message}")
    bid = result.data["browser_id"]

    # Navigate to example.com
    navigate_result = browser_client.navigate_browser(bid, payload=NavigateBrowserRequest(url="https://example.com"))
    if navigate_result is None or not navigate_result.success:
        try:
            browser_client.close_browser(bid)
        except Exception:
            pass
        message = None if navigate_result is None else navigate_result.message
        pytest.skip(f"Browser navigation unavailable for GUI tests: {message}")

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
                    <div style="margin: 16px 0;">
                        <input id="terms-checkbox" type="checkbox">
                        <label id="terms-label" for="terms-checkbox" style="cursor: pointer; margin-left: 8px;">
                            Accept terms
                        </label>
                    </div>
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
    execute_result = browser_client.execute_script(bid, payload=exec_request)
    if execute_result is None or not execute_result.success:
        try:
            browser_client.close_browser(bid)
        except Exception:
            pass
        message = None if execute_result is None else execute_result.message
        pytest.skip(f"Browser scripting unavailable for GUI tests: {message}")

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiTypeXy:
    """Tests for gui_type_xy operation."""

    def test_gui_type_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_type_xy action is properly registered and executes."""
        bid = browser_with_form

        # Call the endpoint with valid coordinates
        # Even if the actual GUI operation fails (headless), the action should be recognized
        result = browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=500.0, y=300.0, text="test@example.com"))

        # The action should be recognized (not "Unknown action")
        # It may fail for other reasons in headless mode, but action routing works
        assert result is not None
        if not result.success:
            # Should NOT be "Unknown action" error - that means execute_action is missing the handler
            assert "Unknown action" not in str(result.message), "gui_type_xy action not registered in execute_action"

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
        with pytest.raises(ValidationError):
            browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=None, y=100.0, text="test"))

    def test_gui_type_xy_validation_missing_text(self, browser_client, browser_with_form):
        """Test that missing text fails validation."""
        bid = browser_with_form

        with pytest.raises(ValidationError):
            browser_client.gui_type_xy(bid, payload=GuiTypeXyRequest(x=100.0, y=100.0, text=None))


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiHoverXy:
    """Tests for gui_hover_xy operation."""

    def test_gui_hover_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_hover_xy action is properly registered and executes."""
        bid = browser_with_form

        result = browser_client.gui_hover_xy(bid, payload=GuiHoverXyRequest(x=500.0, y=300.0))

        assert result is not None
        if not result.success:
            # Should NOT be "Unknown action" error
            assert "Unknown action" not in str(result.message), "gui_hover_xy action not registered in execute_action"

    def test_gui_hover_xy_with_timeframe(self, browser_client, browser_with_form):
        """Test gui_hover_xy with custom timeframe parameter."""
        bid = browser_with_form

        result = browser_client.gui_hover_xy(bid, payload=GuiHoverXyRequest(x=500.0, y=300.0, timeframe=0.5))

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message)

    def test_gui_hover_xy_validation_missing_coords(self, browser_client, browser_with_form):
        """Test that missing coordinates fails validation."""
        bid = browser_with_form

        with pytest.raises(ValidationError):
            browser_client.gui_hover_xy(bid, payload=GuiHoverXyRequest(x=None, y=100.0))


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiClickXy:
    """Tests for gui_click_xy operation (via gui_click endpoint)."""

    def test_gui_click_xy_action_registered(self, browser_client, browser_with_form):
        """Test that gui_click with x,y coordinates works."""
        bid = browser_with_form

        result = browser_client.gui_click(bid, payload=GuiClickRequest(x=500.0, y=300.0))

        assert result is not None
        if not result.success:
            assert "Unknown action" not in str(result.message), "gui_click_xy action not registered in execute_action"

    def test_gui_click_reports_focus_changed(self, browser_client, browser_with_form):
        """Test that clicking an input reports focus_changed in auto postcheck mode."""
        bid = browser_with_form
        x, y = screen_point_for_selector(browser_client, bid, "#email-input", fx=0.25, fy=0.5)

        result = browser_client.gui_click(
            bid,
            payload=GuiClickRequest(
                x=x,
                y=y,
                pre_click_validate="strict",
                auto_snap="nearest_interactive",
                post_click_feedback="auto",
                post_click_timeout_ms=200,
            ),
        )

        assert result is not None
        assert result.success is True
        data = result_to_dict(result.data) or {}
        assert data.get("outcome_status") in {"clicked_exact", "clicked_snapped"}
        assert data.get("postcheck", {}).get("status") == "focus_changed"

    def test_gui_click_reports_visible_state_changed_for_checkbox(self, browser_client, browser_with_form):
        """Test that checkbox toggles produce visible_state_changed feedback."""
        bid = browser_with_form
        x, y = screen_point_for_selector(browser_client, bid, "#terms-checkbox")

        result = browser_client.gui_click(
            bid,
            payload=GuiClickRequest(
                x=x,
                y=y,
                pre_click_validate="strict",
                auto_snap="nearest_clickable",
                post_click_feedback="visible",
                post_click_timeout_ms=200,
            ),
        )

        assert result is not None
        assert result.success is True
        data = result_to_dict(result.data) or {}
        assert data.get("outcome_status") in {"clicked_exact", "clicked_snapped"}
        assert data.get("postcheck", {}).get("status") == "visible_state_changed"
        assert "checked" in (data.get("postcheck", {}).get("changed_fields") or [])

    def test_gui_click_reports_visible_state_changed_for_checkbox_label_surface(
        self, browser_client, browser_with_form
    ):
        """Test that label-surface clicks validate and toggle associated checkbox state."""
        bid = browser_with_form
        x, y = screen_point_for_selector(browser_client, bid, "#terms-label")

        result = browser_client.gui_click(
            bid,
            payload=GuiClickRequest(
                x=x,
                y=y,
                pre_click_validate="strict",
                auto_snap="off",
                post_click_feedback="visible",
                post_click_timeout_ms=200,
            ),
        )

        assert result is not None
        assert result.success is True
        data = result_to_dict(result.data) or {}
        assert data.get("outcome_status") == "clicked_exact"
        assert data.get("postcheck", {}).get("status") == "visible_state_changed"
        assert "checked" in (data.get("postcheck", {}).get("changed_fields") or [])


@pytest.mark.browser
@pytest.mark.isolated
class TestGuiOperationsIntegration:
    """Integration tests for GUI operations with vision."""

    @pytest.mark.slow
    def test_detect_coordinates_with_gui_click(self, browser_client, browser_with_form):
        """Test the vision + GUI workflow: detect_coordinates -> gui_click_xy."""
        bid = browser_with_form

        if not has_vision_config():
            pytest.skip("Vision config not set")

        from airbrowser_client.models import DetectCoordinatesRequest

        result = browser_client.detect_coordinates(bid, payload=DetectCoordinatesRequest(prompt="the Submit button"))

        if result.success:
            coords = result.data
            assert "x" in str(coords) or "click_point" in str(coords)

    @pytest.mark.slow
    def test_detect_coordinates_with_gui_type(self, browser_client, browser_with_form):
        """Test the vision + GUI workflow: detect_coordinates -> gui_type_xy."""
        bid = browser_with_form

        if not has_vision_config():
            pytest.skip("Vision config not set")

        from airbrowser_client.models import DetectCoordinatesRequest

        result = browser_client.detect_coordinates(
            bid, payload=DetectCoordinatesRequest(prompt="the email input field")
        )

        if result.success:
            coords = result.data
            assert "x" in str(coords) or "click_point" in str(coords)
