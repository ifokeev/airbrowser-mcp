from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


def pytest_configure():
    """
    Make the in-repo OpenAPI-generated Python client importable without requiring
    `pip install -e generated-clients/python`.
    """
    repo_root = Path(__file__).resolve().parents[1]

    generated_python_root = repo_root / "generated-clients" / "python"
    if generated_python_root.exists():
        sys.path.insert(0, str(generated_python_root))

    src_root = repo_root / "src"
    if src_root.exists():
        sys.path.insert(0, str(src_root))


def get_api_base_url():
    """Get the API base URL from environment or default to localhost."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.fixture(scope="session")
def api_base_url():
    """Fixture providing the API base URL."""
    return get_api_base_url()


@pytest.fixture(scope="session")
def api_configuration():
    """Fixture providing a configured API client configuration."""
    import airbrowser_client

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    return configuration


@pytest.fixture(scope="session")
def health_client(api_configuration):
    """Fixture providing a HealthApi client."""
    import airbrowser_client
    from airbrowser_client.api import health_api

    return health_api.HealthApi(airbrowser_client.ApiClient(api_configuration))


@pytest.fixture(scope="session")
def browser_client(api_configuration):
    """Fixture providing a BrowserApi client."""
    import airbrowser_client
    from airbrowser_client.api import browser_api

    return browser_api.BrowserApi(airbrowser_client.ApiClient(api_configuration))


@pytest.fixture(scope="session")
def pool_client(api_configuration):
    """Fixture providing a PoolApi client."""
    import airbrowser_client
    from airbrowser_client.api import pool_api

    return pool_api.PoolApi(airbrowser_client.ApiClient(api_configuration))


@pytest.fixture(scope="session")
def profiles_client(api_configuration):
    """Fixture providing a ProfilesApi client."""
    import airbrowser_client
    from airbrowser_client.api import profiles_api

    return profiles_api.ProfilesApi(airbrowser_client.ApiClient(api_configuration))
