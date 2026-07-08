---
type: Reference
title: when settingSources loads them. You can also add programmatic hooks:
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# when settingSources loads them. You can also add programmatic hooks:
async for message in query(
    prompt="Refactor the auth module",
    options=ClaudeAgentOptions(
        setting_sources=["project"],  # Loads hooks from .claude/settings.json
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[audit_bash]),
            ]
        },
    ),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

### [​](#when-to-use-which-hook-type) When to use which hook type

| Hook type | Best for |
| --- | --- |
| **Filesystem** (`settings.json`) | Sharing hooks between CLI and SDK sessions. Supports `"command"` (shell scripts), `"http"` (POST to an endpoint), `"mcp_tool"` (call a connected MCP server’s tool), `"prompt"` (LLM evaluates a prompt), and `"agent"` (spawns a verifier agent). These fire in the main agent and any subagents it spawns. |
| **Programmatic** (callbacks in `query()`) | Application-specific logic, structured decisions, and in-process integration. These also fire inside subagents. The callback receives `agent_id` and `agent_type` to distinguish. |

The TypeScript SDK supports additional hook events beyond Python, including `SessionStart`, `SessionEnd`, `TeammateIdle`, and `TaskCompleted`. See the [hooks guide](/docs/en/agent-sdk/hooks) for the full event compatibility table.

For full details on programmatic hooks, see [Control execution with hooks](/docs/en/agent-sdk/hooks). For filesystem hook syntax, see [Hooks](/docs/en/hooks).

## [​](#choose-the-right-feature) Choose the right feature

The Agent SDK gives you access to several ways to extend your agent’s behavior. If you’re unsure which to use, this table maps common goals to the right approach.

| You want to… | Use | SDK surface |
| --- | --- | --- |
| Set project conventions your agent always follows | [CLAUDE.md](/docs/en/memory) | `settingSources: ["project"]` loads it automatically |
| Give the agent reference material it loads when relevant | [Skills](/docs/en/agent-sdk/skills) | `settingSources` + `skills` option |
| Run a reusable workflow (deploy, review, release) | [User-invocable skills](/docs/en/agent-sdk/skills) | `settingSources` + `skills` option |
| Delegate an isolated subtask to a fresh context (research, review) | [Subagents](/docs/en/agent-sdk/subagents) | `agents` parameter + `allowedTools: ["Agent"]` |
| Coordinate multiple Claude Code instances with shared task lists and direct inter-agent messaging | [Agent teams](/docs/en/agent-teams) | Not directly configured via SDK options. Agent teams are a CLI feature where one session acts as the team lead, coordinating work across independent teammates |
| Run deterministic logic on tool calls (audit, block, transform) | [Hooks](/docs/en/agent-sdk/hooks) | `hooks` parameter with callbacks, or shell scripts loaded via `settingSources` |
| Give Claude structured tool access to an external service | [MCP](/docs/en/agent-sdk/mcp) | `mcpServers` parameter |

**Subagents versus agent teams:** Subagents are ephemeral and isolated: fresh conversation, one task, summary returned to parent. Agent teams coordinate multiple independent Claude Code instances that share a task list and message each other directly. Agent teams are a CLI feature. See [What subagents inherit](/docs/en/agent-sdk/subagents#what-subagents-inherit) and the [agent teams comparison](/docs/en/agent-teams#compare-with-subagents) for details.

Every feature you enable adds to your agent’s context window. For per-feature costs and how these features layer together, see [Extend Claude Code](/docs/en/features-overview#understand-context-costs).

## [​](#related-resources) Related resources

* [Extend Claude Code](/docs/en/features-overview): Conceptual overview of all extension features, with comparison tables and context cost analysis
* [Skills in the SDK](/docs/en/agent-sdk/skills): Full guide to using skills programmatically
* [Subagents](/docs/en/agent-sdk/subagents): Define and invoke subagents for isolated subtasks
* [Hooks](/docs/en/agent-sdk/hooks): Intercept and control agent behavior at key execution points
* [Permissions](/docs/en/agent-sdk/permissions): Control tool access with modes, rules, and callbacks
* [System prompts](/docs/en/agent-sdk/modifying-system-prompts): Inject context without CLAUDE.md files

Was this page helpful?

YesNo

[How the agent loop works](/docs/en/agent-sdk/agent-loop)[Work with sessions](/docs/en/agent-sdk/sessions)

⌘I

---