---
title: Notification hook: ping the desktop when Claude Code needs attention.
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Notification hook: ping the desktop when Claude Code needs attention.
input=$(cat)
title="Claude Code"
body=$(jq -r '.message // "Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

The `{ "terminalSequence": "..." }` shape is the same from any shell or language. On Windows, build the escape string in PowerShell or a script and emit the same JSON object.

`terminalSequence` is the supported replacement for hooks that previously wrote escape sequences directly to `/dev/tty`. The allowlist is restricted to sequences that cannot move the cursor or alter colors, so a hook can never corrupt an on-screen prompt.

#### [​](#add-context-for-claude) Add context for Claude

The `additionalContext` field passes a string from your hook into Claude’s context window. Claude Code wraps the string in a system reminder and inserts it into the conversation at the point where the hook fired. Claude reads the reminder on the next model request, but it does not appear as a chat message in the interface.
Return `additionalContext` inside `hookSpecificOutput` alongside the event name:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Where the reminder appears depends on the event:

* [SessionStart](#sessionstart), [Setup](#setup), and [SubagentStart](#subagentstart): at the start of the conversation, before the first prompt
* [UserPromptSubmit](#userpromptsubmit) and [UserPromptExpansion](#userpromptexpansion): alongside the submitted prompt
* [PreToolUse](#pretooluse), [PostToolUse](#posttooluse), [PostToolUseFailure](#posttoolusefailure), and [PostToolBatch](#posttoolbatch): next to the tool result
* [Stop](#stop) and [SubagentStop](#subagentstop): at the end of the turn. The conversation continues so Claude can act on the feedback. See [Stop decision control](#stop-decision-control)

When several hooks return `additionalContext` for the same event, Claude receives all of the values. If a value exceeds 10,000 characters, Claude Code writes the full text to a file in the session directory and passes Claude the file path with a short preview instead.
Use `additionalContext` for information Claude should know about the current state of your environment or the operation that just ran:

* **Environment state**: the current branch, deployment target, or active feature flags
* **Conditional project rules**: which test command applies to the file just edited, which directories are read-only in this worktree
* **External data**: open issues assigned to you, recent CI results, content fetched from an internal service

For instructions that never change, prefer [CLAUDE.md](/docs/en/memory). It loads without running a script and is the standard place for static project conventions.
Write the text as factual statements rather than imperative system instructions. Phrasing such as “The deployment target is production” or “This repo uses `bun test`” reads as project information. Text framed as out-of-band system commands can trigger Claude’s prompt-injection defenses, which causes Claude to surface the text to you instead of treating it as context.
Once injected, the text is saved in the session transcript. For mid-session events like `PostToolUse` or `UserPromptSubmit`, resuming with `--continue` or `--resume` replays the saved text rather than re-running the hook for past turns, so values like timestamps or commit SHAs become stale on resume. `SessionStart` hooks run again on resume with `source` set to `"resume"`, so they can refresh their context.

#### [​](#decision-control) Decision control

Not every event supports blocking or controlling behavior through JSON. The events that do each use a different set of fields to express that decision. Use this table as a quick reference before writing a hook:

| Events | Decision pattern | Key fields |
| --- | --- | --- |
| UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | Top-level `decision` | `decision: "block"`, `reason`. Stop and SubagentStop also accept `hookSpecificOutput.additionalContext` for [non-error feedback that continues the conversation](#stop-decision-control) |
| TeammateIdle, TaskCreated, TaskCompleted | Exit code or `continue: false` | Exit code 2 blocks the action with stderr feedback. JSON `{"continue": false, "stopReason": "..."}` also stops the teammate entirely, matching `Stop` hook behavior |
| PreToolUse | `hookSpecificOutput` | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason` |
| PermissionRequest | `hookSpecificOutput` | `decision.behavior` (allow/deny) |
| PermissionDenied | `hookSpecificOutput` | `retry: true` tells the model it may retry the denied tool call |
| WorktreeCreate | path return | Command hook prints path on stdout; HTTP hook returns `hookSpecificOutput.worktreePath`. Hook failure or missing path fails creation |
| Elicitation | `hookSpecificOutput` | `action` (accept/decline/cancel), `content` (form field values for accept) |
| ElicitationResult | `hookSpecificOutput` | `action` (accept/decline/cancel), `content` (form field values override) |
| MessageDisplay | `hookSpecificOutput` | `displayContent` replaces the displayed text on screen. Display-only: the transcript and what Claude sees keep the original |
| SessionStart, Setup, SubagentStart | Context only | `hookSpecificOutput.additionalContext` adds context for Claude. SessionStart also accepts [`initialUserMessage`, `watchPaths`, `sessionTitle`, and `reloadSkills`](#sessionstart-decision-control). No blocking or decision control |
| WorktreeRemove, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged | None | No decision control. Used for side effects like logging or cleanup |

A few events can also rewrite content rather than only allow or block it:

* `PreToolUse`: `updatedInput` directly under `hookSpecificOutput` replaces a tool’s arguments before it runs. See [PreToolUse decision control](#pretooluse-decision-control)
* `PermissionRequest`: `updatedInput` inside the `decision` object. See [PermissionRequest decision control](#permissionrequest-decision-control)
* `PostToolUse`: `updatedToolOutput` replaces the tool’s result. See [PostToolUse decision control](#posttooluse-decision-control)
* `UserPromptSubmit`: cannot replace the prompt; it only injects `additionalContext` alongside it

For redaction or transformation use cases, intercept at `PreToolUse` for outbound tool inputs and `PostToolUse` for inbound tool results.
Here are examples of each pattern in action:

* Top-level decision
* PreToolUse
* PermissionRequest

Used by `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange`, and `PreCompact`. The only value is `"block"`. To allow the action to proceed, omit `decision` from your JSON, or exit 0 without any JSON at all:

```
{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}
```

Uses `hookSpecificOutput` for richer control: allow, deny, or escalate to the user. You can also modify tool input before it runs or inject additional context for Claude. See [PreToolUse decision control](#pretooluse-decision-control) for the full set of options.

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed"
  }
}
```

Uses `hookSpecificOutput` to allow or deny a permission request on behalf of the user. When allowing, you can also modify the tool’s input or apply permission rules so the user isn’t prompted again. See [PermissionRequest decision control](#permissionrequest-decision-control) for the full set of options.

```
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

For extended examples including Bash command validation, prompt filtering, and auto-approval scripts, see [What you can automate](/docs/en/hooks-guide#what-you-can-automate) in the guide and the [Bash command validator reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## [​](#hook-events) Hook events

Each event corresponds to a point in Claude Code’s lifecycle where hooks can run. The sections below are ordered to match the lifecycle: from session setup through the agentic loop to session end. Each section describes when the event fires, what matchers it supports, the JSON input it receives, and how to control behavior through output.

### [​](#sessionstart) SessionStart

Runs when Claude Code starts a new session or resumes an existing session. Useful for loading development context like existing issues or recent changes to your codebase, or setting up environment variables. For static context that does not require a script, use [CLAUDE.md](/docs/en/memory) instead.
SessionStart runs on every session, so keep these hooks fast. Only `type: "command"` and `type: "mcp_tool"` hooks are supported.
The matcher value corresponds to how the session was initiated:

| Matcher | When it fires |
| --- | --- |
| `startup` | New session |
| `resume` | `--resume`, `--continue`, or `/resume` |
| `clear` | `/clear` |
| `compact` | Auto or manual compaction |

#### [​](#sessionstart-input) SessionStart input

In addition to the [common input fields](#common-input-fields), SessionStart hooks receive `source` and optionally `model`, `agent_type`, and `session_title`. The `source` field indicates how the session started: `"startup"` for new sessions, `"resume"` for resumed sessions, `"clear"` after `/clear`, or `"compact"` after compaction. The `model` field contains the active model identifier. It can be omitted, for example after `/clear` or when a session is restored through conversation recovery, so check for the field before reading it. If you start Claude Code with `claude --agent <name>`, an `agent_type` field contains the agent name. The `session_title` field carries the current session title if one is already set, for example via `--name` or `/rename`. A hook that emits `sessionTitle` can check `session_title` first to avoid overwriting a title the user set explicitly.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### [​](#sessionstart-decision-control) SessionStart decision control

Any text your hook script prints to stdout is added as context for Claude. In addition to the [JSON output fields](#json-output) available to all hooks, you can return these event-specific fields:

| Field | Description |
| --- | --- |
| `additionalContext` | String added to Claude’s context at the start of the conversation, before the first prompt. See [Add context for Claude](#add-context-for-claude) for how the text is delivered and what to put in it |
| `initialUserMessage` | String used as the first user message of the session. Applies in [non-interactive mode](/docs/en/headless) (`-p`), where it becomes the first turn even if no prompt is provided. If a prompt is provided, it follows as the next turn. Unlike `additionalContext`, which attaches to an existing turn, this creates the turn |
| `sessionTitle` | Sets the session title, with the same effect as `/rename`. Use to name sessions automatically from the launch folder, git branch, or worktree name. Applies only when `source` is `"startup"` or `"resume"`; ignored on `"clear"` and `"compact"` |
| `watchPaths` | Array of absolute paths to watch for [FileChanged](#filechanged) events during this session |
| `reloadSkills` | Boolean. When `true`, Claude Code re-scans the [skill](/docs/en/skills) and command directories after the SessionStart hooks complete, so skills the hook installed are available in the same session, starting with the first prompt |

```
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2",
    "sessionTitle": "auth-refactor"
  }
}
```

Since plain stdout already reaches Claude for this event, a hook that only loads context can print to stdout directly without building JSON. Use the JSON form when you need to combine context with other fields such as `suppressOutput` or `sessionTitle`.
Use `reloadSkills` when a SessionStart hook installs or updates skills. Skill discovery normally runs before SessionStart hooks finish, so files the hook writes into `~/.claude/skills/` or `.claude/skills/` would otherwise only appear in the next session. This example syncs a shared skills repository and requests the re-scan:

```
#!/bin/bash

git -C ~/.claude/skills/team-skills pull --quiet 2>/dev/null || \
  git clone --quiet https://git.example.com/your-org/team-skills.git ~/.claude/skills/team-skills

echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "reloadSkills": true}}'
```

#### [​](#persist-environment-variables) Persist environment variables

SessionStart hooks have access to the `CLAUDE_ENV_FILE` environment variable, which provides a file path where you can persist environment variables for subsequent Bash commands.
To set individual environment variables, write `export` statements to `CLAUDE_ENV_FILE`. Use append (`>>`) to preserve variables set by other hooks:

```
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

To capture all environment changes from setup commands, compare the exported variables before and after:

```
#!/bin/bash

ENV_BEFORE=$(export -p | sort)