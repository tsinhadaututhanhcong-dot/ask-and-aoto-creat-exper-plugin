# Microsoft Teams | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/teams](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/teams)

本页总览

将 Hermes Agent 作为机器人接入 Microsoft Teams。与 Slack 的 Socket Mode 不同，Teams 通过调用**公开 HTTPS webhook**（钩子）来投递消息，因此你的实例需要一个可公开访问的端点——本地开发时使用开发隧道，生产环境使用真实域名。

如果你需要的是来自 Microsoft Graph 事件的会议摘要，而非普通的机器人对话，请使用专用设置页面：[Teams 会议](/docs/zh-Hans/user-guide/messaging/teams-meetings)。

## 机器人的响应方式[​](#机器人的响应方式 "机器人的响应方式的直接链接")

| 场景 | 行为 |
| --- | --- |
| **个人聊天（私信）** | 机器人响应每一条消息，无需 @提及。 |
| **群聊** | 机器人仅在被 @提及时响应。 |
| **频道** | 机器人仅在被 @提及时响应。 |

Teams 将 @提及作为普通消息投递，其中包含 `<at>BotName</at>` 标签，Hermes 在处理前会自动去除这些标签。

---

## 第一步：安装 Teams CLI[​](#第一步安装-teams-cli "第一步：安装 Teams CLI的直接链接")

`@microsoft/teams.cli` 可自动完成机器人注册，无需进入 Azure 门户。

```
npm install -g @microsoft/teams.cli@preview  
teams login
```

验证登录状态并查找你自己的 AAD 对象 ID（`TEAMS_ALLOWED_USERS` 需要用到）：

```
teams status --verbose
```

---

## 第二步：暴露 Webhook 端口[​](#第二步暴露-webhook-端口 "第二步：暴露 Webhook 端口的直接链接")

Teams 无法向 `localhost` 投递消息。本地开发时，使用任意隧道工具获取一个公开的 HTTPS URL。默认端口为 `3978`，如需更改可通过 `TEAMS_PORT` 设置。

```
# devtunnel（Microsoft 官方）  
devtunnel create hermes-bot --allow-anonymous  
devtunnel port create hermes-bot -p 3978 --protocol https  # 如已修改 TEAMS_PORT，请替换 3978  
devtunnel host hermes-bot  
  
# ngrok  
ngrok http 3978  # 如已修改 TEAMS_PORT，请替换 3978  
  
# cloudflared  
cloudflared tunnel --url http://localhost:3978  # 如已修改 TEAMS_PORT，请替换 3978
```

从输出中复制 `https://` URL——下一步会用到。开发期间保持隧道运行。

生产环境请将机器人端点指向服务器的公开域名（参见[生产部署](#production-deployment)）。

---

## 第三步：创建机器人[​](#第三步创建机器人 "第三步：创建机器人的直接链接")

```
teams app create \  
  --name "Hermes" \  
  --endpoint "https://<your-tunnel-url>/api/messages"
```

CLI 会输出你的 `CLIENT_ID`、`CLIENT_SECRET` 和 `TENANT_ID`，以及第六步所需的安装链接。请保存客户端密钥——它不会再次显示。

---

## 第四步：配置环境变量[​](#第四步配置环境变量 "第四步：配置环境变量的直接链接")

添加到 `~/.hermes/.env`：

```
# 必填  
TEAMS_CLIENT_ID=<your-client-id>  
TEAMS_CLIENT_SECRET=<your-client-secret>  
TEAMS_TENANT_ID=<your-tenant-id>  
  
# 限制特定用户访问（推荐）  
# 使用 `teams status --verbose` 获取 AAD 对象 ID  
TEAMS_ALLOWED_USERS=<your-aad-object-id>
```

---

## 第五步：启动 Gateway[​](#第五步启动-gateway "第五步：启动 Gateway的直接链接")

```
HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d gateway
```

此命令启动 gateway。默认 webhook 端口为 `3978`（可通过 `TEAMS_PORT` 覆盖）。检查运行状态：

```
curl http://localhost:3978/health   # 应返回：ok  
docker logs -f hermes
```

查找以下日志：

```
[teams] Webhook server listening on 0.0.0.0:3978/api/messages
```

---

## 第六步：在 Teams 中安装应用[​](#第六步在-teams-中安装应用 "第六步：在 Teams 中安装应用的直接链接")

```
teams app get <teamsAppId> --install-link
```

在浏览器中打开输出的链接——它会直接在 Teams 客户端中打开。安装完成后，向机器人发送一条私信，即可开始使用。

---

## 配置参考[​](#配置参考 "配置参考的直接链接")

### 环境变量[​](#环境变量 "环境变量的直接链接")

| 变量 | 说明 |
| --- | --- |
| `TEAMS_CLIENT_ID` | Azure AD 应用（客户端）ID |
| `TEAMS_CLIENT_SECRET` | Azure AD 客户端密钥 |
| `TEAMS_TENANT_ID` | Azure AD 租户 ID |
| `TEAMS_ALLOWED_USERS` | 允许使用机器人的 AAD 对象 ID，逗号分隔 |
| `TEAMS_ALLOW_ALL_USERS` | 设为 `true` 可跳过白名单，允许所有人使用 |
| `TEAMS_HOME_CHANNEL` | 用于 cron/主动消息投递的会话 ID |
| `TEAMS_HOME_CHANNEL_NAME` | 主频道的显示名称 |
| `TEAMS_PORT` | Webhook 端口（默认：`3978`） |

### config.yaml[​](#configyaml "config.yaml的直接链接")

也可通过 `~/.hermes/config.yaml` 进行配置：

```
platforms:  
  teams:  
    enabled: true  
    extra:  
      client_id: "your-client-id"  
      client_secret: "your-secret"  
      tenant_id: "your-tenant-id"  
      port: 3978
```

---

## 功能特性[​](#功能特性 "功能特性的直接链接")

### 交互式审批卡片[​](#交互式审批卡片 "交互式审批卡片的直接链接")

当 Agent 需要执行可能存在风险的命令时，它会发送一张带有四个按钮的 Adaptive Card，而不是要求你输入 `/approve`：

* **Allow Once**——仅批准此次特定命令
* **Allow Session**——在本次会话期间批准此模式
* **Always Allow**——永久批准此模式
* **Deny**——拒绝该命令

点击按钮即可内联完成审批，卡片会被替换为决策结果。

### 会议摘要投递（Teams 会议 Pipeline）[​](#会议摘要投递teams-会议-pipeline "会议摘要投递（Teams 会议 Pipeline）的直接链接")

当 [Teams 会议 pipeline 插件](/docs/zh-Hans/user-guide/messaging/msgraph-webhook)启用后，此适配器同时负责会议摘要的出站投递——一个 Teams 集成面，而非两个。会议转录摘要生成后，写入器会将摘要发布到你指定的 Teams 目标。

Pipeline 摘要投递在 `teams` 平台条目下与机器人配置并列配置：

```
platforms:  
  teams:  
    enabled: true  
    extra:  
      # 现有机器人配置（client_id、client_secret、tenant_id、port）...  
  
      # 会议摘要投递（仅在 teams_pipeline 插件启用时生效）  
      delivery_mode: "graph"       # 或 "incoming_webhook"  
      # 对于 delivery_mode: graph — 选择其中一项：  
      chat_id: "19:meeting_..."    # 发布到 Teams 聊天  
      # team_id: "..."             # 或发布到频道  
      # channel_id: "..."  
      # access_token: "..."        # 可选；回退到 MSGRAPH_* 应用凭据  
      # 对于 delivery_mode: incoming_webhook：  
      # incoming_webhook_url: "https://outlook.office.com/webhook/..."
```

| 模式 | 适用场景 | 权衡 |
| --- | --- | --- |
| `incoming_webhook` | 使用 Teams 生成的静态 URL，简单地将摘要发布到某个频道。 | 不支持回复线程和表情回应，显示为 webhook 配置的身份。 |
| `graph` | 通过 Microsoft Graph 以机器人身份发布带线程的频道帖子或 1:1/群聊消息。 | 需要完成 [Graph 应用注册](/docs/zh-Hans/guides/microsoft-graph-app-registration)，并具备 `ChannelMessage.Send`（频道）或 `Chat.ReadWrite.All`（聊天）应用权限。 |

如果 `teams_pipeline` 插件**未启用**，这些设置不会生效——它们仅在 pipeline 运行时绑定到 Graph webhook 入口时才会激活。

---

## 生产部署[​](#生产部署 "生产部署的直接链接")

对于永久服务器，跳过 devtunnel，使用服务器的公开 HTTPS 端点注册机器人：

```
teams app create \  
  --name "Hermes" \  
  --endpoint "https://your-domain.com/api/messages"
```

如果机器人已创建，只需更新端点：

```
teams app update --id <teamsAppId> --endpoint "https://your-domain.com/api/messages"
```

确保你配置的端口（`TEAMS_PORT`，默认 `3978`）可从互联网访问，且 TLS 证书有效——Teams 会拒绝自签名证书。

---

## 故障排查[​](#故障排查 "故障排查的直接链接")

| 问题 | 解决方案 |
| --- | --- |
| `health` 端点正常但机器人不响应 | 检查隧道是否仍在运行，以及机器人的消息端点是否与隧道 URL 匹配 |
| 日志中出现 `KeyError: 'teams'` | 重启容器——此问题已在当前版本中修复 |
| 机器人响应时出现认证错误 | 验证 `TEAMS_CLIENT_ID`、`TEAMS_CLIENT_SECRET` 和 `TEAMS_TENANT_ID` 是否均已正确设置 |
| `No inference provider configured` | 检查 `~/.hermes/.env` 中是否设置了 `ANTHROPIC_API_KEY`（或其他提供商密钥） |
| 机器人收到消息但忽略它们 | 你的 AAD 对象 ID 可能不在 `TEAMS_ALLOWED_USERS` 中。运行 `teams status --verbose` 查找 |
| 隧道 URL 在重启后变更 | 使用命名隧道（`devtunnel create hermes-bot`）时，devtunnel URL 是持久的。ngrok 和 cloudflared 每次运行都会生成新 URL（除非你有付费计划）——URL 变更时请用 `teams app update` 更新机器人端点 |
| Teams 显示"此机器人未响应" | Webhook 返回了错误。检查 `docker logs hermes` 中的错误堆栈 |
| 日志中出现 `[teams] Failed to connect` | SDK 认证失败。仔细检查凭据，并确认租户 ID 与 `teams login` 时使用的账户匹配 |

---

## 安全性[​](#安全性 "安全性的直接链接")

注意

**务必设置 `TEAMS_ALLOWED_USERS`**，填入授权用户的 AAD 对象 ID。否则，任何能找到或安装你的机器人的人都可以与其交互。

将 `TEAMS_CLIENT_SECRET` 视同密码对待——定期通过 Azure 门户或 Teams CLI 进行轮换。

* 将凭据存储在权限为 `600` 的 `~/.hermes/.env` 中（`chmod 600 ~/.hermes/.env`）
* 机器人仅接受 `TEAMS_ALLOWED_USERS` 中用户的消息；未授权的消息会被静默丢弃
* 你的公开端点（`/api/messages`）由 Teams Bot Framework 进行认证——不含有效 JWT 的请求会被拒绝

## 相关文档[​](#相关文档 "相关文档的直接链接")

* [Teams 会议](/docs/zh-Hans/user-guide/messaging/teams-meetings)
* [运营 Teams 会议 Pipeline](/docs/zh-Hans/guides/operate-teams-meeting-pipeline)

* [机器人的响应方式](#机器人的响应方式)
* [第一步：安装 Teams CLI](#第一步安装-teams-cli)
* [第二步：暴露 Webhook 端口](#第二步暴露-webhook-端口)
* [第三步：创建机器人](#第三步创建机器人)
* [第四步：配置环境变量](#第四步配置环境变量)
* [第五步：启动 Gateway](#第五步启动-gateway)
* [第六步：在 Teams 中安装应用](#第六步在-teams-中安装应用)
* [配置参考](#配置参考)
  + [环境变量](#环境变量)
  + [config.yaml](#configyaml)
* [功能特性](#功能特性)
  + [交互式审批卡片](#交互式审批卡片)
  + [会议摘要投递（Teams 会议 Pipeline）](#会议摘要投递teams-会议-pipeline)
* [生产部署](#生产部署)
* [故障排查](#故障排查)
* [安全性](#安全性)
* [相关文档](#相关文档)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/microsoft-graph-app-registration](./docs-zh-Hans-guides-microsoft-graph-app-registration.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/operate-teams-meeting-pipeline](./docs-zh-Hans-guides-operate-teams-meeting-pipeline.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/msgraph-webhook](./docs-zh-Hans-user-guide-messaging-msgraph-webhook.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/teams-meetings](./docs-zh-Hans-user-guide-messaging-teams-meetings.md)
