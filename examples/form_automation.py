#!/usr/bin/env python3
"""
Form Automation Example

Demonstrates: filling forms, clicking buttons, waiting for elements,
and handling common web interactions that AI agents need.
"""

import time

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi

import os
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def main():
    config = Configuration(host=API_BASE)

    with ApiClient(config) as client:
        api = BrowserApi(client)

        # Create browser
        print("Creating browser...")
        response = api.create_browser(payload={
            "uc": True,
            "headless": False,
            "window_size": [1366, 768]
        })
        browser_id = response.data['browser_id']
        print(f"Browser: {browser_id}")

        try:
            # Navigate to a form page (using httpbin as example)
            print("\nNavigating to test form...")
            api.navigate_browser(
                browser_id=browser_id,
                payload={"url": "https://httpbin.org/forms/post", "timeout": 30}
            )

            # Wait for form to be ready
            print("Waiting for form...")
            api.wait_element(
                browser_id=browser_id,
                payload={"selector": "form", "until": "visible", "timeout": 10}
            )

            # Fill text fields
            print("Filling form fields...")

            # Customer name
            api.type_text(
                browser_id=browser_id,
                payload={
                    "selector": "input[name='custname']",
                    "text": "John Doe"
                }
            )

            # Telephone
            api.type_text(
                browser_id=browser_id,
                payload={
                    "selector": "input[name='custtel']",
                    "text": "555-1234"
                }
            )

            # Email
            api.type_text(
                browser_id=browser_id,
                payload={
                    "selector": "input[name='custemail']",
                    "text": "john@example.com"
                }
            )

            # Click a radio button (pizza size)
            print("Selecting options...")
            api.click(
                browser_id=browser_id,
                payload={"selector": "input[value='medium']"}
            )

            # Check a checkbox (topping)
            api.click(
                browser_id=browser_id,
                payload={"selector": "input[name='topping'][value='cheese']"}
            )

            # Fill textarea
            api.type_text(
                browser_id=browser_id,
                payload={
                    "selector": "textarea[name='comments']",
                    "text": "Please deliver to the back door."
                }
            )

            # Take screenshot before submit
            print("\nTaking screenshot of filled form...")
            screenshot = api.take_screenshot(browser_id=browser_id, payload={})
            print(f"Screenshot: {screenshot.data.get('screenshot_url')}")

            # Submit the form
            print("\nSubmitting form...")
            api.click(
                browser_id=browser_id,
                payload={"selector": "button"}  # httpbin uses <button>Submit order</button>
            )

            # Wait for response page
            time.sleep(2)

            # Get the response content
            api.get_content(browser_id=browser_id)
            print("\nForm submitted! Response page loaded.")
            print(f"New URL: {api.get_url(browser_id=browser_id).data.get('url')}")

        finally:
            print("\nClosing browser...")
            api.close_browser(browser_id=browser_id)
            print("Done!")


if __name__ == "__main__":
    main()
