# 这是一个更接近真实的亚马逊 VC 拉取报告 Agent 示例代码
import asyncio
import os
import sys
from agentscope.agent import ReActAgent
from agentscope.mcp import StdIOStatefulClient
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit
from agentscope.message import Msg

async def run_vc_report_bot():
    print("======== 开始 RPA 自动化: 亚马逊 VC 报告拉取 ========")
    
    # 1. 准备语言模型
    model_config = DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.environ.get("DASHSCOPE_API_KEY", "your_api_key_here"),
        stream=False,
    )

    # 2. 连接 Playwright MCP 代理
    # 注意: 这个服务会在后台启动一个真正的浏览器
    print("正在启动无头浏览器(Playwright MCP Server)...")
    try:
        browser_client = StdIOStatefulClient(
            command="npx",
            args=["-y", "@playwright/mcp@latest"],
        )
        await browser_client.connect()
    except Exception as e:
        print(f"启动 Playwright 服务失败: {e}\n请检查是否安装了 Node.js 以及网络是否通畅。")
        sys.exit(1)

    # 3. 注册工具箱
    toolkit = Toolkit()
    await toolkit.register_mcp_client(browser_client)
    print("浏览器工具集已成功注册到 AgentScope!")

    # 4. 配置专门针对 Amazon VC 的 RPA 智能体
    sys_prompt = """你是一个自动化的亚马逊 VC (Vendor Central) 报表下载机器人。
你拥有操作浏览器的能力（包括导航 url、点击特定选择器、填写表单文本、截取网页等）。

【你的核心任务步骤】：
1. 导航前往 `https://vendorcentral.amazon.com/`
2. 观察页面是否需要登录。如果出现登录框，尝试填入预设的用户账号和密码，并点击 `Sign-In` 按钮。
3. （重要）很多情况下亚马逊会有两步验证 (2SV) 或图形验证码。如果遇到验证码拦截，明确告知用户无法继续自动化，并保留当前状态。
4. 如果登录成功，进入 Dashboard。寻找并点击 `Reports`（报告） -> `Analytics`（分析）或是对应的财务账单入口。
5. 寻找 `Download` 或者 `Export` 按钮，将当月的数据报表以 CSV 或 Excel 格式保存。
6. 最后报告当前的操作结果。

请按照 ReAct 思维模式，一步一步地使用合适的浏览器工具。如果遇到找不到元素的情况，请尝试等待或重新观察页面 DOM。"""

    vc_agent = ReActAgent(
        name="VC_Automation_Agent",
        sys_prompt=sys_prompt,
        model=model_config,
        toolkit=toolkit,
    )

    # 5. 指发实际指令
    # 警告: 实际生产环境中, 切记不要把真实密码硬编码在脚本里!
    task_desc = """
请开始任务：
1. 访问亚马逊 VC 登录页。
2. 检查页面状态，如果需要输入账号密码，请先告诉我你看到了哪些输入框的标签。
由于安全原因，我们此次只做一个"导航并确认登录框是否存在"的测试，确认存在登录框后就可以结束任务。
"""
    
    try:
        response = await vc_agent(Msg("User", content=task_desc, role="user"))
        print("\n======== RPA 任务结束 ========")
        print("机器人反馈:", response.content)
    except Exception as e:
        print(f"\n任务执行异常: {e}")
    finally:
        # 6. 关闭释放资源
        await browser_client.close()
        print("浏览器资源已释放。")

if __name__ == "__main__":
    asyncio.run(run_vc_report_bot())
