"""使用 AgentScope + Playwright MCP 在 GitHub 上搜索 agent，并找出热度最高的 Python 项目。

这个脚本是“执行入口”：
- 真正打开浏览器沙盒
- 打开 GitHub
- 进入搜索结果页
- 读取页面 snapshot
- 解析出热度最高的 Python 仓库名

说明：
- 为了让流程更稳定，这里不是模拟人工逐字输入搜索框，
  而是先打开 github.com，再跳转到等价的搜索结果 URL。
- 这个 URL 等价于在 GitHub 里搜索：
    agent language:Python
  并按 stars 从高到低排序。
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


def 安全打印(标题: str, 内容: Any, 最大长度: int = 3000) -> None:
    """安全打印文本，避免 Windows 终端因为编码问题直接报错。"""
    文本 = str(内容)
    if len(文本) > 最大长度:
        文本 = 文本[:最大长度] + "\n... [输出过长，已截断]"

    print(标题)
    try:
        print(文本)
    except UnicodeEncodeError:
        # 某些 Windows 终端默认不是 UTF-8，这里用替换策略避免脚本崩掉。
        安全文本 = 文本.encode(
            sys.stdout.encoding or "utf-8",
            errors="replace",
        ).decode(sys.stdout.encoding or "utf-8", errors="replace")
        print(安全文本)


async def 调用浏览器工具(
    toolkit: Toolkit,
    工具名: str,
    **参数: Any,
) -> Any:
    """调用一个已经注册到 Toolkit 中的浏览器工具。"""
    请求 = ToolUseBlock(
        type="tool_use",
        id=f"call-{工具名}",
        name=工具名,
        input=参数,
    )

    所有分片 = []
    async for 分片 in await toolkit.call_tool_function(请求):
        所有分片.append(分片.content)

    return 所有分片[-1] if 所有分片 else None


def 解析仓库名(snapshot文本: str) -> str | None:
    """从 GitHub 搜索结果页的 snapshot 文本中提取第一个有效仓库名。"""
    候选列表 = re.findall(
        r"/url: /([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
        snapshot文本,
    )

    需要排除的首段 = {
        "search",
        "topics",
        "login",
        "signup",
        "pricing",
        "features",
        "collections",
        "marketplace",
        "organizations",
        "settings",
        "sponsors",
        "site",
    }

    需要排除的尾段 = {
        "stargazers",
        "issues",
        "pulls",
        "actions",
        "discussions",
        "forks",
        "security",
        "releases",
        "commits",
    }

    for 仓库路径 in 候选列表:
        片段 = 仓库路径.split("/")
        if len(片段) != 2:
            continue

        首段, 尾段 = 片段
        if 首段 in 需要排除的首段:
            continue
        if 尾段 in 需要排除的尾段:
            continue

        return 仓库路径

    return None


async def main() -> None:
    """执行整个 GitHub 搜索流程。"""
    toolkit = Toolkit()

    # 这里通过 npx 启动 Playwright MCP，然后由 AgentScope 连接它。
    browser_client = StdIOStatefulClient(
        name="playwright-mcp",
        command="npx",
        args=["@playwright/mcp@latest"],
    )

    搜索URL = (
        "https://github.com/search?"
        "q=agent+language%3APython&type=repositories&s=stars&o=desc"
    )

    print("正在连接浏览器沙盒服务...")
    await browser_client.connect()
    await toolkit.register_mcp_client(browser_client)
    print("连接成功。")

    try:
        print("\n=== 第一步：打开 GitHub 首页 ===")
        首页结果 = await 调用浏览器工具(
            toolkit,
            "browser_navigate",
            url="https://github.com",
        )
        安全打印("首页打开结果 =", 首页结果, 最大长度=1200)

        print("\n=== 第二步：进入搜索结果页 ===")
        搜索结果 = await 调用浏览器工具(
            toolkit,
            "browser_navigate",
            url=搜索URL,
        )
        安全打印("搜索页打开结果 =", 搜索结果, 最大长度=1800)

        print("\n=== 第三步：读取页面快照 ===")
        snapshot结果 = await 调用浏览器工具(toolkit, "browser_snapshot")
        snapshot文本 = str(snapshot结果)
        安全打印("snapshot 预览 =", snapshot结果, 最大长度=2500)

        # 如果 GitHub 触发了频率限制，就不要继续误判。
        if "Too many requests" in snapshot文本:
            print("\nGitHub 当前触发了频率限制，暂时无法稳定读取搜索结果。")
            print("请稍后再运行这个脚本，或者登录 GitHub 后再尝试。")
            return

        print("\n=== 第四步：解析热度最高的 Python 仓库 ===")
        仓库名 = 解析仓库名(snapshot文本)
        if not 仓库名:
            print("没有成功从页面快照中解析出仓库名。")
            return

        print(f"找到的仓库名称：{仓库名}")

        print("\n=== 第五步：保存截图 ===")
        截图结果 = await 调用浏览器工具(toolkit, "browser_take_screenshot")
        安全打印("截图结果 =", 截图结果, 最大长度=1800)

        匹配 = re.search(r"\(([^)]+\.png)\)", str(截图结果))
        if 匹配:
            截图路径 = Path(匹配.group(1))
            print(f"截图保存路径：{截图路径}")
            print(f"截图文件是否存在：{截图路径.exists()}")

    finally:
        print("\n正在关闭浏览器沙盒连接...")
        await browser_client.close()
        print("连接已关闭。")


if __name__ == "__main__":
    asyncio.run(main())
