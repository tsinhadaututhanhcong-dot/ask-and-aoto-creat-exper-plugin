# Polymarket — 查询 Polymarket：市场、价格、订单簿、历史记录 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/research/research-polymarket](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/research/research-polymarket)

本页总览

查询 Polymarket：市场、价格、订单簿、历史记录。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/research/polymarket` |
| 版本 | `1.0.0` |
| 作者 | Hermes Agent + Teknium |
| 平台 | linux, macos, windows |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# Polymarket — 预测市场数据

使用 Polymarket 的公开 REST API 查询预测市场数据。
所有端点均为只读，无需任何身份验证。

完整端点参考及 curl 示例请见 `references/api-endpoints.md`。

## 使用场景[​](#使用场景 "使用场景的直接链接")

* 用户询问预测市场、博彩赔率或事件概率
* 用户想了解"X 发生的概率是多少？"
* 用户专门询问 Polymarket
* 用户需要市场价格、订单簿数据或价格历史
* 用户希望监控或追踪预测市场动态

## 核心概念[​](#核心概念 "核心概念的直接链接")

* **Events（事件）** 包含一个或多个 **Markets（市场）**（1:many 关系）
* **Markets** 是二元结果，Yes/No 价格区间为 0.00 到 1.00
* 价格即概率：价格 0.65 表示市场认为该事件有 65% 的可能性发生
* `outcomePrices` 字段：JSON 编码的数组，格式如 `["0.80", "0.20"]`
* `clobTokenIds` 字段：包含两个 token ID 的 JSON 编码数组 [Yes, No]，用于价格/订单簿查询
* `conditionId` 字段：十六进制字符串，用于价格历史查询
* 成交量单位为 USDC（美元）

## 三个公开 API[​](#三个公开-api "三个公开 API的直接链接")

1. **Gamma API**，地址 `gamma-api.polymarket.com` — 发现、搜索、浏览
2. **CLOB API**，地址 `clob.polymarket.com` — 实时价格、订单簿、历史记录
3. **Data API**，地址 `data-api.polymarket.com` — 交易记录、未平仓合约

## 典型工作流程[​](#典型工作流程 "典型工作流程的直接链接")

当用户询问预测市场赔率时：

1. **搜索** — 使用 Gamma API 的 public-search 端点，传入用户的查询词
2. **解析** — 处理响应，提取 events 及其嵌套的 markets
3. **展示** — 市场问题、当前价格（以百分比表示）及成交量
4. **深入分析** — 如有需要，使用 `clobTokenIds` 查询订单簿，使用 `conditionId` 查询历史记录

## 结果展示[​](#结果展示 "结果展示的直接链接")

将价格格式化为百分比以提高可读性：

* `outcomePrices` 为 `["0.652", "0.348"]` 时，展示为"Yes: 65.2%，No: 34.8%"
* 始终显示市场问题和概率
* 有成交量时一并展示

示例：`"Will X happen?" — 65.2% Yes（成交量 $1.2M）`

## 解析双重编码字段[​](#解析双重编码字段 "解析双重编码字段的直接链接")

Gamma API 返回的 `outcomePrices`、`outcomes` 和 `clobTokenIds` 是 JSON 响应中的 JSON 字符串（双重编码）。在 Python 中处理时，需使用 `json.loads(market['outcomePrices'])` 解析以获取实际数组。

## 速率限制[​](#速率限制 "速率限制的直接链接")

限制宽松，正常使用基本不会触发：

* Gamma：每 10 秒 4,000 次请求（通用）
* CLOB：每 10 秒 9,000 次请求（通用）
* Data：每 10 秒 1,000 次请求（通用）

## 限制说明[​](#限制说明 "限制说明的直接链接")

* 此 skill 为只读模式，不支持下单交易
* 交易需要基于钱包的加密身份验证（EIP-712 签名）
* 部分新市场的价格历史可能为空
* 交易受地理限制，但只读数据在全球范围内均可访问

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [使用场景](#使用场景)
* [核心概念](#核心概念)
* [三个公开 API](#三个公开-api)
* [典型工作流程](#典型工作流程)
* [结果展示](#结果展示)
* [解析双重编码字段](#解析双重编码字段)
* [速率限制](#速率限制)
* [限制说明](#限制说明)