"""Test browser status lifecycle - browsers should appear immediately with 'creating' status."""

import concurrent.futures
import time


class TestBrowserStatusLifecycle:
    """Test that browsers appear in list immediately with status updates."""

    def test_browser_shows_creating_status_immediately(self, browser_client):
        """Browser should appear in list with 'creating' status before creation completes."""
        from airbrowser_client.models import BrowsersRequest, CreateBrowserRequest

        creating_status_seen = False
        browser_id_found = None

        def create_browser():
            """Create browser in background thread."""
            config = CreateBrowserRequest()
            return browser_client.create_browser(payload=config)

        def poll_for_creating_status(timeout=30):
            """Poll browser list looking for 'creating' status."""
            nonlocal creating_status_seen, browser_id_found
            start = time.time()

            while time.time() - start < timeout:
                try:
                    result = browser_client.browsers(payload=BrowsersRequest(action="list"))
                    if result.success and result.data.get("browsers", []):
                        for browser in result.data.get("browsers", []):
                            # browsers are returned as dicts
                            if browser.get("status") == "creating":
                                creating_status_seen = True
                                browser_id_found = browser.get("id")
                                return True
                except Exception:
                    pass

                time.sleep(0.2)

            return False

        # Run create and poll concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Start polling first
            poll_future = executor.submit(poll_for_creating_status)

            # Small delay then start creation
            time.sleep(0.1)
            create_future = executor.submit(create_browser)

            # Wait for both to complete
            create_result = create_future.result(timeout=120)
            poll_future.result(timeout=35)

        # Verify creation succeeded
        assert create_result.success is True, "Browser creation failed"
        created_browser_id = create_result.data["browser_id"]

        # Verify we saw 'creating' status
        assert creating_status_seen, "Browser should appear with 'creating' status during creation"

        # Verify browser now shows 'ready' status
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        created_browser = next(
            (b for b in list_result.data.get("browsers", []) if b.get("id") == created_browser_id), None
        )

        if created_browser:
            assert (
                created_browser.get("status") == "ready"
            ), f"Browser should be 'ready' after creation, got: {created_browser.get('status')}"

        # Cleanup
        if created_browser_id:
            browser_client.close_browser(created_browser_id)

    def test_browser_status_after_creation(self, browser_client):
        """Verify browser has 'ready' status after creation completes."""
        from airbrowser_client.models import BrowsersRequest, CreateBrowserRequest

        # Create browser (blocking call)
        config = CreateBrowserRequest()
        response = browser_client.create_browser(payload=config)

        assert response.success is True
        browser_id = response.data["browser_id"]

        try:
            # List browsers and check status
            list_response = browser_client.browsers(payload=BrowsersRequest(action="list"))
            browsers = list_response.data.get("browsers", [])

            # browsers are returned as dicts
            created_browser = next((b for b in browsers if b.get("id") == browser_id), None)
            assert created_browser is not None, "Created browser should be in list"
            assert (
                created_browser.get("status") == "ready"
            ), f"Expected 'ready' status, got: {created_browser.get('status')}"

        finally:
            # Cleanup
            browser_client.close_browser(browser_id)
