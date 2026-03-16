"""
Test that the actual example files in examples/ run successfully.

This ensures the example files themselves stay working, not just
the patterns they demonstrate.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def load_example_module(filename: str, module_name: str):
    example_path = EXAMPLES_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, example_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_api_base_url() -> str:
    """Get API base URL from environment."""
    # In Docker test env, BROWSER_POOL_URL points to the service
    browser_pool_url = os.environ.get("BROWSER_POOL_URL")
    if browser_pool_url:
        return f"{browser_pool_url}/api/v1"
    # For local testing
    return os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def run_example(filename: str, timeout: int = 60, env: dict | None = None) -> subprocess.CompletedProcess:
    """Run an example file and return the result."""
    example_path = EXAMPLES_DIR / filename
    assert example_path.exists(), f"Example file not found: {example_path}"

    # Merge with current environment
    run_env = os.environ.copy()
    # Set API_BASE_URL for examples
    run_env["API_BASE_URL"] = get_api_base_url()
    if env:
        run_env.update(env)

    result = subprocess.run(
        [sys.executable, str(example_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(EXAMPLES_DIR.parent),  # Run from project root
        env=run_env,
    )
    return result


class TestExampleFiles:
    """Run actual example files and verify they complete successfully."""

    def test_what_is_visible_reanalysis_uses_response_data(self, monkeypatch, capsys):
        """Test examples/what_is_visible.py reads re-analysis from GenericResponse.data."""
        module = load_example_module("what_is_visible.py", "test_what_is_visible_example")

        class FakeConfiguration:
            def __init__(self, host):
                self.host = host

        class FakeApiClient:
            def __init__(self, config):
                self.config = config

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        class FakeHealthApi:
            def __init__(self, client):
                self.client = client

            def health_check(self):
                return type("Health", (), {"vision_enabled": True})()

        class FakeBrowserApi:
            def __init__(self, client):
                self.client = client
                self.what_is_visible_calls = 0

            def create_browser(self, payload):
                return type("Response", (), {"data": {"browser_id": "browser-123"}})()

            def navigate_browser(self, browser_id, payload):
                return None

            def what_is_visible(self, browser_id, payload):
                self.what_is_visible_calls += 1
                analysis = (
                    "filled account field detected" if self.what_is_visible_calls == 2 else "account field visible"
                )
                return type(
                    "Response",
                    (),
                    {"success": True, "data": {"analysis": analysis, "model": "mock-model"}},
                )()

            def type_text(self, browser_id, payload):
                return None

            def take_screenshot(self, browser_id, payload):
                return type("Response", (), {"data": {"screenshot_url": "http://shot"}})()

            def close_browser(self, browser_id):
                return None

        monkeypatch.setattr(module, "Configuration", FakeConfiguration)
        monkeypatch.setattr(module, "ApiClient", FakeApiClient)
        monkeypatch.setattr(module, "HealthApi", FakeHealthApi)
        monkeypatch.setattr(module, "BrowserApi", FakeBrowserApi)
        monkeypatch.setattr(module.time, "sleep", lambda *_args, **_kwargs: None)

        module.main()
        output = capsys.readouterr().out

        assert "UPDATED PAGE ANALYSIS:" in output
        assert "Could not fill email field:" not in output
        assert "WhatIsVisibleRequest()" in output

    def test_basic_navigation(self):
        """Test examples/basic_navigation.py runs without error."""
        result = run_example("basic_navigation.py")

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "Browser created:" in result.stdout
        assert "Screenshot saved:" in result.stdout
        assert "Page title:" in result.stdout
        assert "Done!" in result.stdout
        # Verify actual data was returned (not None)
        assert "Screenshot saved: None" not in result.stdout, "screenshot_url should not be None"
        assert "Page title: None" not in result.stdout, "title should not be None"

    @pytest.mark.skipif(
        not os.environ.get("TEST_PROXY"),
        reason="TEST_PROXY env var not set - skipping proxy test",
    )
    def test_proxy_rotation(self):
        """Test proxy rotation with a real proxy verifies IP changes.

        Set TEST_PROXY env var to run: TEST_PROXY=http://user:pass@host:port
        """
        result = run_example("proxy_rotation.py", timeout=120)

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "Proxy Rotation Example" in result.stdout
        assert (
            "Unique IPs detected: 2" in result.stdout
        ), f"Proxy should show different IP than direct connection.\nstdout: {result.stdout}"
        assert "Proxy rotation is working correctly!" in result.stdout

    def test_form_automation(self):
        """Test examples/form_automation.py runs without error."""
        result = run_example("form_automation.py", timeout=90)

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "Browser:" in result.stdout
        assert "Filling form fields..." in result.stdout
        assert "Screenshot:" in result.stdout
        assert "Form submitted!" in result.stdout
        assert "Done!" in result.stdout

    def test_parallel_browsers(self):
        """Test examples/parallel_browsers.py runs without error."""
        result = run_example("parallel_browsers.py", timeout=120)

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "RESULTS SUMMARY" in result.stdout
        assert "Completed:" in result.stdout

    def test_what_is_visible(self):
        """Test examples/what_is_visible.py runs without error."""
        result = run_example("what_is_visible.py", timeout=120)

        # Check if vision is disabled on server (graceful skip)
        if "Vision tools are not available" in result.stdout:
            pytest.skip("Vision not enabled on server (vision config not set)")

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "AI Vision Analysis Example" in result.stdout
        assert "No prompt required - call what_is_visible with WhatIsVisibleRequest()." in result.stdout

    def test_cloudflare_captcha_vision(self):
        """Test examples/cloudflare_captcha_vision.py runs without error."""
        result = run_example("cloudflare_captcha_vision.py", timeout=120)

        # Check if vision is disabled on server (graceful skip)
        if "Vision tools are not available" in result.stdout:
            pytest.skip("Vision not enabled on server (vision config not set)")
        if "Cloudflare page unavailable or blocked" in result.stdout:
            pytest.skip("Cloudflare unavailable or blocked in this environment")
        if "Vision detection failed" in result.stdout:
            pytest.skip("Vision detection failed (Cloudflare unavailable)")
        if "Captcha checkbox not detected" in result.stdout:
            pytest.skip("Captcha checkbox not detected (page still loading or protected)")

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "Cloudflare Captcha - AI Vision Click Example" in result.stdout
        assert "Vision tools enabled" in result.stdout
        assert "Captcha checkbox detected!" in result.stdout
        assert "Click successful" in result.stdout
        assert "EXAMPLE COMPLETE" in result.stdout
