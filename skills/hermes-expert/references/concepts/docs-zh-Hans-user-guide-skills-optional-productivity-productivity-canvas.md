# Canvas — Canvas LMS 集成 — 使用 API token 认证获取已注册课程和作业 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-canvas](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-canvas)

本页总览

Canvas LMS 集成 — 使用 API token（令牌）认证获取已注册课程和作业。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/productivity/canvas` 安装 |
| 路径 | `optional-skills/productivity/canvas` |
| 版本 | `1.0.0` |
| 作者 | community |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `Canvas`, `LMS`, `Education`, `Courses`, `Assignments` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# Canvas LMS — 课程与作业访问

对 Canvas LMS 的只读访问，用于列出课程和作业。

## 脚本[​](#脚本 "脚本的直接链接")

* `scripts/canvas_api.py` — 用于 Canvas API 调用的 Python CLI

## 配置[​](#配置 "配置的直接链接")

1. 在浏览器中登录你的 Canvas 实例
2. 进入 **Account → Settings**（点击个人头像，然后点击 Settings）
3. 滚动到 **Approved Integrations**，点击 **+ New Access Token**
4. 为 token 命名（例如 "Hermes Agent"），设置可选的过期时间，然后点击 **Generate Token**
5. 复制 token 并添加到 `~/.hermes/.env`：

```
CANVAS_API_TOKEN=your_token_here  
CANVAS_BASE_URL=https://yourschool.instructure.com
```

base URL 即你登录 Canvas 后浏览器地址栏中显示的地址（末尾不加斜杠）。

## 使用方法[​](#使用方法 "使用方法的直接链接")

```
CANVAS="python $HERMES_HOME/skills/productivity/canvas/scripts/canvas_api.py"  
  
# 列出所有已激活的课程  
$CANVAS list_courses --enrollment-state active  
  
# 列出所有课程（任意状态）  
$CANVAS list_courses  
  
# 列出指定课程的作业  
$CANVAS list_assignments 12345  
  
# 按截止日期排序列出作业  
$CANVAS list_assignments 12345 --order-by due_at
```

## 输出格式[​](#输出格式 "输出格式的直接链接")

**list\_courses** 返回：

```
[{"id": 12345, "name": "Intro to CS", "course_code": "CS101", "workflow_state": "available", "start_at": "...", "end_at": "..."}]
```

**list\_assignments** 返回：

```
[{"id": 67890, "name": "Homework 1", "due_at": "2025-02-15T23:59:00Z", "points_possible": 100, "submission_types": ["online_upload"], "html_url": "...", "description": "...", "course_id": 12345}]
```

注意：作业描述截断为 500 个字符。`html_url` 字段链接到 Canvas 中完整的作业页面。

## API 参考（curl）[​](#api-参考curl "API 参考（curl）的直接链接")

```
# 列出课程  
curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
  "$CANVAS_BASE_URL/api/v1/courses?enrollment_state=active&per_page=10"  
  
# 列出某课程的作业  
curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \  
  "$CANVAS_BASE_URL/api/v1/courses/COURSE_ID/assignments?per_page=10&order_by=due_at"
```

Canvas 使用 `Link` 响应头进行分页。Python 脚本会自动处理分页。

## 规则[​](#规则 "规则的直接链接")

* 此 skill 为**只读** — 仅获取数据，不修改课程或作业
* 首次使用时，运行 `$CANVAS list_courses` 验证认证 — 若返回 401 错误，请引导用户完成配置
* Canvas 限速约为每 10 分钟 700 次请求；若触及限制，请检查 `X-Rate-Limit-Remaining` 响应头

## 故障排查[​](#故障排查 "故障排查的直接链接")

| 问题 | 解决方法 |
| --- | --- |
| 401 Unauthorized | Token 无效或已过期 — 在 Canvas Settings 中重新生成 |
| 403 Forbidden | Token 无权访问此课程 |
| 课程列表为空 | 尝试 `--enrollment-state active` 或省略该参数以查看所有状态 |
| 机构错误 | 确认 `CANVAS_BASE_URL` 与浏览器中的地址一致 |
| 超时错误 | 检查与 Canvas 实例的网络连接 |

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [脚本](#脚本)
* [配置](#配置)
* [使用方法](#使用方法)
* [输出格式](#输出格式)
* [API 参考（curl）](#api-参考curl)
* [规则](#规则)
* [故障排查](#故障排查)