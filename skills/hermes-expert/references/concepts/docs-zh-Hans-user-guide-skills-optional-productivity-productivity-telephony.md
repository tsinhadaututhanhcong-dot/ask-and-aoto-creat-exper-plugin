# 电话功能 — 无需修改核心工具即可赋予 Hermes 电话能力 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-telephony](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-telephony)

本页总览

无需修改核心工具即可赋予 Hermes 电话能力。配置并持久化 Twilio 号码，收发 SMS/MMS，直接拨打电话，以及通过 Bland.ai 或 Vapi 发起 AI 驱动的外呼。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 使用 `hermes skills install official/productivity/telephony` 安装 |
| 路径 | `optional-skills/productivity/telephony` |
| 版本 | `1.0.0` |
| 作者 | Nous Research |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `telephony`, `phone`, `sms`, `mms`, `voice`, `twilio`, `bland.ai`, `vapi`, `calling`, `texting` |
| 相关 skill | [`maps`](/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-maps), [`google-workspace`](/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-google-workspace), [`agentmail`](/docs/zh-Hans/user-guide/skills/optional/email/email-agentmail) |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时看到的指令内容。

# Telephony — 无需修改核心工具即可使用号码、通话和短信

此可选 skill 为 Hermes 提供实用的电话能力，同时将电话功能保留在核心工具列表之外。

它附带一个辅助脚本 `scripts/telephony.py`，可以：

* 将服务商凭据保存到 `~/.hermes/.env`
* 搜索并购买 Twilio 电话号码
* 记住已拥有的号码以供后续会话使用
* 从已拥有的号码发送 SMS / MMS
* 无需 webhook 服务器即可轮询该号码的入站 SMS
* 使用 TwiML `<Say>` 或 `<Play>` 直接拨打 Twilio 电话
* 将已拥有的 Twilio 号码导入 Vapi
* 通过 Bland.ai 或 Vapi 发起 AI 外呼

## 此 skill 解决的问题[​](#此-skill-解决的问题 "此 skill 解决的问题的直接链接")

此 skill 旨在覆盖用户实际需要的电话任务：

* 外呼
* 发短信
* 拥有一个可复用的 agent 号码
* 查看之后发送到该号码的消息
* 在会话之间保留该号码及相关 ID
* 为入站 SMS 轮询和其他自动化提供面向未来的电话身份

它**不会**将 Hermes 变成实时入站电话网关（gateway）。入站 SMS 通过轮询 Twilio REST API 处理。这对许多工作流已经足够，包括通知和部分一次性验证码获取，无需添加核心 webhook 基础设施。

## 安全规则 — 强制执行[​](#安全规则--强制执行 "安全规则 — 强制执行的直接链接")

1. 在拨打电话或发送短信前，始终先确认。
2. 禁止拨打紧急号码。
3. 禁止将电话功能用于骚扰、垃圾信息、冒充他人或任何违法行为。
4. 将第三方电话号码视为敏感操作数据：
   * 不要将其保存到 Hermes 记忆中
   * 除非用户明确要求，否则不要将其包含在 skill 文档、摘要或后续笔记中
5. 持久化**agent 拥有的 Twilio 号码**是允许的，因为这是用户配置的一部分。
6. VoIP 号码**不保证**适用于所有第三方双因素认证流程。请谨慎使用，并向用户明确说明预期。

## 决策树 — 选择哪个服务？[​](#决策树--选择哪个服务 "决策树 — 选择哪个服务？的直接链接")

使用以下逻辑，而非硬编码的服务商路由：

### 1）"我希望 Hermes 拥有一个真实的电话号码"[​](#1我希望-hermes-拥有一个真实的电话号码 "1）\"我希望 Hermes 拥有一个真实的电话号码\"的直接链接")

使用 **Twilio**。

原因：

* 购买并保留号码的最简路径
* 最佳 SMS / MMS 支持
* 最简单的入站 SMS 轮询方案
* 未来接入入站 webhook 或通话处理的最清晰路径

使用场景：

* 稍后接收短信
* 发送部署告警 / cron 通知
* 为 agent 维护可复用的电话身份
* 之后试验基于电话的认证流程

### 2）"我现在只需要最简单的 AI 外呼"[​](#2我现在只需要最简单的-ai-外呼 "2）\"我现在只需要最简单的 AI 外呼\"的直接链接")

使用 **Bland.ai**。

原因：

* 最快速的配置
* 只需一个 API key
* 无需先自行购买/导入号码

权衡：

* 灵活性较低
* 语音质量尚可，但不是最佳

### 3）"我想要最佳的对话式 AI 语音质量"[​](#3我想要最佳的对话式-ai-语音质量 "3）\"我想要最佳的对话式 AI 语音质量\"的直接链接")

使用 **Twilio + Vapi**。

原因：

* Twilio 提供已拥有的号码
* Vapi 提供更好的对话式 AI 通话质量和更多语音/模型灵活性

推荐流程：

1. 购买/保存 Twilio 号码
2. 将其导入 Vapi
3. 保存返回的 `VAPI_PHONE_NUMBER_ID`
4. 使用 `ai-call --provider vapi`

### 4）"我想用自定义预录语音消息拨打电话"[​](#4我想用自定义预录语音消息拨打电话 "4）\"我想用自定义预录语音消息拨打电话\"的直接链接")

使用 **Twilio 直接通话**配合公开音频 URL。

原因：

* 播放自定义 MP3 的最简方式
* 与 Hermes `text_to_speech` 加公开文件托管或隧道配合良好

## 文件与持久化状态[​](#文件与持久化状态 "文件与持久化状态的直接链接")

此 skill 在两个位置持久化电话状态：

### `~/.hermes/.env`[​](#hermesenv "hermesenv的直接链接")

用于长期存储的服务商凭据和已拥有号码的 ID，例如：

* `TWILIO_ACCOUNT_SID`
* `TWILIO_AUTH_TOKEN`
* `TWILIO_PHONE_NUMBER`
* `TWILIO_PHONE_NUMBER_SID`
* `BLAND_API_KEY`
* `VAPI_API_KEY`
* `VAPI_PHONE_NUMBER_ID`
* `PHONE_PROVIDER`（AI 外呼服务商：bland 或 vapi）

### `~/.hermes/telephony_state.json`[​](#hermestelephony_statejson "hermestelephony_statejson的直接链接")

用于仅限 skill 使用的、应在会话间保留的状态，例如：

* 记住的默认 Twilio 号码 / SID
* 记住的 Vapi 电话号码 ID
* 用于收件箱轮询检查点的最后一条入站消息 SID/日期

这意味着：

* 下次加载 skill 时，`diagnose` 可以告知已配置的号码
* `twilio-inbox --since-last --mark-seen` 可以从上次检查点继续

## 定位辅助脚本[​](#定位辅助脚本 "定位辅助脚本的直接链接")

安装此 skill 后，按如下方式定位脚本：

```
SCRIPT="$(find ~/.hermes/skills -path '*/telephony/scripts/telephony.py' -print -quit)"
```

如果 `SCRIPT` 为空，说明 skill 尚未安装。

## 安装[​](#安装 "安装的直接链接")

这是一个官方可选 skill，从 Skills Hub 安装：

```
hermes skills search telephony  
hermes skills install official/productivity/telephony
```

## 服务商配置[​](#服务商配置 "服务商配置的直接链接")

### Twilio — 拥有号码、SMS/MMS、直接通话、入站 SMS 轮询[​](#twilio--拥有号码smsmms直接通话入站-sms-轮询 "Twilio — 拥有号码、SMS/MMS、直接通话、入站 SMS 轮询的直接链接")

注册地址：

* <https://www.twilio.com/try-twilio>

然后将凭据保存到 Hermes：

```
python3 "$SCRIPT" save-twilio ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX your_auth_token_here
```

搜索可用号码：

```
python3 "$SCRIPT" twilio-search --country US --area-code 702 --limit 5
```

购买并记住一个号码：

```
python3 "$SCRIPT" twilio-buy "+17025551234" --save-env
```

列出已拥有的号码：

```
python3 "$SCRIPT" twilio-owned
```

之后将其中一个设为默认：

```
python3 "$SCRIPT" twilio-set-default "+17025551234" --save-env  
# 或  
python3 "$SCRIPT" twilio-set-default PNXXXXXXXXXXXXXXXXXXXXXXXXXXXX --save-env
```

### Bland.ai — 最简单的 AI 外呼[​](#blandai--最简单的-ai-外呼 "Bland.ai — 最简单的 AI 外呼的直接链接")

注册地址：

* <https://app.bland.ai>

保存配置：

```
python3 "$SCRIPT" save-bland your_bland_api_key --voice mason
```

### Vapi — 更好的对话式语音质量[​](#vapi--更好的对话式语音质量 "Vapi — 更好的对话式语音质量的直接链接")

注册地址：

* <https://dashboard.vapi.ai>

先保存 API key：

```
python3 "$SCRIPT" save-vapi your_vapi_api_key
```

将已拥有的 Twilio 号码导入 Vapi 并持久化返回的电话号码 ID：

```
python3 "$SCRIPT" vapi-import-twilio --save-env
```

如果已知 Vapi 电话号码 ID，可直接保存：

```
python3 "$SCRIPT" save-vapi your_vapi_api_key --phone-number-id vapi_phone_number_id_here
```

## 诊断当前状态[​](#诊断当前状态 "诊断当前状态的直接链接")

随时检查 skill 已知的信息：

```
python3 "$SCRIPT" diagnose
```

在后续会话中恢复工作时，请先运行此命令。

## 常见工作流[​](#常见工作流 "常见工作流的直接链接")

### A. 购买 agent 号码并在之后继续使用[​](#a-购买-agent-号码并在之后继续使用 "A. 购买 agent 号码并在之后继续使用的直接链接")

1. 保存 Twilio 凭据：

```
python3 "$SCRIPT" save-twilio AC... auth_token_here
```

2. 搜索号码：

```
python3 "$SCRIPT" twilio-search --country US --area-code 702 --limit 10
```

3. 购买并保存到 `~/.hermes/.env` 及状态文件：

```
python3 "$SCRIPT" twilio-buy "+17025551234" --save-env
```

4. 下次会话时运行：

```
python3 "$SCRIPT" diagnose
```

这将显示记住的默认号码和收件箱检查点状态。

### B. 从 agent 号码发送短信[​](#b-从-agent-号码发送短信 "B. 从 agent 号码发送短信的直接链接")

```
python3 "$SCRIPT" twilio-send-sms "+15551230000" "Your deployment completed successfully."
```

带媒体文件：

```
python3 "$SCRIPT" twilio-send-sms "+15551230000" "Here is the chart." --media-url "https://example.com/chart.png"
```

### C. 无需 webhook 服务器即可查看入站短信[​](#c-无需-webhook-服务器即可查看入站短信 "C. 无需 webhook 服务器即可查看入站短信的直接链接")

轮询默认 Twilio 号码的收件箱：

```
python3 "$SCRIPT" twilio-inbox --limit 20
```

仅显示上次检查点之后收到的消息，读取完毕后推进检查点：

```
python3 "$SCRIPT" twilio-inbox --since-last --mark-seen
```

这是"下次加载 skill 时如何访问该号码收到的消息"的主要解决方案。

### D. 使用内置 TTS 直接拨打 Twilio 电话[​](#d-使用内置-tts-直接拨打-twilio-电话 "D. 使用内置 TTS 直接拨打 Twilio 电话的直接链接")

```
python3 "$SCRIPT" twilio-call "+15551230000" --message "Hello! This is Hermes calling with your status update." --voice Polly.Joanna
```

### E. 使用预录/自定义语音消息拨打电话[​](#e-使用预录自定义语音消息拨打电话 "E. 使用预录/自定义语音消息拨打电话的直接链接")

这是复用 Hermes 现有 `text_to_speech` 支持的主要路径。

适用场景：

* 希望通话使用 Hermes 配置的 TTS 语音，而非 Twilio `<Say>`
* 需要单向语音传递（简报、告警、提醒、状态更新）
* **不**需要实时对话式电话通话

单独生成或托管音频，然后：

```
python3 "$SCRIPT" twilio-call "+155****0000" --audio-url "https://example.com/briefing.mp3"
```

推荐的 Hermes TTS -> Twilio Play 工作流：

1. 使用 Hermes `text_to_speech` 生成音频。
2. 使生成的 MP3 可公开访问。
3. 使用 `--audio-url` 拨打 Twilio 电话进行传递。

示例 agent 流程：

* 让 Hermes 使用 `text_to_speech` 创建消息音频
* 如有需要，通过临时静态托管/隧道/对象存储 URL 暴露文件
* 使用 `twilio-call --audio-url ...` 通过电话传递

MP3 的推荐托管方式：

* 临时公开对象/存储 URL
* 指向本地静态文件服务器的短期隧道
* 电话服务商可直接获取的任意 HTTPS URL

重要说明：

* Hermes TTS 非常适合预录外呼消息
* Bland/Vapi 更适合**实时对话式 AI 通话**，因为它们自行处理实时电话音频栈
* 此处单独使用 Hermes STT/TTS 并非作为全双工电话对话引擎；那将需要比此 skill 所要引入的更重量级的流式/webhook 集成

### F. 使用 Twilio 直接通话导航电话树 / IVR[​](#f-使用-twilio-直接通话导航电话树--ivr "F. 使用 Twilio 直接通话导航电话树 / IVR的直接链接")

如果需要在通话接通后按键，请使用 `--send-digits`。
Twilio 将 `w` 解释为短暂等待。

```
python3 "$SCRIPT" twilio-call "+18005551234" --message "Connecting to billing now." --send-digits "ww1w2w3"
```

这对于在转接人工或传递简短状态消息之前进入特定菜单分支非常有用。

### G. 通过 Bland.ai 发起 AI 外呼[​](#g-通过-blandai-发起-ai-外呼 "G. 通过 Bland.ai 发起 AI 外呼的直接链接")

```
python3 "$SCRIPT" ai-call "+15551230000" "Call the dental office, ask for a cleaning appointment on Tuesday afternoon, and if they do not have Tuesday availability, ask for Wednesday or Thursday instead." --provider bland --voice mason --max-duration 3
```

查看状态：

```
python3 "$SCRIPT" ai-status <call_id> --provider bland
```

通话结束后向 Bland 提问分析：

```
python3 "$SCRIPT" ai-status <call_id> --provider bland --analyze "Was the appointment confirmed?,What date and time?,Any special instructions?"
```

### H. 通过 Vapi 使用已拥有号码发起 AI 外呼[​](#h-通过-vapi-使用已拥有号码发起-ai-外呼 "H. 通过 Vapi 使用已拥有号码发起 AI 外呼的直接链接")

1. 将 Twilio 号码导入 Vapi：

```
python3 "$SCRIPT" vapi-import-twilio --save-env
```

2. 拨打电话：

```
python3 "$SCRIPT" ai-call "+15551230000" "You are calling to make a dinner reservation for two at 7:30 PM. If that is unavailable, ask for the nearest time between 6:30 and 8:30 PM." --provider vapi --max-duration 4
```

3. 查看结果：

```
python3 "$SCRIPT" ai-status <call_id> --provider vapi
```

## 建议的 agent 操作流程[​](#建议的-agent-操作流程 "建议的 agent 操作流程的直接链接")

当用户请求通话或发送短信时：

1. 通过决策树确定适合请求的路径。
2. 如果配置状态不明确，运行 `diagnose`。
3. 收集完整的任务详情。
4. 在拨号或发送短信前与用户确认。
5. 使用正确的命令。
6. 如有需要，轮询结果。
7. 总结结果，不要将第三方电话号码持久化到 Hermes 记忆中。

## 此 skill 仍不支持的功能[​](#此-skill-仍不支持的功能 "此 skill 仍不支持的功能的直接链接")

* 实时入站电话接听
* 基于 webhook 的实时 SMS 推送到 agent 循环
* 对任意第三方双因素认证服务商的保证支持

这些功能需要比纯可选 skill 更多的基础设施。

## 注意事项[​](#注意事项 "注意事项的直接链接")

* Twilio 试用账户和地区规则可能限制可拨打/发送短信的对象。
* 部分服务拒绝 VoIP 号码用于双因素认证。
* `twilio-inbox` 轮询 REST API；不是即时推送传递。
* Vapi 外呼仍依赖于拥有有效的已导入号码。
* Bland 最简单，但音质不一定最佳。
* 不要将任意第三方电话号码存储在 Hermes 记忆中。

## 验证清单[​](#验证清单 "验证清单的直接链接")

配置完成后，仅使用此 skill 应能完成以下所有操作：

1. `diagnose` 显示服务商就绪状态和记住的状态
2. 搜索并购买 Twilio 号码
3. 将该号码持久化到 `~/.hermes/.env`
4. 从已拥有的号码发送 SMS
5. 之后轮询已拥有号码的入站短信
6. 拨打直接 Twilio 电话
7. 通过 Bland 或 Vapi 发起 AI 外呼

## 参考资料[​](#参考资料 "参考资料的直接链接")

* Twilio 电话号码：<https://www.twilio.com/docs/phone-numbers/api>
* Twilio 消息：<https://www.twilio.com/docs/messaging/api/message-resource>
* Twilio 语音：<https://www.twilio.com/docs/voice/api/call-resource>
* Vapi 文档：<https://docs.vapi.ai/>
* Bland.ai：<https://app.bland.ai/>

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [此 skill 解决的问题](#此-skill-解决的问题)
* [安全规则 — 强制执行](#安全规则--强制执行)
* [决策树 — 选择哪个服务？](#决策树--选择哪个服务)
  + [1）"我希望 Hermes 拥有一个真实的电话号码"](#1我希望-hermes-拥有一个真实的电话号码)
  + [2）"我现在只需要最简单的 AI 外呼"](#2我现在只需要最简单的-ai-外呼)
  + [3）"我想要最佳的对话式 AI 语音质量"](#3我想要最佳的对话式-ai-语音质量)
  + [4）"我想用自定义预录语音消息拨打电话"](#4我想用自定义预录语音消息拨打电话)
* [文件与持久化状态](#文件与持久化状态)
  + [`~/.hermes/.env`](#hermesenv)
  + [`~/.hermes/telephony_state.json`](#hermestelephony_statejson)
* [定位辅助脚本](#定位辅助脚本)
* [安装](#安装)
* [服务商配置](#服务商配置)
  + [Twilio — 拥有号码、SMS/MMS、直接通话、入站 SMS 轮询](#twilio--拥有号码smsmms直接通话入站-sms-轮询)
  + [Bland.ai — 最简单的 AI 外呼](#blandai--最简单的-ai-外呼)
  + [Vapi — 更好的对话式语音质量](#vapi--更好的对话式语音质量)
* [诊断当前状态](#诊断当前状态)
* [常见工作流](#常见工作流)
  + [A. 购买 agent 号码并在之后继续使用](#a-购买-agent-号码并在之后继续使用)
  + [B. 从 agent 号码发送短信](#b-从-agent-号码发送短信)
  + [C. 无需 webhook 服务器即可查看入站短信](#c-无需-webhook-服务器即可查看入站短信)
  + [D. 使用内置 TTS 直接拨打 Twilio 电话](#d-使用内置-tts-直接拨打-twilio-电话)
  + [E. 使用预录/自定义语音消息拨打电话](#e-使用预录自定义语音消息拨打电话)
  + [F. 使用 Twilio 直接通话导航电话树 / IVR](#f-使用-twilio-直接通话导航电话树--ivr)
  + [G. 通过 Bland.ai 发起 AI 外呼](#g-通过-blandai-发起-ai-外呼)
  + [H. 通过 Vapi 使用已拥有号码发起 AI 外呼](#h-通过-vapi-使用已拥有号码发起-ai-外呼)
* [建议的 agent 操作流程](#建议的-agent-操作流程)
* [此 skill 仍不支持的功能](#此-skill-仍不支持的功能)
* [注意事项](#注意事项)
* [验证清单](#验证清单)
* [参考资料](#参考资料)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-google-workspace](./docs-zh-Hans-user-guide-skills-bundled-productivity-productivity-google-workspace.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-maps](./docs-zh-Hans-user-guide-skills-bundled-productivity-productivity-maps.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/email/email-agentmail](./docs-zh-Hans-user-guide-skills-optional-email-email-agentmail.md)
