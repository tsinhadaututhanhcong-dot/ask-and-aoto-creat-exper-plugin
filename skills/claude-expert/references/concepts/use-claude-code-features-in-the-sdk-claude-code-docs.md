---
type: Reference
title: Use Claude Code features in the SDK - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Use Claude Code features in the SDK - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/claude-code-features](https://code.claude.com/docs/en/agent-sdk/claude-code-features)

The Agent SDK is built on the same foundation as Claude Code, which means your SDK agents have access to the same filesystem-based features: project instructions (`CLAUDE.md` and rules), skills, hooks, and more.
When you omit `settingSources`, `query()` reads the same filesystem settings as the Claude Code CLI: user, project, and local settings, CLAUDE.md files, and `.claude/` skills, agents, and commands. To run without these, pass `settingSources: []`, which limits the agent to what you configure programmatically. Managed policy settings and the global `~/.claude.json` config are read regardless of this option. See [What settingSources does not control](#what-settingsources-does-not-control).
For a conceptual overview of what each feature does and when to use it, see [Extend Claude Code](/docs/en/features-overview).

## [​](#control-filesystem-settings-with-settingsources) Control filesystem settings with settingSources

The setting sources option ([`setting_sources`](/docs/en/agent-sdk/python#claudeagentoptions) in Python, [`settingSources`](/docs/en/agent-sdk/typescript#settingsource) in TypeScript) controls which filesystem-based settings the SDK loads. Pass an explicit list to opt in to specific sources, or pass an empty array to disable user, project, and local settings.
This example loads both user-level and project-level settings by setting `settingSources` to `["user", "project"]`:

Python

TypeScript

```
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async for message in query(
    prompt="Help me refactor the auth module",
    options=ClaudeAgentOptions(
        # "user" loads from ~/.claude/, "project" loads from ./.claude/ in cwd.
        # Together they give the agent access to CLAUDE.md, skills, hooks, and
        # permissions from both locations.
        setting_sources=["user", "project"],
        allowed_tools=["Read", "Edit", "Bash"],
    ),
):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if hasattr(block, "text"):
                print(block.text)
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(f"\nResult: {message.result}")
```

Each source loads settings from a specific location, where `<cwd>` is the working directory you pass via the `cwd` option, or the process’s current directory if unset. For the full type definition, see [`SettingSource`](/docs/en/agent-sdk/typescript#settingsource) (TypeScript) or [`SettingSource`](/docs/en/agent-sdk/python#settingsource) (Python).

| Source | What it loads | Location |
| --- | --- | --- |
| `"project"` | Project CLAUDE.md, `.claude/rules/*.md`, project skills, project hooks, project `settings.json` | `<cwd>/.claude/` for `settings.json` and hooks; `<cwd>` and every parent directory for CLAUDE.md and rules; `<cwd>` and every parent directory up to the repository root for skills |
| `"user"` | User CLAUDE.md, `~/.claude/rules/*.md`, user skills, user settings | `~/.claude/` |
| `"local"` | CLAUDE.local.md, `.claude/settings.local.json` | `<cwd>/.claude/` for `settings.local.json`; `<cwd>` and every parent directory for CLAUDE.local.md |

Omitting `settingSources` is equivalent to `["user", "project", "local"]`.
The `cwd` option determines where the SDK looks for project-level inputs. CLAUDE.md and rules load from `<cwd>` and from every parent directory. Skills load from `<cwd>` and from every parent directory up to the repository root. Project `settings.json` and hooks load only from `<cwd>/.claude/` with no parent-directory fallback.

### [​](#what-settingsources-does-not-control) What settingSources does not control

`settingSources` covers user, project, and local settings. A few inputs are read regardless of its value:

| Input | Behavior | To disable |
| --- | --- | --- |
| Managed policy settings | Endpoint-managed policy, such as an MDM plist, registry policy, or managed settings file, loads from the host. [Server-managed settings](/docs/en/server-managed-settings) are fetched on an [eligible configuration](/docs/en/server-managed-settings#platform-availability) when the session authenticates with an organization OAuth login or a directly configured API key | Endpoint policy: remove the managed settings file, plist, or registry policy from the host. Server-managed settings: controlled by your org admin; cannot be disabled from the SDK |
| `~/.claude.json` global config | Always read | Relocate with `CLAUDE_CONFIG_DIR` in `env` |
| Auto memory at `~/.claude/projects/<project>/memory/` | Loaded by default into the system prompt | Set `autoMemoryEnabled: false` in settings, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env` |
| [claude.ai MCP connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) | Loaded when the active authentication method is a claude.ai subscription. Passing `mcpServers: {}` does not suppress them | Set `strictMcpConfig: true`, [`disableClaudeAiConnectors: true`](/docs/en/mcp#disable-claude-ai-connectors) in settings, or `ENABLE_CLAUDEAI_MCP_SERVERS=false` in `env` |

Do not rely on default `query()` options for multi-tenant isolation. Because the inputs above are read regardless of `settingSources`, an SDK process can pick up host-level configuration and per-directory memory. For multi-tenant deployments, run each tenant in its own filesystem and set `settingSources: []` plus `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`. [Server-managed settings](/docs/en/server-managed-settings) are fetched when the process authenticates with an organization credential; filesystem isolation does not remove them. See [Secure deployment](/docs/en/agent-sdk/secure-deployment).

## [​](#project-instructions-claude-md-and-rules) Project instructions (CLAUDE.md and rules)

`CLAUDE.md` files and `.claude/rules/*.md` files give your agent persistent context about your project: coding conventions, build commands, architecture decisions, and instructions. When `settingSources` includes `"project"` (as in the example above), the SDK loads these files into context at session start. The agent then follows your project conventions without you repeating them in every prompt.

### [​](#claude-md-load-locations) CLAUDE.md load locations

| Level | Location | When loaded |
| --- | --- | --- |
| Project (root) | `<cwd>/CLAUDE.md` or `<cwd>/.claude/CLAUDE.md` | `settingSources` includes `"project"` |
| Project rules | `<cwd>/.claude/rules/*.md` and `.claude/rules/*.md` in every parent directory | `settingSources` includes `"project"` |
| Project (parent dirs) | `CLAUDE.md` files in directories above `cwd` | `settingSources` includes `"project"`, loaded at session start |
| Project (child dirs) | `CLAUDE.md` files in subdirectories of `cwd` | `settingSources` includes `"project"`, loaded on demand when the agent reads a file in that subtree |
| Local | `<cwd>/CLAUDE.local.md` and `CLAUDE.local.md` in every parent directory | `settingSources` includes `"local"` |
| User | `~/.claude/CLAUDE.md` | `settingSources` includes `"user"` |
| User rules | `~/.claude/rules/*.md` | `settingSources` includes `"user"` |

All levels are additive: if both project and user CLAUDE.md files exist, the agent sees both. There is no hard precedence rule between levels; if instructions conflict, the outcome depends on how Claude interprets them. Write non-conflicting rules, or state precedence explicitly in the more specific file (“These project instructions override any conflicting user-level defaults”).

You can also inject context directly via `systemPrompt` without using CLAUDE.md files. See [Modify system prompts](/docs/en/agent-sdk/modifying-system-prompts). Use CLAUDE.md when you want the same context shared between interactive Claude Code sessions and your SDK agents.

For how to structure and organize CLAUDE.md content, see [Manage Claude’s memory](/docs/en/memory).

## [​](#skills) Skills

Skills are markdown files that give your agent specialized knowledge and invocable workflows. Unlike `CLAUDE.md` (which loads every session), skills load on demand. The agent receives skill descriptions at startup and loads the full content when relevant.
Skills are discovered from the filesystem through `settingSources`. When the `skills` option on `query()` is omitted, discovered user and project skills are enabled and the Skill tool is available, matching CLI behavior. To control which skills are enabled, pass `skills` as `"all"`, a list of skill names, or `[]` to disable all. When `skills` is set, the SDK adds the Skill tool to `allowedTools` automatically. If you also pass an explicit `tools` list, include `"Skill"` in that list so Claude can invoke skills.

Python

TypeScript

```
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage