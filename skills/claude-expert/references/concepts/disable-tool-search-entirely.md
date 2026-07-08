---
type: Reference
title: Disable tool search entirely
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Disable tool search entirely
ENABLE_TOOL_SEARCH=false claude
```

Or set the value in your [settings.json `env` field](/docs/en/settings#available-settings).
You can also disable the `ToolSearch` tool specifically:

```
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

### [​](#exempt-a-server-from-deferral) Exempt a server from deferral

If a server’s tools should always be visible to Claude without a search step, set `alwaysLoad` to `true` in that server’s configuration. Every tool from that server then loads into context at session start regardless of the `ENABLE_TOOL_SEARCH` setting. Use this for a small number of tools that Claude needs on every turn, since each upfront tool consumes context that would otherwise be available for your conversation.
The following `.mcp.json` entry exempts one HTTP server while leaving other servers deferred:

```
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

The `alwaysLoad` field is available on all server types and requires Claude Code v2.1.121 or later. An MCP server can also mark individual tools as always-loaded by including `"anthropic/alwaysLoad": true` in the tool’s `_meta` object, which has the same effect for that tool only.
Setting `alwaysLoad: true` also blocks startup until the server connects, capped at the standard 5-second connect timeout. This applies even though MCP startup is otherwise [non-blocking by default](/docs/en/env-vars), since the tools must be present when the first prompt is built. Other servers continue to connect in the background.

## [​](#use-mcp-prompts-as-commands) Use MCP prompts as commands

MCP servers can expose prompts that become available as commands in Claude Code.

### [​](#execute-mcp-prompts) Execute MCP prompts

1

Discover available prompts

Type `/` to see all available commands, including those from MCP servers. MCP prompts appear with the format `/mcp__servername__promptname`.

2

Execute a prompt without arguments

```
/mcp__github__list_prs
```

3

Execute a prompt with arguments

Many prompts accept arguments. Pass them space-separated after the command:

```
/mcp__github__pr_review 456
```

```
/mcp__jira__create_issue "Bug in login flow" high
```

Tips:

* MCP prompts are dynamically discovered from connected servers
* Arguments are parsed based on the prompt’s defined parameters
* Prompt results are injected directly into the conversation
* Server and prompt names are normalized, with spaces converted to underscores

## [​](#managed-mcp-configuration) Managed MCP configuration

For organizations that need centralized control over which MCP servers users can connect to, see [Managed MCP configuration](/docs/en/managed-mcp). It covers deploying a fixed server set with `managed-mcp.json`, restricting servers with `allowedMcpServers` and `deniedMcpServers`, and what users see when a server is blocked.

Was this page helpful?

YesNo

[Quickstart](/docs/en/mcp-quickstart)[Extend Claude with skills](/docs/en/skills)

⌘I

---