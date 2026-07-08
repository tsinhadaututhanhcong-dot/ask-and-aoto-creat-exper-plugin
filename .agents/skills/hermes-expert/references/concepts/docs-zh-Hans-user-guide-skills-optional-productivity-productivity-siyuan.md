# Siyuan | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-siyuan](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/productivity/productivity-siyuan)

本页总览

通过 curl 调用 SiYuan Note API，在自托管知识库中搜索、读取、创建和管理块与文档。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 使用 `hermes skills install official/productivity/siyuan` 安装 |
| 路径 | `optional-skills/productivity/siyuan` |
| 版本 | `1.0.0` |
| 作者 | FEUAZUR |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `SiYuan`, `Notes`, `Knowledge Base`, `PKM`, `API` |
| 相关 skill | [`obsidian`](/docs/zh-Hans/user-guide/skills/bundled/note-taking/note-taking-obsidian), [`notion`](/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-notion) |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# SiYuan Note API

通过 curl 调用 [SiYuan](https://github.com/siyuan-note/siyuan) 内核 API，在自托管知识库中搜索、读取、创建、更新和删除块与文档。无需额外工具 — 只需 curl 和 API token。

## 前提条件[​](#前提条件 "前提条件的直接链接")

1. 安装并运行 SiYuan（桌面版或 Docker）
2. 获取 API token：**设置 > 关于 > API token**
3. 将其存储在 `~/.hermes/.env` 中：

   ```
   SIYUAN_TOKEN=your_token_here  
   SIYUAN_URL=http://127.0.0.1:6806
   ```

   若未设置，`SIYUAN_URL` 默认为 `http://127.0.0.1:6806`。

## API 基础[​](#api-基础 "API 基础的直接链接")

所有 SiYuan API 调用均为 **POST 请求，携带 JSON 请求体**。每个请求遵循以下模式：

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/..." \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"param": "value"}'
```

响应为 JSON，结构如下：

```
{"code": 0, "msg": "", "data": { ... }}
```

`code: 0` 表示成功。其他值均为错误 — 请检查 `msg` 获取详情。

**ID 格式：** SiYuan ID 形如 `20210808180117-6v0mkxr`（14 位时间戳 + 7 位字母数字字符）。

## 快速参考[​](#快速参考 "快速参考的直接链接")

| 操作 | 端点 |
| --- | --- |
| 全文搜索 | `/api/search/fullTextSearchBlock` |
| SQL 查询 | `/api/query/sql` |
| 读取块 | `/api/block/getBlockKramdown` |
| 读取子块 | `/api/block/getChildBlocks` |
| 获取路径 | `/api/filetree/getHPathByID` |
| 获取属性 | `/api/attr/getBlockAttrs` |
| 列出笔记本 | `/api/notebook/lsNotebooks` |
| 列出文档 | `/api/filetree/listDocsByPath` |
| 创建笔记本 | `/api/notebook/createNotebook` |
| 创建文档 | `/api/filetree/createDocWithMd` |
| 追加块 | `/api/block/appendBlock` |
| 更新块 | `/api/block/updateBlock` |
| 重命名文档 | `/api/filetree/renameDocByID` |
| 设置属性 | `/api/attr/setBlockAttrs` |
| 删除块 | `/api/block/deleteBlock` |
| 删除文档 | `/api/filetree/removeDocByID` |
| 导出为 Markdown | `/api/export/exportMdContent` |

## 常用操作[​](#常用操作 "常用操作的直接链接")

### 搜索（全文）[​](#搜索全文 "搜索（全文）的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/search/fullTextSearchBlock" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"query": "meeting notes", "page": 0}' | jq '.data.blocks[:5]'
```

### 搜索（SQL）[​](#搜索sql "搜索（SQL）的直接链接")

直接查询块数据库。仅 SELECT 语句是安全的。

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/query/sql" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"stmt": "SELECT id, content, type, box FROM blocks WHERE content LIKE '\''%keyword%'\'' AND type='\''p'\'' LIMIT 20"}' | jq '.data'
```

常用列：`id`、`parent_id`、`root_id`、`box`（笔记本 ID）、`path`、`content`、`type`、`subtype`、`created`、`updated`。

### 读取块内容[​](#读取块内容 "读取块内容的直接链接")

以 Kramdown（类 Markdown）格式返回块内容。

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getBlockKramdown" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data.kramdown'
```

### 读取子块[​](#读取子块 "读取子块的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getChildBlocks" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 获取人类可读路径[​](#获取人类可读路径 "获取人类可读路径的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/getHPathByID" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 获取块属性[​](#获取块属性 "获取块属性的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/getBlockAttrs" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 列出笔记本[​](#列出笔记本 "列出笔记本的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/lsNotebooks" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{}' | jq '.data.notebooks[] | {id, name, closed}'
```

### 列出笔记本中的文档[​](#列出笔记本中的文档 "列出笔记本中的文档的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/listDocsByPath" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"notebook": "NOTEBOOK_ID", "path": "/"}' | jq '.data.files[] | {id, name}'
```

### 创建文档[​](#创建文档 "创建文档的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/createDocWithMd" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "notebook": "NOTEBOOK_ID",  
    "path": "/Meeting Notes/2026-03-22",  
    "markdown": "# Meeting Notes\n\n- Discussed project timeline\n- Assigned tasks"  
  }' | jq '.data'
```

### 创建笔记本[​](#创建笔记本 "创建笔记本的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/createNotebook" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"name": "My New Notebook"}' | jq '.data.notebook.id'
```

### 向文档追加块[​](#向文档追加块 "向文档追加块的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/appendBlock" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "parentID": "DOCUMENT_OR_BLOCK_ID",  
    "data": "New paragraph added at the end.",  
    "dataType": "markdown"  
  }' | jq '.data'
```

另有：`/api/block/prependBlock`（参数相同，在开头插入）和 `/api/block/insertBlock`（使用 `previousID` 代替 `parentID`，在指定块之后插入）。

### 更新块内容[​](#更新块内容 "更新块内容的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/updateBlock" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "id": "BLOCK_ID",  
    "data": "Updated content here.",  
    "dataType": "markdown"  
  }' | jq '.data'
```

### 重命名文档[​](#重命名文档 "重命名文档的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/renameDocByID" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "DOCUMENT_ID", "title": "New Title"}'
```

### 设置块属性[​](#设置块属性 "设置块属性的直接链接")

自定义属性必须以 `custom-` 为前缀：

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/setBlockAttrs" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "id": "BLOCK_ID",  
    "attrs": {  
      "custom-status": "reviewed",  
      "custom-priority": "high"  
    }  
  }'
```

### 删除块[​](#删除块 "删除块的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/deleteBlock" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "BLOCK_ID"}'
```

删除整个文档：使用 `/api/filetree/removeDocByID`，参数为 `{"id": "DOC_ID"}`。
删除笔记本：使用 `/api/notebook/removeNotebook`，参数为 `{"notebook": "NOTEBOOK_ID"}`。

### 将文档导出为 Markdown[​](#将文档导出为-markdown "将文档导出为 Markdown的直接链接")

```
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/export/exportMdContent" \  
  -H "Authorization: Token $SIYUAN_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"id": "DOCUMENT_ID"}' | jq -r '.data.content'
```

## 块类型[​](#块类型 "块类型的直接链接")

SQL 查询中常见的 `type` 值：

| 类型 | 描述 |
| --- | --- |
| `d` | 文档（根块） |
| `p` | 段落 |
| `h` | 标题 |
| `l` | 列表 |
| `i` | 列表项 |
| `c` | 代码块 |
| `m` | 数学块 |
| `t` | 表格 |
| `b` | 引用块 |
| `s` | 超级块 |
| `html` | HTML 块 |

## 注意事项[​](#注意事项 "注意事项的直接链接")

* **所有端点均为 POST** — 即使是只读操作也不例外。不要使用 GET。
* **SQL 安全性**：仅使用 SELECT 查询。INSERT/UPDATE/DELETE/DROP 有危险，绝不应发送。
* **ID 校验**：ID 匹配模式 `YYYYMMDDHHmmss-xxxxxxx`。不符合此模式的应予以拒绝。
* **错误响应**：处理 `data` 之前，始终检查响应中的 `code != 0`。
* **大型文档**：块内容和导出结果可能非常大。SQL 中使用 `LIMIT`，并通过 `jq` 管道仅提取所需内容。
* **笔记本 ID**：操作特定笔记本时，先通过 `lsNotebooks` 获取其 ID。

## 替代方案：MCP Server[​](#替代方案mcp-server "替代方案：MCP Server的直接链接")

如果您更倾向于使用原生集成而非 curl，可安装 SiYuan MCP server：

```
# In ~/.hermes/config.yaml under mcp_servers:  
mcp_servers:  
  siyuan:  
    command: npx  
    args: ["-y", "@porkll/siyuan-mcp"]  
    env:  
      SIYUAN_TOKEN: "your_token"  
      SIYUAN_URL: "http://127.0.0.1:6806"
```

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [前提条件](#前提条件)
* [API 基础](#api-基础)
* [快速参考](#快速参考)
* [常用操作](#常用操作)
  + [搜索（全文）](#搜索全文)
  + [搜索（SQL）](#搜索sql)
  + [读取块内容](#读取块内容)
  + [读取子块](#读取子块)
  + [获取人类可读路径](#获取人类可读路径)
  + [获取块属性](#获取块属性)
  + [列出笔记本](#列出笔记本)
  + [列出笔记本中的文档](#列出笔记本中的文档)
  + [创建文档](#创建文档)
  + [创建笔记本](#创建笔记本)
  + [向文档追加块](#向文档追加块)
  + [更新块内容](#更新块内容)
  + [重命名文档](#重命名文档)
  + [设置块属性](#设置块属性)
  + [删除块](#删除块)
  + [将文档导出为 Markdown](#将文档导出为-markdown)
* [块类型](#块类型)
* [注意事项](#注意事项)
* [替代方案：MCP Server](#替代方案mcp-server)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/note-taking/note-taking-obsidian](./docs-zh-Hans-user-guide-skills-bundled-note-taking-note-taking-obsidian.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-notion](./docs-zh-Hans-user-guide-skills-bundled-productivity-productivity-notion.md)
