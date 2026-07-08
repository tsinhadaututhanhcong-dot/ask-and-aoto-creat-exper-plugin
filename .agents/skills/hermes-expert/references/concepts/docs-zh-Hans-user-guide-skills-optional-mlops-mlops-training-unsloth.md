# Unsloth — Unsloth：2-5倍更快的 LoRA/QLoRA 微调，更少显存 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-training-unsloth](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-training-unsloth)

本页总览

Unsloth：2-5倍更快的 LoRA/QLoRA 微调，更少显存。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/mlops/unsloth` 安装 |
| 路径 | `optional-skills/mlops/training/unsloth` |
| 版本 | `1.0.0` |
| 作者 | Orchestra Research |
| 许可证 | MIT |
| 依赖项 | `unsloth`, `torch`, `transformers`, `trl`, `datasets`, `peft` |
| 平台 | linux, macos |
| 标签 | `Fine-Tuning`, `Unsloth`, `Fast Training`, `LoRA`, `QLoRA`, `Memory-Efficient`, `Optimization`, `Llama`, `Mistral`, `Gemma`, `Qwen` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# Unsloth Skill

基于官方文档生成的 unsloth 开发综合辅助。

## 何时使用此 Skill[​](#何时使用此-skill "何时使用此 Skill的直接链接")

以下情况应触发此 skill：

* 使用 unsloth 进行开发
* 询问 unsloth 功能或 API
* 实现 unsloth 解决方案
* 调试 unsloth 代码
* 学习 unsloth 最佳实践

## 快速参考[​](#快速参考 "快速参考的直接链接")

### 常用模式[​](#常用模式 "常用模式的直接链接")

*随着你使用此 skill，快速参考模式将逐步添加。*

## 参考文件[​](#参考文件 "参考文件的直接链接")

此 skill 在 `references/` 中包含完整文档：

* **llms-txt.md** - Llms-Txt 文档

需要详细信息时，使用 `view` 读取特定参考文件。

## 使用此 Skill[​](#使用此-skill "使用此 Skill的直接链接")

### 面向初学者[​](#面向初学者 "面向初学者的直接链接")

从 getting\_started 或 tutorials 参考文件入手，了解基础概念。

### 针对特定功能[​](#针对特定功能 "针对特定功能的直接链接")

使用相应分类的参考文件（api、guides 等）获取详细信息。

### 获取代码示例[​](#获取代码示例 "获取代码示例的直接链接")

上方快速参考部分包含从官方文档中提取的常用模式。

## 资源[​](#资源 "资源的直接链接")

### references/[​](#references "references/的直接链接")

从官方来源提取的有组织文档，包含：

* 详细说明
* 带语言标注的代码示例
* 原始文档链接
* 便于快速导航的目录

### scripts/[​](#scripts "scripts/的直接链接")

在此添加用于常见自动化任务的辅助脚本。

### assets/[​](#assets "assets/的直接链接")

在此添加模板、样板代码或示例项目。

## 说明[​](#说明 "说明的直接链接")

* 此 skill 由官方文档自动生成
* 参考文件保留了源文档的结构和示例
* 代码示例包含语言检测以提供更好的语法高亮
* 快速参考模式从文档中的常见用法示例中提取

## 更新[​](#更新 "更新的直接链接")

如需使用最新文档刷新此 skill：

1. 使用相同配置重新运行爬取程序
2. Skill 将以最新信息重新构建

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [何时使用此 Skill](#何时使用此-skill)
* [快速参考](#快速参考)
  + [常用模式](#常用模式)
* [参考文件](#参考文件)
* [使用此 Skill](#使用此-skill)
  + [面向初学者](#面向初学者)
  + [针对特定功能](#针对特定功能)
  + [获取代码示例](#获取代码示例)
* [资源](#资源)
  + [references/](#references)
  + [scripts/](#scripts)
  + [assets/](#assets)
* [说明](#说明)
* [更新](#更新)