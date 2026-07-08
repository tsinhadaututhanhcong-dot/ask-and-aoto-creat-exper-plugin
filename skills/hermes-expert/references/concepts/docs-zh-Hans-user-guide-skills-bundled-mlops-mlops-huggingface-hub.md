# Huggingface Hub — HuggingFace hf CLI：搜索/下载/上传模型、数据集 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/mlops/mlops-huggingface-hub](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/mlops/mlops-huggingface-hub)

本页总览

HuggingFace hf CLI：搜索/下载/上传模型、数据集。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/mlops/huggingface-hub` |
| 版本 | `1.0.0` |
| 作者 | Hugging Face |
| 许可证 | MIT |
| 平台 | linux, macos, windows |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# Hugging Face CLI（`hf`）参考指南

`hf` 命令是与 Hugging Face Hub 交互的现代命令行界面，提供管理仓库、模型、数据集和 Spaces 的工具。

> **重要：** `hf` 命令取代了现已弃用的 `huggingface-cli` 命令。

## 快速开始[​](#快速开始 "快速开始的直接链接")

* **安装：** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
* **帮助：** 使用 `hf --help` 查看所有可用功能及实际示例。
* **认证：** 推荐通过 `HF_TOKEN` 环境变量或 `--token` 标志进行认证。

---

## 核心命令[​](#核心命令 "核心命令的直接链接")

### 通用操作[​](#通用操作 "通用操作的直接链接")

* `hf download REPO_ID`：从 Hub 下载文件。
* `hf upload REPO_ID`：上传文件/文件夹（推荐用于单次提交）。
* `hf upload-large-folder REPO_ID LOCAL_PATH`：推荐用于大型目录的可恢复上传。
* `hf sync`：在本地目录与存储桶之间同步文件。
* `hf env` / `hf version`：查看环境和版本详情。

### 认证（`hf auth`）[​](#认证hf-auth "认证hf-auth的直接链接")

* `login` / `logout`：使用来自 [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) 的 token 管理会话。
* `list` / `switch`：管理并切换多个已存储的访问 token。
* `whoami`：查看当前登录账户。

### 仓库管理（`hf repos`）[​](#仓库管理hf-repos "仓库管理hf-repos的直接链接")

* `create` / `delete`：创建或永久删除仓库。
* `duplicate`：将模型、数据集或 Space 克隆到新 ID。
* `move`：在命名空间之间迁移仓库。
* `branch` / `tag`：管理类 Git 引用。
* `delete-files`：使用模式匹配删除特定文件。

---

## 专项 Hub 交互[​](#专项-hub-交互 "专项 Hub 交互的直接链接")

### 数据集与模型[​](#数据集与模型 "数据集与模型的直接链接")

* **数据集：** `hf datasets list`、`info` 以及 `parquet`（列出 parquet URL）。
* **SQL 查询：** `hf datasets sql SQL` — 通过 DuckDB 对数据集 parquet URL 执行原始 SQL。
* **模型：** `hf models list` 和 `info`。
* **论文：** `hf papers list` — 查看每日论文。

### 讨论与 Pull Request（`hf discussions`）[​](#讨论与-pull-requesthf-discussions "讨论与-pull-requesthf-discussions的直接链接")

* 管理 Hub 贡献的完整生命周期：`list`、`create`、`info`、`comment`、`close`、`reopen` 和 `rename`。
* `diff`：查看 PR 中的变更。
* `merge`：完成 pull request 合并。

### 基础设施与计算[​](#基础设施与计算 "基础设施与计算的直接链接")

* **Endpoints：** 部署和管理推理端点（`deploy`、`pause`、`resume`、`scale-to-zero`、`catalog`）。
* **Jobs：** 在 HF 基础设施上运行计算任务。包括 `hf jobs uv`（用于运行带内联依赖的 Python 脚本）和 `stats`（用于资源监控）。
* **Spaces：** 管理交互式应用。包括 `dev-mode` 和 `hot-reload`，可在不完全重启的情况下热更新 Python 文件。

### 存储与自动化[​](#存储与自动化 "存储与自动化的直接链接")

* **Buckets：** 完整的类 S3 存储桶管理（`create`、`cp`、`mv`、`rm`、`sync`）。
* **Cache（缓存）：** 使用 `list`、`prune`（删除已分离的修订版本）和 `verify`（校验和检查）管理本地存储。
* **Webhooks：** 通过管理 Hub webhook（`create`、`watch`、`enable`/`disable`）自动化工作流。
* **Collections：** 将 Hub 条目整理到集合中（`add-item`、`update`、`list`）。

---

## 高级用法与技巧[​](#高级用法与技巧 "高级用法与技巧的直接链接")

### 全局标志[​](#全局标志 "全局标志的直接链接")

* `--format json`：生成适合自动化的机器可读输出。
* `-q` / `--quiet`：将输出限制为仅显示 ID。

### 扩展与 Skills[​](#扩展与-skills "扩展与 Skills的直接链接")

* **扩展：** 通过 GitHub 仓库使用 `hf extensions install REPO_ID` 扩展 CLI 功能。
* **Skills：** 使用 `hf skills add` 管理 AI 助手 skill。

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [快速开始](#快速开始)
* [核心命令](#核心命令)
  + [通用操作](#通用操作)
  + [认证（`hf auth`）](#认证hf-auth)
  + [仓库管理（`hf repos`）](#仓库管理hf-repos)
* [专项 Hub 交互](#专项-hub-交互)
  + [数据集与模型](#数据集与模型)
  + [讨论与 Pull Request（`hf discussions`）](#讨论与-pull-requesthf-discussions)
  + [基础设施与计算](#基础设施与计算)
  + [存储与自动化](#存储与自动化)
* [高级用法与技巧](#高级用法与技巧)
  + [全局标志](#全局标志)
  + [扩展与 Skills](#扩展与-skills)