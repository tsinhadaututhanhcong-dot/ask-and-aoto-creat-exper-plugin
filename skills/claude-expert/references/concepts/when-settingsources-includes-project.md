---
title: when settingSources includes "project"
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# when settingSources includes "project"
async for message in query(
    prompt="Review this PR using our code review checklist",
    options=ClaudeAgentOptions(
        setting_sources=["user", "project"],
        skills="all",
        allowed_tools=["Read", "Grep", "Glob"],
    ),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

Skills must be created as filesystem artifacts (`.claude/skills/<name>/SKILL.md`). The SDK does not have a programmatic API for registering skills. See [Agent Skills in the SDK](/docs/en/agent-sdk/skills) for full details.

For more on creating and using skills, see [Agent Skills in the SDK](/docs/en/agent-sdk/skills).

## [​](#hooks) Hooks

The SDK supports two ways to define hooks, and they run side by side:

* **Filesystem hooks:** shell commands defined in `settings.json`, loaded when `settingSources` includes the relevant source. These are the same hooks you’d configure for [interactive Claude Code sessions](/docs/en/hooks-guide).
* **Programmatic hooks:** callback functions passed directly to `query()`. These run in your application process and can return structured decisions. See [Control execution with hooks](/docs/en/agent-sdk/hooks).

Both types execute during the same hook lifecycle. If you already have hooks in your project’s `.claude/settings.json` and you set `settingSources: ["project"]`, those hooks run automatically in the SDK with no extra configuration.
Hook callbacks receive the tool input and return a decision dict. Returning `{}` means allow the tool to proceed. To block execution, return a `hookSpecificOutput` object with `permissionDecision: "deny"` and a `permissionDecisionReason`. The reason is sent to Claude as the tool result. The top-level `decision` and `reason` fields are deprecated for `PreToolUse`. See the [hooks guide](/docs/en/agent-sdk/hooks) for the full callback signature and return types.

Python

TypeScript

```
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, ResultMessage