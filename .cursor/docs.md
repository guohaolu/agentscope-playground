# Cursor Docs 配置说明

本项目的 AI 辅助编写建议使用以下文档作为上下文。

## LLM 文档 URL

| 用途     | URL |
|----------|-----|
| **推荐** | `https://java.agentscope.io/llms-full.txt` |

该文件为 AgentScope Java 的 [llms.txt 标准](https://llmstxt.org/) 完整文档，包含安装、关键概念、ReAct Agent、Message、Model、Tool、MCP、RAG、Hook、Memory、Plan、Pipeline、Studio 等说明，便于 Cursor 在编写或审查代码时参考。

## 在 Cursor 中添加为 Doc

1. 打开 **Cursor 设置** → **Features** → **Docs**
2. 点击 **+ Add new Doc**
3. 填入 URL：`https://java.agentscope.io/llms-full.txt`

添加后，在对话或编辑时可引用该文档内容。
