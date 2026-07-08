# 学习路径 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/getting-started/learning-path](https://hermes-agent.nousresearch.com/docs/zh-Hans/getting-started/learning-path)

本页总览

Hermes Agent 功能丰富——CLI 助手、Telegram/Discord 机器人、任务自动化、强化学习训练等。本页帮助您根据自身经验水平和目标，确定从哪里开始、阅读哪些内容。

从这里开始

如果您尚未安装 Hermes Agent，请先阅读[安装指南](/docs/zh-Hans/getting-started/installation)，然后完成[快速入门](/docs/zh-Hans/getting-started/quickstart)。以下内容均假设您已完成安装。

## 如何使用本页[​](#如何使用本页 "如何使用本页的直接链接")

* **已知自己的水平？** 跳转至[按经验水平](#by-experience-level)表格，按照对应层级的阅读顺序进行。
* **有明确目标？** 跳至[按使用场景](#by-use-case)，找到匹配的场景。
* **随便浏览？** 查看[主要功能](#key-features-at-a-glance)表格，快速了解 Hermes Agent 的全部能力。

## 按经验水平[​](#按经验水平 "按经验水平的直接链接")

| 水平 | 目标 | 推荐阅读 | 预计时间 |
| --- | --- | --- | --- |
| **初级** | 快速上手，进行基本对话，使用内置工具 | [安装](/docs/zh-Hans/getting-started/installation) → [快速入门](/docs/zh-Hans/getting-started/quickstart) → [CLI 用法](/docs/zh-Hans/user-guide/cli) → [配置](/docs/zh-Hans/user-guide/configuration) | 约 1 小时 |
| **中级** | 搭建消息机器人，使用记忆、cron 任务、技能等高级功能 | [会话](/docs/zh-Hans/user-guide/sessions) → [消息](/docs/zh-Hans/user-guide/messaging) → [工具](/docs/zh-Hans/user-guide/features/tools) → [技能](/docs/zh-Hans/user-guide/features/skills) → [记忆](/docs/zh-Hans/user-guide/features/memory) → [Cron](/docs/zh-Hans/user-guide/features/cron) | 约 2–3 小时 |
| **高级** | 构建自定义工具、创建技能、使用强化学习训练模型、参与项目贡献 | [架构](/docs/zh-Hans/developer-guide/architecture) → [添加工具](/docs/zh-Hans/developer-guide/adding-tools) → [创建技能](/docs/zh-Hans/developer-guide/creating-skills) → [强化学习训练](/docs/zh-Hans/user-guide/features/rl-training) → [贡献指南](/docs/zh-Hans/developer-guide/contributing) | 约 4–6 小时 |

## 按使用场景[​](#按使用场景 "按使用场景的直接链接")

选择与您目标匹配的场景，每个场景均按推荐顺序链接到相关文档。

### "我想要一个 CLI 编程助手"[​](#我想要一个-cli-编程助手 "\"我想要一个 CLI 编程助手\"的直接链接")

将 Hermes Agent 用作交互式终端助手，用于编写、审查和运行代码。

1. [安装](/docs/zh-Hans/getting-started/installation)
2. [快速入门](/docs/zh-Hans/getting-started/quickstart)
3. [CLI 用法](/docs/zh-Hans/user-guide/cli)
4. [代码执行](/docs/zh-Hans/user-guide/features/code-execution)
5. [上下文文件](/docs/zh-Hans/user-guide/features/context-files)
6. [技巧与窍门](/docs/zh-Hans/guides/tips)

提示

通过上下文文件将文件直接传入对话。Hermes Agent 可以读取、编辑并运行您项目中的代码。

### "我想要一个 Telegram/Discord 机器人"[​](#我想要一个-telegramdiscord-机器人 "\"我想要一个 Telegram/Discord 机器人\"的直接链接")

将 Hermes Agent 部署为您常用消息平台上的机器人。

1. [安装](/docs/zh-Hans/getting-started/installation)
2. [配置](/docs/zh-Hans/user-guide/configuration)
3. [消息概览](/docs/zh-Hans/user-guide/messaging)
4. [Telegram 配置](/docs/zh-Hans/user-guide/messaging/telegram)
5. [Discord 配置](/docs/zh-Hans/user-guide/messaging/discord)
6. [语音模式](/docs/zh-Hans/user-guide/features/voice-mode)
7. [在 Hermes 中使用语音模式](/docs/zh-Hans/guides/use-voice-mode-with-hermes)
8. [安全](/docs/zh-Hans/user-guide/security)

完整项目示例请参阅：

* [每日简报机器人](/docs/zh-Hans/guides/daily-briefing-bot)
* [团队 Telegram 助手](/docs/zh-Hans/guides/team-telegram-assistant)

### "我想自动化任务"[​](#我想自动化任务 "\"我想自动化任务\"的直接链接")

调度周期性任务、运行批处理作业，或将多个 agent 动作串联起来。

1. [快速入门](/docs/zh-Hans/getting-started/quickstart)
2. [Cron 调度](/docs/zh-Hans/user-guide/features/cron)
3. [批处理](/docs/zh-Hans/user-guide/features/batch-processing)
4. [委派](/docs/zh-Hans/user-guide/features/delegation)
5. [Hooks](/docs/zh-Hans/user-guide/features/hooks)

提示

Cron 任务让 Hermes Agent 按计划执行任务——每日摘要、定期检查、自动报告——无需您在场。

### "我想构建自定义工具/技能"[​](#我想构建自定义工具技能 "\"我想构建自定义工具/技能\"的直接链接")

通过自定义工具和可复用技能包扩展 Hermes Agent。

1. [插件](/docs/zh-Hans/user-guide/features/plugins)
2. [构建 Hermes 插件](/docs/zh-Hans/developer-guide/plugins)
3. [工具概览](/docs/zh-Hans/user-guide/features/tools)
4. [技能概览](/docs/zh-Hans/user-guide/features/skills)
5. [MCP（模型上下文协议）](/docs/zh-Hans/user-guide/features/mcp)
6. [架构](/docs/zh-Hans/developer-guide/architecture)
7. [添加工具](/docs/zh-Hans/developer-guide/adding-tools)
8. [创建技能](/docs/zh-Hans/developer-guide/creating-skills)

提示

对于大多数自定义工具的创建，建议从插件开始。[添加工具](/docs/zh-Hans/developer-guide/adding-tools)页面面向 Hermes 核心内置开发，而非常规用户/自定义工具路径。

### "我想训练模型"[​](#我想训练模型 "\"我想训练模型\"的直接链接")

使用强化学习（RL）通过 Hermes Agent 内置的 RL 训练流水线对模型行为进行微调。

1. [快速入门](/docs/zh-Hans/getting-started/quickstart)
2. [配置](/docs/zh-Hans/user-guide/configuration)
3. [强化学习训练](/docs/zh-Hans/user-guide/features/rl-training)
4. [Provider 路由](/docs/zh-Hans/user-guide/features/provider-routing)
5. [架构](/docs/zh-Hans/developer-guide/architecture)

提示

强化学习训练在您已了解 Hermes Agent 如何处理对话和工具调用的基础上效果最佳。如果您是新手，请先完成初级路径。

### "我想将其作为 Python 库使用"[​](#我想将其作为-python-库使用 "\"我想将其作为 Python 库使用\"的直接链接")

以编程方式将 Hermes Agent 集成到您自己的 Python 应用中。

1. [安装](/docs/zh-Hans/getting-started/installation)
2. [快速入门](/docs/zh-Hans/getting-started/quickstart)
3. [Python 库指南](/docs/zh-Hans/guides/python-library)
4. [架构](/docs/zh-Hans/developer-guide/architecture)
5. [工具](/docs/zh-Hans/user-guide/features/tools)
6. [会话](/docs/zh-Hans/user-guide/sessions)

## 主要功能一览[​](#主要功能一览 "主要功能一览的直接链接")

不确定有哪些功能？以下是主要功能的快速目录：

| 功能 | 说明 | 链接 |
| --- | --- | --- |
| **工具** | Agent 可调用的内置工具（文件 I/O、搜索、Shell 等） | [工具](/docs/zh-Hans/user-guide/features/tools) |
| **技能** | 可安装的插件包，用于添加新能力 | [技能](/docs/zh-Hans/user-guide/features/skills) |
| **记忆** | 跨会话的持久化记忆 | [记忆](/docs/zh-Hans/user-guide/features/memory) |
| **上下文文件** | 将文件和目录传入对话 | [上下文文件](/docs/zh-Hans/user-guide/features/context-files) |
| **MCP** | 通过模型上下文协议连接外部工具服务器 | [MCP](/docs/zh-Hans/user-guide/features/mcp) |
| **Cron** | 调度周期性 agent 任务 | [Cron](/docs/zh-Hans/user-guide/features/cron) |
| **委派** | 生成子 agent 以并行处理工作 | [委派](/docs/zh-Hans/user-guide/features/delegation) |
| **代码执行** | 运行以编程方式调用 Hermes 工具的 Python 脚本 | [代码执行](/docs/zh-Hans/user-guide/features/code-execution) |
| **浏览器** | 网页浏览与抓取 | [浏览器](/docs/zh-Hans/user-guide/features/browser) |
| **Hooks** | 事件驱动的回调与中间件 | [Hooks](/docs/zh-Hans/user-guide/features/hooks) |
| **批处理** | 批量处理多个输入 | [批处理](/docs/zh-Hans/user-guide/features/batch-processing) |
| **强化学习训练** | 使用强化学习微调模型 | [强化学习训练](/docs/zh-Hans/user-guide/features/rl-training) |
| **Provider 路由** | 在多个 LLM provider 之间路由请求 | [Provider 路由](/docs/zh-Hans/user-guide/features/provider-routing) |

## 下一步阅读[​](#下一步阅读 "下一步阅读的直接链接")

根据您当前所处阶段：

* **刚完成安装？** → 前往[快速入门](/docs/zh-Hans/getting-started/quickstart)，运行您的第一次对话。
* **完成了快速入门？** → 阅读 [CLI 用法](/docs/zh-Hans/user-guide/cli)和[配置](/docs/zh-Hans/user-guide/configuration)，自定义您的设置。
* **已熟悉基础？** → 探索[工具](/docs/zh-Hans/user-guide/features/tools)、[技能](/docs/zh-Hans/user-guide/features/skills)和[记忆](/docs/zh-Hans/user-guide/features/memory)，释放 agent 的全部能力。
* **为团队部署？** → 阅读[安全](/docs/zh-Hans/user-guide/security)和[会话](/docs/zh-Hans/user-guide/sessions)，了解访问控制与对话管理。
* **准备好开发了？** → 进入[开发者指南](/docs/zh-Hans/developer-guide/architecture)，了解内部机制并开始贡献。
* **想要实际示例？** → 查看[指南](/docs/zh-Hans/guides/tips)部分，获取真实项目案例和技巧。

提示

您无需阅读所有内容。选择与您目标匹配的路径，按顺序跟随链接，即可快速上手。随时可以回到本页寻找下一步。

* [如何使用本页](#如何使用本页)
* [按经验水平](#按经验水平)
* [按使用场景](#按使用场景)
  + ["我想要一个 CLI 编程助手"](#我想要一个-cli-编程助手)
  + ["我想要一个 Telegram/Discord 机器人"](#我想要一个-telegramdiscord-机器人)
  + ["我想自动化任务"](#我想自动化任务)
  + ["我想构建自定义工具/技能"](#我想构建自定义工具技能)
  + ["我想训练模型"](#我想训练模型)
  + ["我想将其作为 Python 库使用"](#我想将其作为-python-库使用)
* [主要功能一览](#主要功能一览)
* [下一步阅读](#下一步阅读)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/developer-guide/adding-tools](./docs-zh-Hans-developer-guide-adding-tools.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/developer-guide/architecture](./docs-zh-Hans-developer-guide-architecture.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/developer-guide/contributing](./docs-zh-Hans-developer-guide-contributing.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/developer-guide/creating-skills](./docs-zh-Hans-developer-guide-creating-skills.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/developer-guide/plugins](./docs-zh-Hans-developer-guide-plugins.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/getting-started/installation](./docs-zh-Hans-getting-started-installation.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/getting-started/quickstart](./docs-zh-Hans-getting-started-quickstart.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/daily-briefing-bot](./docs-zh-Hans-guides-daily-briefing-bot.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/python-library](./docs-zh-Hans-guides-python-library.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/team-telegram-assistant](./docs-zh-Hans-guides-team-telegram-assistant.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/tips](./docs-zh-Hans-guides-tips.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/use-voice-mode-with-hermes](./docs-zh-Hans-guides-use-voice-mode-with-hermes.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/cli](./docs-zh-Hans-user-guide-cli.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/configuration](./docs-zh-Hans-user-guide-configuration.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/batch-processing](./docs-zh-Hans-user-guide-features-batch-processing.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/browser](./docs-zh-Hans-user-guide-features-browser.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/code-execution](./docs-zh-Hans-user-guide-features-code-execution.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/context-files](./docs-zh-Hans-user-guide-features-context-files.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/cron](./docs-zh-Hans-user-guide-features-cron.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/delegation](./docs-zh-Hans-user-guide-features-delegation.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/hooks](./docs-zh-Hans-user-guide-features-hooks.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/mcp](./docs-zh-Hans-user-guide-features-mcp.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/memory](./docs-zh-Hans-user-guide-features-memory.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/plugins](./docs-zh-Hans-user-guide-features-plugins.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/provider-routing](./docs-zh-Hans-user-guide-features-provider-routing.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/skills](./docs-zh-Hans-user-guide-features-skills.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/tools](./docs-zh-Hans-user-guide-features-tools.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/voice-mode](./docs-zh-Hans-user-guide-features-voice-mode.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging](./docs-zh-Hans-user-guide-messaging.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/discord](./docs-zh-Hans-user-guide-messaging-discord.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/telegram](./docs-zh-Hans-user-guide-messaging-telegram.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/security](./docs-zh-Hans-user-guide-security.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/sessions](./docs-zh-Hans-user-guide-sessions.md)
