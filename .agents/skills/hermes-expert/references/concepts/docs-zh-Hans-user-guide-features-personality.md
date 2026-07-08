# 个性与 SOUL.md | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/personality](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/personality)

本页总览

Hermes Agent 的个性完全可自定义。`SOUL.md` 是**主要身份标识**——它是系统提示词（prompt）中的第一项内容，定义了 Agent 是谁。

* `SOUL.md` — 存放在 `HERMES_HOME` 中的持久角色文件，作为 Agent 的身份标识（系统提示词中的第 1 个槽位）
* 内置或自定义的 `/personality` 预设 — 会话级系统提示词覆盖层

如果你想改变 Hermes 的身份，或将其替换为完全不同的 Agent 角色，请编辑 `SOUL.md`。

## SOUL.md 的工作方式[​](#soulmd-的工作方式 "SOUL.md 的工作方式的直接链接")

Hermes 现在会自动在以下位置生成默认的 `SOUL.md`：

```
~/.hermes/SOUL.md
```

更准确地说，它使用当前实例的 `HERMES_HOME`，因此如果你以自定义主目录运行 Hermes，它将使用：

```
$HERMES_HOME/SOUL.md
```

### 重要行为[​](#重要行为 "重要行为的直接链接")

* **SOUL.md 是 Agent 的主要身份标识。** 它占据系统提示词的第 1 个槽位，替代硬编码的默认身份。
* 如果 `SOUL.md` 尚不存在，Hermes 会自动创建一个初始文件
* 已有的用户 `SOUL.md` 文件不会被覆盖
* Hermes 仅从 `HERMES_HOME` 加载 `SOUL.md`
* Hermes 不会在当前工作目录中查找 `SOUL.md`
* 如果 `SOUL.md` 存在但为空，或无法加载，Hermes 将回退到内置的默认身份
* 如果 `SOUL.md` 有内容，该内容在经过安全扫描和截断处理后将原样注入
* SOUL.md **不会**在上下文文件部分重复出现——它仅作为身份标识出现一次

这使 `SOUL.md` 成为真正的每用户或每实例身份标识，而不仅仅是一个附加层。

## 此设计的原因[​](#此设计的原因 "此设计的原因的直接链接")

这样可以保持个性的可预测性。

如果 Hermes 从你启动它的任意目录加载 `SOUL.md`，你的个性可能会在不同项目之间意外改变。通过仅从 `HERMES_HOME` 加载，个性归属于 Hermes 实例本身。

这也让用户更容易理解：

* "编辑 `~/.hermes/SOUL.md` 来更改 Hermes 的默认个性。"

## 编辑位置[​](#编辑位置 "编辑位置的直接链接")

对于大多数用户：

```
~/.hermes/SOUL.md
```

如果你使用自定义主目录：

```
$HERMES_HOME/SOUL.md
```

## SOUL.md 应该写什么？[​](#soulmd-应该写什么 "SOUL.md 应该写什么？的直接链接")

用于持久的语气和个性指导，例如：

* 语气
* 沟通风格
* 直接程度
* 默认交互风格
* 风格上应避免的内容
* Hermes 应如何处理不确定性、分歧或模糊情况

不适合写入的内容：

* 一次性项目说明
* 文件路径
* 代码库规范
* 临时工作流细节

这些内容属于 `AGENTS.md`，而不是 `SOUL.md`。

## 优质 SOUL.md 内容[​](#优质-soulmd-内容 "优质 SOUL.md 内容的直接链接")

一个好的 SOUL 文件应该：

* 在不同上下文中保持稳定
* 足够宽泛，适用于多种对话场景
* 足够具体，能实质性地塑造语气
* 专注于沟通和身份，而非特定任务的指令

### 示例[​](#示例 "示例的直接链接")

```
# Personality  
  
You are a pragmatic senior engineer with strong taste.  
You optimize for truth, clarity, and usefulness over politeness theater.  
  
## Style  
- Be direct without being cold  
- Prefer substance over filler  
- Push back when something is a bad idea  
- Admit uncertainty plainly  
- Keep explanations compact unless depth is useful  
  
## What to avoid  
- Sycophancy  
- Hype language  
- Repeating the user's framing if it's wrong  
- Overexplaining obvious things  
  
## Technical posture  
- Prefer simple systems over clever systems  
- Care about operational reality, not idealized architecture  
- Treat edge cases as part of the design, not cleanup
```

## Hermes 注入提示词的内容[​](#hermes-注入提示词的内容 "Hermes 注入提示词的内容的直接链接")

`SOUL.md` 的内容直接进入系统提示词的第 1 个槽位——即 Agent 身份位置。不会在其周围添加任何包装语言。

内容会经过以下处理：

* 提示词注入扫描
* 内容过大时进行截断

如果文件为空、仅含空白字符或无法读取，Hermes 将回退到内置默认身份（"You are Hermes Agent, an intelligent AI assistant created by Nous Research..."）。当 `skip_context_files` 被设置时（例如在子 Agent/委托上下文中），同样适用此回退。

## 安全扫描[​](#安全扫描 "安全扫描的直接链接")

`SOUL.md` 与其他携带上下文的文件一样，在被包含前会进行提示词注入模式扫描。

这意味着你仍应将其专注于角色/语气，而不是试图混入奇怪的元指令。

## SOUL.md 与 AGENTS.md[​](#soulmd-与-agentsmd "SOUL.md 与 AGENTS.md的直接链接")

这是最重要的区别。

### SOUL.md[​](#soulmd "SOUL.md的直接链接")

用于：

* 身份
* 语气
* 风格
* 沟通默认值
* 个性层面的行为

### AGENTS.md[​](#agentsmd "AGENTS.md的直接链接")

用于：

* 项目架构
* 编码规范
* 工具偏好
* 代码库特定工作流
* 命令、端口、路径、部署说明

一个实用的判断规则：

* 如果它应该随你到处适用，属于 `SOUL.md`
* 如果它属于某个项目，属于 `AGENTS.md`

## SOUL.md 与 `/personality`[​](#soulmd-与-personality "soulmd-与-personality的直接链接")

`SOUL.md` 是你的持久默认个性。

`/personality` 是会话级覆盖层，用于更改或补充当前系统提示词。

因此：

* `SOUL.md` = 基础语气
* `/personality` = 临时模式切换

示例：

* 保持务实的默认 SOUL，然后在辅导对话中使用 `/personality teacher`
* 保持简洁的 SOUL，然后在头脑风暴时使用 `/personality creative`

## 内置个性[​](#内置个性 "内置个性的直接链接")

Hermes 内置了多种个性，可通过 `/personality` 切换。

| 名称 | 描述 |
| --- | --- |
| **helpful** | 友好的通用助手 |
| **concise** | 简短、直击要点的回复 |
| **technical** | 详尽、准确的技术专家 |
| **creative** | 创新、突破常规的思维 |
| **teacher** | 耐心的教育者，配有清晰示例 |
| **kawaii** | 可爱表达、闪光效果与热情 ★ |
| **catgirl** | 带有猫咪表达方式的 Neko-chan，nya~ |
| **pirate** | 船长 Hermes，精通技术的海盗 |
| **shakespeare** | 充满戏剧张力的吟游诗人风格 |
| **surfer** | 超级冷静的冲浪者氛围 |
| **noir** | 硬派侦探叙事风格 |
| **uwu** | 极致可爱的 uwu 语气 |
| **philosopher** | 对每个问题深度沉思 |
| **hype** | 最大能量与热情！！！ |

## 使用命令切换个性[​](#使用命令切换个性 "使用命令切换个性的直接链接")

### CLI[​](#cli "CLI的直接链接")

```
/personality  
/personality concise  
/personality technical
```

### 消息平台[​](#消息平台 "消息平台的直接链接")

```
/personality teacher
```

这些是便捷的覆盖层，但你的全局 `SOUL.md` 仍然赋予 Hermes 持久的默认个性，除非覆盖层对其进行了实质性更改。

## 在配置中定义自定义个性[​](#在配置中定义自定义个性 "在配置中定义自定义个性的直接链接")

你也可以在 `~/.hermes/config.yaml` 的 `agent.personalities` 下定义命名的自定义个性。

```
agent:  
  personalities:  
    codereviewer: >  
      You are a meticulous code reviewer. Identify bugs, security issues,  
      performance concerns, and unclear design choices. Be precise and constructive.
```

然后通过以下方式切换：

```
/personality codereviewer
```

## 推荐工作流[​](#推荐工作流 "推荐工作流的直接链接")

一个强健的默认配置：

1. 在 `~/.hermes/SOUL.md` 中维护一个经过深思熟虑的全局 `SOUL.md`
2. 将项目说明放在 `AGENTS.md` 中
3. 仅在需要临时模式切换时使用 `/personality`

这样你将获得：

* 稳定的语气
* 项目特定行为归属于正确位置
* 需要时的临时控制

## 个性如何与完整提示词交互[​](#个性如何与完整提示词交互 "个性如何与完整提示词交互的直接链接")

从高层次来看，提示词栈包含：

1. **SOUL.md**（Agent 身份——如果 SOUL.md 不可用则使用内置回退）
2. 工具感知行为指导
3. 记忆/用户上下文
4. 技能指导
5. 上下文文件（`AGENTS.md`、`.cursorrules`）
6. 时间戳
7. 平台特定格式提示
8. 可选的系统提示词覆盖层，如 `/personality`

`SOUL.md` 是基础——其他所有内容都建立在它之上。

## 相关文档[​](#相关文档 "相关文档的直接链接")

* [上下文文件](/docs/zh-Hans/user-guide/features/context-files)
* [配置](/docs/zh-Hans/user-guide/configuration)
* [技巧与最佳实践](/docs/zh-Hans/guides/tips)
* [SOUL.md 指南](/docs/zh-Hans/guides/use-soul-with-hermes)

## CLI 外观与对话个性[​](#cli-外观与对话个性 "CLI 外观与对话个性的直接链接")

对话个性与 CLI 外观是相互独立的：

* `SOUL.md`、`agent.system_prompt` 和 `/personality` 影响 Hermes 的说话方式
* `display.skin` 和 `/skin` 影响 Hermes 在终端中的显示外观

关于终端外观，请参阅 [皮肤与主题](/docs/zh-Hans/user-guide/features/skins)。

* [SOUL.md 的工作方式](#soulmd-的工作方式)
  + [重要行为](#重要行为)
* [此设计的原因](#此设计的原因)
* [编辑位置](#编辑位置)
* [SOUL.md 应该写什么？](#soulmd-应该写什么)
* [优质 SOUL.md 内容](#优质-soulmd-内容)
  + [示例](#示例)
* [Hermes 注入提示词的内容](#hermes-注入提示词的内容)
* [安全扫描](#安全扫描)
* [SOUL.md 与 AGENTS.md](#soulmd-与-agentsmd)
  + [SOUL.md](#soulmd)
  + [AGENTS.md](#agentsmd)
* [SOUL.md 与 `/personality`](#soulmd-与-personality)
* [内置个性](#内置个性)
* [使用命令切换个性](#使用命令切换个性)
  + [CLI](#cli)
  + [消息平台](#消息平台)
* [在配置中定义自定义个性](#在配置中定义自定义个性)
* [推荐工作流](#推荐工作流)
* [个性如何与完整提示词交互](#个性如何与完整提示词交互)
* [相关文档](#相关文档)
* [CLI 外观与对话个性](#cli-外观与对话个性)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/tips](./docs-zh-Hans-guides-tips.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/use-soul-with-hermes](./docs-zh-Hans-guides-use-soul-with-hermes.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/configuration](./docs-zh-Hans-user-guide-configuration.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/context-files](./docs-zh-Hans-user-guide-features-context-files.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/skins](./docs-zh-Hans-user-guide-features-skins.md)
