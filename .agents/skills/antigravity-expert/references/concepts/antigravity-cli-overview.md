---
type: Reference
title: "Antigravity CLI Overview"
description: "> Nguồn: Google Antigravity Master Corpus"
timestamp: 2026-07-06T03:34:16Z
---
# Antigravity CLI Overview

> Nguồn: Google Antigravity Master Corpus
> Phân loại: concept
> Trạng thái: active
> Ngày tạo: 2026-06-21


*Source URL*: https://antigravity.google/docs/cli-overview

The Antigravity CLI is the lightweight Terminal User Interface (TUI) surface of Antigravity. It brings the same core agentic capabilities as Antigravity 2.0—including multi-step reasoning, multi-file editing, tool calling, and conversation history—directly to your terminal.

The CLI is the ideal tool for keyboard-centric developers and remote SSH workflows, optimized for speed and low resource overhead.

### Philosophical Split: CLI vs. Antigravity 2.0

Antigravity CLI complements Antigravity 2.0 as a terminal-first alternative.

* **CLI**: Optimized for speed, keyboard efficiency, and low overhead.
* **Antigravity 2.0**: Optimized for comprehensiveness, visual orchestration, and project management.

**Integration Features**

* **Shared Agent Harness**: Both products run on the same core agent engine. Any improvements to reasoning or tool use automatically apply to both.
* **Shared Settings**: Core preferences and permissions are shared. Changing a setting in the CLI updates it in the Antigravity, and vice versa.
* **Conversation Export**: While conversations are separate by default, you can easily export a CLI conversation to Antigravity 2.0 to continue with the agent-first interface.

### Getting Started & Migration

To install the CLI, follow the [Installation Guide](/docs/cli-getting-started).

### Migrating from Gemini CLI

If you are transitioning from Gemini CLI, the onboarding process supports a one-time import to automatically migrate your existing Gemini CLI extensions, skills, and settings. To learn more, read [Migrating from Gemini CLI](/docs/gcli-migration).

### Deep Dives & References

For detailed instructions on specific features, refer to the following guides:

* **[Getting Started](/docs/cli-getting-started)**: Details on silent keyring sign-in and remote SSH session auth.
* **[Using AGY CLI](/docs/cli-using)**: Learn about slash commands, configuration settings, and default keybindings.
* **[Features](/docs/cli-features)**: Learn how the agent delegates parallel background tasks, how to use fast-path approvals, and other advanced capabilities.
* **[Tools & Extensions](/docs/plugins)**: Reference for installing, enabling, and managing third-party skills and MCP servers.



---