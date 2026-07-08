# 在 Hermes 中使用 SOUL.md | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/use-soul-with-hermes](https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/use-soul-with-hermes)

本页总览

`SOUL.md` 是你的 Hermes 实例的**主要身份标识**。它是系统提示词（system prompt）中的第一项内容——定义了 Agent 是谁、如何表达，以及应避免什么。

如果你希望每次与 Hermes 交谈时都感受到一致的助手风格，或者想用自己的角色完全替换 Hermes 的默认人设，这就是你需要编辑的文件。

## SOUL.md 的用途[​](#soulmd-的用途 "SOUL.md 的用途的直接链接")

`SOUL.md` 适用于：

* 语气
* 个性
* 沟通风格
* Hermes 应有多直接或多温和
* Hermes 在风格上应避免什么
* Hermes 如何应对不确定性、分歧和模糊情况

简而言之：

* `SOUL.md` 关注的是 Hermes 是谁，以及 Hermes 如何表达

## SOUL.md 不适用的内容[​](#soulmd-不适用的内容 "SOUL.md 不适用的内容的直接链接")

不要在其中放置：

* 特定代码仓库的编码规范
* 文件路径
* 命令
* 服务端口
* 架构说明
* 项目工作流指令

这些内容属于 `AGENTS.md`。

一个简单的判断原则：

* 如果某项内容应在所有地方生效，放入 `SOUL.md`
* 如果某项内容只属于某个项目，放入 `AGENTS.md`

## 文件位置[​](#文件位置 "文件位置的直接链接")

Hermes 目前仅使用当前实例的全局 SOUL 文件：

```
~/.hermes/SOUL.md
```

如果你使用自定义主目录运行 Hermes，路径变为：

```
$HERMES_HOME/SOUL.md
```

## 首次运行行为[​](#首次运行行为 "首次运行行为的直接链接")

如果 `SOUL.md` 尚不存在，Hermes 会自动为你生成一个初始文件。

这意味着大多数用户一开始就有一个可以立即阅读和编辑的真实文件。

注意：

* 如果你已有 `SOUL.md`，Hermes 不会覆盖它
* 如果文件存在但为空，Hermes 不会从中向提示词添加任何内容

## Hermes 如何使用它[​](#hermes-如何使用它 "Hermes 如何使用它的直接链接")

Hermes 启动会话时，会从 `HERMES_HOME` 读取 `SOUL.md`，扫描其中的提示词注入（prompt-injection）模式，必要时进行截断，并将其作为 **Agent 身份标识**——系统提示词中的第 1 个槽位。这意味着 `SOUL.md` 会完全替换内置的默认身份文本。

如果 `SOUL.md` 缺失、为空或无法加载，Hermes 将回退到内置的默认身份。

文件内容不会被任何包装语言包裹。内容本身才是关键——按照你希望 Agent 思考和表达的方式来写。

## 第一次编辑建议[​](#第一次编辑建议 "第一次编辑建议的直接链接")

如果你只做一件事，打开文件并修改几行，让它感觉像你自己的风格。

例如：

```
You are direct, calm, and technically precise.  
Prefer substance over politeness theater.  
Push back clearly when an idea is weak.  
Keep answers compact unless deeper detail is useful.
```

仅此一项就能明显改变 Hermes 的感觉。

## 示例风格[​](#示例风格 "示例风格的直接链接")

### 1. 务实工程师[​](#1-务实工程师 "1. 务实工程师的直接链接")

```
You are a pragmatic senior engineer.  
You care more about correctness and operational reality than sounding impressive.  
  
## Style  
- Be direct  
- Be concise unless complexity requires depth  
- Say when something is a bad idea  
- Prefer practical tradeoffs over idealized abstractions  
  
## Avoid  
- Sycophancy  
- Hype language  
- Overexplaining obvious things
```

### 2. 研究伙伴[​](#2-研究伙伴 "2. 研究伙伴的直接链接")

```
You are a thoughtful research collaborator.  
You are curious, honest about uncertainty, and excited by unusual ideas.  
  
## Style  
- Explore possibilities without pretending certainty  
- Distinguish speculation from evidence  
- Ask clarifying questions when the idea space is underspecified  
- Prefer conceptual depth over shallow completeness
```

### 3. 教师／讲解者[​](#3-教师讲解者 "3. 教师／讲解者的直接链接")

```
You are a patient technical teacher.  
You care about understanding, not performance.  
  
## Style  
- Explain clearly  
- Use examples when they help  
- Do not assume prior knowledge unless the user signals it  
- Build from intuition to details
```

### 4. 严格审阅者[​](#4-严格审阅者 "4. 严格审阅者的直接链接")

```
You are a rigorous reviewer.  
You are fair, but you do not soften important criticism.  
  
## Style  
- Point out weak assumptions directly  
- Prioritize correctness over harmony  
- Be explicit about risks and tradeoffs  
- Prefer blunt clarity to vague diplomacy
```

## 什么是优质的 SOUL.md？[​](#什么是优质的-soulmd "什么是优质的 SOUL.md？的直接链接")

优质的 `SOUL.md` 具备以下特点：

* 稳定
* 广泛适用
* 风格具体
* 不堆砌临时指令

劣质的 `SOUL.md` 则是：

* 充斥项目细节
* 自相矛盾
* 试图微观管理每一个回复的形式
* 大量泛泛之词，如"要有帮助"和"要清晰"

Hermes 本身已经尽力做到有帮助且清晰。`SOUL.md` 应当赋予真实的个性和风格，而不是重申显而易见的默认行为。

## 建议结构[​](#建议结构 "建议结构的直接链接")

不需要标题，但标题有助于组织内容。

一个实用的简单结构：

```
# Identity  
Who Hermes is.  
  
# Style  
How Hermes should sound.  
  
# Avoid  
What Hermes should not do.  
  
# Defaults  
How Hermes should behave when ambiguity appears.
```

## SOUL.md 与 /personality 的区别[​](#soulmd-与-personality-的区别 "SOUL.md 与 /personality 的区别的直接链接")

两者互为补充。

使用 `SOUL.md` 作为持久的基础设定。
使用 `/personality` 进行临时的模式切换。

示例：

* 你的默认 SOUL 是务实且直接的
* 某次会话中你使用 `/personality teacher`
* 之后切换回来，无需修改基础风格文件

## SOUL.md 与 AGENTS.md 的区别[​](#soulmd-与-agentsmd-的区别 "SOUL.md 与 AGENTS.md 的区别的直接链接")

这是最常见的误用。

### 放入 SOUL.md 的内容[​](#放入-soulmd-的内容 "放入 SOUL.md 的内容的直接链接")

* "Be direct."
* "Avoid hype language."
* "Prefer short answers unless depth helps."
* "Push back when the user is wrong."

### 放入 AGENTS.md 的内容[​](#放入-agentsmd-的内容 "放入 AGENTS.md 的内容的直接链接")

* "Use pytest, not unittest."
* "Frontend lives in `frontend/`."
* "Never edit migrations directly."
* "The API runs on port 8000."

## 如何编辑[​](#如何编辑 "如何编辑的直接链接")

```
nano ~/.hermes/SOUL.md
```

或

```
vim ~/.hermes/SOUL.md
```

然后重启 Hermes 或开启新会话。

## 实用工作流[​](#实用工作流 "实用工作流的直接链接")

1. 从自动生成的默认文件开始
2. 删除不符合你期望风格的内容
3. 添加 4–8 行清晰定义语气和默认行为的文字
4. 与 Hermes 交谈一段时间
5. 根据仍感觉不对的地方进行调整

这种迭代方式比一次性设计完美人设更有效。

## 故障排查[​](#故障排查 "故障排查的直接链接")

### 我编辑了 SOUL.md，但 Hermes 听起来还是一样[​](#我编辑了-soulmd但-hermes-听起来还是一样 "我编辑了 SOUL.md，但 Hermes 听起来还是一样的直接链接")

检查：

* 你编辑的是 `~/.hermes/SOUL.md` 或 `$HERMES_HOME/SOUL.md`
* 而不是某个仓库本地的 `SOUL.md`
* 文件不为空
* 编辑后已重启会话
* 没有 `/personality` 覆盖层主导了结果

### Hermes 忽略了我 SOUL.md 中的部分内容[​](#hermes-忽略了我-soulmd-中的部分内容 "Hermes 忽略了我 SOUL.md 中的部分内容的直接链接")

可能原因：

* 更高优先级的指令覆盖了它
* 文件中包含相互冲突的指导内容
* 文件过长被截断
* 部分文本类似提示词注入内容，可能被扫描器拦截或修改

### 我的 SOUL.md 变得过于项目化[​](#我的-soulmd-变得过于项目化 "我的 SOUL.md 变得过于项目化的直接链接")

将项目指令移入 `AGENTS.md`，保持 `SOUL.md` 专注于身份标识和风格。

## 相关文档[​](#相关文档 "相关文档的直接链接")

* [个性与 SOUL.md](/docs/zh-Hans/user-guide/features/personality)
* [上下文文件](/docs/zh-Hans/user-guide/features/context-files)
* [配置](/docs/zh-Hans/user-guide/configuration)
* [技巧与最佳实践](/docs/zh-Hans/guides/tips)

* [SOUL.md 的用途](#soulmd-的用途)
* [SOUL.md 不适用的内容](#soulmd-不适用的内容)
* [文件位置](#文件位置)
* [首次运行行为](#首次运行行为)
* [Hermes 如何使用它](#hermes-如何使用它)
* [第一次编辑建议](#第一次编辑建议)
* [示例风格](#示例风格)
  + [1. 务实工程师](#1-务实工程师)
  + [2. 研究伙伴](#2-研究伙伴)
  + [3. 教师／讲解者](#3-教师讲解者)
  + [4. 严格审阅者](#4-严格审阅者)
* [什么是优质的 SOUL.md？](#什么是优质的-soulmd)
* [建议结构](#建议结构)
* [SOUL.md 与 /personality 的区别](#soulmd-与-personality-的区别)
* [SOUL.md 与 AGENTS.md 的区别](#soulmd-与-agentsmd-的区别)
  + [放入 SOUL.md 的内容](#放入-soulmd-的内容)
  + [放入 AGENTS.md 的内容](#放入-agentsmd-的内容)
* [如何编辑](#如何编辑)
* [实用工作流](#实用工作流)
* [故障排查](#故障排查)
  + [我编辑了 SOUL.md，但 Hermes 听起来还是一样](#我编辑了-soulmd但-hermes-听起来还是一样)
  + [Hermes 忽略了我 SOUL.md 中的部分内容](#hermes-忽略了我-soulmd-中的部分内容)
  + [我的 SOUL.md 变得过于项目化](#我的-soulmd-变得过于项目化)
* [相关文档](#相关文档)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/tips](./docs-zh-Hans-guides-tips.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/configuration](./docs-zh-Hans-user-guide-configuration.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/context-files](./docs-zh-Hans-user-guide-features-context-files.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/personality](./docs-zh-Hans-user-guide-features-personality.md)
