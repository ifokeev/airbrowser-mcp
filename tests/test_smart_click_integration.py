import os
import time

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    DetectCoordinatesRequest,
    EmulateRequest,
    ExecuteScriptRequest,
    GuiClickRequest,
    NavigateBrowserRequest,
)

pytestmark = pytest.mark.isolated


def has_vision_config() -> bool:
    return all(os.environ.get(name) for name in ("VISION_API_BASE_URL", "VISION_API_KEY", "VISION_MODEL"))


def result_to_dict(value):
    if value is None or isinstance(value, dict):
        return value
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if hasattr(value, "model_dump"):
        return value.model_dump(by_alias=True)
    return value


def execute_script_value(browser_client, browser_id, script: str):
    result = browser_client.execute_script(browser_id, payload=ExecuteScriptRequest(script=script))
    assert result is not None and result.success
    payload = result.data.get("result") if isinstance(result.data, dict) else None
    if isinstance(payload, dict):
        return payload.get("value")
    return payload


def screen_point_from_resolver(browser_client, browser_id, resolver: str, fx: float = 0.5, fy: float = 0.5):
    script = f"""
        const resolver = new Function({resolver!r});
        const fx = {fx};
        const fy = {fy};
        const element = resolver();
        if (!element) return null;
        try {{
            element.scrollIntoView({{block: 'center', inline: 'nearest'}});
        }} catch (error) {{
            // Ignore scroll failures and use current geometry.
        }}
        const rect = element.getBoundingClientRect();
        const vv = window.visualViewport || {{scale: 1, offsetLeft: 0, offsetTop: 0}};
        const scale = Number(vv.scale) || 1;
        const offsetLeft = Number(vv.offsetLeft) || 0;
        const offsetTop = Number(vv.offsetTop) || 0;
        return {{
            x: window.screenX + (rect.left + rect.width * fx + offsetLeft) * scale,
            y: window.screenY + (window.outerHeight - window.innerHeight)
                + (rect.top + rect.height * fy + offsetTop) * scale,
        }};
        """
    value = execute_script_value(
        browser_client,
        browser_id,
        script,
    )
    assert value is not None, f"resolver did not return an element: {resolver}"
    return float(value["x"]), float(value["y"])


def detect_with_retry(browser_client, browser_id, prompt: str, attempts: int = 3, delay: float = 1.0):
    last_result = None
    last_data = None
    for attempt in range(1, attempts + 1):
        last_result = browser_client.detect_coordinates(
            browser_id,
            payload=DetectCoordinatesRequest(
                prompt=prompt,
                hit_test="strict",
                auto_snap="nearest_clickable",
            ),
        )
        last_data = result_to_dict(last_result.data) or {}
        if last_result.success and last_data.get("click_point"):
            return last_result, last_data
        if attempt < attempts:
            time.sleep(delay)
    return last_result, last_data or {}


@pytest.fixture
def browser_session(browser_client):
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    if result is None or not result.success:
        message = None if result is None else result.message
        pytest.skip(f"Browser environment unavailable for smart click integration tests: {message}")
    browser_id = result.data["browser_id"]

    navigate_result = browser_client.navigate_browser(
        browser_id,
        payload=NavigateBrowserRequest(url="https://example.com"),
    )
    if navigate_result is None or not navigate_result.success:
        try:
            browser_client.close_browser(browser_id)
        except Exception:
            pass
        message = None if navigate_result is None else navigate_result.message
        pytest.skip(f"Browser navigation unavailable for smart click integration tests: {message}")

    yield browser_id

    try:
        browser_client.close_browser(browser_id)
    except Exception:
        pass


@pytest.mark.browser
@pytest.mark.skipif(not has_vision_config(), reason="Vision config not set")
def test_example_domain_detect_then_gui_click_snaps_and_navigates(browser_client, browser_session):
    browser_id = browser_session
    detect_result, detect_data = detect_with_retry(browser_client, browser_id, "the Learn more link near the paragraph")

    assert detect_result is not None and detect_result.success is True
    assert detect_data["outcome_status"] == "snapped_match"
    assert detect_data["resolved_click_point"] != detect_data["click_point"]

    raw_point = detect_data["click_point"]
    click = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=float(raw_point["x"]),
            y=float(raw_point["y"]),
            pre_click_validate="strict",
            auto_snap="nearest_clickable",
            post_click_feedback="auto",
            post_click_timeout_ms=500,
        ),
    )

    assert click.success is True
    click_data = result_to_dict(click.data) or {}
    assert click_data["outcome_status"] == "clicked_snapped"
    assert click_data["postcheck"]["status"] == "url_changed"
    assert click_data["postcheck"]["after_url"].startswith("https://www.iana.org/help/example-domains")


@pytest.mark.browser
def test_iframe_boundary_returns_switch_to_iframe_context(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = `
            <div style="padding: 40px;">
                <iframe
                    id="demo-frame"
                    srcdoc="<!doctype html><html><body style='margin:0;display:flex;align-items:center;justify-content:center;min-height:160px;'><button id='inside-frame'>Inside frame</button></body></html>"
                    style="width: 320px; height: 180px; border: 2px solid #333;"
                ></iframe>
            </div>
        `;
        return true;
        """,
    )
    x, y = screen_point_from_resolver(browser_client, browser_id, "return document.querySelector('#demo-frame');")

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="nearest_clickable",
        ),
    )

    assert result.success is False
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] == "click_failed_precheck"
    assert data["reason"] == "hit_iframe_boundary"
    assert data["recommended_next_action"] == "switch_to_iframe_context"


@pytest.mark.browser
def test_open_shadow_root_click_succeeds(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = '<div id="shadow-output">Idle</div><open-box-element id="open-host"></open-box-element>';
        if (!customElements.get('open-box-element')) {
            customElements.define('open-box-element', class extends HTMLElement {
                connectedCallback() {
                    if (this.shadowRoot) return;
                    const root = this.attachShadow({mode: 'open'});
                    root.innerHTML = '<button id="shadow-button" type="button" style="width:220px;height:56px;">Open shadow action</button>';
                    root.getElementById('shadow-button').addEventListener('click', () => {
                        document.getElementById('shadow-output').textContent = 'Clicked from open shadow';
                    });
                }
            });
        }
        const host = document.getElementById('open-host');
        host.style.display = 'inline-block';
        host.style.margin = '40px';
        return true;
        """,
    )
    x, y = screen_point_from_resolver(
        browser_client,
        browser_id,
        "return document.querySelector('open-box-element').shadowRoot.querySelector('#shadow-button');",
    )

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="nearest_clickable",
            post_click_feedback="content",
            post_click_timeout_ms=200,
        ),
    )

    assert result.success is True
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] in {"clicked_exact", "clicked_snapped"}
    assert data["postcheck"]["status"] == "content_changed"


@pytest.mark.browser
def test_open_shadow_root_visible_postcheck_tracks_shadow_target(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = '<open-toggle-box id="open-toggle-host"></open-toggle-box>';
        if (!customElements.get('open-toggle-box')) {
            customElements.define('open-toggle-box', class extends HTMLElement {
                connectedCallback() {
                    if (this.shadowRoot) return;
                    const root = this.attachShadow({mode: 'open'});
                    root.innerHTML = `
                        <div
                            id="shadow-toggle"
                            role="button"
                            aria-pressed="false"
                            class="toggle"
                            style="display:block;width:220px;height:56px;line-height:56px;border:1px solid #333;"
                        >
                            Shadow toggle
                        </div>
                    `;
                    root.getElementById('shadow-toggle').addEventListener('click', (event) => {
                        const control = event.currentTarget;
                        const pressed = control.getAttribute('aria-pressed') === 'true';
                        control.setAttribute('aria-pressed', pressed ? 'false' : 'true');
                        control.className = pressed ? 'toggle' : 'toggle is-active';
                    });
                }
            });
        }
        const host = document.getElementById('open-toggle-host');
        host.style.display = 'inline-block';
        host.style.margin = '40px';
        return true;
        """,
    )
    x, y = screen_point_from_resolver(
        browser_client,
        browser_id,
        "return document.querySelector('open-toggle-box').shadowRoot.querySelector('#shadow-toggle');",
    )

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="off",
            post_click_feedback="visible",
            post_click_timeout_ms=200,
        ),
    )

    assert result.success is True
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] == "clicked_exact"
    assert data["postcheck"]["status"] == "visible_state_changed"
    assert set(data["postcheck"]["changed_fields"]) & {"pressed", "class_name"}


@pytest.mark.browser
def test_open_shadow_root_auto_snap_recovers_nearby_button(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = '<div id="shadow-output">Idle</div><open-snap-box id="open-snap-host"></open-snap-box>';
        if (!customElements.get('open-snap-box')) {
            customElements.define('open-snap-box', class extends HTMLElement {
                connectedCallback() {
                    if (this.shadowRoot) return;
                    const root = this.attachShadow({mode: 'open'});
                    root.innerHTML = `
                        <div id="shadow-shell" style="box-sizing:border-box;width:280px;height:120px;padding:32px 40px;background:#eef2f7;">
                            <button id="shadow-button" type="button" style="width:180px;height:56px;">Open shadow action</button>
                        </div>
                    `;
                    root.getElementById('shadow-button').addEventListener('click', () => {
                        document.getElementById('shadow-output').textContent = 'Clicked from open shadow snap';
                    });
                }
            });
        }
        const host = document.getElementById('open-snap-host');
        host.style.display = 'inline-block';
        host.style.margin = '40px';
        return true;
        """,
    )
    x, y = screen_point_from_resolver(
        browser_client, browser_id, "return document.querySelector('#open-snap-host');", 0.05, 0.5
    )

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="nearest_clickable",
            post_click_feedback="content",
            post_click_timeout_ms=200,
        ),
    )

    assert result.success is True
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] == "clicked_snapped"
    assert data["execution"]["mode"] == "snapped"
    assert data["postcheck"]["status"] == "content_changed"


@pytest.mark.browser
def test_closed_shadow_root_returns_boundary_result(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = '<closed-box-element id="closed-host"></closed-box-element>';
        if (!customElements.get('closed-box-element')) {
            customElements.define('closed-box-element', class extends HTMLElement {
                connectedCallback() {
                    const root = this.attachShadow({mode: 'closed'});
                    const button = document.createElement('button');
                    button.id = 'closed-button';
                    button.type = 'button';
                    button.textContent = 'Closed shadow action';
                    button.style.width = '220px';
                    button.style.height = '56px';
                    root.appendChild(button);
                }
            });
        }
        const host = document.getElementById('closed-host');
        host.style.display = 'inline-block';
        host.style.margin = '40px';
        host.style.width = '220px';
        host.style.height = '56px';
        host.style.border = '1px solid #333';
        return true;
        """,
    )
    x, y = screen_point_from_resolver(browser_client, browser_id, "return document.querySelector('#closed-host');")

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="nearest_clickable",
        ),
    )

    assert result.success is False
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] == "click_failed_precheck"
    assert data["reason"] == "shadow_boundary"
    assert data["recommended_next_action"] == "switch_to_selector_click"


@pytest.mark.browser
def test_reverse_transform_survives_scroll_and_chrome_offset(browser_client, browser_session):
    browser_id = browser_session
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = `
            <div style="height: 1200px;"></div>
            <button
                id="scrolled-button"
                type="button"
                style="display:block;width:220px;height:48px;margin:0 auto;"
                onclick="this.classList.add('clicked'); this.style.border='4px solid rgb(0, 128, 0)'; this.textContent='Clicked';"
            >
                Scroll target
            </button>
            <div style="height: 1400px;"></div>
        `;
        window.scrollTo(0, 0);
        return true;
        """,
    )
    x, y = screen_point_from_resolver(browser_client, browser_id, "return document.querySelector('#scrolled-button');")

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="off",
            post_click_feedback="visible",
            post_click_timeout_ms=200,
        ),
    )

    assert result.success is True
    data = result_to_dict(result.data) or {}
    assert data["outcome_status"] == "clicked_exact"
    assert data["execution"]["clicked_point"] == {"x": x, "y": y}
    assert data["postcheck"]["status"] == "visible_state_changed"


@pytest.mark.browser
def test_scaled_viewport_returns_stable_mapping_or_hit_test_unavailable(browser_client, browser_session):
    browser_id = browser_session
    emulate = browser_client.emulate(
        browser_id,
        payload=EmulateRequest(action="set", width=1280, height=720, device_scale_factor=1.5, mobile=False),
    )
    assert emulate is not None and emulate.success
    execute_script_value(
        browser_client,
        browser_id,
        """
        document.body.innerHTML = `
            <div style="padding: 64px;">
                <button
                    id="scaled-button"
                    type="button"
                    style="width:220px;height:48px;"
                    onclick="this.classList.add('clicked'); this.style.background='rgb(0, 128, 0)';"
                >
                    Scaled target
                </button>
            </div>
        `;
        return true;
        """,
    )
    x, y = screen_point_from_resolver(browser_client, browser_id, "return document.querySelector('#scaled-button');")

    result = browser_client.gui_click(
        browser_id,
        payload=GuiClickRequest(
            x=x,
            y=y,
            pre_click_validate="strict",
            auto_snap="off",
            post_click_feedback="visible",
            post_click_timeout_ms=200,
        ),
    )

    data = result_to_dict(result.data) or {}
    if result.success:
        assert data["outcome_status"] == "clicked_exact"
        assert data["postcheck"]["status"] == "visible_state_changed"
    else:
        if data["outcome_status"] == "click_failed_precheck":
            assert data["reason"] == "hit_test_unavailable"
            assert data["recommended_next_action"] == "inspect_page"
        else:
            assert data["outcome_status"] == "click_uncertain"
            assert data["precheck"]["outcome_status"] == "exact_match"
            assert data["execution"]["clicked_point"] == {"x": x, "y": y}
            assert data["postcheck"]["status"] == "no_observable_change"
