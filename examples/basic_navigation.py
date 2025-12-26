#!/usr/bin/env python3
"""
Basic Navigation Example

Demonstrates: creating a browser, navigating to URLs, taking screenshots,
and cleaning up. This is the simplest starting point for airbrowser.
"""

import os

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi

# Configuration - use env var for Docker/CI, default for local dev
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def main():
    # Setup client
    config = Configuration(host=API_BASE)

    with ApiClient(config) as client:
        api = BrowserApi(client)

        # 1. Create an undetectable browser
        print("Creating browser...")
        response = api.create_browser(payload={"window_size": [1280, 800]})
        browser_id = response.data["browser_id"]
        print(f"Browser created: {browser_id}")

        try:
            # 2. Navigate to a URL
            print("Navigating to example.com...")
            api.navigate_browser(browser_id=browser_id, payload={"url": "https://example.com", "timeout": 30})
            print("Navigation complete")

            # 3. Get current URL (verify navigation worked)
            url_response = api.get_url(browser_id=browser_id)
            print(f"Current URL: {url_response.data.get('url')}")

            # 4. Take a screenshot
            print("Taking screenshot...")
            screenshot = api.take_screenshot(browser_id=browser_id, payload={})
            print(f"Screenshot saved: {screenshot.data.get('screenshot_url')}")

            # 5. Get page content (HTML)
            content = api.get_content(browser_id=browser_id)
            print(f"Page title: {content.data.get('title')}")

        finally:
            # 6. Always clean up
            print("Closing browser...")
            api.close_browser(browser_id=browser_id)
            print("Done!")


if __name__ == "__main__":
    main()
