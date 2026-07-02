---
title: Run the test suite
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### [​](#stop) Stop

Runs when the main Claude Code agent has finished responding. Does not run if
the stoppage occurred due to a user interrupt. API errors fire
[StopFailure](#stopfailure) instead.

The [`/goal`](/docs/en/goal) command is a built-in shortcut for a session-scoped prompt-based Stop hook. Use it when you want Claude to keep working until a condition holds without writing hook configuration.

#### [​](#stop-input) Stop input

In addition to the [common input fields](#common-input-fields), Stop hooks receive `stop_hook_active`, `last_assistant_message`, `background_tasks`, and `session_crons`. The `stop_hook_active` field is `true` when Claude Code is already continuing as a result of a stop hook. Check this value or process the transcript to avoid blocking on a condition that will never resolve. Claude Code overrides the hook and ends the turn after 8 consecutive blocks.
The `last_assistant_message` field contains the text content of Claude’s final response, so hooks can access it without parsing the transcript file.
The `background_tasks` and `session_crons` arrays, available in Claude Code v2.1.145 or later, let hooks distinguish “session is done” from “session is paused waiting for background work to wake it back up”. Both arrays are present when the task registry is reachable and are empty when nothing is in flight or scheduled.
Each entry in `background_tasks` describes one in-flight task and uses these fields:

| Field | Description |
| --- | --- |
| `id` | Task identifier |
| `type` | Friendly task-type label such as `shell`, `subagent`, `monitor`, `workflow`, `teammate`, `cloud session`, or `MCP task`. Each label identifies which Claude Code feature created the task. Falls back to the raw discriminant for unrecognized types |
| `status` | Current task status |
| `description` | Free-text description, capped at 1000 characters with an in-string `… [+N chars]` marker when clipped |
| `command` | Shell command line, capped at 1000 characters. Present only for `shell` tasks |
| `agent_type` | Subagent type name. Present only for `subagent` tasks |
| `server` | MCP server name. Present only for `monitor` and `MCP task` tasks |
| `tool` | MCP tool name. Present only for `monitor` and `MCP task` tasks |
| `name` | Workflow name. Present only for `workflow` tasks |

Each entry in `session_crons` describes one session-scoped scheduled wakeup, sourced from `CronCreate`, `ScheduleWakeup`, and `/loop`:

| Field | Description |
| --- | --- |
| `id` | Cron task identifier |
| `schedule` | Cron expression, for example `0 9 * * 1-5` |
| `recurring` | `false` for one-shot wakeups whose schedule encodes a single fire time, `true` for tasks that re-fire on every match |
| `prompt` | Prompt submitted when the cron fires, capped at 1000 characters with the same `… [+N chars]` marker |

This example shows a Stop input with one in-flight shell task and one recurring cron:

```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary...",
  "background_tasks": [
    {
      "id": "task-001",
      "type": "shell",
      "status": "running",
      "description": "tail logs",
      "command": "tail -f /var/log/syslog"
    }
  ],
  "session_crons": [
    {
      "id": "cron-001",
      "schedule": "0 9 * * 1-5",
      "recurring": true,
      "prompt": "check the build"
    }
  ]
}
```

#### [​](#stop-decision-control) Stop decision control

`Stop` and `SubagentStop` hooks can control whether Claude continues. In addition to the [JSON output fields](#json-output) available to all hooks, your hook script can return these event-specific fields:

| Field | Description |
| --- | --- |
| `decision` | `"block"` prevents Claude from stopping. Omit to allow Claude to stop |
| `reason` | Required when `decision` is `"block"`. Tells Claude why it should continue |
| `hookSpecificOutput.additionalContext` | Non-error feedback for Claude. The conversation continues so Claude can act on it, but unlike `decision: "block"` it is shown in the transcript as hook feedback rather than a hook error |

```
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

Use `additionalContext` when the hook is working as designed and giving Claude guidance, such as “run the test suite before finishing”. It keeps the conversation going through the same loop protections as `decision: "block"`, namely the `stop_hook_active` input and the 8-consecutive-continuation cap, but the transcript labels it `Stop hook feedback` and no hook error notification is shown:

```
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Please run the test suite before finishing"
  }
}
```

### [​](#stopfailure) StopFailure

Runs instead of [Stop](#stop) when the turn ends due to an API error. Output and exit code are ignored. Use this to log failures, send alerts, or take recovery actions when Claude cannot complete a response due to rate limits, authentication problems, or other API errors.

#### [​](#stopfailure-input) StopFailure input

In addition to the [common input fields](#common-input-fields), StopFailure hooks receive `error`, optional `error_details`, and optional `last_assistant_message`. The `error` field identifies the error type and is used for matcher filtering.

| Field | Description |
| --- | --- |
| `error` | Error type: `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, or `unknown` |
| `error_details` | Additional details about the error, when available |
| `last_assistant_message` | The rendered error text shown in the conversation. Unlike `Stop` and `SubagentStop`, where this field holds Claude’s conversational output, for `StopFailure` it contains the API error string itself, such as `"API Error: Rate limit reached"` |

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure hooks have no decision control. They run for notification and logging purposes only.

### [​](#teammateidle) TeammateIdle

Runs when an [agent team](/docs/en/agent-teams) teammate is about to go idle after finishing its turn. Use this to enforce quality gates before a teammate stops working, such as requiring passing lint checks or verifying that output files exist.
When a `TeammateIdle` hook exits with code 2, the teammate receives the stderr message as feedback and continues working instead of going idle. To stop the teammate entirely instead of re-running it, return JSON with `{"continue": false, "stopReason": "..."}`. TeammateIdle hooks do not support matchers and fire on every occurrence.

#### [​](#teammateidle-input) TeammateIdle input

In addition to the [common input fields](#common-input-fields), TeammateIdle hooks receive `teammate_name` and `team_name`.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "session-a1b2c3d4"
}
```

| Field | Description |
| --- | --- |
| `teammate_name` | Name of the teammate that is about to go idle |
| `team_name` | Deprecated. Session-derived team name; will be removed in a future release |

#### [​](#teammateidle-decision-control) TeammateIdle decision control

TeammateIdle hooks support two ways to control teammate behavior:

* **Exit code 2**: the teammate receives the stderr message as feedback and continues working instead of going idle.
* **JSON `{"continue": false, "stopReason": "..."}`**: stops the teammate entirely, matching `Stop` hook behavior. The `stopReason` is shown to the user.

This example checks that a build artifact exists before allowing a teammate to go idle:

```
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### [​](#configchange) ConfigChange

Runs when a configuration file changes during a session. Use this to audit settings changes, enforce security policies, or block unauthorized modifications to configuration files.
ConfigChange hooks fire for changes to settings files, managed policy settings, and skill files. The `source` field in the input tells you which type of configuration changed, and the optional `file_path` field provides the path to the changed file.
The matcher filters on the configuration source:

| Matcher | When it fires |
| --- | --- |
| `user_settings` | `~/.claude/settings.json` changes |
| `project_settings` | `.claude/settings.json` changes |
| `local_settings` | `.claude/settings.local.json` changes |
| `policy_settings` | Managed policy settings change |
| `skills` | A skill file in `.claude/skills/` changes |

This example logs all configuration changes for security auditing:

```
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/audit-config-change.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

#### [​](#configchange-input) ConfigChange input

In addition to the [common input fields](#common-input-fields), ConfigChange hooks receive `source` and optionally `file_path`. The `source` field indicates which configuration type changed, and `file_path` provides the path to the specific file that was modified.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### [​](#configchange-decision-control) ConfigChange decision control

ConfigChange hooks can block configuration changes from taking effect. Use exit code 2 or a JSON `decision` to prevent the change. When blocked, the new settings are not applied to the running session.

| Field | Description |
| --- | --- |
| `decision` | `"block"` prevents the configuration change from being applied. Omit to allow the change |
| `reason` | Explanation shown to the user when `decision` is `"block"` |

```
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` changes cannot be blocked. Hooks still fire for `policy_settings` sources, so you can use them for audit logging, but any blocking decision is ignored. This ensures enterprise-managed settings always take effect.

### [​](#cwdchanged) CwdChanged

Runs when the working directory changes during a session, for example when Claude executes a `cd` command. Use this to react to directory changes: reload environment variables, activate project-specific toolchains, or run setup scripts automatically. Pairs with [FileChanged](#filechanged) for tools like [direnv](https://direnv.net/) that manage per-directory environment.
CwdChanged hooks have access to `CLAUDE_ENV_FILE`. Variables written to that file persist into subsequent Bash commands for the session, just as in [SessionStart hooks](#persist-environment-variables).
CwdChanged does not support matchers and fires on every directory change.

#### [​](#cwdchanged-input) CwdChanged input

In addition to the [common input fields](#common-input-fields), CwdChanged hooks receive `old_cwd` and `new_cwd`.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### [​](#cwdchanged-output) CwdChanged output

In addition to the [JSON output fields](#json-output) available to all hooks, CwdChanged hooks can return `watchPaths` to dynamically set which file paths [FileChanged](#filechanged) watches:

| Field | Description |
| --- | --- |
| `watchPaths` | Array of absolute paths. Replaces the current dynamic watch list (paths from your `matcher` configuration are always watched). Returning an empty array clears the dynamic list, which is typical when entering a new directory |

CwdChanged hooks have no decision control. They cannot block the directory change.

### [​](#filechanged) FileChanged

Runs when a watched file changes on disk. Useful for reloading environment variables when project configuration files are modified.
The `matcher` for this event serves two roles:

* **Build the watch list**: the value is split on `|` and each segment is registered as a literal filename in the working directory, so `".envrc|.env"` watches exactly those two files. Regex patterns are not useful here: a value like `^\.env` would watch a file literally named `^\.env`.
* **Filter which hooks run**: when a watched file changes, the same value filters which hook groups run using the standard [matcher rules](#matcher-patterns) against the changed file’s basename.

FileChanged hooks have access to `CLAUDE_ENV_FILE`. Variables written to that file persist into subsequent Bash commands for the session, just as in [SessionStart hooks](#persist-environment-variables).

#### [​](#filechanged-input) FileChanged input

In addition to the [common input fields](#common-input-fields), FileChanged hooks receive `file_path` and `event`.

| Field | Description |
| --- | --- |
| `file_path` | Absolute path to the file that changed |
| `event` | What happened: `"change"` (file modified), `"add"` (file created), or `"unlink"` (file deleted) |

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### [​](#filechanged-output) FileChanged output

In addition to the [JSON output fields](#json-output) available to all hooks, FileChanged hooks can return `watchPaths` to dynamically update which file paths are watched:

| Field | Description |
| --- | --- |
| `watchPaths` | Array of absolute paths. Replaces the current dynamic watch list (paths from your `matcher` configuration are always watched). Use this when your hook script discovers additional files to watch based on the changed file |

FileChanged hooks have no decision control. They cannot block the file change from occurring.

### [​](#worktreecreate) WorktreeCreate

When you run `claude --worktree` or a [subagent uses `isolation: "worktree"`](/docs/en/sub-agents#choose-the-subagent-scope), Claude Code creates an isolated working copy using `git worktree`. If you configure a WorktreeCreate hook, it replaces the default git behavior, letting you use a different version control system like SVN, Perforce, or Mercurial.
Because the hook replaces the default behavior entirely, [`.worktreeinclude`](/docs/en/worktrees#copy-gitignored-files-into-worktrees) is not processed. If you need to copy local configuration files like `.env` into the new worktree, do it inside your hook script.
The hook must return the absolute path to the created worktree directory. Claude Code uses this path as the working directory for the isolated session. Command hooks print it on stdout; HTTP hooks return it via `hookSpecificOutput.worktreePath`.
This example creates an SVN working copy and prints the path for Claude Code to use. Replace the repository URL with your own:

```
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

The hook reads the worktree `name` from the JSON input on stdin, checks out a fresh copy into a new directory, and prints the directory path. The `echo` on the last line is what Claude Code reads as the worktree path. Redirect any other output to stderr so it doesn’t interfere with the path.

#### [​](#worktreecreate-input) WorktreeCreate input

In addition to the [common input fields](#common-input-fields), WorktreeCreate hooks receive the `name` field. This is a slug identifier for the new worktree, either specified by the user or auto-generated (for example, `bold-oak-a3f2`).

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### [​](#worktreecreate-output) WorktreeCreate output

WorktreeCreate hooks do not use the standard allow/block decision model. Instead, the hook’s success or failure determines the outcome. The hook must return the absolute path to the created worktree directory:

* **Command hooks** (`type: "command"`): print the path on stdout.
* **HTTP hooks** (`type: "http"`): return `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` in the response body.

If the hook fails or produces no path, worktree creation fails with an error.

### [​](#worktreeremove) WorktreeRemove

The cleanup counterpart to [WorktreeCreate](#worktreecreate). This hook fires when a worktree is being removed, either when you exit a `--worktree` session and choose to remove it, or when a subagent with `isolation: "worktree"` finishes. For git-based worktrees, Claude handles cleanup automatically with `git worktree remove`. If you configured a WorktreeCreate hook for a non-git version control system, pair it with a WorktreeRemove hook to handle cleanup. Without one, the worktree directory is left on disk.
Claude Code passes the path returned by WorktreeCreate as `worktree_path` in the hook input. This example reads that path and removes the directory:

```
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### [​](#worktreeremove-input) WorktreeRemove input

In addition to the [common input fields](#common-input-fields), WorktreeRemove hooks receive the `worktree_path` field, which is the absolute path to the worktree being removed.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove hooks have no decision control. They cannot block worktree removal but can perform cleanup tasks like removing version control state or archiving changes. Hook failures are logged in debug mode only.

### [​](#precompact) PreCompact

Runs before Claude Code is about to run a compact operation.
The matcher value indicates whether compaction was triggered manually or automatically:

| Matcher | When it fires |
| --- | --- |
| `manual` | `/compact` |
| `auto` | Auto-compact when the context window is full |

Exit with code 2 to block compaction. For a manual `/compact`, the stderr message is shown to the user. You can also block by returning JSON with `"decision": "block"`.
Blocking automatic compaction has different effects depending on when it fires. If compaction was triggered proactively before the context limit, Claude Code skips it and the conversation continues uncompacted. If compaction was triggered to recover from a context-limit error already returned by the API, the underlying error surfaces and the current request fails.

#### [​](#precompact-input) PreCompact input

In addition to the [common input fields](#common-input-fields), PreCompact hooks receive `trigger` and `custom_instructions`. For `manual`, `custom_instructions` contains what the user passes into `/compact`. For `auto`, `custom_instructions` is empty.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### [​](#postcompact) PostCompact

Runs after Claude Code completes a compact operation. Use this event to react to the new compacted state, for example to log the generated summary or update external state.
The same matcher values apply as for `PreCompact`:

| Matcher | When it fires |
| --- | --- |
| `manual` | After `/compact` |
| `auto` | After auto-compact when the context window is full |

#### [​](#postcompact-input) PostCompact input

In addition to the [common input fields](#common-input-fields), PostCompact hooks receive `trigger` and `compact_summary`. The `compact_summary` field contains the conversation summary generated by the compact operation.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact hooks have no decision control. They cannot affect the compaction result but can perform follow-up tasks.

### [​](#sessionend) SessionEnd

Runs when a Claude Code session ends. Useful for cleanup tasks, logging session
statistics, or saving session state. Supports matchers to filter by exit reason.
The `reason` field in the hook input indicates why the session ended:

| Reason | Description |
| --- | --- |
| `clear` | Session cleared with `/clear` command |
| `resume` | Session switched via interactive `/resume` |
| `logout` | User logged out |
| `prompt_input_exit` | User exited while prompt input was visible |
| `bypass_permissions_disabled` | Bypass permissions mode was disabled |
| `other` | Other exit reasons |

#### [​](#sessionend-input) SessionEnd input

In addition to the [common input fields](#common-input-fields), SessionEnd hooks receive a `reason` field indicating why the session ended. See the [reason table](#sessionend) above for all values.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd hooks have no decision control. They cannot block session termination but can perform cleanup tasks.
SessionEnd hooks have a default timeout of 1.5 seconds. This applies to session exit, `/clear`, and switching sessions via interactive `/resume`. If a hook needs more time, set a per-hook `timeout` in the hook configuration. The overall budget is automatically raised to the highest per-hook timeout configured in settings files, up to 60 seconds. Timeouts set on plugin-provided hooks do not raise the budget. To override the budget explicitly, set the `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` environment variable in milliseconds.

```
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### [​](#elicitation) Elicitation

Runs when an MCP server requests user input mid-task. By default, Claude Code shows an interactive dialog for the user to respond. Hooks can intercept this request and respond programmatically, skipping the dialog entirely.
The matcher field matches against the MCP server name.

#### [​](#elicitation-input) Elicitation input

In addition to the [common input fields](#common-input-fields), Elicitation hooks receive `mcp_server_name`, `message`, and optional `mode`, `url`, `elicitation_id`, and `requested_schema` fields.
For form-mode elicitation (the most common case):

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

For URL-mode elicitation (browser-based authentication):

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### [​](#elicitation-output) Elicitation output

To respond programmatically without showing the dialog, return a JSON object with `hookSpecificOutput`:

```
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Field | Values | Description |
| --- | --- | --- |
| `action` | `accept`, `decline`, `cancel` | Whether to accept, decline, or cancel the request |
| `content` | object | Form field values to submit. Only used when `action` is `accept` |

Exit code 2 denies the elicitation and shows stderr to the user.

### [​](#elicitationresult) ElicitationResult

Runs after a user responds to an MCP elicitation. Hooks can observe, modify, or block the response before it is sent back to the MCP server.
The matcher field matches against the MCP server name.

#### [​](#elicitationresult-input) ElicitationResult input

In addition to the [common input fields](#common-input-fields), ElicitationResult hooks receive `mcp_server_name`, `action`, and optional `mode`, `elicitation_id`, and `content` fields.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### [​](#elicitationresult-output) ElicitationResult output

To override the user’s response, return a JSON object with `hookSpecificOutput`:

```
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Field | Values | Description |
| --- | --- | --- |
| `action` | `accept`, `decline`, `cancel` | Overrides the user’s action |
| `content` | object | Overrides form field values. Only meaningful when `action` is `accept` |

Exit code 2 blocks the response, changing the effective action to `decline`.

## [​](#prompt-based-hooks) Prompt-based hooks

In addition to command, HTTP, and MCP tool hooks, Claude Code supports prompt-based hooks (`type: "prompt"`) that use an LLM to evaluate whether to allow or block an action, and agent hooks (`type: "agent"`) that spawn an agentic verifier with tool access. Not all events support every hook type.
Events that support all five hook types (`command`, `http`, `mcp_tool`, `prompt`, and `agent`):

* `PermissionDenied`
* `PermissionRequest`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `TeammateIdle`
* `UserPromptExpansion`
* `UserPromptSubmit`

Events that support `command`, `http`, and `mcp_tool` hooks but not `prompt` or `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` and `Setup` support `command` and `mcp_tool` hooks. They do not support `http`, `prompt`, or `agent` hooks.

### [​](#how-prompt-based-hooks-work) How prompt-based hooks work

Instead of executing a Bash command, prompt-based hooks:

1. Send the hook input and your prompt to a Claude model, Haiku by default
2. The LLM responds with structured JSON containing a decision
3. Claude Code processes the decision automatically

### [​](#prompt-hook-configuration) Prompt hook configuration

Set `type` to `"prompt"` and provide a `prompt` string instead of a `command`. Use the `$ARGUMENTS` placeholder to inject the hook’s JSON input data into your prompt text. Claude Code sends the combined prompt and input to a fast Claude model, which returns a JSON decision.
This `Stop` hook asks the LLM to evaluate whether all tasks are complete before allowing Claude to finish:

```
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Field | Required | Description |
| --- | --- | --- |
| `type` | yes | Must be `"prompt"` |
| `prompt` | yes | The prompt text to send to the LLM. Use `$ARGUMENTS` as a placeholder for the hook input JSON. If `$ARGUMENTS` is not present, input JSON is appended to the prompt |
| `model` | no | Model to use for evaluation. Defaults to a fast model |
| `timeout` | no | Timeout in seconds. Default: 30 |
| `continueOnBlock` | no | When the prompt returns `ok: false`, feed the reason back to Claude and continue the turn instead of stopping. Default: `false`. Implemented as `continue: true` on the resulting `decision: "block"`. See [Response schema](#response-schema) for per-event behavior |

### [​](#response-schema) Response schema

The LLM must respond with JSON containing:

```
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Field | Description |
| --- | --- |
| `ok` | `true` to allow. `false` produces a `decision: "block"`. See the per-event behavior below |
| `reason` | Required when `ok` is `false`. Used as the block reason |

What happens on `ok: false` depends on the event:

* `Stop` and `SubagentStop`: the reason is fed back to Claude as its next instruction and the turn continues
* `PreToolUse`: the tool call is denied and the reason is returned to Claude as the tool error, equivalent to a command hook’s `permissionDecision: "deny"`
* `PostToolUse`: by default the turn ends and the reason appears in the chat as a warning line. Set `continueOnBlock: true` to feed the reason back to Claude and continue the turn instead
* `PostToolBatch`, `UserPromptSubmit`, and `UserPromptExpansion`: the turn ends and the reason appears as a warning line. These events end the turn on `decision: "block"` regardless of `continue`
* `PostToolUseFailure`, `TaskCreated`, and `TaskCompleted`: the reason is returned to Claude as a tool error, similar to `PreToolUse`
* `TeammateIdle`: by default the teammate stops and the reason appears as a warning line. Set `continueOnBlock: true` to feed the reason back to the teammate and keep it working instead
* `PermissionRequest`: `ok: false` has no effect. To deny an approval from a hook, use a [command hook](#command-hook-fields) returning `hookSpecificOutput.decision.behavior: "deny"`
* `PermissionDenied`: `ok: false` has no effect because the denial already happened. The only output this event reads is `hookSpecificOutput.retry`, which prompt and agent hooks cannot set. They run on this event, but their output is discarded. Use a [command hook](#command-hook-fields) to return `retry`

If you need finer control on any event, use a [command hook](#command-hook-fields) with the per-event fields described in [Decision control](#decision-control).

### [​](#example-multi-criteria-stop-hook) Example: Multi-criteria Stop hook

This `Stop` hook uses a detailed prompt to check three conditions before allowing Claude to stop. If `"ok"` is `false`, Claude continues working with the provided reason as its next instruction. `SubagentStop` hooks use the same format to evaluate whether a [subagent](/docs/en/sub-agents) should stop:

```
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## [​](#agent-based-hooks) Agent-based hooks

Agent hooks are experimental. Behavior and configuration may change in future releases. For production workflows, prefer [command hooks](#command-hook-fields).

Agent-based hooks (`type: "agent"`) are like prompt-based hooks but with multi-turn tool access. Instead of a single LLM call, an agent hook spawns a subagent that can read files, search code, and inspect the codebase to verify conditions. Agent hooks support the same events as prompt-based hooks.

### [​](#how-agent-hooks-work) How agent hooks work

When an agent hook fires:

1. Claude Code spawns a subagent with your prompt and the hook’s JSON input
2. The subagent can use tools like Read, Grep, and Glob to investigate
3. After up to 50 turns, the subagent returns a structured `{ "ok": true/false }` decision
4. Claude Code processes the decision the same way as a prompt hook

Agent hooks are useful when verification requires inspecting actual files or test output, not just evaluating the hook input data alone.

### [​](#agent-hook-configuration) Agent hook configuration

Set `type` to `"agent"` and provide a `prompt` string. The configuration fields are the same as [prompt hooks](#prompt-hook-configuration), with a longer default timeout:

| Field | Required | Description |
| --- | --- | --- |
| `type` | yes | Must be `"agent"` |
| `prompt` | yes | Prompt describing what to verify. Use `$ARGUMENTS` as a placeholder for the hook input JSON |
| `model` | no | Model to use. Defaults to a fast model |
| `timeout` | no | Timeout in seconds. Default: 60 |

The response schema is the same as prompt hooks: `{ "ok": true }` to allow or `{ "ok": false, "reason": "..." }` to block.
This `Stop` hook verifies that all unit tests pass before allowing Claude to finish:

```
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## [​](#run-hooks-in-the-background) Run hooks in the background

By default, hooks block Claude’s execution until they complete. For long-running tasks like deployments, test suites, or external API calls, set `"async": true` to run the hook in the background while Claude continues working. Async hooks cannot block or control Claude’s behavior: response fields like `decision`, `permissionDecision`, and `continue` have no effect, because the action they would have controlled has already completed.

### [​](#configure-an-async-hook) Configure an async hook

Add `"async": true` to a command hook’s configuration to run it in the background without blocking Claude. This field is only available on `type: "command"` hooks.
This hook runs a test script after every `Write` tool call. Claude continues working immediately while `run-tests.sh` executes for up to 120 seconds. When the script finishes, its output is delivered on the next conversation turn:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

The `timeout` field sets the maximum time in seconds for the background process. If not specified, async hooks use the same 10-minute default as sync hooks.

### [​](#how-async-hooks-execute) How async hooks execute

When an async hook fires, Claude Code starts the hook process and immediately continues without waiting for it to finish. The hook receives the same JSON input via stdin as a synchronous hook.
After the background process exits, if the hook produced a JSON response with an `additionalContext` field, that content is delivered to Claude as context on the next conversation turn. A `systemMessage` field is shown to you, not to Claude.
Async hook completion notifications are suppressed by default. To see them, enable verbose mode with `Ctrl+O` or start Claude Code with `--verbose`.

### [​](#example-run-tests-after-file-changes) Example: run tests after file changes

This hook starts a test suite in the background whenever Claude writes a file, then reports the results back to Claude when the tests finish. Save this script to `.claude/hooks/run-tests-async.sh` in your project and make it executable with `chmod +x`:

```
#!/bin/bash