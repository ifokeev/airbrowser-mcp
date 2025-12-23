"""
Test that the actual example files in examples/ run successfully.

This ensures the example files themselves stay working, not just
the patterns they demonstrate.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def get_api_base_url() -> str:
    """Get API base URL from environment."""
    # In Docker test env, BROWSER_POOL_URL points to the service
    browser_pool_url = os.environ.get("BROWSER_POOL_URL")
    if browser_pool_url:
        return f"{browser_pool_url}/api/v1"
    # For local testing
    return os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def run_example(filename: str, timeout: int = 60, env: dict = None) -> subprocess.CompletedProcess:
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

    def test_proxy_rotation(self):
        """Test examples/proxy_rotation.py runs without error."""
        result = run_example("proxy_rotation.py")

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "Proxy Rotation Example" in result.stdout
        assert "Detected IP:" in result.stdout

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

    @pytest.mark.skipif(
        not os.environ.get("OPENROUTER_API_KEY"),
        reason="Requires OPENROUTER_API_KEY environment variable"
    )
    def test_what_is_visible(self):
        """Test examples/what_is_visible.py runs without error."""
        result = run_example("what_is_visible.py", timeout=120)

        assert result.returncode == 0, f"Example failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        assert "AI Vision Analysis Example" in result.stdout
