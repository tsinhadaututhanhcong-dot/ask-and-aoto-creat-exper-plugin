# Nano Pdf — 通过 nano-pdf CLI 编辑 PDF 文本/错别字/标题（自然语言 prompt） | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-nano-pdf](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-nano-pdf)

本页总览

通过 nano-pdf CLI 编辑 PDF 文本/错别字/标题（自然语言 prompt（提示词））。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/productivity/nano-pdf` |
| 版本 | `1.0.0` |
| 作者 | community |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `PDF`, `Documents`, `Editing`, `NLP`, `Productivity` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发该 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# nano-pdf

使用自然语言指令编辑 PDF。指定页面并描述需要修改的内容。

## 前置条件[​](#前置条件 "前置条件的直接链接")

```
# Install with uv (recommended — already available in Hermes)  
uv pip install nano-pdf  
  
# Or with pip  
pip install nano-pdf
```

## 用法[​](#用法 "用法的直接链接")

```
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## 示例[​](#示例 "示例的直接链接")

```
# Change a title on page 1  
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"  
  
# Update a date on a specific page  
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"  
  
# Fix content  
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

## 注意事项[​](#注意事项 "注意事项的直接链接")

* 页码可能从 0 或 1 开始，具体取决于版本——如果编辑命中了错误的页面，请用 ±1 重试
* 编辑后务必验证输出的 PDF（使用 `read_file` 检查文件大小，或直接打开查看）
* 该工具底层使用 LLM——需要 API 密钥（运行 `nano-pdf --help` 查看配置说明）
* 适合文本内容修改；复杂的版式调整可能需要其他方案

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [前置条件](#前置条件)
* [用法](#用法)
* [示例](#示例)
* [注意事项](#注意事项)