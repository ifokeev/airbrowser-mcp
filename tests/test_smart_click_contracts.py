import asyncio
import json
from pathlib import Path

import pytest
from airbrowser_client.models import GuiClickRequest
from flask import Flask
from flask_restx import Api
from pydantic import ValidationError

import airbrowser.server.app as app_module
from airbrowser.server.mcp.integration import MCPIntegration
from airbrowser.server.mcp.tool_descriptions import TOOL_DESCRIPTIONS
from airbrowser.server.models import ActionResult
from airbrowser.server.schemas.browser import register_browser_schemas
from airbrowser.server.services.browser_operations import BrowserOperations


def _gui_click_payload(
    *,
    logical_success: bool = True,
    outcome_status: str = "clicked_snapped",
    recommended_next_action: str = "proceed",
    postcheck_status: str = "url_changed",
) -> dict:
    return {
        "status": "success",
        "success": logical_success,
        "message": "Clicked snapped target",
        "x": 325,
        "y": 403,
        "outcome_status": outcome_status,
        "precheck": {
            "outcome_status": "snapped_match",
            "original_point": {"x": 325, "y": 403},
            "resolved_point": {"x": 324, "y": 345},
            "resolved_element": {"tag": "A", "text": "Learn more"},
        },
        "execution": {
            "clicked_point": {"x": 324, "y": 345},
            "mode": "snapped",
        },
        "postcheck": {
            "status": postcheck_status,
            "before_url": "https://example.com/",
            "after_url": "https://www.iana.org/help/example-domains",
        },
        "recommended_next_action": recommended_next_action,
    }


class StaticBrowserPool:
    def __init__(self, result: ActionResult):
        self.result = result
        self.actions = []

    def execute_action(self, browser_id: str, action):
        self.actions.append((browser_id, action))
        return self.result


class CapturingBrowserPool:
    instances = []

    def __init__(self, max_browsers: int = 50):
        self.max_browsers = max_browsers
        self.actions = []
        self.result = ActionResult(success=True, message="Clicked snapped target", data=_gui_click_payload())
        type(self).instances.append(self)

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


def list_discovered_tool_names(browser_ops: BrowserOperations) -> set[str]:
    integration = MCPIntegration(browser_ops=browser_ops)
    return {tool.name for tool in asyncio.run(integration.mcp.list_tools())}


def test_gui_click_xy_is_still_discoverable_for_mcp_tools():
    browser_ops = BrowserOperations(StaticBrowserPool(ActionResult(success=True, message="ok", data={})))

    tool_names = list_discovered_tool_names(browser_ops)

    assert "gui_click_xy" in tool_names


def test_tool_descriptions_recommend_smart_mode():
    assert "pre_click_validate" in TOOL_DESCRIPTIONS["gui_click"]
    assert "auto_snap" in TOOL_DESCRIPTIONS["detect_coordinates"]


def test_gui_click_xy_tool_description_documents_alias_parity():
    assert "compatibility alias" in TOOL_DESCRIPTIONS["gui_click_xy"]
    assert "coordinate-mode `gui_click`" in TOOL_DESCRIPTIONS["gui_click_xy"]


def test_gui_click_routes_publish_typed_gui_click_response_schema(monkeypatch):
    monkeypatch.setenv("ENABLE_MCP", "false")
    monkeypatch.setattr(app_module, "BrowserPoolAdapter", CapturingBrowserPool)

    app, _ = app_module.create_app()
    response = app.test_client().get("/api/v1/swagger.json")
    spec = response.get_json()

    gui_click_schema = spec["paths"]["/browser/{browser_id}/gui_click"]["post"]["responses"]["200"]["schema"]
    gui_click_xy_schema = spec["paths"]["/browser/{browser_id}/gui_click_xy"]["post"]["responses"]["200"]["schema"]

    assert gui_click_schema == {"$ref": "#/definitions/GuiClickResult"}
    assert gui_click_xy_schema == {"$ref": "#/definitions/GuiClickResult"}


def test_gui_click_routes_publish_rich_request_schemas(monkeypatch):
    monkeypatch.setenv("ENABLE_MCP", "false")
    monkeypatch.setattr(app_module, "BrowserPoolAdapter", CapturingBrowserPool)

    app, _ = app_module.create_app()
    response = app.test_client().get("/api/v1/swagger.json")
    spec = response.get_json()

    gui_click_schema = spec["paths"]["/browser/{browser_id}/gui_click"]["post"]["parameters"][0]["schema"]
    gui_click_xy_schema = spec["paths"]["/browser/{browser_id}/gui_click_xy"]["post"]["parameters"][0]["schema"]
    gui_click_props = spec["definitions"]["GuiClickRequest"]["properties"]
    gui_click_xy_props = spec["definitions"]["GuiClickXYRequest"]["properties"]

    assert gui_click_schema == {"$ref": "#/definitions/GuiClickRequest"}
    assert gui_click_xy_schema == {"$ref": "#/definitions/GuiClickXYRequest"}
    assert gui_click_props["pre_click_validate"]["description"] == "Pre-click validation mode"
    assert gui_click_props["pre_click_validate"]["enum"] == ["off", "warn", "strict"]
    assert gui_click_props["auto_snap"]["description"] == "Auto-snap mode for nearby targets"
    assert gui_click_props["auto_snap"]["enum"] == ["off", "nearest_clickable", "nearest_interactive"]
    assert gui_click_props["post_click_feedback"]["description"] == "Post-click feedback mode"
    assert gui_click_xy_props["pre_click_validate"]["description"] == "Pre-click validation mode"
    assert gui_click_xy_props["pre_click_validate"]["enum"] == ["off", "warn", "strict"]
    assert gui_click_xy_props["auto_snap"]["description"] == "Auto-snap mode for nearby targets"
    assert gui_click_xy_props["auto_snap"]["enum"] == ["off", "nearest_clickable", "nearest_interactive"]


def test_generated_client_request_models_enforce_smart_click_enums():
    from airbrowser_client.models import GuiClickXYRequest

    with pytest.raises(ValidationError):
        GuiClickRequest(pre_click_validate="invalid")

    with pytest.raises(ValidationError):
        GuiClickXYRequest(x=325, y=403, auto_snap="invalid")


def test_generated_client_contract_smoke(monkeypatch):
    import airbrowser_client
    from airbrowser_client.api.browser_api import BrowserApi
    from airbrowser_client.models import GuiClickData, GuiClickResult, GuiClickXYRequest

    class FakeRestResponse:
        def __init__(self, payload: dict):
            self.status = 200
            self.reason = "OK"
            self.headers = {"content-type": "application/json"}
            self.data = None
            self._payload = json.dumps(payload).encode("utf-8")

        def read(self):
            self.data = self._payload
            return self.data

    api_client = airbrowser_client.ApiClient(airbrowser_client.Configuration())
    browser_api = BrowserApi(api_client)
    payload = _gui_click_payload(outcome_status="clicked_exact")

    def fake_call_api(*args, **kwargs):
        return FakeRestResponse({"success": True, "message": "Clicked exact target", "data": payload})

    monkeypatch.setattr(api_client, "call_api", fake_call_api)

    result = browser_api.gui_click(
        "browser-123",
        payload=GuiClickRequest(x=325, y=403, pre_click_validate="off", auto_snap="off"),
    )
    alias_result = browser_api.gui_click_xy(
        "browser-123",
        payload=GuiClickXYRequest(x=325, y=403, pre_click_validate="off", auto_snap="off"),
    )

    assert isinstance(result, GuiClickResult)
    assert isinstance(result.data, GuiClickData)
    assert result.data.outcome_status == "clicked_exact"
    assert result.data.message == "Clicked snapped target"
    assert result.data.success is True
    assert alias_result.data.outcome_status == "clicked_exact"
    assert alias_result.data.message == "Clicked snapped target"
    assert alias_result.data.success is True


def test_detect_preserves_legacy_click_point_and_adds_resolved_click_point():
    browser_ops = BrowserOperations(
        StaticBrowserPool(
            ActionResult(
                success=True,
                message="Found: learn more",
                data={
                    "coordinates": {
                        "x": 280,
                        "y": 393,
                        "width": 90,
                        "height": 20,
                        "confidence": 0.52,
                        "click_point": {"x": 325, "y": 403},
                        "resolved_click_point": {"x": 324, "y": 345},
                        "outcome_status": "snapped_match",
                        "reason": "hit_html_root",
                        "reason_detail": "hit non-interactive root element",
                        "resolved_target": {
                            "point": {"x": 324, "y": 345},
                            "element": {"tag": "A", "text": "Learn more", "interactive": True},
                        },
                        "snap_result": {
                            "applied": True,
                            "strategy": "nearest_clickable",
                            "distance_px": 58,
                            "snapped_point": {"x": 324, "y": 345},
                        },
                        "recommended_next_action": "proceed",
                        "screenshot_url": "http://shot",
                    }
                },
            )
        )
    )

    result = browser_ops.detect_coordinates(
        browser_id="b1",
        prompt="the Learn more link",
        hit_test="strict",
        auto_snap="nearest_clickable",
    )

    assert result["success"] is True
    assert result["data"]["click_point"] == {"x": 325, "y": 403}
    assert result["data"]["resolved_click_point"] == {"x": 324, "y": 345}
    assert result["data"]["outcome_status"] == "snapped_match"


def test_detect_structured_failure_keeps_data_payload_on_warn_or_fail():
    browser_ops = BrowserOperations(
        StaticBrowserPool(
            ActionResult(
                success=False,
                message="Vision point missed target",
                data={
                    "coordinates": {
                        "x": 280,
                        "y": 393,
                        "width": 90,
                        "height": 20,
                        "click_point": {"x": 325, "y": 403},
                        "resolved_click_point": {"x": 325, "y": 403},
                        "outcome_status": "fail_no_target",
                        "reason": "no_candidate_within_radius",
                        "reason_detail": "no candidate fell within the configured snap radius",
                        "recommended_next_action": "retry_with_larger_radius",
                        "screenshot_url": "http://shot",
                    }
                },
            )
        )
    )

    result = browser_ops.detect_coordinates(
        browser_id="b1",
        prompt="missing target",
        hit_test="strict",
        auto_snap="nearest_clickable",
    )

    assert result["success"] is False
    assert result["message"] == "Vision point missed target"
    assert result["data"]["outcome_status"] == "fail_no_target"
    assert result["data"]["click_point"] == {"x": 325, "y": 403}
    assert result["data"]["recommended_next_action"] == "retry_with_larger_radius"


def test_gui_click_coordinate_mode_preserves_requested_x_y():
    browser_ops = BrowserOperations(
        StaticBrowserPool(
            ActionResult(
                success=True,
                message="Clicked snapped target",
                data=_gui_click_payload(),
            )
        )
    )

    result = browser_ops.gui_click(
        browser_id="b1",
        x=325,
        y=403,
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
    )

    assert result["success"] is True
    assert result["data"]["x"] == 325
    assert result["data"]["y"] == 403
    assert result["data"]["execution"]["clicked_point"] == {"x": 324, "y": 345}


def test_gui_click_xy_alias_matches_gui_click_coordinate_response():
    browser_pool = StaticBrowserPool(
        ActionResult(
            success=True,
            message="Clicked snapped target",
            data=_gui_click_payload(),
        )
    )
    browser_ops = BrowserOperations(browser_pool)

    direct = browser_ops.gui_click(
        browser_id="b1",
        x=325,
        y=403,
        timeframe=0.4,
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        snap_radius=96,
        post_click_feedback="auto",
        post_click_timeout_ms=1500,
        return_content=True,
        content_limit_chars=800,
        include_debug=True,
    )
    alias = browser_ops.gui_click_xy(
        browser_id="b1",
        x=325,
        y=403,
        timeframe=0.4,
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        snap_radius=96,
        post_click_feedback="auto",
        post_click_timeout_ms=1500,
        return_content=True,
        content_limit_chars=800,
        include_debug=True,
    )

    assert alias["success"] is True
    assert alias["data"]["outcome_status"] == direct["data"]["outcome_status"]
    assert alias["data"]["execution"] == direct["data"]["execution"]
    assert browser_pool.actions[0][1].options == browser_pool.actions[1][1].options


def test_gui_click_rejects_selector_and_coordinates_together():
    browser_ops = BrowserOperations(StaticBrowserPool(ActionResult(success=True, message="ok", data={})))

    with pytest.raises(TypeError):
        browser_ops.gui_click(browser_id="b1", selector="a", x=1, y=2)


def test_gui_click_structured_failure_keeps_data_payload():
    browser_ops = BrowserOperations(
        StaticBrowserPool(
            ActionResult(
                success=True,
                message="Validation inconclusive",
                data=_gui_click_payload(
                    logical_success=False,
                    outcome_status="click_uncertain",
                    recommended_next_action="inspect_page",
                    postcheck_status="no_observable_change",
                ),
            )
        )
    )

    result = browser_ops.gui_click(
        browser_id="b1",
        x=325,
        y=403,
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        post_click_feedback="auto",
    )

    assert result["success"] is False
    assert result["message"] == "Validation inconclusive"
    assert result["data"]["outcome_status"] == "click_uncertain"
    assert result["data"]["recommended_next_action"] == "inspect_page"


def test_gui_click_route_rejects_selector_and_coordinates_together(browser_route_client):
    client, browser_pool = browser_route_client

    response = client.post(
        "/api/v1/browser/browser-123/gui_click",
        json={"selector": "a", "x": 1, "y": 2},
    )

    assert response.status_code == 400
    assert "Invalid parameters" in response.json["error"]
    assert browser_pool.actions == []


def test_gui_click_route_returns_http_200_with_structured_failure_payload(browser_route_client):
    client, browser_pool = browser_route_client
    browser_pool.result = ActionResult(
        success=True,
        message="Validation inconclusive",
        data=_gui_click_payload(
            logical_success=False,
            outcome_status="click_uncertain",
            recommended_next_action="inspect_page",
            postcheck_status="no_observable_change",
        ),
    )

    response = client.post(
        "/api/v1/browser/browser-123/gui_click",
        json={
            "x": 325,
            "y": 403,
            "pre_click_validate": "strict",
            "auto_snap": "nearest_clickable",
            "post_click_feedback": "auto",
        },
    )

    assert response.status_code == 200
    assert response.json["success"] is False
    assert response.json["data"]["outcome_status"] == "click_uncertain"
    assert response.json["data"]["execution"]["clicked_point"] == {"x": 324, "y": 345}


def test_gui_click_route_returns_http_500_for_unexpected_backend_fault(browser_route_client):
    client, browser_pool = browser_route_client

    def exploding_execute_action(browser_id, action):
        raise RuntimeError("browser service exploded")

    browser_pool.execute_action = exploding_execute_action

    response = client.post(
        "/api/v1/browser/browser-123/gui_click",
        json={"x": 325, "y": 403},
    )

    assert response.status_code == 500
    assert response.json == {"success": False, "error": "browser service exploded"}


def test_generated_client_outputs_have_no_trailing_whitespace_or_blank_eof():
    generated_roots = [
        Path("generated-clients/python"),
        Path("generated-clients/typescript"),
    ]
    checked_files = 0

    for root in generated_roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part.endswith(".egg-info") for part in path.parts):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            checked_files += 1
            assert not content.endswith("\n\n"), f"{path} has a blank line at EOF"
            for line_number, line in enumerate(content.splitlines(), start=1):
                assert line == line.rstrip(), f"{path}:{line_number} has trailing whitespace"

    assert checked_files > 0


def test_detect_coordinate_request_and_response_schemas_include_smart_targeting_fields():
    api = Api(Flask(__name__))
    browser_schemas = register_browser_schemas(api)

    detect_request_props = browser_schemas["DetectCoordinatesRequest"].__schema__["properties"]
    detect_result_props = browser_schemas["DetectCoordinatesResult"].__schema__["properties"]
    detect_data_props = browser_schemas["DetectCoordinatesData"].__schema__["properties"]

    assert detect_request_props["hit_test"]["default"] == "off"
    assert detect_request_props["auto_snap"]["default"] == "off"
    assert detect_request_props["snap_radius"]["default"] == 96
    assert detect_request_props["include_debug"]["default"] is False
    assert detect_result_props["data"]["allOf"] == [{"$ref": "#/definitions/DetectCoordinatesData"}]
    assert "resolved_click_point" in detect_data_props
    assert "outcome_status" in detect_data_props
    assert "resolved_target" in detect_data_props
    assert "snap_result" in detect_data_props
    assert "recommended_next_action" in detect_data_props


def test_gui_click_request_and_response_schemas_include_smart_targeting_fields():
    api = Api(Flask(__name__))
    browser_schemas = register_browser_schemas(api)

    gui_click_props = browser_schemas["GuiClickRequest"].__schema__["properties"]
    gui_click_xy_props = browser_schemas["GuiClickXYRequest"].__schema__["properties"]
    combined_gui_click_props = browser_schemas["CombinedGuiClickRequest"].__schema__["properties"]
    gui_result_props = browser_schemas["GuiClickResult"].__schema__["properties"]
    gui_data_props = browser_schemas["GuiClickData"].__schema__["properties"]

    assert gui_click_props["pre_click_validate"]["default"] == "off"
    assert gui_click_props["auto_snap"]["default"] == "off"
    assert gui_click_props["post_click_feedback"]["default"] == "none"
    assert gui_click_props["post_click_timeout_ms"]["default"] == 1500
    assert gui_click_props["return_content"]["default"] is False
    assert gui_click_props["content_limit_chars"]["default"] == 4000
    assert gui_click_props["include_debug"]["default"] is False
    assert gui_click_xy_props["pre_click_validate"]["default"] == "off"
    assert gui_click_xy_props["auto_snap"]["default"] == "off"
    assert combined_gui_click_props["pre_click_validate"]["default"] == "off"
    assert combined_gui_click_props["post_click_feedback"]["default"] == "none"
    assert gui_result_props["data"]["allOf"] == [{"$ref": "#/definitions/GuiClickData"}]
    assert "execution" in gui_data_props
    assert "message" in gui_data_props
    assert "precheck" in gui_data_props
    assert "postcheck" in gui_data_props
    assert "outcome_status" in gui_data_props
    assert "recommended_next_action" in gui_data_props
    assert "success" in gui_data_props
