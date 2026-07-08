# Gif Search — 通过 curl + jq 搜索/下载 Tenor GIF | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/media/media-gif-search](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/media/media-gif-search)

本页总览

通过 curl + jq 搜索/下载 Tenor GIF。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/media/gif-search` |
| 版本 | `1.1.0` |
| 作者 | Hermes Agent |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `GIF`, `Media`, `Search`, `Tenor`, `API` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发该 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# GIF Search（Tenor API）

通过 Tenor API 使用 curl 直接搜索和下载 GIF，无需额外工具。

## 使用场景[​](#使用场景 "使用场景的直接链接")

适用于查找反应 GIF、创建视觉内容以及在聊天中发送 GIF。

## 配置[​](#配置 "配置的直接链接")

在环境中设置 Tenor API 密钥（添加到 `~/.hermes/.env`）：

```
TENOR_API_KEY=your_key_here
```

在 <https://developers.google.com/tenor/guides/quickstart> 免费获取 API 密钥 —— Google Cloud Console Tenor API 密钥免费且具有较高的速率限制。

## 前置条件[​](#前置条件 "前置条件的直接链接")

* `curl` 和 `jq`（macOS/Linux 标准工具）
* `TENOR_API_KEY` 环境变量

## 搜索 GIF[​](#搜索-gif "搜索 GIF的直接链接")

```
# 搜索并获取 GIF URL  
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'  
  
# 获取较小的预览版本  
curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'
```

## 下载 GIF[​](#下载-gif "下载 GIF的直接链接")

```
# 搜索并下载排名第一的结果  
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')  
curl -sL "$URL" -o celebration.gif
```

## 获取完整元数据[​](#获取完整元数据 "获取完整元数据的直接链接")

```
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'
```

## API 参数[​](#api-参数 "API 参数的直接链接")

| 参数 | 说明 |
| --- | --- |
| `q` | 搜索查询（空格用 `+` 进行 URL 编码） |
| `limit` | 最大结果数（1-50，默认 20） |
| `key` | API 密钥（来自 `$TENOR_API_KEY` 环境变量） |
| `media_filter` | 过滤格式：`gif`、`tinygif`、`mp4`、`tinymp4`、`webm` |
| `contentfilter` | 安全级别：`off`、`low`、`medium`、`high` |
| `locale` | 语言：`en_US`、`es`、`fr` 等 |

## 可用媒体格式[​](#可用媒体格式 "可用媒体格式的直接链接")

每个结果在 `.media_formats` 下包含多种格式：

| 格式 | 使用场景 |
| --- | --- |
| `gif` | 完整质量 GIF |
| `tinygif` | 小型预览 GIF |
| `mp4` | 视频版本（文件体积更小） |
| `tinymp4` | 小型预览视频 |
| `webm` | WebM 视频 |
| `nanogif` | 微型缩略图 |

## 注意事项[​](#注意事项 "注意事项的直接链接")

* 对查询进行 URL 编码：空格用 `+`，特殊字符用 `%XX`
* 在聊天中发送时，`tinygif` URL 更轻量
* GIF URL 可直接用于 markdown：`![alt](https://github.com/NousResearch/hermes-agent/blob/main/skills/media/gif-search/url)`

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [使用场景](#使用场景)
* [配置](#配置)
* [前置条件](#前置条件)
* [搜索 GIF](#搜索-gif)
* [下载 GIF](#下载-gif)
* [获取完整元数据](#获取完整元数据)
* [API 参数](#api-参数)
* [可用媒体格式](#可用媒体格式)
* [注意事项](#注意事项)