#!/usr/bin/env python3
"""
Parallel Browsers Example

Demonstrates: running multiple browsers concurrently for parallel scraping,
testing, or automation tasks. Shows proper resource management.
"""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi

# Optional: aiohttp for async version
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

# Configuration - use env var for Docker/CI, default for local dev
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")

# URLs to visit in parallel
URLS = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://jsonplaceholder.typicode.com",
    "https://news.ycombinator.com",
]


def process_url(url: str, browser_num: int) -> dict:
    """Process a single URL with its own browser instance."""

    config = Configuration(host=API_BASE)
    result = {"url": url, "browser": browser_num, "success": False}

    with ApiClient(config) as client:
        api = BrowserApi(client)

        # Create browser
        try:
            response = api.create_browser(payload={
                "uc": True,
                "headless": True,  # Headless for parallel execution
                "window_size": [1280, 800]
            })
            browser_id = response.data.browser_id
            result["browser_id"] = browser_id
            print(f"[Browser {browser_num}] Created: {browser_id[:8]}...")

        except Exception as e:
            result["error"] = f"Failed to create browser: {e}"
            return result

        try:
            # Navigate
            print(f"[Browser {browser_num}] Navigating to {url}...")
            api.navigate_browser(
                browser_id=browser_id,
                payload={"url": url, "timeout": 30}
            )

            # Get page info
            content = api.get_content(browser_id=browser_id)
            result["title"] = content.data.title

            # Take screenshot
            screenshot = api.take_screenshot(browser_id=browser_id)
            result["screenshot"] = screenshot.data.screenshot_url

            result["success"] = True
            print(f"[Browser {browser_num}] Done: {result['title'][:40]}...")

        except Exception as e:
            result["error"] = str(e)
            print(f"[Browser {browser_num}] Error: {e}")

        finally:
            # Always clean up
            try:
                api.delete_browser(browser_id=browser_id)
                print(f"[Browser {browser_num}] Closed")
            except Exception:
                pass

    return result


def run_parallel_sync():
    """Run browsers in parallel using ThreadPoolExecutor."""

    print(f"\nProcessing {len(URLS)} URLs with parallel browsers...")
    print("=" * 60)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_url, url, i)
            for i, url in enumerate(URLS)
        ]

        results = [f.result() for f in futures]

    return results


async def run_parallel_async():
    """Alternative: run with asyncio + aiohttp for higher concurrency."""

    async def process_url_async(session: aiohttp.ClientSession, url: str, num: int):
        result = {"url": url, "browser": num, "success": False}

        try:
            # Create browser
            async with session.post(f"{API_BASE}/browser/create", json={
                "uc": True, "headless": True
            }) as resp:
                data = await resp.json()
                browser_id = data["data"]["browser_id"]
                result["browser_id"] = browser_id

            # Navigate
            async with session.post(
                f"{API_BASE}/browser/{browser_id}/navigate",
                json={"url": url, "timeout": 30}
            ) as resp:
                await resp.json()

            # Get content
            async with session.get(f"{API_BASE}/browser/{browser_id}/content") as resp:
                data = await resp.json()
                result["title"] = data["data"]["title"]

            # Screenshot
            async with session.post(
                f"{API_BASE}/browser/{browser_id}/screenshot"
            ) as resp:
                data = await resp.json()
                result["screenshot"] = data["data"]["screenshot_url"]

            result["success"] = True

            # Cleanup
            await session.delete(f"{API_BASE}/browser/{browser_id}")

        except Exception as e:
            result["error"] = str(e)

        return result

    print(f"\nProcessing {len(URLS)} URLs with async parallel browsers...")
    print("=" * 60)

    async with aiohttp.ClientSession() as session:
        tasks = [
            process_url_async(session, url, i)
            for i, url in enumerate(URLS)
        ]
        results = await asyncio.gather(*tasks)

    return results


def main():
    print("=" * 60)
    print("Parallel Browsers Example")
    print("=" * 60)

    # Method 1: ThreadPoolExecutor (synchronous client)
    results = run_parallel_sync()

    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    for r in results:
        status = "OK" if r["success"] else "FAILED"
        title = r.get("title", r.get("error", "unknown"))[:50]
        print(f"[{status}] {r['url']}")
        print(f"        {title}")

    successful = sum(1 for r in results if r["success"])
    print(f"\nCompleted: {successful}/{len(results)} successful")

    # Uncomment to try async version:
    # results = asyncio.run(run_parallel_async())


if __name__ == "__main__":
    main()
