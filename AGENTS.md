# AGENTS.md

## 项目定位

这个仓库是一个用于学习 Python 和 AgentScope 的个人练习项目，不是生产项目。

核心目标不是“尽快把代码写完”，而是：

- 帮助用户真正理解代码在做什么
- 帮助用户理解 AgentScope 的能力边界和设计思路
- 帮助用户把 Python 基础和 AgentScope 概念一起学会
- 通过可运行、可拆解、可观察的 notebook 逐步建立认知

在这个仓库里，教学价值优先于工程炫技。

## 用户背景假设

默认用户是：

- Python 新手
- AgentScope 新手
- 希望得到非常详细的中文解释
- 希望通过 Jupyter Notebook 学习，而不是直接看大段 `.py` 文件

因此，在这个仓库里工作时，必须优先考虑“是否便于学习和理解”，而不是只考虑“是否最短、最快、最抽象”。

## 语言要求

- 默认使用中文进行解释、说明、引导和总结。
- 可以保留必要的英文 API 名称、类名、函数名、路径名。
- 如果出现英文术语，优先补一句中文解释。
- 如果某个概念容易让新手混淆，必须明确指出它的中文含义和作用。

例如需要主动解释：

- `Msg` 是什么，和普通字符串有什么区别
- `Toolkit` 是什么，和普通 Python 函数集合有什么区别
- `memory` 是什么，和 Python 变量、列表不是一个层级的概念
- `async def` / `await` 为什么出现，和普通函数的差异是什么

## 教学优先规则

在这个仓库中，默认采用“教学模式”。

这意味着：

- 解释要详细，不能只给结论
- 示例要循序渐进，不能一开始把太多概念堆在一起
- 注释要明显多于普通工程项目
- 代码要可读，不要为了简洁牺牲理解成本
- 输出要让用户看完后知道“为什么这样写”

完成代码后，通常应当按下面顺序解释：

1. 这段代码的学习目标是什么
2. 它涉及哪些核心对象或模块
3. 代码整体执行流程是什么
4. 关键行或关键单元格分别做了什么
5. 运行后应该看到什么现象
6. 这个例子帮助理解了 AgentScope 的哪一部分
7. 下一步建议学什么

## Notebook 优先

这个项目默认优先使用 Jupyter Notebook 来承载学习内容。

规则如下：

- 如果任务是学习、实验、演示、源码理解、概念讲解，优先写到 `notebooks/`
- 除非用户明确要求，否则不要优先把学习内容写成纯 `.py` 脚本
- 如果主题和现有 notebook 对应，优先补充或改进现有 notebook
- 如果现有 notebook 不适合承载新主题，再新增一个编号 notebook

新增或改写 notebook 时，优先遵循以下结构：

1. 标题
2. 学习目标
3. 前置知识
4. 概念说明
5. 最小可运行示例
6. 逐步扩展
7. 结果观察
8. 总结
9. 可选练习

Notebook 编写要求：

- 每个代码单元只做一件清晰的事
- 尽量保证从上到下顺序执行即可运行
- 不要制造太多跨单元隐式依赖
- Markdown 单元要承担“教学引导”的职责
- 代码单元要承担“可运行验证”的职责
- 对新手不直观的地方要加注释

如果确实需要把复用逻辑放进 `.py` 文件，也必须保证 notebook 是主入口，并且在 notebook 中解释那个 `.py` 文件为什么存在、里面的函数是做什么的。

## Python 新手友好规则

默认用户可能还不熟悉以下内容，因此在代码和解释中要主动照顾：

- `import`
- 类实例化
- 方法调用
- 关键字参数
- 列表、字典、对象属性访问
- 环境变量
- 异步函数
- `await`
- 返回值与副作用

如果代码中用了这些内容：

- 不要假设用户自然懂
- 第一次出现时要解释
- 如果语法稍微复杂，要在代码旁和代码后都解释一次

避免在教学代码中默认使用以下风格，除非有明确必要：

- 过度抽象
- 花哨的 Python 写法
- 不利于新手理解的“短而巧”表达
- 一次性引入太多框架对象

## 注释规范

这个仓库是“注释可以明显多写”的例外项目。

要求：

- 注释应帮助理解“意图”和“心智模型”
- 不要只重复语法表面含义
- 注释优先解释“为什么这样写”和“这一行在 AgentScope 体系里扮演什么角色”

好的注释示例：

- “创建 Toolkit 对象。AgentScope 会把注册进去的 Python 函数当成可调用工具暴露给 Agent。”
- “这里使用 `await`，因为当前调用的是异步接口；如果不等待结果，后续代码会拿不到真正的返回值。”

不好的注释示例：

- “把值赋给变量”
- “调用函数”

## AgentScope 研究与查证规则

不要凭印象猜 AgentScope API。

因为 AgentScope 迭代较快，而且很多能力横跨 agent、message、tool、memory、pipeline、hook 等多个模块，所以只要涉及非平凡的 AgentScope 代码修改、示例设计或源码解释，必须优先查证。

优先级顺序如下：

1. 本地已安装包源码：`.venv/Lib/site-packages/agentscope/`
2. 官方 AgentScope 源码仓库：`https://github.com/agentscope-ai/agentscope`
3. 官方 Python 文档：`https://doc.agentscope.io/`
4. 官方 CoPaw 仓库：`https://github.com/agentscope-ai/CoPaw`
5. 用户补充的 `llms.txt` 文档源：`https://java.agentscope.io/llms-full.txt`

### 关于 `llms-full.txt`

用户额外提供了这个文档源：

- `https://java.agentscope.io/llms-full.txt`

使用规则：

- 可以把它当作 AgentScope 相关概念、模块导航、功能面概览的补充资料
- 它适合帮助智能编码助手理解 AgentScope 整体生态和文档目录
- 但它来自 Java 文档体系，不应直接当成 Python API 的最终依据
- 如果 `llms-full.txt` 与 Python 源码或 Python 官方文档不一致，必须以 Python 源码和 Python 官方文档为准

简化规则：

- 学 Python AgentScope：先看 Python 源码和 Python 文档
- 做概念补充和全局导航：可以参考 `llms-full.txt`

## 源码优先解释

在解释 AgentScope 时，尽量把说明落到真实源码模块上，而不是只做抽象描述。

尤其要优先结合这些目录和文件：

- `agentscope/agent/`
- `agentscope/message/`
- `agentscope/tool/`
- `agentscope/memory/`
- `agentscope/pipeline/`
- `agentscope/hooks/`
- `agentscope/plan/`
- `agentscope/rag/`

如果相关概念适合从源码切入，应明确说明：

- 这个能力在哪个模块里
- 这个类或函数在框架里负责什么
- 它和其他模块如何协作

例如解释时可以主动映射：

- `ReActAgent` 对应 `agentscope/agent/_react_agent.py`
- `Msg` 和内容块对应 `agentscope/message/`
- `Toolkit` 对应 `agentscope/tool/_toolkit.py`

如果某个说法是根据源码推断出来的，而不是文档直接写明的，要明确标注“这是根据源码推断的”。

## CoPaw 参考规则

CoPaw 是官方团队基于 AgentScope 构建的实际项目，可以作为“真实使用方式”的重要参考。

在以下主题上，优先参考 CoPaw 的实践：

- hooks 的使用
- memory 管理
- context compaction
- tool 组织方式
- agent 组合方式
- 多组件协作方式

但要注意：

- CoPaw 是更完整的应用项目，不适合直接照搬成新手的第一个例子
- 如果 CoPaw 的实现较复杂，应先提炼出最小教学版本，再逐步展开
- 教学中要说明“这个做法来自 CoPaw 的真实项目实践”

## AgentScope 教学示例设计规则

设计 AgentScope 示例时，优先选择“概念单一、路径清晰、便于观察”的例子。

建议按主题拆开，不要一开始就把所有能力混在一个 notebook 里：

- message
- model
- formatter
- memory
- tool
- workflow
- hook
- plan
- rag

创建 Agent 时，教学上优先显式展示这些组件，而不是把它们隐藏在封装里：

- `model`
- `formatter`
- `memory`
- `toolkit`

原因：

- 这些是 AgentScope 的核心拼装点
- 用户后续读官方示例或源码时会更容易建立映射

## 解释 AgentScope 代码时必须回答的问题

只要在讲 AgentScope 代码，原则上都要尽量回答这些问题：

1. 这里创建了哪个 AgentScope 对象
2. 这个对象的职责是什么
3. 它接收什么输入
4. 它返回什么，或者会改变什么状态
5. 它和其他 AgentScope 组件怎么协作

如果是异步调用，还要补充：

6. 为什么这里是异步
7. `await` 等待的到底是什么结果

## 环境变量与敏感信息

- 不要在代码、notebook、文档里硬编码 API Key、Token、私有路径
- 优先使用环境变量
- 在 notebook 中，如果某个单元需要 API Key 或联网，必须先用 Markdown 明确提示
- 如果可以先用 mock、占位结构、假数据教学，就先不要强依赖真实外部服务

## 命令与运行方式

这个项目使用 `uv`，因此默认使用项目内环境运行命令。

优先命令：

- `uv run python`
- `uv run jupyter lab`

如果需要给用户运行指导，优先写成和本项目环境一致的形式。

## 修改现有内容时的约束

- 仓库中已有大量按编号组织的 notebook，应尽量保持这条学习路径
- 修改现有 notebook 时，不要破坏原有学习节奏
- 如果重写某个 notebook，应说明为什么这样改更利于理解
- 未经用户明确要求，不要随意覆盖用户已有实验内容

## 最终输出要求

在这个仓库中完成任务后，通常应告诉用户：

- 改了什么
- 应该打开哪个 notebook 或文件
- 如何用 `uv` 运行
- 阅读或执行时重点关注什么
- 建议下一步学什么

如果是 notebook，尽量补一个简短的阅读指引，例如：

- 先看第一个 Markdown 单元
- 先运行环境检查单元
- 跑完某个单元后观察输出
- 对比两个单元来理解某个概念差异

## 决策原则

如果出现这些取舍：

- 代码更短 vs 更容易理解
- 注释更少 vs 更适合教学
- 实现更快 vs 学习引导更完整

在这个仓库里，优先选择更利于学习的方案，只要代码仍然正确、可运行、结构清晰。
