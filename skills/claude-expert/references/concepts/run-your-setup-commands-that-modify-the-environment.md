---
title: Run your setup commands that modify the environment
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Any variables written to this file will be available in all subsequent Bash commands that Claude Code executes during the session.

`CLAUDE_ENV_FILE` is available for SessionStart, [Setup](#setup), [CwdChanged](#cwdchanged), and [FileChanged](#filechanged) hooks. Other hook types do not have access to this variable.

### [​](#setup) Setup

Fires only when you launch Claude Code with `--init-only`, or with `--init` or `--maintenance` in print mode (`-p`). It does not fire on normal startup. Use it for one-time dependency installation or scheduled cleanup that you trigger explicitly from CI or scripts, separate from normal session startup. For per-session initialization, use [SessionStart](#sessionstart) instead.
The matcher value corresponds to the CLI flag that triggered the hook:

| Matcher | When it fires |
| --- | --- |
| `init` | `claude --init-only` or `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

`--init-only` runs Setup hooks and `SessionStart` hooks with the `startup` matcher, then exits without starting a conversation. `--init` and `--maintenance` fire Setup hooks only when combined with `-p` (print mode); in an interactive session those two flags do not currently fire Setup hooks.
Because Setup does not fire on every launch, a plugin that needs a dependency installed cannot rely on Setup alone. The practical pattern is to check for the dependency on first use and install on miss, for example a hook or skill that tests for `${CLAUDE_PLUGIN_DATA}/node_modules` and runs `npm install` if absent. See the [persistent data directory](/docs/en/plugins-reference#persistent-data-directory) for where to store installed dependencies.

#### [​](#setup-input) Setup input

In addition to the [common input fields](#common-input-fields), Setup hooks receive a `trigger` field set to either `"init"` or `"maintenance"`:

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### [​](#setup-decision-control) Setup decision control

Setup hooks cannot block. On exit code 2, stderr is shown to the user; on any other non-zero exit code, stderr appears only when you launch with `--verbose`. In both cases execution continues. To pass information into Claude’s context, return `additionalContext` in JSON output; plain stdout is written to the debug log only. In addition to the [JSON output fields](#json-output) available to all hooks, you can return these event-specific fields:

| Field | Description |
| --- | --- |
| `additionalContext` | String added to Claude’s context. Multiple hooks’ values are concatenated |

```
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Dependencies installed: node_modules, .venv"
  }
}
```

Setup hooks have access to `CLAUDE_ENV_FILE`. Variables written to that file persist into subsequent Bash commands for the session, just as in [SessionStart hooks](#persist-environment-variables). Only `type: "command"` and `type: "mcp_tool"` hooks are supported.

### [​](#instructionsloaded) InstructionsLoaded

Fires when a `CLAUDE.md` or `.claude/rules/*.md` file is loaded into context. This event fires at session start for eagerly-loaded files and again later when files are lazily loaded, for example when Claude accesses a subdirectory that contains a nested `CLAUDE.md` or when conditional rules with `paths:` frontmatter match. The hook does not support blocking or decision control. It runs asynchronously for observability purposes.
The matcher runs against `load_reason`. For example, use `"matcher": "session_start"` to fire only for files loaded at session start, or `"matcher": "path_glob_match|nested_traversal"` to fire only for lazy loads.

#### [​](#instructionsloaded-input) InstructionsLoaded input

In addition to the [common input fields](#common-input-fields), InstructionsLoaded hooks receive these fields:

| Field | Description |
| --- | --- |
| `file_path` | Absolute path to the instruction file that was loaded |
| `memory_type` | Scope of the file: `"User"`, `"Project"`, `"Local"`, or `"Managed"` |
| `load_reason` | Why the file was loaded: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"`, or `"compact"`. The `"compact"` value fires when instruction files are re-loaded after a compaction event |
| `globs` | Path glob patterns from the file’s `paths:` frontmatter, if any. Present only for `path_glob_match` loads |
| `trigger_file_path` | Path to the file whose access triggered this load, for lazy loads |
| `parent_file_path` | Path to the parent instruction file that included this one, for `include` loads |

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### [​](#instructionsloaded-decision-control) InstructionsLoaded decision control

InstructionsLoaded hooks have no decision control. They cannot block or modify instruction loading. Use this event for audit logging, compliance tracking, or observability.

### [​](#userpromptsubmit) UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it. This allows you
to add additional context based on the prompt/conversation, validate prompts, or
block certain types of prompts.
`UserPromptSubmit` hooks have a default timeout of 30 seconds for `command`, `http`, and `mcp_tool` types, shorter than the 600-second default for those types on most other events. Because this hook runs before every prompt and blocks model processing until it completes, a stuck hook stalls the session. If your hook needs more time, set the `timeout` field in the hook entry.

#### [​](#userpromptsubmit-input) UserPromptSubmit input

In addition to the [common input fields](#common-input-fields), UserPromptSubmit hooks receive the `prompt` field containing the text the user submitted.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### [​](#userpromptsubmit-decision-control) UserPromptSubmit decision control

`UserPromptSubmit` hooks can control whether a user prompt is processed and add context. All [JSON output fields](#json-output) are available.
There are two ways to add context to the conversation on exit code 0:

* **Plain text stdout**: any non-JSON text written to stdout is added as context
* **JSON with `additionalContext`**: use the JSON format below for more control. The `additionalContext` field is added as context

Plain stdout is shown as hook output in the transcript. The `additionalContext` field is added more discretely.
To block a prompt, return a JSON object with `decision` set to `"block"`:

| Field | Description |
| --- | --- |
| `decision` | `"block"` prevents the prompt from being processed and erases it from context. Omit to allow the prompt to proceed |
| `reason` | Shown to the user when `decision` is `"block"`. Not added to context |
| `additionalContext` | String added to Claude’s context alongside the submitted prompt. See [Add context for Claude](#add-context-for-claude) |
| `sessionTitle` | Sets the session title. Use to name sessions automatically based on the prompt content |
| `suppressOriginalPrompt` | If `true` when `decision` is `"block"`, omits the original prompt text from the block message shown to the user |

```
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

The JSON format isn’t required for simple use cases. To add context, you can print plain text to stdout with exit code 0. Use JSON when you need to
block prompts or want more structured control.

### [​](#userpromptexpansion) UserPromptExpansion

Runs when a user-typed slash command expands into a prompt before reaching Claude. Use this to block specific commands from direct invocation, inject context for a particular skill, or log which commands users invoke. For example, a hook matching `deploy` can block `/deploy` unless an approval file is present, or a hook matching a review skill can append the team’s review checklist as `additionalContext`.
This event covers the path `PreToolUse` does not: a `PreToolUse` hook matching the `Skill` tool fires only when Claude calls the tool, but typing `/skillname` directly bypasses `PreToolUse`. `UserPromptExpansion` fires on that direct path.
Matches on `command_name`. Leave the matcher empty to fire on every prompt-type slash command.

#### [​](#userpromptexpansion-input) UserPromptExpansion input

In addition to the [common input fields](#common-input-fields), UserPromptExpansion hooks receive `expansion_type`, `command_name`, `command_args`, `command_source`, and the original `prompt` string. The `expansion_type` field is `slash_command` for skill and custom commands, or `mcp_prompt` for MCP server prompts.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

#### [​](#userpromptexpansion-decision-control) UserPromptExpansion decision control

`UserPromptExpansion` hooks can block the expansion or add context. All [JSON output fields](#json-output) are available.

| Field | Description |
| --- | --- |
| `decision` | `"block"` prevents the slash command from expanding. Omit to allow it to proceed |
| `reason` | Shown to the user when `decision` is `"block"` |
| `additionalContext` | String added to Claude’s context alongside the expanded prompt. See [Add context for Claude](#add-context-for-claude) |

```
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### [​](#messagedisplay) MessageDisplay

Runs while an assistant message streams to the screen. Claude Code displays the message in increments: each time a batch of newly completed lines is ready to render, the hook runs once with those lines and Claude Code renders the hook’s replacement text in their place. A long message produces several calls; a short message may produce only one.
Use MessageDisplay to:

* strip markdown for a minimal display
* transform the text an Agent SDK application shows its users
* redact API keys or internal hostnames from Claude’s responses

Claude Code holds each batch until your hook returns, so keep the hook fast. If the hook fails or times out, Claude Code displays the original text. The default timeout for this event is 10 seconds; if your hook needs more time, set the `timeout` field in the hook entry.
MessageDisplay is display-only: the replacement text changes only what is rendered on screen. The transcript and what Claude sees keep the original text, so Claude never sees the replacement, and verbose mode shows the original. The hook receives assistant message text only, so tool results and the text you type render unchanged.
MessageDisplay does not support matchers and fires for every assistant message that streams text; messages with no text, such as tool-call-only responses, do not trigger it.
In non-interactive runs, including Agent SDK queries and `claude -p`, MessageDisplay runs once per assistant message instead of once per batch of lines. The single call arrives after the message completes and carries the full message text: `index` is `0`, `final` is `true`, and `delta` holds the entire message. A hook that collects the `delta` text for each message receives the same total text in both modes.

#### [​](#messagedisplay-input) MessageDisplay input

In addition to the [common input fields](#common-input-fields), MessageDisplay hooks receive identifiers for the turn and message, the position of this call within the message, and the new text in `delta`. Batch boundaries depend on how the text streams, so use `index` and `final` to track progress through a message rather than expecting lines to be grouped a particular way.

| Field | Description |
| --- | --- |
| `turn_id` | UUID of the current turn |
| `message_id` | UUID of the assistant message being displayed. Stable across every batch of the same message. This is not the API `msg_…` id, so it cannot be correlated with transcript message ids |
| `index` | Zero-based index of this batch within the message |
| `final` | `true` on the message’s last batch. Each message has exactly one final batch |
| `delta` | The newly completed lines since the prior batch, terminating newlines included. Always whole lines, except the final batch which may end mid-line. In interactive runs, the final batch’s delta is empty when the message ends on a newline, so treat `final`, not a non-empty delta, as the end-of-message signal. In Agent SDK and `claude -p` runs, the single call carries the entire message |

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "MessageDisplay",
  "turn_id": "0c9e6a2f-7d41-4f4e-9a15-3f4f7c2b8d10",
  "message_id": "5b2a9c8e-1f63-4d8a-b7c4-9e0d2a6f1c3b",
  "index": 0,
  "final": false,
  "delta": "Here is the plan:\n"
}
```

#### [​](#messagedisplay-output) MessageDisplay output

In addition to the [JSON output fields](#json-output) available to all hooks, MessageDisplay hooks can return `displayContent` to replace the delta on screen:

| Field | Description |
| --- | --- |
| `displayContent` | Text displayed in place of the delta. Omit it to display the original |

MessageDisplay hooks have no decision control. They cannot block the message or change what is stored in the transcript or sent to Claude.
This example strips markdown formatting from Claude’s responses for a plain-text display. The script reads each batch from stdin, removes bold markers and inline code backticks from `delta`, and returns the result as `displayContent`.

* macOS/Linux
* Windows (PowerShell)

Register a command hook for the event in your settings file:

```
{
  "hooks": {
    "MessageDisplay": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Save this script to `.claude/hooks/plain-display.sh` in your project and make it executable with `chmod +x`:

```
#!/bin/bash
jq '{hookSpecificOutput: {hookEventName: "MessageDisplay", displayContent: (.delta | gsub("\\*\\*"; "") | gsub("`"; ""))}}'
```

The script needs `jq` on your `PATH`.

Register a command hook that runs the script through PowerShell:

```
{
  "hooks": {
    "MessageDisplay": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe",
            "args": [
              "-NoProfile",
              "-ExecutionPolicy",
              "Bypass",
              "-File",
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.ps1"
            ]
          }
        ]
      }
    ]
  }
}
```

The `-NoProfile` flag skips loading your PowerShell profile so the hook starts fast, and `-ExecutionPolicy Bypass` lets PowerShell run the local script file.Save this script to `.claude/hooks/plain-display.ps1` in your project:

```
$batch = [Console]::In.ReadToEnd() | ConvertFrom-Json
$text = $batch.delta -replace '\*\*', '' -replace '`', ''
@{
  hookSpecificOutput = @{
    hookEventName = "MessageDisplay"
    displayContent = $text
  }
} | ConvertTo-Json
```

Batches with no markdown pass through unchanged. If the script fails, for example because `jq` is missing, Claude Code displays the original text and notes the failure only in [debug output](#debug-hooks), not in the session.

### [​](#pretooluse) PreToolUse

Runs after Claude creates tool parameters and before processing the tool call. Matches on tool name: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode`, and any [MCP tool names](#match-mcp-tools).
Use [PreToolUse decision control](#pretooluse-decision-control) to allow, deny, ask, or defer the tool call.

#### [​](#pretooluse-input) PreToolUse input

In addition to the [common input fields](#common-input-fields), PreToolUse hooks receive `tool_name`, `tool_input`, and `tool_use_id`. The `tool_input` fields depend on the tool:

##### Bash

Executes shell commands.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `command` | string | `"npm test"` | The shell command to execute |
| `description` | string | `"Run test suite"` | Optional description of what the command does |
| `timeout` | number | `120000` | Optional timeout in milliseconds |
| `run_in_background` | boolean | `false` | Whether to run the command in background |

##### Write

Creates or overwrites a file.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `file_path` | string | `"/path/to/file.txt"` | Absolute path to the file to write |
| `content` | string | `"file content"` | Content to write to the file |

##### Edit

Replaces a string in an existing file.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `file_path` | string | `"/path/to/file.txt"` | Absolute path to the file to edit |
| `old_string` | string | `"original text"` | Text to find and replace |
| `new_string` | string | `"replacement text"` | Replacement text |
| `replace_all` | boolean | `false` | Whether to replace all occurrences |

##### Read

Reads file contents.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `file_path` | string | `"/path/to/file.txt"` | Absolute path to the file to read |
| `offset` | number | `10` | Optional line number to start reading from |
| `limit` | number | `50` | Optional number of lines to read |

##### Glob

Finds files matching a glob pattern.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `pattern` | string | `"**/*.ts"` | Glob pattern to match files against |
| `path` | string | `"/path/to/dir"` | Optional directory to search in. Defaults to current working directory |

##### Grep

Searches file contents with regular expressions.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `pattern` | string | `"TODO.*fix"` | Regular expression pattern to search for |
| `path` | string | `"/path/to/dir"` | Optional file or directory to search in |
| `glob` | string | `"*.ts"` | Optional glob pattern to filter files |
| `output_mode` | string | `"content"` | `"content"`, `"files_with_matches"`, or `"count"`. Defaults to `"files_with_matches"` |
| `-i` | boolean | `true` | Case insensitive search |
| `multiline` | boolean | `false` | Enable multiline matching |

##### WebFetch

Fetches and processes web content.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `url` | string | `"https://example.com/api"` | URL to fetch content from |
| `prompt` | string | `"Extract the API endpoints"` | Prompt to run on the fetched content |

##### WebSearch

Searches the web.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `query` | string | `"react hooks best practices"` | Search query |
| `allowed_domains` | array | `["docs.example.com"]` | Optional: only include results from these domains |
| `blocked_domains` | array | `["spam.example.com"]` | Optional: exclude results from these domains |

##### Agent

Spawns a [subagent](/docs/en/sub-agents).

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `prompt` | string | `"Find all API endpoints"` | The task for the agent to perform |
| `description` | string | `"Find API endpoints"` | Short description of the task |
| `subagent_type` | string | `"Explore"` | Type of specialized agent to use |
| `model` | string | `"sonnet"` | Optional model alias to override the default |

In `PostToolUse`, `tool_response` for a completed Agent call carries the subagent’s final text along with usage telemetry. Read these fields to record per-subagent cost from a hook:

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `status` | string | `"completed"` | `"completed"` for synchronous calls, `"async_launched"` for `run_in_background: true` |
| `agentId` | string | `"a4d2c8f1e0b3a297"` | Identifier for the subagent run |
| `content` | array | `[{"type": "text", "text": "Found 12 endpoints..."}]` | The subagent’s final text blocks |
| `resolvedModel` | string | `"claude-sonnet-4-5"` | Model the subagent ran on, which may differ from the requested model. Requires Claude Code v2.1.174 or later |
| `totalTokens` | number | `12450` | Total tokens billed across the subagent’s turns |
| `totalDurationMs` | number | `48211` | Wall-clock duration of the subagent run |
| `totalToolUseCount` | number | `7` | Count of tool calls the subagent made |
| `usage` | object | `{"input_tokens": 8320, ...}` | Per-type token breakdown: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` |

For `run_in_background: true` calls, the tool returns immediately after launching the subagent, so `tool_response` carries no usage fields. It has `status: "async_launched"`, `agentId`, `description`, `prompt`, `outputFile`, and `resolvedModel`.
The `resolvedModel` field names the model the subagent actually runs on, which can differ from the `model` value in `tool_input`, such as when `availableModels` or another override applies. It requires Claude Code v2.1.174 or later.


##### AskUserQuestion

Asks the user one to four multiple-choice questions.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `questions` | array | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Questions to present, each with a `question` string, short `header`, `options` array, and optional `multiSelect` flag |
| `answers` | object | `{"Which framework?": "React"}` | Optional. Maps question text to the selected option label. Multi-select answers join labels with commas. Claude does not set this field; supply it via `updatedInput` to answer programmatically |

##### ExitPlanMode

Presents a plan and asks the user to approve it before Claude leaves [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode). Claude writes the plan to a file on disk before calling the tool, so the literal `tool_input` from the model only carries `allowedPrompts`. Claude Code injects the plan content and file path before passing the input to hooks.

| Field | Type | Example | Description |
| --- | --- | --- | --- |
| `plan` | string | `"## Refactor auth\n1. Extract..."` | Plan content in Markdown. Injected from the plan file on disk |
| `planFilePath` | string | `"/Users/.../plans/refactor-auth.md"` | Path to the plan file. Injected |
| `allowedPrompts` | array | `[{"tool": "Bash", "prompt": "run tests"}]` | Optional. Prompt-based permissions Claude is requesting to implement the plan, each with a `tool` name and a `prompt` describing the category of action |

In `PostToolUse`, `tool_response` is an object with `plan` and `filePath` fields holding the approved plan, plus internal status flags. Read `tool_response.plan` for the plan content rather than re-reading the file from disk.

#### [​](#pretooluse-decision-control) PreToolUse decision control

`PreToolUse` hooks can control whether a tool call proceeds. Unlike other hooks that use a top-level `decision` field, PreToolUse returns its decision inside a `hookSpecificOutput` object. This gives it richer control: four outcomes (allow, deny, ask, or defer) plus the ability to modify tool input before execution.

| Field | Description |
| --- | --- |
| `permissionDecision` | `"allow"` skips the permission prompt. `"deny"` prevents the tool call. `"ask"` prompts the user to confirm. `"defer"` exits gracefully so the tool can be resumed later. [Deny and ask rules](/docs/en/permissions#manage-permissions) are still evaluated regardless of what the hook returns |
| `permissionDecisionReason` | For `"allow"` and `"ask"`, shown to the user but not Claude. For `"deny"`, shown to Claude. For `"defer"`, ignored |
| `updatedInput` | Modifies the tool’s input parameters before execution. Replaces the entire input object, so include unchanged fields alongside modified ones. Combine with `"allow"` to auto-approve, or `"ask"` to show the modified input to the user. For `"defer"`, ignored |
| `additionalContext` | String added to Claude’s context alongside the tool result. Ignored when `permissionDecision` is `"defer"`. See [Add context for Claude](#add-context-for-claude) |

When multiple PreToolUse hooks return different decisions, precedence is `deny` > `defer` > `ask` > `allow`.
When a hook returns `"ask"`, the permission prompt displayed to the user includes a label identifying where the hook came from: for example, `[User]`, `[Project]`, `[Plugin]`, or `[Local]`. This helps users understand which configuration source is requesting confirmation.

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` and `ExitPlanMode` require user interaction and normally block in [non-interactive mode](/docs/en/headless) with the `-p` flag. Returning `permissionDecision: "allow"` together with `updatedInput` satisfies that requirement: the hook reads the tool’s input from stdin, collects the answer through your own UI, and returns it in `updatedInput` so the tool runs without prompting. Returning `"allow"` alone is not sufficient for these tools. For `AskUserQuestion`, echo back the original `questions` array and add an [`answers`](#askuserquestion) object mapping each question’s text to the chosen answer.

PreToolUse previously used top-level `decision` and `reason` fields, but these are deprecated for this event. Use `hookSpecificOutput.permissionDecision` and `hookSpecificOutput.permissionDecisionReason` instead. The deprecated values `"approve"` and `"block"` map to `"allow"` and `"deny"` respectively. Other events like PostToolUse and Stop continue to use top-level `decision` and `reason` as their current format.

#### [​](#defer-a-tool-call-for-later) Defer a tool call for later

`"defer"` is for integrations that run `claude -p` as a subprocess and read its JSON output, such as an Agent SDK app or a custom UI built on top of Claude Code. It lets that calling process pause Claude at a tool call, collect input through its own interface, and resume where it left off. Claude Code honors this value only in [non-interactive mode](/docs/en/headless) with the `-p` flag. In interactive sessions it logs a warning and ignores the hook result.

The `defer` value requires Claude Code v2.1.89 or later. Earlier versions do not recognize it and the tool proceeds through the normal permission flow.

The `AskUserQuestion` tool is the typical case: Claude wants to ask the user something, but there is no terminal to answer in. The round trip works like this:

1. Claude calls `AskUserQuestion`. The `PreToolUse` hook fires.
2. The hook returns `permissionDecision: "defer"`. The tool does not execute. The process exits with `stop_reason: "tool_deferred"` and the pending tool call preserved in the transcript.
3. The calling process reads `deferred_tool_use` from the SDK result, surfaces the question in its own UI, and waits for an answer.
4. The calling process runs `claude -p --resume <session-id>`. The same tool call fires `PreToolUse` again.
5. The hook returns `permissionDecision: "allow"` with the answer in `updatedInput`. The tool executes and Claude continues.

The `deferred_tool_use` field carries the tool’s `id`, `name`, and `input`. The `input` is the parameters Claude generated for the tool call, captured before execution:

```
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

There is no timeout or retry limit. The session remains on disk until you resume it, subject to the [`cleanupPeriodDays`](/docs/en/settings#available-settings) retention sweep that deletes session files after 30 days by default. If the answer is not ready when you resume, the hook can return `"defer"` again and the process exits the same way. The calling process controls when to break the loop by eventually returning `"allow"` or `"deny"` from the hook.
`"defer"` only works when Claude makes a single tool call in the turn. If Claude makes several tool calls at once, `"defer"` is ignored with a warning and the tool proceeds through the normal permission flow. The constraint exists because resume can only re-run one tool: there is no way to defer one call from a batch without leaving the others unresolved.
If the deferred tool is no longer available when you resume, the process exits with `stop_reason: "tool_deferred_unavailable"` and `is_error: true` before the hook fires. This happens when an MCP server that provided the tool is not connected for the resumed session. The `deferred_tool_use` payload is still included so you can identify which tool went missing.

`--resume` restores the permission mode that was active when the tool was deferred, so you do not need to pass `--permission-mode` again. The exceptions are `plan` and `bypassPermissions`, which are never carried over. Passing `--permission-mode` explicitly on resume overrides the restored value.

### [​](#permissionrequest) PermissionRequest

Runs when the user is shown a permission dialog.
Use [PermissionRequest decision control](#permissionrequest-decision-control) to allow or deny on behalf of the user.
Matches on tool name, same values as PreToolUse.

#### [​](#permissionrequest-input) PermissionRequest input

PermissionRequest hooks receive `tool_name` and `tool_input` fields like PreToolUse hooks, but without `tool_use_id`. An optional `permission_suggestions` array contains the “always allow” options the user would normally see in the permission dialog. The difference is when the hook fires: PermissionRequest hooks run when a permission dialog is about to be shown to the user, while PreToolUse hooks run before tool execution regardless of permission status.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### [​](#permissionrequest-decision-control) PermissionRequest decision control

`PermissionRequest` hooks can allow or deny permission requests. In addition to the [JSON output fields](#json-output) available to all hooks, your hook script can return a `decision` object with these event-specific fields:

| Field | Description |
| --- | --- |
| `behavior` | `"allow"` grants the permission, `"deny"` denies it. [Deny and ask rules](/docs/en/permissions#manage-permissions) are still evaluated, so a hook returning `"allow"` does not override a matching deny rule |
| `updatedInput` | For `"allow"` only: modifies the tool’s input parameters before execution. Replaces the entire input object, so include unchanged fields alongside modified ones. The modified input is re-evaluated against deny and ask rules |
| `updatedPermissions` | For `"allow"` only: array of [permission update entries](#permission-update-entries) to apply, such as adding an allow rule or changing the session permission mode |
| `message` | For `"deny"` only: tells Claude why the permission was denied |
| `interrupt` | For `"deny"` only: if `true`, stops Claude |

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

#### [​](#permission-update-entries) Permission update entries

The `updatedPermissions` output field and the [`permission_suggestions` input field](#permissionrequest-input) both use the same array of entry objects. Each entry has a `type` that determines its other fields, and a `destination` that controls where the change is written.

| `type` | Fields | Effect |
| --- | --- | --- |
| `addRules` | `rules`, `behavior`, `destination` | Adds permission rules. `rules` is an array of `{toolName, ruleContent?}` objects. Omit `ruleContent` to match the whole tool. `behavior` is `"allow"`, `"deny"`, or `"ask"` |
| `replaceRules` | `rules`, `behavior`, `destination` | Replaces all rules of the given `behavior` at the `destination` with the provided `rules` |
| `removeRules` | `rules`, `behavior`, `destination` | Removes matching rules of the given `behavior` |
| `setMode` | `mode`, `destination` | Changes the permission mode. Valid modes are `default`, `auto`, `acceptEdits`, `dontAsk`, `bypassPermissions`, and `plan` |
| `addDirectories` | `directories`, `destination` | Adds working directories. `directories` is an array of path strings |
| `removeDirectories` | `directories`, `destination` | Removes working directories |

`setMode` with `bypassPermissions` only takes effect if the session was launched with bypass mode already available: `--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions`, or `permissions.defaultMode: "bypassPermissions"` in settings, and the mode is not disabled by [`permissions.disableBypassPermissionsMode`](/docs/en/permissions#managed-settings). Otherwise the update is a no-op. `bypassPermissions` is never persisted as `defaultMode` regardless of `destination`.

The `destination` field on every entry determines whether the change stays in memory or persists to a settings file.

| `destination` | Writes to |
| --- | --- |
| `session` | in-memory only, discarded when the session ends |
| `localSettings` | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json` |
| `userSettings` | `~/.claude/settings.json` |

A hook can echo one of the `permission_suggestions` it received as its own `updatedPermissions` output, which is equivalent to the user selecting that “always allow” option in the dialog.

### [​](#posttooluse) PostToolUse

Runs immediately after a tool completes successfully.
Matches on tool name, same values as PreToolUse.

#### [​](#posttooluse-input) PostToolUse input

`PostToolUse` hooks fire after a tool has already executed successfully. The input includes both `tool_input`, the arguments sent to the tool, and `tool_response`, the result it returned. The exact schema for both depends on the tool.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| Field | Description |
| --- | --- |
| `duration_ms` | Optional. Tool execution time in milliseconds. Excludes time spent in permission prompts and PreToolUse hooks |

#### [​](#posttooluse-decision-control) PostToolUse decision control

`PostToolUse` hooks can provide feedback to Claude after tool execution. In addition to the [JSON output fields](#json-output) available to all hooks, your hook script can return these event-specific fields:

| Field | Description |
| --- | --- |
| `decision` | `"block"` adds the `reason` next to the tool result. Claude still sees the original output; to replace it, use `updatedToolOutput` |
| `reason` | Explanation shown to Claude when `decision` is `"block"` |
| `additionalContext` | String added to Claude’s context alongside the tool result. See [Add context for Claude](#add-context-for-claude) |
| `updatedToolOutput` | Replaces the tool’s output with the provided value before it is sent to Claude. The value must match the tool’s output shape |
| `updatedMCPToolOutput` | Replaces the output for [MCP tools](#match-mcp-tools) only. Prefer `updatedToolOutput`, which works for all tools |

The example below replaces the output of a `Bash` call. The replacement value matches the `Bash` tool’s output shape:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

`updatedToolOutput` only changes what Claude sees. The tool has already run by the time the hook fires, so any files written, commands executed, or network requests sent have already taken effect. Telemetry such as OpenTelemetry tool spans and analytics events also captures the original output before the hook runs. To prevent or modify a tool call before it runs, use a [PreToolUse](#pretooluse) hook instead.The replacement value must match the tool’s output shape. Built-in tools return structured objects rather than plain strings. For example, `Bash` returns an object with `stdout`, `stderr`, `interrupted`, and `isImage` fields. For built-in tools, a value that does not match the tool’s output schema is ignored and the original output is used. MCP tool output is passed through without schema validation. Stripping error details that Claude needs can cause it to proceed on a false assumption.

### [​](#posttoolusefailure) PostToolUseFailure

Runs when a tool execution fails. This event fires for tool calls that throw errors or return failure results. Use this to log failures, send alerts, or provide corrective feedback to Claude.
Matches on tool name, same values as PreToolUse.

#### [​](#posttoolusefailure-input) PostToolUseFailure input

PostToolUseFailure hooks receive the same `tool_name` and `tool_input` fields as PostToolUse, along with error information as top-level fields:

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| Field | Description |
| --- | --- |
| `error` | String describing what went wrong |
| `is_interrupt` | Optional boolean indicating whether the failure was caused by user interruption |
| `duration_ms` | Optional. Tool execution time in milliseconds. Excludes time spent in permission prompts and PreToolUse hooks |

#### [​](#posttoolusefailure-decision-control) PostToolUseFailure decision control

`PostToolUseFailure` hooks can provide context to Claude after a tool failure. In addition to the [JSON output fields](#json-output) available to all hooks, your hook script can return these event-specific fields:

| Field | Description |
| --- | --- |
| `additionalContext` | String added to Claude’s context alongside the error. See [Add context for Claude](#add-context-for-claude) |

```
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### [​](#posttoolbatch) PostToolBatch

Runs once after every tool call in a batch has resolved, before Claude Code sends the next request to the model. `PostToolUse` fires once per tool, which means it fires concurrently when Claude makes parallel tool calls. `PostToolBatch` fires exactly once with the full batch, so it is the right place to inject context that depends on the set of tools that ran rather than on any single tool. There is no matcher for this event.

#### [​](#posttoolbatch-input) PostToolBatch input

In addition to the [common input fields](#common-input-fields), PostToolBatch hooks receive `tool_calls`, an array describing every tool call in the batch:

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    }
  ]
}
```

`tool_response` contains the same content the model receives in the corresponding `tool_result` block. The value is a serialized string or content-block array, exactly as the tool emitted it. For `Read`, that means line-number-prefixed text rather than raw file contents. Responses can be large, so parse only the fields you need.

The `tool_response` shape differs from `PostToolUse`’s. `PostToolUse` passes the tool’s structured `Output` object, such as `{filePath: "...", success: true}` for `Write`; `PostToolBatch` passes the serialized `tool_result` content the model sees.

#### [​](#posttoolbatch-decision-control) PostToolBatch decision control

`PostToolBatch` hooks can inject context for Claude. In addition to the [JSON output fields](#json-output) available to all hooks, your hook script can return these event-specific fields:

| Field | Description |
| --- | --- |
| `additionalContext` | Context string injected once before the next model call. See [Add context for Claude](#add-context-for-claude) for delivery details, what to put in it, and how resumed sessions handle past values |

```
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

Returning `decision: "block"` or `continue: false` stops the agentic loop before the next model call.

### [​](#permissiondenied) PermissionDenied

Runs when the [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) classifier denies a tool call. This hook only fires in auto mode: it does not run when you manually deny a permission dialog, when a `PreToolUse` hook blocks a call, or when a `deny` rule matches. Use it to log classifier denials, adjust configuration, or tell the model it may retry the tool call.
Matches on tool name, same values as PreToolUse.

#### [​](#permissiondenied-input) PermissionDenied input

In addition to the [common input fields](#common-input-fields), PermissionDenied hooks receive `tool_name`, `tool_input`, `tool_use_id`, and `reason`.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Field | Description |
| --- | --- |
| `reason` | The classifier’s explanation for why the tool call was denied |

#### [​](#permissiondenied-decision-control) PermissionDenied decision control

PermissionDenied hooks can tell the model it may retry the denied tool call. Return a JSON object with `hookSpecificOutput.retry` set to `true`:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

When `retry` is `true`, Claude Code adds a message to the conversation telling the model it may retry the tool call. The denial itself is not reversed. If your hook does not return JSON, or returns `retry: false`, the denial stands and the model receives the original rejection message.

### [​](#notification) Notification

Runs when Claude Code sends notifications. Matches on notification type: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`. Omit the matcher to run hooks for all notification types.
Use separate matchers to run different handlers depending on the notification type. This configuration triggers a permission-specific alert script when Claude needs permission approval and a different notification when Claude has been idle:

```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### [​](#notification-input) Notification input

In addition to the [common input fields](#common-input-fields), Notification hooks receive `message` with the notification text, an optional `title`, and `notification_type` indicating which type fired.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification hooks cannot block or modify notifications. They are intended for side effects such as forwarding the notification to an external service. The [common JSON output fields](#json-output) such as `systemMessage` apply.

### [​](#subagentstart) SubagentStart

Runs when a Claude Code subagent is spawned via the Agent tool. Supports matchers to filter by agent type name. For built-in agents, this is the agent name like `general-purpose`, `Explore`, or `Plan`. For [custom subagents](/docs/en/sub-agents), this is the `name` field from the agent’s frontmatter, not the filename.

#### [​](#subagentstart-input) SubagentStart input

In addition to the [common input fields](#common-input-fields), SubagentStart hooks receive `agent_id` with the unique identifier for the subagent and `agent_type` with the agent name (built-in agents like `"general-purpose"`, `"Explore"`, `"Plan"`, or custom agent names).

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart hooks cannot block subagent creation, but they can inject context into the subagent. In addition to the [JSON output fields](#json-output) available to all hooks, you can return:

| Field | Description |
| --- | --- |
| `additionalContext` | String added to the subagent’s context at the start of its conversation, before its first prompt. See [Add context for Claude](#add-context-for-claude) |

```
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### [​](#subagentstop) SubagentStop

Runs when a Claude Code subagent has finished responding. Matches on agent type, same values as SubagentStart.

#### [​](#subagentstop-input) SubagentStop input

In addition to the [common input fields](#common-input-fields), SubagentStop hooks receive `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, and `last_assistant_message`. The `agent_type` field is the value used for matcher filtering. The `transcript_path` is the main session’s transcript, while `agent_transcript_path` is the subagent’s own transcript stored in a nested `subagents/` folder. The `last_assistant_message` field contains the text content of the subagent’s final response, so hooks can access it without parsing the transcript file.
SubagentStop hooks also receive the `background_tasks` and `session_crons` arrays described under [Stop input](#stop-input), available in Claude Code v2.1.145 or later. Both arrays are scoped to the parent session, not the subagent.

```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues...",
  "background_tasks": [],
  "session_crons": []
}
```

SubagentStop hooks use the same decision control format as [Stop hooks](#stop-decision-control), including `hookSpecificOutput.additionalContext` with `hookEventName` set to `"SubagentStop"`, for non-error feedback that keeps the subagent running. Returning `decision: "block"` with a `reason` keeps the subagent running and delivers `reason` to the subagent as its next instruction. To inject context into the parent session after a subagent returns, use a [`PostToolUse`](#posttooluse) hook on the `Agent` tool instead.

### [​](#taskcreated) TaskCreated

Runs when a task is being created via the `TaskCreate` tool. Use this to enforce naming conventions, require task descriptions, or prevent certain tasks from being created.
When a `TaskCreated` hook exits with code 2, the task is not created and the stderr message is fed back to the model as feedback. To stop the teammate entirely instead of re-running it, return JSON with `{"continue": false, "stopReason": "..."}`. TaskCreated hooks do not support matchers and fire on every occurrence.

#### [​](#taskcreated-input) TaskCreated input

In addition to the [common input fields](#common-input-fields), TaskCreated hooks receive `task_id`, `task_subject`, and optionally `task_description`, `teammate_name`, and `team_name`.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| Field | Description |
| --- | --- |
| `task_id` | Identifier of the task being created |
| `task_subject` | Title of the task |
| `task_description` | Detailed description of the task. May be absent |
| `teammate_name` | Name of the teammate creating the task. May be absent |
| `team_name` | Deprecated. Session-derived team name; will be removed in a future release |

#### [​](#taskcreated-decision-control) TaskCreated decision control

TaskCreated hooks support two ways to control task creation:

* **Exit code 2**: the task is not created and the stderr message is fed back to the model as feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: stops the teammate entirely, matching `Stop` hook behavior. The `stopReason` is shown to the user.

This example blocks tasks whose subjects don’t follow the required format:

```
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### [​](#taskcompleted) TaskCompleted

Runs when a task is being marked as completed. This fires in two situations: when any agent explicitly marks a task as completed through the TaskUpdate tool, or when an [agent team](/docs/en/agent-teams) teammate finishes its turn with in-progress tasks. Use this to enforce completion criteria like passing tests or lint checks before a task can close.
When a `TaskCompleted` hook exits with code 2, the task is not marked as completed and the stderr message is fed back to the model as feedback. To stop the teammate entirely instead of re-running it, return JSON with `{"continue": false, "stopReason": "..."}`. TaskCompleted hooks do not support matchers and fire on every occurrence.

#### [​](#taskcompleted-input) TaskCompleted input

In addition to the [common input fields](#common-input-fields), TaskCompleted hooks receive `task_id`, `task_subject`, and optionally `task_description`, `teammate_name`, and `team_name`.

```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| Field | Description |
| --- | --- |
| `task_id` | Identifier of the task being completed |
| `task_subject` | Title of the task |
| `task_description` | Detailed description of the task. May be absent |
| `teammate_name` | Name of the teammate completing the task. May be absent |
| `team_name` | Deprecated. Session-derived team name; will be removed in a future release |

#### [​](#taskcompleted-decision-control) TaskCompleted decision control

TaskCompleted hooks support two ways to control task completion:

* **Exit code 2**: the task is not marked as completed and the stderr message is fed back to the model as feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: stops the teammate entirely, matching `Stop` hook behavior. The `stopReason` is shown to the user.

This example runs tests and blocks task completion if they fail:

```
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')