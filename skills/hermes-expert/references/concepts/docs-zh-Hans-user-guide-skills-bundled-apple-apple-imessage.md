# Imessage — 通过 macOS 上的 imsg CLI 发送和接收 iMessages/SMS | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/apple/apple-imessage](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/apple/apple-imessage)

本页总览

通过 macOS 上的 imsg CLI 发送和接收 iMessages/SMS。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/apple/imessage` |
| 版本 | `1.0.0` |
| 作者 | Hermes Agent |
| 许可证 | MIT |
| 平台 | macos |
| 标签 | `iMessage`, `SMS`, `messaging`, `macOS`, `Apple` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# iMessage

使用 `imsg` 通过 macOS Messages.app 读取和发送 iMessage/SMS。

## 前提条件[​](#前提条件 "前提条件的直接链接")

* **macOS** 且 Messages.app 已登录
* 安装：`brew install steipete/tap/imsg`
* 在终端授予完全磁盘访问权限（系统设置 → 隐私与安全 → 完全磁盘访问）
* 在提示时授予 Messages.app 的自动化权限

## 何时使用[​](#何时使用 "何时使用的直接链接")

* 用户请求发送 iMessage 或短信
* 读取 iMessage 对话历史
* 查看 Messages.app 最近的聊天记录
* 发送至电话号码或 Apple ID

## 何时不使用[​](#何时不使用 "何时不使用的直接链接")

* Telegram/Discord/Slack/WhatsApp 消息 → 使用相应的 gateway 频道
* 群聊管理（添加/移除成员）→ 不支持
* 批量/群发消息 → 始终先与用户确认

## 快速参考[​](#快速参考 "快速参考的直接链接")

### 列出聊天[​](#列出聊天 "列出聊天的直接链接")

```
imsg chats --limit 10 --json
```

### 查看历史记录[​](#查看历史记录 "查看历史记录的直接链接")

```
# 通过聊天 ID  
imsg history --chat-id 1 --limit 20 --json  
  
# 包含附件信息  
imsg history --chat-id 1 --limit 20 --attachments --json
```

### 发送消息[​](#发送消息 "发送消息的直接链接")

```
# 仅文本  
imsg send --to "+14155551212" --text "Hello!"  
  
# 带附件  
imsg send --to "+14155551212" --text "Check this out" --file /path/to/image.jpg  
  
# 强制使用 iMessage 或 SMS  
imsg send --to "+14155551212" --text "Hi" --service imessage  
imsg send --to "+14155551212" --text "Hi" --service sms
```

### 监听新消息[​](#监听新消息 "监听新消息的直接链接")

```
imsg watch --chat-id 1 --attachments
```

## 服务选项[​](#服务选项 "服务选项的直接链接")

* `--service imessage` — 强制使用 iMessage（要求收件人已开启 iMessage）
* `--service sms` — 强制使用 SMS（绿色气泡）
* `--service auto` — 由 Messages.app 自动决定（默认）

## 规则[​](#规则 "规则的直接链接")

1. **发送前始终确认收件人和消息内容**
2. **未经用户明确批准，不得向未知号码发送消息**
3. **附件前验证文件路径**是否存在
4. **不要刷屏** — 自行控制发送频率

## 示例工作流[​](#示例工作流 "示例工作流的直接链接")

用户："发短信告诉妈妈我会晚到"

```
# 1. 找到妈妈的聊天  
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("Mom"))'  
  
# 2. 与用户确认："找到 Mom，号码为 +1555123456。通过 iMessage 发送'I'll be late'？"  
  
# 3. 确认后发送  
imsg send --to "+1555123456" --text "I'll be late"
```

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [前提条件](#前提条件)
* [何时使用](#何时使用)
* [何时不使用](#何时不使用)
* [快速参考](#快速参考)
  + [列出聊天](#列出聊天)
  + [查看历史记录](#查看历史记录)
  + [发送消息](#发送消息)
  + [监听新消息](#监听新消息)
* [服务选项](#服务选项)
* [规则](#规则)
* [示例工作流](#示例工作流)