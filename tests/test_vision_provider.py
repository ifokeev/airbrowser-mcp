import asyncio
import os
from pathlib import Path

import pytest
from flask import Flask
from flask_restx import Api

import airbrowser.server.app as app_module
import airbrowser.server.browser.commands.vision as vision_commands
import airbrowser.server.services.browser_pool as browser_pool_module
from airbrowser.server.mcp.integration import MCPIntegration
from airbrowser.server.mcp.tool_descriptions import TOOL_DESCRIPTIONS
from airbrowser.server.models import ActionResult, BrowserAction
from airbrowser.server.schemas.browser import register_browser_schemas
from airbrowser.server.schemas.responses import register_response_schemas
from airbrowser.server.services.operations.page import PageOperations
from airbrowser.server.services.operations.pool import PoolOperations
from airbrowser.server.services.operations.vision import VisionOperations
from airbrowser.server.vision.config import (
    VisionSettings,
    load_vision_settings,
    resolve_vision_stream,
    vision_is_enabled,
)
from airbrowser.server.vision.openai_compatible import OpenAICompatibleVisionClient


class FakePool:
    max_browsers = 1

    def get_status(self):
        return {"healthy": True, "active_browsers": 0, "total_browsers": 0, "available_browsers": 0}


class FakeBrowserOperations:
    def create_browser(self):
        return {}

    def detect_coordinates(self, browser_id: str, prompt: str):
        return {}

    def what_is_visible(self, browser_id: str):
        return {}


class CapturingBrowserPool:
    instances = []

    def __init__(self, max_browsers: int = 50):
        self.max_browsers = max_browsers
        self.actions = []
        self.override_result = None
        type(self).instances.append(self)

    def execute_action(self, browser_id: str, action):
        self.actions.append((browser_id, action))

        if self.override_result is not None:
            return self.override_result

        if action.action == "detect_coordinates":
            return ActionResult(
                success=True,
                message="Found: submit",
                data={
                    "coordinates": {
                        "x": 10,
                        "y": 20,
                        "width": 30,
                        "height": 40,
                        "confidence": 0.9,
                        "click_point": {"x": 25, "y": 40},
                        "resolved_click_point": {"x": 24, "y": 35},
                        "outcome_status": "snapped_match",
                        "reason": "hit_html_root",
                        "reason_detail": "hit non-interactive root element",
                        "resolved_target": {
                            "point": {"x": 24, "y": 35},
                            "element": {"tag": "A", "text": "Submit", "interactive": True},
                        },
                        "snap_result": {
                            "applied": True,
                            "strategy": "nearest_clickable",
                            "distance_px": 18,
                            "snapped_point": {"x": 24, "y": 35},
                        },
                        "recommended_next_action": "proceed",
                        "image_size": {"width": 100, "height": 80},
                        "transform_info": {"scale": {"x": 1.0, "y": 1.0}},
                        "screenshot_url": "http://shot",
                    }
                },
            )

        if action.action == "what_is_visible":
            return ActionResult(
                success=True,
                message="Page analyzed",
                data={
                    "analysis": "Visible analysis",
                    "model": action.options.get("model"),
                    "screenshot_url": "http://shot",
                    "timestamp": 123.4,
                },
            )

        raise AssertionError(f"Unexpected action: {action.action}")


class CapturingIPCClient:
    instances = []

    def __init__(self):
        self.calls = []
        type(self).instances.append(self)

    def execute_command(self, browser_id: str, command: str, **kwargs):
        self.calls.append((browser_id, command, kwargs))

        if command == "screenshot":
            return {
                "status": "success",
                "url": "http://localhost:18080/screenshots/example.png",
                "path": "/app/screenshots/example.png",
                "filename": "example.png",
            }

        if command == "detect_coordinates":
            return {
                "status": "success",
                "message": "Found: submit",
                "coordinates": {"x": 1, "y": 2, "width": 3, "height": 4},
            }

        if command == "what_is_visible":
            return {
                "status": "success",
                "message": "Page analyzed",
                "analysis": "Visible analysis",
                "model": kwargs.get("model"),
            }

        raise AssertionError(f"Unexpected command: {command}")


class StaticBrowserPool:
    def __init__(self, result: ActionResult):
        self.result = result
        self.actions = []

    def execute_action(self, browser_id: str, action):
        self.actions.append((browser_id, action))
        return self.result


@pytest.fixture
def browser_route_client(monkeypatch):
    CapturingBrowserPool.instances.clear()
    monkeypatch.setenv("ENABLE_MCP", "false")
    monkeypatch.setattr(app_module, "BrowserPoolAdapter", CapturingBrowserPool)

    app, _ = app_module.create_app()
    app.testing = True
    return app.test_client(), CapturingBrowserPool.instances[-1]


@pytest.fixture
def browser_pool_adapter(monkeypatch):
    CapturingIPCClient.instances.clear()
    monkeypatch.setattr(browser_pool_module, "BrowserIPCClient", CapturingIPCClient)
    adapter = browser_pool_module.BrowserPoolAdapter(max_browsers=1)
    return adapter, CapturingIPCClient.instances[-1]


def _set_vision_env(monkeypatch, *, stream_default: str | None = None):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")
    if stream_default is None:
        monkeypatch.delenv("VISION_STREAM_DEFAULT", raising=False)
    else:
        monkeypatch.setenv("VISION_STREAM_DEFAULT", stream_default)


def _make_detect_resolution():
    return type(
        "Resolution",
        (),
        {
            "success": True,
            "outcome_status": "raw_vision_point",
            "reason": "raw_vision_point",
            "reason_detail": None,
            "recommended_next_action": "proceed",
            "resolved_screen_point": vision_commands.Point(17.0, 25.0),
            "snap_candidate": None,
            "hit_test_result": None,
            "original_viewport_point": None,
            "resolved_viewport_point": None,
            "original_screen_point": None,
        },
    )()


def test_load_vision_settings_reads_generic_env(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")

    settings = load_vision_settings()

    assert settings is not None
    assert settings.base_url == "https://cliproxy.ldc-fe.org/v1"
    assert settings.api_key == "test-key"
    assert settings.model == "rightcode/gpt-5.4"
    assert vision_is_enabled() is True


def test_load_vision_settings_reads_stream_default_true(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")
    monkeypatch.setenv("VISION_STREAM_DEFAULT", "true")

    settings = load_vision_settings()

    assert settings is not None
    assert settings.stream_default is True


def test_load_vision_settings_reads_stream_default_false(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")
    monkeypatch.setenv("VISION_STREAM_DEFAULT", "off")

    settings = load_vision_settings()

    assert settings is not None
    assert settings.stream_default is False


def test_load_vision_settings_uses_false_when_stream_default_is_unset(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")
    monkeypatch.delenv("VISION_STREAM_DEFAULT", raising=False)

    settings = load_vision_settings()

    assert settings is not None
    assert settings.stream_default is False


def test_load_vision_settings_invalid_stream_default_logs_warning(monkeypatch, caplog):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")
    monkeypatch.setenv("VISION_STREAM_DEFAULT", "sometimes")
    caplog.set_level("WARNING")

    settings = load_vision_settings()

    assert settings is not None
    assert settings.stream_default is False
    assert "VISION_STREAM_DEFAULT" in caplog.text


def test_resolve_vision_stream_prefers_request_value():
    settings = VisionSettings(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
        stream_default=False,
    )

    assert resolve_vision_stream(True, settings) is True


def test_resolve_vision_stream_allows_request_false_to_override_true_default():
    settings = VisionSettings(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
        stream_default=True,
    )

    assert resolve_vision_stream(False, settings) is False


def test_resolve_vision_stream_uses_settings_default_when_request_omitted():
    settings = VisionSettings(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
        stream_default=True,
    )

    assert resolve_vision_stream(None, settings) is True


@pytest.mark.parametrize("missing_env", ["VISION_API_BASE_URL", "VISION_API_KEY", "VISION_MODEL"])
def test_vision_is_disabled_when_any_required_env_is_missing(monkeypatch, missing_env):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")
    monkeypatch.delenv(missing_env, raising=False)

    assert load_vision_settings() is None
    assert vision_is_enabled() is False


def test_health_check_reports_generic_vision_enablement(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "rightcode/gpt-5.4")

    result = PoolOperations(browser_pool=FakePool()).health_check()

    assert result["data"]["vision_enabled"] is True


def test_mcp_integration_skips_vision_tools_without_generic_config(monkeypatch):
    monkeypatch.setenv("UNUSED_VISION_API_KEY", "unused-value")
    monkeypatch.delenv("VISION_API_BASE_URL", raising=False)
    monkeypatch.delenv("VISION_API_KEY", raising=False)
    monkeypatch.delenv("VISION_MODEL", raising=False)
    monkeypatch.delenv("MCP_INCLUDE_ALL_TOOLS", raising=False)

    integration = MCPIntegration(browser_ops=FakeBrowserOperations())
    tool_names = {tool.name for tool in asyncio.run(integration.mcp.list_tools())}

    assert "what_is_visible" not in tool_names
    assert "detect_coordinates" not in tool_names


def test_tool_descriptions_are_provider_agnostic():
    assert "If AI vision is configured" in TOOL_DESCRIPTIONS["take_screenshot"]
    assert "If AI vision is configured" in TOOL_DESCRIPTIONS["click"]


def test_openai_compatible_client_preserves_model_name_with_slash(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            captured["base_url"] = base_url
            captured["api_key"] = api_key

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    assert client.model == "rightcode/gpt-5.4"
    assert captured == {"base_url": "https://cliproxy.ldc-fe.org/v1", "api_key": "test-key"}


def test_openai_compatible_client_returns_error_when_image_missing(tmp_path):
    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(tmp_path / "missing.png"), "describe it")

    assert result["success"] is False
    assert "not found" in result["error"].lower()


def test_openai_compatible_client_returns_error_for_malformed_response(monkeypatch, tmp_path):
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            self.chat = type(
                "Chat",
                (),
                {
                    "completions": type(
                        "Completions",
                        (),
                        {"create": staticmethod(lambda **kwargs: type("Response", (), {"choices": []})())},
                    )()
                },
            )()

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(image_path), "describe it")

    assert result["success"] is False
    assert "malformed" in result["error"].lower()


def _make_stream_chunk(
    *, content=None, include_choices=True, include_delta=True, missing_choices=False, missing_delta=False
):
    if missing_choices:
        return type("Chunk", (), {})()

    if not include_choices:
        return type("Chunk", (), {"choices": []})()

    if missing_delta:
        choice = type("Choice", (), {})()
    else:
        delta = None if not include_delta else type("Delta", (), {"content": content})()
        choice = type("Choice", (), {"delta": delta})()

    return type("Chunk", (), {"choices": [choice]})()


def test_openai_compatible_client_uses_non_streaming_chat_completion(monkeypatch, tmp_path):
    captured = {}
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            self.chat = type(
                "Chat",
                (),
                {
                    "completions": type(
                        "Completions",
                        (),
                        {
                            "create": staticmethod(
                                lambda **kwargs: (
                                    captured.update(kwargs)
                                    or type(
                                        "Response",
                                        (),
                                        {
                                            "choices": [
                                                type(
                                                    "Choice",
                                                    (),
                                                    {"message": type("Message", (), {"content": "visible analysis"})()},
                                                )()
                                            ]
                                        },
                                    )()
                                )
                            )
                        },
                    )()
                },
            )()

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(image_path), "describe it", stream=False)

    assert result == {"success": True, "explanation": "visible analysis", "model": "rightcode/gpt-5.4"}
    assert captured.get("stream") is False


def test_openai_compatible_client_assembles_streamed_text(monkeypatch, tmp_path):
    captured = {}
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            self.chat = type(
                "Chat",
                (),
                {
                    "completions": type(
                        "Completions",
                        (),
                        {
                            "create": staticmethod(
                                lambda **kwargs: (
                                    captured.update(kwargs)
                                    or iter(
                                        [
                                            _make_stream_chunk(content="visible"),
                                            _make_stream_chunk(content=None),
                                            _make_stream_chunk(content=" analysis"),
                                            _make_stream_chunk(include_delta=False),
                                            _make_stream_chunk(missing_delta=True),
                                            _make_stream_chunk(include_choices=False),
                                            _make_stream_chunk(missing_choices=True),
                                            _make_stream_chunk(content=""),
                                        ]
                                    )
                                )
                            )
                        },
                    )()
                },
            )()

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(image_path), "describe it", stream=True)

    assert result == {"success": True, "explanation": "visible analysis", "model": "rightcode/gpt-5.4"}
    assert captured.get("stream") is True


def test_openai_compatible_client_returns_error_for_empty_stream(monkeypatch, tmp_path):
    captured = {}
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            self.chat = type(
                "Chat",
                (),
                {
                    "completions": type(
                        "Completions",
                        (),
                        {
                            "create": staticmethod(
                                lambda **kwargs: (
                                    captured.update(kwargs)
                                    or iter(
                                        [
                                            _make_stream_chunk(content=None),
                                            _make_stream_chunk(include_delta=False),
                                            _make_stream_chunk(include_choices=False),
                                            _make_stream_chunk(content=""),
                                        ]
                                    )
                                )
                            )
                        },
                    )()
                },
            )()

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(image_path), "describe it", stream=True)

    assert result["success"] is False
    assert captured.get("stream") is True
    assert any(term in result["error"].lower() for term in ("empty", "no text"))


def test_openai_compatible_client_returns_error_when_stream_iteration_fails(monkeypatch, tmp_path):
    captured = {}
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    def failing_stream():
        yield _make_stream_chunk(content="visible")
        raise RuntimeError("stream interrupted")

    class FakeOpenAI:
        def __init__(self, *, base_url, api_key):
            self.chat = type(
                "Chat",
                (),
                {
                    "completions": type(
                        "Completions",
                        (),
                        {"create": staticmethod(lambda **kwargs: captured.update(kwargs) or failing_stream())},
                    )()
                },
            )()

    monkeypatch.setattr("airbrowser.server.vision.openai_compatible.OpenAI", FakeOpenAI)

    client = OpenAICompatibleVisionClient(
        base_url="https://cliproxy.ldc-fe.org/v1",
        api_key="test-key",
        model="rightcode/gpt-5.4",
    )

    result = client.explain_screenshot(str(image_path), "describe it", stream=True)

    assert result == {"success": False, "error": "API request failed: stream interrupted"}
    assert captured.get("stream") is True


def test_request_model_override_allows_slash_names(monkeypatch):
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    assert vision_commands.resolve_vision_model({"model": "rightcode/gpt-5.4"}) == "rightcode/gpt-5.4"


def test_browser_pool_detect_coordinates_forwards_model_to_ipc(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(
            action="detect_coordinates",
            options={"prompt": "the submit button", "fx": 0.25, "fy": 0.75, "model": "rightcode/gpt-5.4"},
        ),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "detect_coordinates",
        {"prompt": "the submit button", "fx": 0.25, "fy": 0.75, "model": "rightcode/gpt-5.4"},
    )


def test_browser_pool_detect_coordinates_forwards_stream_to_ipc(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(action="detect_coordinates", options={"prompt": "the submit button", "stream": True}),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "detect_coordinates",
        {"prompt": "the submit button", "stream": True},
    )


def test_browser_pool_detect_coordinates_forwards_smart_targeting_options_to_ipc(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(
            action="detect_coordinates",
            options={
                "prompt": "the submit button",
                "hit_test": "strict",
                "auto_snap": "nearest_clickable",
                "snap_radius": 96,
                "include_debug": True,
            },
        ),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "detect_coordinates",
        {
            "prompt": "the submit button",
            "hit_test": "strict",
            "auto_snap": "nearest_clickable",
            "snap_radius": 96,
            "include_debug": True,
        },
    )


def test_browser_pool_what_is_visible_forwards_model_to_ipc(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(action="what_is_visible", options={"model": "rightcode/gpt-5.4"}),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "what_is_visible",
        {"model": "rightcode/gpt-5.4"},
    )


def test_browser_pool_what_is_visible_forwards_stream_to_ipc(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action(
        "browser-123",
        BrowserAction(action="what_is_visible", options={"stream": False}),
    )

    assert result.success is True
    assert ipc_client.calls[-1] == (
        "browser-123",
        "what_is_visible",
        {"stream": False},
    )


def test_vision_operations_detect_coordinates_sets_stream_in_action_options():
    browser_pool = StaticBrowserPool(ActionResult(success=True, message="ok", data={"coordinates": {}}))

    VisionOperations(browser_pool).detect_coordinates("browser-123", prompt="the submit button", stream=True)

    _, action = browser_pool.actions[-1]
    assert action.options["stream"] is True


def test_vision_operations_what_is_visible_sets_stream_in_action_options():
    browser_pool = StaticBrowserPool(ActionResult(success=True, message="ok", data={}))

    VisionOperations(browser_pool).what_is_visible("browser-123", stream=False)

    _, action = browser_pool.actions[-1]
    assert action.options["stream"] is False


def test_browser_pool_screenshot_uses_command_response_url(browser_pool_adapter):
    adapter, ipc_client = browser_pool_adapter

    result = adapter.execute_action("browser-123", BrowserAction(action="screenshot"))

    assert ipc_client.calls[-1] == ("browser-123", "screenshot", {})
    assert result.success is True
    assert result.data == {
        "status": "success",
        "url": "http://localhost:18080/screenshots/example.png",
        "path": "/app/screenshots/example.png",
        "filename": "example.png",
    }


def test_action_result_to_dict_excludes_legacy_screenshot_path():
    result = ActionResult(success=True, message="ok", data={"screenshot_url": "http://shot"})

    assert "screenshot_path" not in result.to_dict()


def test_page_operations_take_screenshot_ignores_legacy_screenshot_url_only_payload():
    operation = PageOperations(
        StaticBrowserPool(
            ActionResult(
                success=True,
                message="Screenshot captured",
                data={"screenshot_url": "http://localhost:18080/screenshots/legacy.png"},
            )
        )
    )

    result = operation.take_screenshot("browser-123")

    assert result["success"] is True
    assert result["data"]["screenshot_url"] is None


def test_detect_coordinates_route_accepts_and_threads_model_override(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/detect_coordinates",
        json={"prompt": "the submit button", "model": "rightcode/gpt-5.4"},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["bounding_box"] == {"x": 10, "y": 20, "width": 30, "height": 40}
    assert browser_pool.actions[-1][0] == "browser-123"
    assert browser_pool.actions[-1][1].options["model"] == "rightcode/gpt-5.4"


def test_detect_coordinates_route_accepts_and_threads_stream_override(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/detect_coordinates",
        json={"prompt": "the submit button", "stream": True},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert browser_pool.actions[-1][0] == "browser-123"
    assert browser_pool.actions[-1][1].options["stream"] is True


def test_detect_coordinates_route_threads_smart_targeting_options_and_returns_additive_fields(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/detect_coordinates",
        json={
            "prompt": "the submit button",
            "hit_test": "strict",
            "auto_snap": "nearest_clickable",
            "snap_radius": 96,
            "include_debug": True,
        },
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["click_point"] == {"x": 25, "y": 40}
    assert response.json["data"]["resolved_click_point"] == {"x": 24, "y": 35}
    assert response.json["data"]["outcome_status"] == "snapped_match"
    assert response.json["data"]["recommended_next_action"] == "proceed"
    assert browser_pool.actions[-1][1].options["hit_test"] == "strict"
    assert browser_pool.actions[-1][1].options["auto_snap"] == "nearest_clickable"
    assert browser_pool.actions[-1][1].options["snap_radius"] == 96
    assert browser_pool.actions[-1][1].options["include_debug"] is True


@pytest.mark.parametrize(
    ("logical_success", "outcome_status", "reason", "recommended_next_action"),
    [
        (False, "fail_iframe_boundary", "hit_iframe_boundary", "switch_to_iframe_context"),
        (True, "warn_hit_test_unavailable", "hit_test_unavailable", "inspect_page"),
    ],
)
def test_detect_coordinates_route_returns_http_200_with_structured_warning_or_failure_payload(
    browser_route_client,
    logical_success,
    outcome_status,
    reason,
    recommended_next_action,
):
    client, browser_pool = browser_route_client
    browser_pool.actions.clear()
    browser_pool.override_result = ActionResult(
        success=logical_success,
        message="Smart targeting produced diagnostics",
        data={
            "coordinates": {
                "x": 280,
                "y": 393,
                "width": 90,
                "height": 20,
                "click_point": {"x": 325, "y": 403},
                "resolved_click_point": {"x": 325, "y": 403},
                "outcome_status": outcome_status,
                "reason": reason,
                "reason_detail": "diagnostic detail",
                "recommended_next_action": recommended_next_action,
                "screenshot_url": "http://shot",
            }
        },
    )

    response = client.post(
        "/api/v1/browser/browser-123/detect_coordinates",
        json={
            "prompt": "the submit button",
            "hit_test": "strict",
            "auto_snap": "nearest_clickable",
        },
    )

    assert response.status_code == 200
    assert response.json["success"] is logical_success
    assert response.json["message"] == "Smart targeting produced diagnostics"
    assert response.json["data"]["outcome_status"] == outcome_status
    assert response.json["data"]["reason"] == reason
    assert response.json["data"]["recommended_next_action"] == recommended_next_action
    assert response.json["data"]["click_point"] == {"x": 325, "y": 403}
    assert browser_pool.actions[-1][0] == "browser-123"
    browser_pool.override_result = None


def test_detect_coordinates_unexpected_backend_fault_bubbles_up():
    from airbrowser.server.services.operations.vision import VisionOperations

    browser_pool = type(
        "ExplodingPool",
        (),
        {
            "execute_action": staticmethod(
                lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("vision backend exploded"))
            )
        },
    )()

    with pytest.raises(RuntimeError, match="vision backend exploded"):
        VisionOperations(browser_pool).detect_coordinates("browser-123", prompt="the submit button")


def test_detect_coordinates_route_returns_http_500_for_unexpected_backend_fault(browser_route_client):
    client, browser_pool = browser_route_client

    def exploding_execute_action(browser_id, action):
        raise RuntimeError("vision backend exploded")

    browser_pool.execute_action = exploding_execute_action

    response = client.post(
        "/api/v1/browser/browser-123/detect_coordinates",
        json={"prompt": "the submit button"},
    )

    assert response.status_code == 500
    assert response.json == {"success": False, "error": "vision backend exploded"}


def test_detect_coordinates_openapi_uses_detect_response_schema(browser_route_client):
    client, _ = browser_route_client

    response = client.get("/api/v1/swagger.json")

    assert response.status_code == 200
    path_item = response.json["paths"]["/browser/{browser_id}/detect_coordinates"]
    assert path_item["post"]["responses"]["200"]["schema"] == {"$ref": "#/definitions/DetectCoordinatesResult"}


def test_detect_coordinates_openapi_uses_hand_authored_request_schema(browser_route_client):
    client, _ = browser_route_client

    response = client.get("/api/v1/swagger.json")

    assert response.status_code == 200
    path_item = response.json["paths"]["/browser/{browser_id}/detect_coordinates"]
    assert path_item["post"]["parameters"] == [
        {
            "name": "payload",
            "required": True,
            "in": "body",
            "schema": {"$ref": "#/definitions/DetectCoordinatesRequest"},
        }
    ]

    request_definition = response.json["definitions"]["DetectCoordinatesRequest"]["properties"]
    assert request_definition["hit_test"]["type"] == "string"
    assert request_definition["hit_test"]["description"] == "Detect-time validation mode"
    assert request_definition["hit_test"]["default"] == "off"
    assert request_definition["hit_test"]["enum"] == ["off", "warn", "strict"]
    assert request_definition["auto_snap"]["type"] == "string"
    assert request_definition["auto_snap"]["description"] == "Auto-snap mode for nearby targets"
    assert request_definition["auto_snap"]["default"] == "off"
    assert request_definition["auto_snap"]["enum"] == ["off", "nearest_clickable", "nearest_interactive"]


def test_detect_coordinates_request_schema_includes_boolean_stream(browser_route_client):
    client, _ = browser_route_client

    response = client.get("/api/v1/swagger.json")

    assert response.status_code == 200
    request_definition = response.json["definitions"]["DetectCoordinatesRequest"]["properties"]
    assert request_definition["stream"]["type"] == "boolean"


def test_generated_python_detect_coordinates_request_includes_stream_field():
    from airbrowser_client.models.detect_coordinates_request import DetectCoordinatesRequest

    payload = DetectCoordinatesRequest(prompt="the submit button", stream=True)

    assert payload.to_dict()["stream"] is True


def test_what_is_visible_route_rejects_missing_request_body(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post("/api/v1/browser/browser-123/what_is_visible")

    assert response.status_code == 400
    assert response.json == {"success": False, "error": "Request body is required"}
    assert browser_pool.actions == []


def test_what_is_visible_route_accepts_empty_request_body(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post("/api/v1/browser/browser-123/what_is_visible", json={})

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["model"] is None
    assert browser_pool.actions[-1][0] == "browser-123"
    assert browser_pool.actions[-1][1].options == {}


def test_what_is_visible_route_accepts_body_model_override(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/what_is_visible",
        json={"model": "rightcode/gpt-5.4"},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["model"] == "rightcode/gpt-5.4"
    assert browser_pool.actions[-1][0] == "browser-123"
    assert browser_pool.actions[-1][1].options["model"] == "rightcode/gpt-5.4"


def test_what_is_visible_route_accepts_body_stream_override(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/what_is_visible",
        json={"stream": False},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert browser_pool.actions[-1][0] == "browser-123"
    assert browser_pool.actions[-1][1].options["stream"] is False


def test_what_is_visible_openapi_requires_request_body(browser_route_client):
    client, _ = browser_route_client

    response = client.get("/api/v1/swagger.json")

    assert response.status_code == 200
    path_item = response.json["paths"]["/browser/{browser_id}/what_is_visible"]
    assert path_item["parameters"] == [{"name": "browser_id", "in": "path", "required": True, "type": "string"}]
    parameters = path_item["post"]["parameters"]
    assert parameters == [
        {
            "name": "payload",
            "required": True,
            "in": "body",
            "schema": {"$ref": "#/definitions/WhatIsVisibleRequest"},
        }
    ]


def test_what_is_visible_request_schema_includes_boolean_stream(browser_route_client):
    client, _ = browser_route_client

    response = client.get("/api/v1/swagger.json")

    assert response.status_code == 200
    request_definition = response.json["definitions"]["WhatIsVisibleRequest"]["properties"]
    assert request_definition["stream"]["type"] == "boolean"


def test_generated_python_what_is_visible_request_includes_stream_field():
    from airbrowser_client.models.what_is_visible_request import WhatIsVisibleRequest

    payload = WhatIsVisibleRequest(stream=False)

    assert payload.to_dict()["stream"] is False


def test_generated_typescript_vision_request_interfaces_include_stream_field():
    api_ts = Path("generated-clients/typescript/api.ts").read_text(encoding="utf-8")

    detect_block = api_ts.split("export interface DetectCoordinatesRequest {", 1)[1].split(
        "export const DetectCoordinatesRequestHitTestEnum", 1
    )[0]
    visible_block = api_ts.split("export interface WhatIsVisibleRequest {", 1)[1].split(
        "/**\n * BrowserApi - axios parameter creator",
        1,
    )[0]

    assert "'stream'?: boolean;" in detect_block
    assert "'stream'?: boolean;" in visible_block


def test_schema_models_exclude_legacy_screenshot_path():
    api = Api(Flask(__name__))
    browser_schemas = register_browser_schemas(api)
    response_schemas = register_response_schemas(api)

    assert "screenshot_path" not in browser_schemas["DetectCoordinatesResult"].__schema__["properties"]
    assert "screenshot_path" not in browser_schemas["WhatIsVisibleResult"].__schema__["properties"]
    assert "screenshot_path" not in api.models["ScreenshotData"].__schema__["properties"]
    assert "data" in response_schemas["ScreenshotResponse"].__schema__["properties"]


def test_serve_screenshot_uses_configured_directory_and_touches_file(monkeypatch, tmp_path):
    monkeypatch.setenv("ENABLE_MCP", "false")
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setattr(app_module, "BrowserPoolAdapter", CapturingBrowserPool)
    filename = "serve-screenshot-hermetic.png"
    configured_bytes = b"configured-shot"
    legacy_bytes = b"legacy-shot"
    image = tmp_path / filename
    image.write_bytes(configured_bytes)
    before = image.stat().st_mtime - 10
    os.utime(image, (before, before))
    legacy_dir = Path("/tmp/screenshots")
    legacy_dir.mkdir(parents=True, exist_ok=True)
    (legacy_dir / filename).write_bytes(legacy_bytes)

    app, _ = app_module.create_app()
    client = app.test_client()
    response = client.get(f"/screenshots/{filename}")

    assert response.status_code == 200
    assert response.data == configured_bytes
    assert image.stat().st_mtime > before


def test_handle_what_is_visible_returns_generic_error_when_unconfigured(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )
    monkeypatch.delenv("VISION_API_BASE_URL", raising=False)
    monkeypatch.delenv("VISION_API_KEY", raising=False)
    monkeypatch.delenv("VISION_MODEL", raising=False)

    result = vision_commands.handle_what_is_visible(driver=object(), command={}, browser_id="test-browser")

    assert result["status"] == "error"
    assert result["message"] == "Vision client not configured"
    assert result["screenshot_url"] == "http://shot"


def test_handle_detect_coordinates_returns_generic_error_when_unconfigured(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )
    monkeypatch.setattr(
        vision_commands,
        "detect_element_coordinates",
        lambda *args, **kwargs: pytest.fail("detect_element_coordinates should not run without vision config"),
    )
    monkeypatch.delenv("VISION_API_BASE_URL", raising=False)
    monkeypatch.delenv("VISION_API_KEY", raising=False)
    monkeypatch.delenv("VISION_MODEL", raising=False)

    result = vision_commands.handle_detect_coordinates(
        driver=object(),
        command={"prompt": "the submit button"},
        browser_id="test-browser",
    )

    assert result["status"] == "error"
    assert result["message"] == "Vision client not configured"
    assert result["screenshot_url"] == "http://shot"


def test_handle_what_is_visible_request_stream_true_overrides_env_false(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            captured["stream"] = stream
            return {"success": True, "explanation": "visible analysis", "model": self.model}

    monkeypatch.setattr(vision_commands, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    _set_vision_env(monkeypatch, stream_default="false")

    result = vision_commands.handle_what_is_visible(
        driver=object(),
        command={"stream": True},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert captured["stream"] is True


def test_handle_what_is_visible_request_stream_false_overrides_env_true(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            captured["stream"] = stream
            return {"success": True, "explanation": "visible analysis", "model": self.model}

    monkeypatch.setattr(vision_commands, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    _set_vision_env(monkeypatch, stream_default="true")

    result = vision_commands.handle_what_is_visible(
        driver=object(),
        command={"stream": False},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert captured["stream"] is False


def test_handle_what_is_visible_omitted_stream_uses_env_default(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            captured["stream"] = stream
            return {"success": True, "explanation": "visible analysis", "model": self.model}

    monkeypatch.setattr(vision_commands, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    _set_vision_env(monkeypatch, stream_default="true")

    result = vision_commands.handle_what_is_visible(driver=object(), command={}, browser_id="test-browser")

    assert result["status"] == "success"
    assert captured["stream"] is True


def test_detect_coordinates_omitted_stream_uses_env_default(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    def fake_detect_element_coordinates(image_path, prompt, model, stream):
        captured["stream"] = stream
        return {
            "success": True,
            "x": 10,
            "y": 20,
            "width": 30,
            "height": 10,
            "confidence": 0.9,
            "model": model,
            "image_size": {"width": 100, "height": 50},
        }

    monkeypatch.setattr(vision_commands, "detect_element_coordinates", fake_detect_element_coordinates)
    monkeypatch.setattr(
        vision_commands,
        "_transform_to_screen_coords",
        lambda driver, coords, fx, fy: {**coords, "click_point": {"x": 17, "y": 25}},
    )
    monkeypatch.setattr(vision_commands, "resolve_detect_target", lambda **kwargs: _make_detect_resolution())
    _set_vision_env(monkeypatch, stream_default="true")

    result = vision_commands.handle_detect_coordinates(
        driver=object(),
        command={"prompt": "the submit button"},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert captured["stream"] is True


def test_detect_coordinates_request_stream_true_overrides_env_false(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    def fake_detect_element_coordinates(image_path, prompt, model, stream):
        captured["stream"] = stream
        return {
            "success": True,
            "x": 10,
            "y": 20,
            "width": 30,
            "height": 10,
            "confidence": 0.9,
            "model": model,
            "image_size": {"width": 100, "height": 50},
        }

    monkeypatch.setattr(vision_commands, "detect_element_coordinates", fake_detect_element_coordinates)
    monkeypatch.setattr(
        vision_commands,
        "_transform_to_screen_coords",
        lambda driver, coords, fx, fy: {**coords, "click_point": {"x": 17, "y": 25}},
    )
    monkeypatch.setattr(vision_commands, "resolve_detect_target", lambda **kwargs: _make_detect_resolution())
    _set_vision_env(monkeypatch, stream_default="false")

    result = vision_commands.handle_detect_coordinates(
        driver=object(),
        command={"prompt": "the submit button", "stream": True},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert captured["stream"] is True


def test_detect_coordinates_request_stream_false_overrides_env_true(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    def fake_detect_element_coordinates(image_path, prompt, model, stream):
        captured["stream"] = stream
        return {
            "success": True,
            "x": 10,
            "y": 20,
            "width": 30,
            "height": 10,
            "confidence": 0.9,
            "model": model,
            "image_size": {"width": 100, "height": 50},
        }

    monkeypatch.setattr(vision_commands, "detect_element_coordinates", fake_detect_element_coordinates)
    monkeypatch.setattr(
        vision_commands,
        "_transform_to_screen_coords",
        lambda driver, coords, fx, fy: {**coords, "click_point": {"x": 17, "y": 25}},
    )
    monkeypatch.setattr(vision_commands, "resolve_detect_target", lambda **kwargs: _make_detect_resolution())
    _set_vision_env(monkeypatch, stream_default="true")

    result = vision_commands.handle_detect_coordinates(
        driver=object(),
        command={"prompt": "the submit button", "stream": False},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert captured["stream"] is False


def test_vision_coordinate_detector_forwards_stream_to_client(monkeypatch, tmp_path):
    captured = {}
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            captured["stream"] = stream
            return {
                "success": True,
                "explanation": '{"found": true, "x": 10, "y": 20, "width": 30, "height": 40, "confidence": 0.9}',
                "model": self.model,
            }

    monkeypatch.setattr("airbrowser.server.vision.coordinates.OpenAICompatibleVisionClient", FakeClient)
    monkeypatch.setattr(
        "airbrowser.server.vision.coordinates.load_vision_settings",
        lambda: VisionSettings(
            base_url="https://cliproxy.ldc-fe.org/v1",
            api_key="test-key",
            model="default/model",
            stream_default=False,
        ),
    )

    from airbrowser.server.vision.coordinates import VisionCoordinateDetector

    result = VisionCoordinateDetector("rightcode/gpt-5.4").detect(str(image_path), "submit button", stream=True)

    assert result["success"] is True
    assert captured["stream"] is True


def test_handle_detect_coordinates_passes_request_model_override(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )
    monkeypatch.setattr(
        vision_commands,
        "detect_element_coordinates",
        lambda image_path, prompt, model, stream=False: {
            "success": True,
            "x": 10,
            "y": 20,
            "width": 30,
            "height": 10,
            "confidence": 0.9,
            "model": model,
            "image_size": {"width": 100, "height": 50},
        },
    )
    monkeypatch.setattr(
        vision_commands,
        "_transform_to_screen_coords",
        lambda driver, coords, fx, fy: {**coords, "click_point": {"x": 17, "y": 25}},
    )
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    result = vision_commands.handle_detect_coordinates(
        driver=object(),
        command={"prompt": "the submit button", "model": "rightcode/gpt-5.4"},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert result["coordinates"]["model"] == "rightcode/gpt-5.4"
    assert result["coordinates"]["click_point"] == {"x": 17, "y": 25}
    assert result["coordinates"]["screenshot_url"] == "http://shot"


def test_handle_what_is_visible_uses_generic_client_on_success(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            return {"success": True, "explanation": "visible analysis", "model": self.model}

    monkeypatch.setattr(vision_commands, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    result = vision_commands.handle_what_is_visible(
        driver=object(),
        command={"model": "rightcode/gpt-5.4"},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert result["analysis"] == "visible analysis"
    assert result["model"] == "rightcode/gpt-5.4"
    assert result["screenshot_url"] == "http://shot"


def test_handle_what_is_visible_preserves_screenshot_on_provider_failure(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )

    class FakeClient:
        def __init__(self, *, base_url, api_key, model):
            self.model = model

        def explain_screenshot(self, image_path, prompt, stream=False):
            return {"success": False, "error": "provider failed"}

    monkeypatch.setattr(vision_commands, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    result = vision_commands.handle_what_is_visible(driver=object(), command={}, browser_id="test-browser")

    assert result["status"] == "error"
    assert result["message"] == "provider failed"
    assert result["screenshot_url"] == "http://shot"


def test_handle_detect_coordinates_auto_biases_wide_elements(monkeypatch):
    monkeypatch.setattr(
        vision_commands,
        "take_screenshot",
        lambda driver, browser_id: {"path": "/tmp/fake.png", "url": "http://shot"},
    )
    monkeypatch.setattr(
        vision_commands,
        "detect_element_coordinates",
        lambda image_path, prompt, model, stream=False: {
            "success": True,
            "x": 400,
            "y": 300,
            "width": 1000,
            "height": 50,
            "confidence": 0.9,
            "model": model,
            "image_size": {"width": 1920, "height": 1080},
        },
    )
    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    class FakeDriver:
        def get_window_rect(self):
            return {"x": 0, "y": 0, "width": 1920, "height": 1080}

        def execute_script(self, script):
            return {"return window.innerWidth;": 1920, "return window.innerHeight;": 1080}[script]

    result = vision_commands.handle_detect_coordinates(
        driver=FakeDriver(),
        command={"prompt": "the text input area of the search box"},
        browser_id="test-browser",
    )

    assert result["status"] == "success"
    assert result["coordinates"]["click_point"]["x"] == 650
    assert result["coordinates"]["screenshot_url"] == "http://shot"
