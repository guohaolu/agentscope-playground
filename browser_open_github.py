"""Use AgentScope + Playwright MCP to open github.com in a browser sandbox.

This script is the execution entrypoint.
The notebook should explain the concepts, while this file performs the real
browser work in a more stable plain-Python environment.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from typing import Any

from agentscope.mcp import StdIOStatefulClient
from agentscope.message import ToolUseBlock
from agentscope.tool import Toolkit


def safe_print(title: str, value: Any, max_chars: int = 4000) -> None:
    """Print text safely on Windows terminals with limited encodings.

    Some tool outputs may contain Unicode characters that the default Windows
    terminal encoding cannot print directly. We therefore fall back to a
    replacement strategy instead of crashing the whole script.
    """
    text = str(value)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [输出过长，已截断]"

    print(title)
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.encode(
            sys.stdout.encoding or "utf-8",
            errors="replace",
        ).decode(sys.stdout.encoding or "utf-8", errors="replace")
        print(safe_text)


async def call_browser_tool(
    toolkit: Toolkit,
    tool_name: str,
    **kwargs: Any,
) -> Any:
    """Call one browser tool registered in the toolkit.

    In AgentScope, browser actions are just tool calls.
    We build a ToolUseBlock to describe which tool we want to call and which
    arguments should be passed to it.
    """
    tool_request = ToolUseBlock(
        type="tool_use",
        id=f"call-{tool_name}",
        name=tool_name,
        input=kwargs,
    )

    chunks = []
    async for chunk in await toolkit.call_tool_function(tool_request):
        chunks.append(chunk.content)

    return chunks[-1] if chunks else None


async def main() -> None:
    """Open github.com, print page data, and save a screenshot."""
    toolkit = Toolkit()

    # StdIOStatefulClient connects AgentScope to an MCP server process.
    # Here the server is Playwright MCP, started through npx.
    browser_client = StdIOStatefulClient(
        name="playwright-mcp",
        command="npx",
        args=["@playwright/mcp@latest"],
    )

    print("正在连接 Playwright MCP 浏览器服务...")
    await browser_client.connect()
    await toolkit.register_mcp_client(browser_client)
    print("连接成功。")

    try:
        tool_names = sorted(toolkit.tools.keys())
        print("\n=== 可用浏览器工具 ===")
        for tool_name in tool_names:
            print(tool_name)

        print("\n=== 第一步：打开 GitHub ===")
        navigate_result = await call_browser_tool(
            toolkit,
            "browser_navigate",
            url="https://github.com",
        )
        safe_print("navigate_result =", navigate_result, max_chars=2000)

        print("\n=== 第二步：获取页面快照 snapshot ===")
        snapshot_result = await call_browser_tool(toolkit, "browser_snapshot")
        safe_print("snapshot_result =", snapshot_result, max_chars=3500)

        print("\n=== 第三步：查看当前标签页信息 ===")
        tabs_result = await call_browser_tool(
            toolkit,
            "browser_tabs",
            action="list",
        )
        safe_print("tabs_result =", tabs_result, max_chars=2000)

        print("\n=== 第四步：截图 ===")
        screenshot_result = await call_browser_tool(
            toolkit,
            "browser_take_screenshot",
        )
        safe_print("screenshot_result =", screenshot_result, max_chars=2500)

        screenshot_text = str(screenshot_result)
        match = re.search(r"\(([^)]+\.png)\)", screenshot_text)
        if match:
            screenshot_path = Path(match.group(1))
            print(f"\n截图已保存到: {screenshot_path}")
            print(f"截图文件是否存在: {screenshot_path.exists()}")
        else:
            print("\n没有从返回结果里解析出截图路径。")

    finally:
        print("\n正在关闭浏览器 MCP 连接...")
        await browser_client.close()
        print("连接已关闭。")


if __name__ == "__main__":
    asyncio.run(main())
