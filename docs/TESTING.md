# Testing Guide

This guide covers how to run and write tests for the Airbrowser project.

## Quick Start

```bash
# Run all tests in Docker (recommended)
./scripts/run_tests.sh

# Run specific tests
./scripts/run_tests.sh -k "test_health"

# Run with verbose output
./scripts/run_tests.sh -v
```

## Test Architecture

### Overview

Tests run inside Docker containers to ensure a consistent environment:

```
┌─────────────────┐     ┌─────────────────┐
│   test-runner   │────▶│  browser-pool   │
│   (pytest)      │     │  (API server)   │
└─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Chrome browser │
                        │  (UC + CDP)     │
                        └─────────────────┘
```

### Test Files

Test files are in the `tests/` directory:

```bash
# List all test files
ls tests/test_*.py

# See all available tests
pytest tests/ --collect-only
```

### Test Markers

Tests are organized with pytest markers. View available markers:

```bash
# List all registered markers
pytest --markers

# Run tests by marker
pytest tests/ -m "browser"
pytest tests/ -m "not slow"
```

## Running Tests

### Docker (Recommended)

The `run_tests.sh` script handles everything:

```bash
# Run all tests
./scripts/run_tests.sh

# Run with forced rebuild
./scripts/run_tests.sh --build

# Run specific tests by name
./scripts/run_tests.sh -k "test_health"

# Run specific tests by marker
./scripts/run_tests.sh -m "quick"

# Stop on first failure
./scripts/run_tests.sh -x

# Show browser-pool logs on failure
./scripts/run_tests.sh --logs

# Keep containers running after tests
./scripts/run_tests.sh --no-cleanup
```

### Local Development

For faster iteration during development:

```bash
# 1. Start the browser-pool server
docker compose up -d browser-pool

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install test dependencies
pip install pytest pytest-xdist pytest-timeout

# 4. Install generated client
pip install -e generated-clients/python

# 5. Run tests
pytest tests/ -v

# 6. Run specific test file
pytest tests/test_all_endpoints.py -v

# 7. Run specific test function
pytest tests/test_all_endpoints.py::TestBrowserEndpoints::test_health_check -v
```

### Parallel Execution

Tests run in parallel by default. Check `pytest.ini` for current worker count:

```bash
# See current parallel config
grep -E "^\s+-n" pytest.ini

# Sequential execution
pytest tests/ -n 0

# Auto-detect CPU count
pytest tests/ -n auto
```

**Two-Phase Execution:** The test runner (`docker/test-entrypoint.sh`) automatically runs tests in two phases:
1. Parallel tests (excluding `close_all` tests)
2. Sequential `close_all` tests (to avoid closing other tests' browsers)

This is handled automatically by `./scripts/run_tests.sh`.

## Test Configuration

### pytest.ini

See `pytest.ini` in the project root for current configuration:

```bash
# View pytest configuration
cat pytest.ini

# List registered markers
pytest --markers | head -20
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `http://localhost:8000/api/v1` | API server URL |
| `PYTEST_ARGS` | | Additional pytest arguments |

### conftest.py Fixtures

See `tests/conftest.py` for available fixtures:

```bash
# List all fixtures with descriptions
pytest --fixtures tests/conftest.py

# View fixture source code
cat tests/conftest.py
```

## Writing Tests

### Basic Test Structure

```python
import pytest
import airbrowser_client
from airbrowser_client.api import browser_api
from airbrowser_client.models import BrowserConfig, NavigateRequest


def get_api_base_url():
    import os
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.mark.browser
def test_create_and_navigate():
    """Test creating a browser and navigating to a URL."""
    # Setup client
    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))

    browser_id = None

    try:
        # Create browser
        config = BrowserConfig(window_size=[1920, 1080])
        result = client.create_browser(payload=config)
        assert result.success
        browser_id = result.data.browser_id

        # Navigate
        nav_request = NavigateRequest(url="https://example.com")
        nav_result = client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success

        # Verify URL
        url_result = client.get_url(browser_id)
        assert url_result.success
        assert "example.com" in url_result.data.url

    finally:
        # Always cleanup
        if browser_id:
            try:
                client.close_browser(browser_id)
            except Exception:
                pass
```

### Using Fixtures

```python
import pytest
from airbrowser_client.models import BrowserConfig


@pytest.mark.browser
def test_with_fixture(browser_client):
    """Test using the browser_client fixture."""
    browser_id = None

    try:
        config = BrowserConfig(window_size=[1920, 1080])
        result = browser_client.create_browser(payload=config)
        assert result.success
        browser_id = result.data.browser_id

        # ... test logic ...

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass
```

### Test Class Pattern

```python
import pytest
import time


class TestBrowserOperations:
    """Group related browser tests."""

    @pytest.fixture(autouse=True)
    def setup(self, browser_client):
        """Setup for each test."""
        self.client = browser_client
        self.browser_id = None
        yield
        # Cleanup
        if self.browser_id:
            try:
                self.client.close_browser(self.browser_id)
            except Exception:
                pass

    def create_browser(self):
        """Helper to create browser."""
        from airbrowser_client.models import BrowserConfig
        config = BrowserConfig(window_size=[1280, 720])
        result = self.client.create_browser(payload=config)
        assert result.success
        self.browser_id = result.data.browser_id
        time.sleep(2)  # Wait for browser to initialize
        return self.browser_id

    @pytest.mark.browser
    def test_navigation(self):
        """Test browser navigation."""
        self.create_browser()
        # ... test navigation ...

    @pytest.mark.browser
    def test_screenshot(self):
        """Test taking screenshot."""
        self.create_browser()
        # ... test screenshot ...
```

### Marking Slow Tests

```python
@pytest.mark.slow
@pytest.mark.browser
def test_complex_workflow():
    """This test takes a long time."""
    # ... complex test ...
```

Run excluding slow tests:
```bash
pytest tests/ -m "not slow"
```

## Debugging Tests

### View Browser (noVNC)

When running in Docker, access the browser visually:

1. Start services: `docker compose up -d browser-pool`
2. Open http://localhost:6080 in your browser
3. Run tests and watch the browser

### Verbose Output

```bash
# More verbose
pytest tests/ -v

# Even more verbose
pytest tests/ -vv

# Show print statements
pytest tests/ -s

# Combined
pytest tests/ -vvs
```

### Stop on Failure

```bash
# Stop at first failure
pytest tests/ -x

# Stop after N failures
pytest tests/ --maxfail=3
```

### Debug Single Test

```bash
# Run single test with full output
pytest tests/test_all_endpoints.py::TestBrowserEndpoints::test_health_check -vvs

# With pdb debugger on failure
pytest tests/test_all_endpoints.py -x --pdb
```

### Check Browser Logs

```bash
# View browser-pool logs
docker compose logs browser-pool

# Follow logs in real-time
docker compose logs -f browser-pool

# After test failure
./scripts/run_tests.sh --logs
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: ./scripts/run_tests.sh

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: tests/.pytest_cache/
```

### Test in CI without Display

Tests work in headless CI environments because browsers run inside Docker with a virtual display (Xvfb).

## Troubleshooting

### Tests Timeout

```bash
# Increase timeout
pytest tests/ --timeout=300

# Or disable timeout
pytest tests/ --timeout=0
```

### Browser Not Starting

```bash
# Check browser-pool health
curl http://localhost:8000/health

# Check logs
docker compose logs browser-pool

# Restart services
docker compose restart browser-pool
```

### Import Errors

```bash
# Regenerate client
./scripts/generate_client.sh

# Reinstall client
pip install -e generated-clients/python --force-reinstall
```

### Port Conflicts

```bash
# Check what's using port 8000
lsof -i :8000

# Stop all containers
docker compose down -v
```

### Flaky Tests

Some tests may be flaky due to:
- Network timing
- Browser initialization delays
- External website changes

Solutions:
- Use `pytest-rerunfailures` to automatically retry flaky tests:
  ```bash
  pytest tests/ --reruns 3 --reruns-delay 2
  ```
- Add appropriate `time.sleep()` delays for browser operations
- Use explicit waits instead of fixed delays when possible
- Mock external dependencies when possible
