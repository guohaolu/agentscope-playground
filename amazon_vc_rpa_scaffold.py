import asyncio
import os
from agentscope.agent import ReActAgent
from agentscope.mcp import StdIOStatefulClient
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit
from agentscope.message import Msg

# -------------------------------------------------------------------
# 亚马逊 VC (Vendor Central) RPA 基础 Agent 脚本
# -------------------------------------------------------------------
# 运行这段代码前，请确保：
# 1. 已经安装了 Node.js
# 2. 能在系统终端通过 `npx -y @playwright/mcp@latest` 启动服务
# 注意：由于操作实际浏览器环境，如果环境不支持无界面模式可适当修改MCP启动参数
# -------------------------------------------------------------------

async def main():
    # 1. 配置大语言模型 (这里以千问大模型为例，你也可以换装 OpenAI/Anthropic 模型)
    model_config = DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.environ.get("DASHSCOPE_API_KEY", "你的_DASHSCOPE_API_KEY"),
        stream=True,
    )

    # 2. 注册 Playwright MCP 客户端
    print("正在连接本地 Playwright MCP 服务器，请确保 Node.js 已安装...")
    browser_client = StdIOStatefulClient(
        command="npx",
        args=["-y", "@playwright/mcp@latest"],
    )
    
    # 建立与 MCP 服务的连接
    await browser_client.connect()
    
    # 3. 初始化工具集并注册 MCP 客户端中的所有浏览器工具
    toolkit = Toolkit()
    await toolkit.register_mcp_client(browser_client)

    # 4. 创建执行 RPA 任务的 ReActAgent 
    # (如果业务复杂，你也可以参考官方用更定制化的 BrowserAgent)
    rpa_agent = ReActAgent(
        name="Amazon_VC_RPA_Bot",
        sys_prompt="""你是一个专业的网页端 RPA (Robotic Process Automation) 机器人。
你的任务是操作浏览器，访问亚马逊 Vendor Central 后台，并执行报告下载等常规事务。
你有能力使用一系列浏览器控制工具（例如导航、点击、填写表单、执行 JS 代码等）。

在执行任务时，请坚持以下原则：
1. 分析当前页面状态。
2. 决定下一步该执行什么操作。
3. 如果遇到验证码或者登录失效，必须如实向用户反馈，不要盲目乱点。
4. 在操作数据表格或拉取报表时，保证选对日期范围。""",
        model=model_config,
        toolkit=toolkit,
    )

    # 5. 指派任务给 Agent
    task_prompt = "请打开浏览器，导航到 'https://vendorcentral.amazon.com/'，并告诉我页面标题是什么，以及页面上是否有登录输入框。"
    
    print(f"下发任务: {task_prompt}")
    
    # 执行任务并获取回复
    try:
        msg = Msg("User", content=task_prompt, role="user")
        response = await rpa_agent(msg)
        print("\n最终执行结果: ", response.content)
    except Exception as e:
        print(f"RPA 机器人执行时出现错误: {e}")
    finally:
        # 6. 安全关闭浏览器服务
        await browser_client.close()
        print("Playwright MCP 服务已安全关闭。")

if __name__ == "__main__":
    asyncio.run(main())
