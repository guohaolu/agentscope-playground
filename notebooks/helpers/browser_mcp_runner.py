"""Windows/Jupyter-friendly helper for running browser MCP actions.

This helper exists because running MCP stdio clients directly inside a
Jupyter notebook on Windows may hit event loop / subprocess compatibility
issues. The notebook calls plain synchronous functions from this file, while
this helper manages its own event loop internally.
"""

from __future__ import annotations

import asyncio
import re
import threading
from pathlib import Path
from typing import Any

from agentscope.mcp import StdIOStatefulClient
from agentscope.message import ToolUseBlock
from agentscope.tool import Toolkit


class BrowserMCPRunner:
    """Encapsulate one short-lived MCP browser session."""

    def __init__(self) -> None:
        # Toolkit is AgentScope's container for registered tools.
        self.toolkit = Toolkit()
        # We use Playwright MCP over stdio, which AgentScope can wrap as tools.
        self.browser_client = StdIOStatefulClient(
            name="playwright-mcp",
            command="npx",
            args=["@playwright/mcp@latest"],
        )

    async def _connect(self) -> None:
        """Connect to Playwright MCP and register browser tools."""
        await self.browser_client.connect()
        await self.toolkit.register_mcp_client(self.browser_client)

    async def _close(self) -> None:
        """Close the MCP client cleanly."""
        await self.browser_client.close()

    async def _call_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """Call one registered browser tool and return its last output chunk."""
        tool_request = ToolUseBlock(
            type="tool_use",
            id=f"call-{tool_name}",
            name=tool_name,
            input=kwargs,
        )

        chunks = []
        async for chunk in await self.toolkit.call_tool_function(tool_request):
            chunks.append(chunk.content)

        return chunks[-1] if chunks else None

    async def run_open_github(self) -> dict[str, Any]:
        """Open github.com, collect observable results, then return them."""
        await self._connect()
        try:
            tool_names = sorted(self.toolkit.tools.keys())

            navigate_result = await self._call_tool(
                "browser_navigate",
                url="https://github.com",
            )
            snapshot_result = await self._call_tool("browser_snapshot")
            tabs_result = await self._call_tool("browser_tabs")
            screenshot_result = await self._call_tool("browser_take_screenshot")

            screenshot_text = str(screenshot_result)
            match = re.search(r"\(([^)]+\.png)\)", screenshot_text)
            screenshot_path = Path(match.group(1)) if match else None

            return {
                "tool_names": tool_names,
                "navigate_result": navigate_result,
                "snapshot_result": snapshot_result,
                "tabs_result": tabs_result,
                "screenshot_result": screenshot_result,
                "screenshot_path": str(screenshot_path) if screenshot_path else None,
            }
        finally:
            await self._close()


async def _run_open_github_async() -> dict[str, Any]:
    """Async entrypoint used by the public synchronous wrapper."""
    runner = BrowserMCPRunner()
    return await runner.run_open_github()


def open_github_in_browser_sandbox() -> dict[str, Any]:
    """Synchronous wrapper for notebook use.

    The notebook should call this plain function instead of directly using
    `await browser_client.connect()` so the helper can own the event loop.
    """
    try:
        # In Jupyter, an event loop is usually already running in the main thread.
        asyncio.get_running_loop()
    except RuntimeError:
        # No running loop in this thread, so normal asyncio.run() is safe.
        return asyncio.run(_run_open_github_async())

    # If we are here, a loop is already running.
    # Run the async workflow inside a dedicated background thread so it can own
    # its own event loop without conflicting with the notebook loop.
    result_box: dict[str, Any] = {}
    error_box: dict[str, BaseException] = {}

    def _thread_target() -> None:
        try:
            result_box["result"] = asyncio.run(_run_open_github_async())
        except BaseException as exc:  # noqa: BLE001
            error_box["error"] = exc

    thread = threading.Thread(target=_thread_target, daemon=True)
    thread.start()
    thread.join()

    if "error" in error_box:
        raise error_box["error"]

    return result_box["result"]
