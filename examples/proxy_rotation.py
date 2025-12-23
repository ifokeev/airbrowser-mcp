#!/usr/bin/env python3
"""
Proxy Rotation Example

Demonstrates: using different proxies for different browser instances,
useful for avoiding rate limits and IP blocks during automation.
"""

import os
import time

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi

# Configuration - use env var for Docker/CI, default for local dev
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")

# Example proxy list (replace with your actual proxies)
# Supports: http://, https://, socks5://
# With auth: http://user:pass@host:port
PROXIES = [
    # "http://user:pass@proxy1.example.com:8080",
    # "socks5://user:pass@proxy2.example.com:1080",
    # "http://proxy3.example.com:3128",
    None,  # No proxy (direct connection) - for testing
]


def check_ip(api: BrowserApi, browser_id: str) -> str:
    """Navigate to IP check service and extract the IP."""

    api.navigate_browser(
        browser_id=browser_id,
        payload={"url": "https://api.ipify.org", "timeout": 30}
    )

    # Execute JS to get the text content
    result = api.execute_script(
        browser_id=browser_id,
        payload={"script": "return document.body.innerText;"}
    )

    # Result is wrapped in {"value": ...}
    if result.data.result:
        ip = result.data.result.get("value", "")
        return ip.strip() if ip else "unknown"
    return "unknown"


def main():
    print("=" * 60)
    print("Proxy Rotation Example")
    print("=" * 60)

    config = Configuration(host=API_BASE)
    results = []

    with ApiClient(config) as client:
        api = BrowserApi(client)

        for i, proxy in enumerate(PROXIES):
            print(f"\n--- Browser {i + 1} ---")
            print(f"Proxy: {proxy or 'None (direct)'}")

            # Create browser with specific proxy
            browser_config = {
                "uc": True,
                "headless": True,
                "window_size": [1280, 800]
            }

            if proxy:
                browser_config["proxy"] = proxy

            try:
                response = api.create_browser(payload=browser_config)
                browser_id = response.data.browser_id
                print(f"Browser created: {browser_id[:8]}...")

            except Exception as e:
                print(f"Failed to create browser: {e}")
                results.append({
                    "proxy": proxy,
                    "success": False,
                    "error": str(e)
                })
                continue

            try:
                # Check what IP this browser appears as
                ip = check_ip(api, browser_id)
                print(f"Detected IP: {ip}")

                results.append({
                    "proxy": proxy or "direct",
                    "success": True,
                    "ip": ip
                })

            except Exception as e:
                print(f"Error checking IP: {e}")
                results.append({
                    "proxy": proxy or "direct",
                    "success": False,
                    "error": str(e)
                })

            finally:
                # Clean up
                try:
                    api.delete_browser(browser_id=browser_id)
                    print("Browser closed")
                except Exception:
                    pass

            # Small delay between browsers
            time.sleep(1)

    # Summary
    print("\n" + "=" * 60)
    print("PROXY ROTATION SUMMARY")
    print("=" * 60)

    for r in results:
        if r["success"]:
            print(f"[OK]     {r['proxy']:40} -> IP: {r['ip']}")
        else:
            print(f"[FAILED] {r['proxy']:40} -> {r.get('error', 'unknown')}")

    # Check for unique IPs
    unique_ips = set(r["ip"] for r in results if r.get("success"))
    print(f"\nUnique IPs detected: {len(unique_ips)}")

    if len(unique_ips) > 1:
        print("Proxy rotation is working correctly!")
    elif len(unique_ips) == 1 and len(PROXIES) > 1:
        print("Warning: All browsers show same IP. Check proxy configuration.")


# Tips for proxy usage
PROXY_TIPS = """
PROXY CONFIGURATION TIPS
========================

1. Proxy formats supported:
   - HTTP:   http://host:port
   - HTTPS:  https://host:port
   - SOCKS5: socks5://host:port
   - With auth: http://user:pass@host:port

2. Recommended proxy providers for web automation:
   - Bright Data (brightdata.com) - residential proxies
   - Oxylabs (oxylabs.io) - datacenter & residential
   - SmartProxy (smartproxy.com) - rotating residential
   - IPRoyal (iproyal.com) - budget option

3. Best practices:
   - Use residential proxies for anti-bot protected sites
   - Rotate proxies per-session, not per-request
   - Match proxy location to target site's region
   - Keep browser fingerprint consistent with proxy location

4. Testing proxies:
   - https://api.ipify.org - simple IP check
   - https://httpbin.org/ip - returns JSON
   - https://whatismyipaddress.com - detailed info
"""

if __name__ == "__main__":
    main()
    print("\n" + PROXY_TIPS)
