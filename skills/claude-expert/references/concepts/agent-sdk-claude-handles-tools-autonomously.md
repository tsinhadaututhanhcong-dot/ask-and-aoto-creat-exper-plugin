---
title: Agent SDK: Claude handles tools autonomously
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

Same capabilities, different interface:

| Use case | Best choice |
| --- | --- |
| Interactive development | CLI |
| CI/CD pipelines | SDK |
| Custom applications | SDK |
| One-off tasks | CLI |
| Production automation | SDK |

Many teams use both: CLI for daily development, SDK for production. Workflows translate directly between them.

[Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) is a hosted REST API: Anthropic runs the agent and the sandbox, and your application sends events and streams back results. The **Agent SDK** is a library that runs the agent loop inside your own process.

|  | Agent SDK | Managed Agents |
| --- | --- | --- |
| **Runs in** | Your process, your infrastructure | Anthropic-managed infrastructure |
| **Interface** | Python or TypeScript library | REST API |
| **Agent works on** | Files on your infrastructure | A managed sandbox per session |
| **Session state** | JSONL on your filesystem | Anthropic-hosted event log |
| **Custom tools** | In-process Python or TypeScript functions | Claude triggers the tool; you execute and return results |
| **Best for** | Local prototyping, agents that work directly on your filesystem and services | Production agents without operating sandbox or session infrastructure, long-running and asynchronous sessions |

A common path is to prototype with the Agent SDK locally, then move to Managed Agents for production.

## [​](#changelog) Changelog

View the full changelog for SDK updates, bug fixes, and new features:

* **TypeScript SDK**: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
* **Python SDK**: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

## [​](#reporting-bugs) Reporting bugs

If you encounter bugs or issues with the Agent SDK:

* **TypeScript SDK**: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
* **Python SDK**: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

## [​](#branding-guidelines) Branding guidelines

For partners integrating the Claude Agent SDK, use of Claude branding is optional. When referencing Claude in your product:
**Allowed:**

* “Claude Agent” (preferred for dropdown menus)
* “Claude” (when within a menu already labeled “Agents”)
* ” Powered by Claude” (if you have an existing agent name)

**Not permitted:**

* “Claude Code” or “Claude Code Agent”
* Claude Code-branded ASCII art or visual elements that mimic Claude Code

Your product should maintain its own branding and not appear to be Claude Code or any Anthropic product. For questions about branding compliance, contact the Anthropic [sales team](https://www.anthropic.com/contact-sales).

## [​](#license-and-terms) License and terms

Use of the Claude Agent SDK is governed by [Anthropic’s Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms), including when you use it to power products and services that you make available to your own customers and end users, except to the extent a specific component or dependency is covered by a different license as indicated in that component’s LICENSE file.

## [​](#next-steps) Next steps

## Quickstart

Build an agent that finds and fixes bugs in minutes

## Example agents

Email assistant, research agent, and more

## TypeScript SDK

Full TypeScript API reference and examples

## Python SDK

Full Python API reference and examples

Was this page helpful?

YesNo

[Quickstart](/docs/en/agent-sdk/quickstart)

⌘I

---