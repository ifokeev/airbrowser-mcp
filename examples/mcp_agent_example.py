#!/usr/bin/env python3
"""
MCP Agent Integration Example

Demonstrates: using airbrowser with MCP (Model Context Protocol) for
AI agent integration. This is the recommended approach for LLM-based agents.

Requirements:
    pip install fastmcp

MCP Endpoint: http://localhost:18080/mcp
"""

import asyncio

from fastmcp import Client


async def main():
    """Example of an AI agent using MCP to control browsers."""

    print("Connecting to airbrowser MCP server...")

    async with Client("http://localhost:18080/mcp") as client:
        # List available tools (useful for agent discovery)
        tools = await client.list_tools()
        print(f"\nAvailable MCP tools: {len(tools)}")
        for tool in tools[:5]:  # Show first 5
            print(f"  - {tool.name}: {tool.description[:60]}...")

        # 1. Create a browser
        print("\n--- Creating Browser ---")
        result = await client.call_tool("create_browser", {"window_size": [1280, 800]})
        browser_id = result["browser_id"]
        print(f"Browser created: {browser_id}")

        try:
            # 2. Navigate to a page
            print("\n--- Navigating ---")
            await client.call_tool(
                "navigate_browser", {"browser_id": browser_id, "url": "https://news.ycombinator.com"}
            )
            print("Navigated to Hacker News")

            # 3. Use AI vision to understand the page
            #    (requires OPENROUTER_API_KEY environment variable)
            print("\n--- Analyzing Page with AI Vision ---")
            try:
                analysis = await client.call_tool("what_is_visible", {"browser_id": browser_id})
                print("Page analysis:")
                print(analysis.get("analysis", "No analysis available")[:500])
            except Exception as e:
                print(f"Vision analysis not available: {e}")
                print("(Set OPENROUTER_API_KEY to enable AI vision)")

            # 4. Take a screenshot
            print("\n--- Taking Screenshot ---")
            screenshot = await client.call_tool("take_screenshot", {"browser_id": browser_id, "full_page": False})
            screenshot_url = screenshot.get("data", {}).get("screenshot_url", "saved")
            print(f"Screenshot: {screenshot_url}")

            # 5. Click on an element
            print("\n--- Clicking First Story ---")
            await client.call_tool(
                "click",
                {
                    "browser_id": browser_id,
                    "selector": ".titleline a",  # First story link
                },
            )
            print("Clicked first story")

            # 6. Get current URL
            await asyncio.sleep(2)  # Wait for navigation
            url_result = await client.call_tool("get_url", {"browser_id": browser_id})
            current_url = url_result.get("data", {}).get("url", "unknown")
            print(f"Now at: {current_url}")

            # 7. Execute JavaScript (get page title)
            print("\n--- Executing JavaScript ---")
            js_result = await client.call_tool(
                "execute_script", {"browser_id": browser_id, "script": "return document.title;"}
            )
            script_result = js_result.get("data", {}).get("result", {})
            title = script_result.get("value", "unknown") if script_result else "unknown"
            print(f"Page title: {title}")

        finally:
            # 8. Clean up
            print("\n--- Closing Browser ---")
            await client.call_tool("close_browser", {"browser_id": browser_id})
            print("Browser closed")

    print("\nMCP example complete!")


# MCP Configuration for AI Agents
MCP_CONFIG_EXAMPLE = """
# Add to your AI agent's MCP configuration (Claude Desktop, Cursor, Cline, etc.):

{
  "mcpServers": {
    "airbrowser": {
      "url": "http://localhost:18080/mcp",
      "transport": "http"
    }
  }
}

# Claude Code CLI:
# claude mcp add airbrowser --transport http http://localhost:18080/mcp
"""

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Agent Integration Example")
    print("=" * 60)
    print("\nMake sure airbrowser is running:")
    print("  docker compose up")
    print("\nMCP endpoint: http://localhost:18080/mcp")
    print("=" * 60)

    asyncio.run(main())
