---
title: .claude/hooks/block-rm.sh
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # no decision; normal permission flow applies
fi
```

Now suppose Claude Code decides to run `Bash "rm -rf /tmp/build"`. Here’s what happens:

![Diagram of hook resolution: PreToolUse fires, the matcher checks for a Bash match, then the if condition checks for a Bash(rm *) match. If both match, the hook command runs and returns permissionDecision deny, so the tool call is blocked and Claude Code continues. If either check fails to match, the hook is skipped and the tool call is allowed to proceed.](https://mintcdn.com/claude-code/ikqp3_70mqIahteV/images/hook-resolution.svg?fit=max&auto=format&n=ikqp3_70mqIahteV&q=85&s=be0bf3053550c26de5f54cd64674c197)

1

Event fires

The `PreToolUse` event fires. Claude Code sends the tool input as JSON on stdin to the hook:

```
{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
```

2

Matcher checks

The matcher `"Bash"` matches the tool name, so this hook group activates. If you omit the matcher or use `"*"`, the group activates on every occurrence of the event.

3

If condition checks

The `if` condition `"Bash(rm *)"` matches because `rm -rf /tmp/build` is a subcommand matching `rm *`, so this handler spawns. If the command had been `npm test`, the `if` check would fail and `block-rm.sh` would never run, avoiding the process spawn overhead. The `if` field is optional; without it, every handler in the matched group runs.

4

Hook handler runs

The script inspects the full command and finds `rm -rf`, so it prints a decision to stdout:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

If the command had been a safer `rm` variant like `rm file.txt`, the script would hit `exit 0` instead. Exit code 0 with no output means the hook has no decision to report, so the tool call continues through the normal [permission flow](/docs/en/permissions). The hook can deny the call, but staying silent doesn’t approve it.

5

Claude Code acts on the result

Claude Code reads the JSON decision, blocks the tool call, and shows Claude the reason.

The [Configuration](#configuration) section below documents the full schema, and each [hook event](#hook-events) section documents what input your command receives and what output it can return.

## [​](#configuration) Configuration

Hooks are defined in JSON settings files. The configuration has three levels of nesting:

1. Choose a [hook event](#hook-events) to respond to, like `PreToolUse` or `Stop`
2. Add a [matcher group](#matcher-patterns) to filter when it fires, like “only for the Bash tool”
3. Define one or more [hook handlers](#hook-handler-fields) to run when matched

See [How a hook resolves](#how-a-hook-resolves) above for a complete walkthrough with an annotated example.

This page uses specific terms for each level: **hook event** for the lifecycle point, **matcher group** for the filter, and **hook handler** for the shell command, HTTP endpoint, MCP tool, prompt, or agent that runs. “Hook” on its own refers to the general feature.

### [​](#hook-locations) Hook locations

Where you define a hook determines its scope:

| Location | Scope | Shareable |
| --- | --- | --- |
| `~/.claude/settings.json` | All your projects | No, local to your machine |
| `.claude/settings.json` | Single project | Yes, can be committed to the repo |
| `.claude/settings.local.json` | Single project | No, gitignored when Claude Code creates it |
| Managed policy settings | Organization-wide | Yes, admin-controlled |
| [Plugin](/docs/en/plugins) `hooks/hooks.json` | When plugin is enabled | Yes, bundled with the plugin |
| [Skill](/docs/en/skills) or [agent](/docs/en/sub-agents) frontmatter | While the component is active | Yes, defined in the component file |

For details on settings file resolution, see [settings](/docs/en/settings). Enterprise administrators can use `allowManagedHooksOnly` to block user, project, and plugin hooks. Hooks from plugins force-enabled in managed settings `enabledPlugins` are exempt, so administrators can distribute vetted hooks through an organization marketplace. See [Hook configuration](/docs/en/settings#hook-configuration).

### [​](#matcher-patterns) Matcher patterns

The `matcher` field filters when hooks fire. How a matcher is evaluated depends on the characters it contains:

| Matcher value | Evaluated as | Example |
| --- | --- | --- |
| `"*"`, `""`, or omitted | Match all | fires on every occurrence of the event |
| Only letters, digits, `_`, spaces, `,`, and `|` | Exact string, or list of exact strings separated by `|` or `,` with optional surrounding whitespace | `Bash` matches only the Bash tool; `Edit|Write` and `Edit, Write` each match either tool exactly |
| Contains any other character | JavaScript regular expression | `^Notebook` matches any tool starting with Notebook; `mcp__memory__.*` matches every tool from the `memory` server |

Comma separators and the surrounding whitespace tolerance require Claude Code v2.1.191 or later. The `FileChanged` and `StopFailure` events accept only `|` as the list separator and treat `,` as a literal character; all other events listed in the table that follows accept `|` or `,`.
The `FileChanged` event does not follow these rules when building its watch list. See [FileChanged](#filechanged).
Each event type matches on a different field:

| Event | What the matcher filters | Example matcher values |
| --- | --- | --- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name | `Bash`, `Edit|Write`, `mcp__.*` |
| `SessionStart` | how the session started | `startup`, `resume`, `clear`, `compact` |
| `Setup` | which CLI flag triggered setup | `init`, `maintenance` |
| `SessionEnd` | why the session ended | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response` |
| `SubagentStart` | agent type | `general-purpose`, `Explore`, `Plan`, or custom agent names |
| `PreCompact`, `PostCompact` | what triggered compaction | `manual`, `auto` |
| `SubagentStop` | agent type | same values as `SubagentStart` |
| `ConfigChange` | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `CwdChanged` | no matcher support | always fires on every directory change |
| `FileChanged` | literal filenames to watch (see [FileChanged](#filechanged)) | `.envrc|.env` |
| `StopFailure` | error type | `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded` | load reason | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `UserPromptExpansion` | command name | your skill or command names |
| `Elicitation` | MCP server name | your configured MCP server names |
| `ElicitationResult` | MCP server name | same values as `Elicitation` |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `MessageDisplay` | no matcher support | always fires on every occurrence |

The matcher runs against a field from the [JSON input](#hook-input-and-output) that Claude Code sends to your hook on stdin. For tool events, that field is `tool_name`. Each [hook event](#hook-events) section lists the full set of matcher values and the input schema for that event.
This example runs a linting script only when Claude writes or edits a file:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, and `CwdChanged` don’t support matchers and always fire on every occurrence. If you add a `matcher` field to these events, it is silently ignored.
For tool events, you can filter more narrowly by setting the [`if` field](#common-fields) on individual hook handlers. `if` uses [permission rule syntax](/docs/en/permissions) to match against the tool name and arguments together, so `"Bash(git *)"` runs when any subcommand of the Bash input matches `git *` and `"Edit(*.ts)"` runs only for TypeScript files.

#### [​](#match-mcp-tools) Match MCP tools

[MCP](/docs/en/mcp) server tools appear as regular tools in tool events (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), so you can match them the same way you match any other tool name.
MCP tools follow the naming pattern `mcp__<server>__<tool>`, for example:

* `mcp__memory__create_entities`: Memory server’s create entities tool
* `mcp__filesystem__read_file`: Filesystem server’s read file tool
* `mcp__github__search_repositories`: GitHub server’s search tool

To match every tool from a server, append `.*` to the server prefix. The `.*` is required: a matcher like `mcp__memory` contains only letters and underscores, so it is compared as an exact string and matches no tool.

* `mcp__memory__.*` matches all tools from the `memory` server
* `mcp__.*__write.*` matches any tool whose name starts with `write` from any server

This example logs all memory server operations and validates write operations from any MCP server:

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### [​](#hook-handler-fields) Hook handler fields

Each object in the inner `hooks` array is a hook handler: the shell command, HTTP endpoint, MCP tool, LLM prompt, or agent that runs when the matcher matches. There are five types:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): run a shell command. Your script receives the event’s [JSON input](#hook-input-and-output) on stdin and communicates results back through exit codes and stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): send the event’s JSON input as an HTTP POST request to a URL. The endpoint communicates results back through the response body using the same [JSON output format](#json-output) as command hooks.
* **[MCP tool hooks](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): call a tool on an already-connected [MCP server](/docs/en/mcp). The tool’s text output is treated like command-hook stdout.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): send a prompt to a Claude model for single-turn evaluation. The model returns a yes/no decision as JSON. See [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): spawn a subagent that can use tools like Read, Grep, and Glob to verify conditions before returning a decision. Agent hooks are experimental and may change. See [Agent-based hooks](#agent-based-hooks).

All matching hooks run in parallel, and identical handlers are deduplicated automatically. Command hooks are deduplicated by command string and `args`, and HTTP hooks are deduplicated by URL.
Handlers run in the current directory with Claude Code’s environment. The `$CLAUDE_CODE_REMOTE` environment variable is set to `"true"` in remote web environments and not set in the local CLI.

#### [​](#common-fields) Common fields

These fields apply to all hook types:

| Field | Required | Description |
| --- | --- | --- |
| `type` | yes | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"`, or `"agent"` |
| `if` | no | Permission rule syntax to filter when this hook runs, such as `"Bash(git *)"` or `"Edit(*.ts)"`. The hook command only runs if the tool call matches the pattern. See the [Bash matching table](#bash-if-matching) below for how Bash patterns evaluate against subcommands, `$()`, and backticks. Only evaluated on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, and `PermissionDenied`. On other events, a hook with `if` set never runs. Uses the same syntax as [permission rules](/docs/en/permissions) |
| `timeout` | no | Seconds before canceling. Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`. [`UserPromptSubmit`](#userpromptsubmit) lowers the `command`, `http`, and `mcp_tool` default to 30, and [`MessageDisplay`](#messagedisplay) lowers it to 10 |
| `statusMessage` | no | Custom spinner message displayed while the hook runs |
| `once` | no | If `true`, runs once per session then is removed. Only honored for hooks declared in [skill frontmatter](#hooks-in-skills-and-agents); ignored in settings files and agent frontmatter |

The `if` field holds exactly one permission rule. There is no `&&`, `||`, or list syntax for combining rules; to apply multiple conditions, define a separate hook handler for each.
For Bash patterns, whether your hook command runs depends on the shape of the pattern and the Bash command Claude is invoking. Leading `VAR=value` assignments are stripped before matching.

| `if` pattern | Bash command | Hook runs? | Why |
| --- | --- | --- | --- |
| `Bash(git *)` | `FOO=bar git push` | yes | leading assignments are stripped; `git push` matches |
| `Bash(git *)` | `npm test && git push` | yes | each subcommand is checked; `git push` matches |
| `Bash(rm *)` | `echo $(rm -rf /)` | yes | commands inside `$()` and backticks are checked; `rm -rf /` matches |
| `Bash(rm *)` | `echo $(date)` | no | no subcommand matches `rm *` |
| `Bash(git push *)` | `echo $(date)` | yes | patterns that specify more than the command name run the hook anyway on `$()`, backticks, or `$VAR` |

The filter also fails open, running your hook regardless of pattern, when the Bash command cannot be parsed. Because the `if` filter is best-effort, use the [permission system](/docs/en/permissions) rather than a hook to enforce a hard allow or deny.

#### [​](#command-hook-fields) Command hook fields

In addition to the [common fields](#common-fields), command hooks accept these fields:

| Field | Required | Description |
| --- | --- | --- |
| `command` | yes | Shell command to execute. With `args`, the executable to spawn directly. See [Exec form and shell form](#exec-form-and-shell-form) |
| `args` | no | Argument list. When present, `command` is resolved as an executable and spawned directly with `args` as the argument vector, with no shell involved. See [Exec form and shell form](#exec-form-and-shell-form) |
| `async` | no | If `true`, runs in the background without blocking. See [Run hooks in the background](#run-hooks-in-the-background) |
| `asyncRewake` | no | If `true`, runs in the background and wakes Claude on exit code 2. Implies `async`. The hook’s stderr, or stdout if stderr is empty, is shown to Claude as a system reminder so it can react to a long-running background failure |
| `shell` | no | Shell to use for this hook. Accepts `"bash"` (default) or `"powershell"`. Setting `"powershell"` runs the command via PowerShell on Windows. Does not require `CLAUDE_CODE_USE_POWERSHELL_TOOL` since hooks spawn PowerShell directly. Ignored when `args` is set |

##### Exec form and shell form

A command hook runs as exec form when `args` is set, and shell form when `args` is omitted. Set `args` whenever the hook references a [path placeholder](#reference-scripts-by-path), since each element is passed as one argument with no quoting. Omit `args` when you need shell features like pipes or `&&`, or when neither concern applies.
**Exec form** runs when `args` is present. Claude Code resolves `command` as an executable on `PATH` and spawns it directly with `args` as the argument vector. There is no shell, so each `args` element is one argument exactly as written, and path placeholders like `${CLAUDE_PLUGIN_ROOT}` are substituted into `command` and into each `args` element as plain strings. Special characters such as apostrophes, `$`, and backticks pass through verbatim because there is no shell to interpret them. No shell tokenization happens on any platform.
**Shell form** runs when `args` is absent. The `command` string is passed to a shell: `sh -c` on macOS and Linux, Git Bash on Windows, or PowerShell when Git Bash isn’t installed. Set the `shell` field to choose explicitly. The shell tokenizes the string, expands variables, and interprets pipes, `&&`, redirects, and globs.

On Windows, exec form requires `command` to resolve to a real executable such as a `.exe`. The `.cmd` and `.bat` shims that npm, npx, eslint, and other tools install in `node_modules/.bin` are not executables and cannot be spawned without a shell. To run them in exec form, invoke the underlying script with `node` directly, for example `"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/node_modules/eslint/bin/eslint.js"]`. The `node` plus script-path pattern works on every platform because `node.exe` is a real binary. To run a `.cmd` or `.bat` shim by name, use shell form.

This example runs a Node script bundled with a plugin. Exec form passes the resolved script path as one argument with no quoting:

```
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

The equivalent shell form needs quoting to handle paths with spaces or special characters:

```
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

Both forms support the same [path placeholders](#reference-scripts-by-path), and both export them as the environment variables `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`, and `CLAUDE_PLUGIN_DATA` on the spawned process, so a script can read `process.env.CLAUDE_PLUGIN_ROOT` regardless of how it was launched. Plugin hooks additionally substitute `${user_config.*}` values; see [User configuration](/docs/en/plugins-reference#user-configuration).

In exec form, `command` is the executable name or path only. If `command` is a bare name with no path separator and contains whitespace alongside `args`, Claude Code logs a warning because the spawn will fail: there is no executable named `node script.js`. Move the extra tokens into `args`. Absolute paths with spaces, such as `C:\Program Files\nodejs\node.exe`, are a single valid executable and do not trigger the warning.

#### [​](#http-hook-fields) HTTP hook fields

In addition to the [common fields](#common-fields), HTTP hooks accept these fields:

| Field | Required | Description |
| --- | --- | --- |
| `url` | yes | URL to send the POST request to |
| `headers` | no | Additional HTTP headers as key-value pairs. Values support environment variable interpolation using `$VAR_NAME` or `${VAR_NAME}` syntax. Only variables listed in `allowedEnvVars` are resolved |
| `allowedEnvVars` | no | List of environment variable names that may be interpolated into header values. References to unlisted variables are replaced with empty strings. Required for any env var interpolation to work |

Claude Code sends the hook’s [JSON input](#hook-input-and-output) as the POST request body with `Content-Type: application/json`. The response body uses the same [JSON output format](#json-output) as command hooks.
Error handling differs from command hooks: non-2xx responses, connection failures, and timeouts all produce non-blocking errors that allow execution to continue. To block a tool call or deny a permission, return a 2xx response with a JSON body containing `decision: "block"` or a `hookSpecificOutput` with `permissionDecision: "deny"`.
This example sends `PreToolUse` events to a local validation service, authenticating with a token from the `MY_TOKEN` environment variable:

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### [​](#mcp-tool-hook-fields) MCP tool hook fields

In addition to the [common fields](#common-fields), MCP tool hooks accept these fields:

| Field | Required | Description |
| --- | --- | --- |
| `server` | yes | Name of a configured MCP server. The server must already be connected; the hook never triggers an OAuth or connection flow |
| `tool` | yes | Name of the tool to call on that server |
| `input` | no | Arguments passed to the tool. String values support `${path}` substitution from the hook’s [JSON input](#hook-input-and-output), such as `"${tool_input.file_path}"` |

The tool’s text content is treated like command-hook stdout: if it parses as valid [JSON output](#json-output) it is processed as a decision, otherwise it is shown as plain text. If the named server is not connected, or the tool returns `isError: true`, the hook produces a non-blocking error and execution continues.
MCP tool hooks are available on every hook event once Claude Code has connected to your MCP servers. `SessionStart` and `Setup` typically fire before servers finish connecting, so hooks on those events should expect the “not connected” error on first run.
This example calls the `security_scan` tool on the `my_server` MCP server after each `Write` or `Edit`, passing the edited file’s path:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

#### [​](#prompt-and-agent-hook-fields) Prompt and agent hook fields

In addition to the [common fields](#common-fields), prompt and agent hooks accept these fields:

| Field | Required | Description |
| --- | --- | --- |
| `prompt` | yes | Prompt text to send to the model. Use `$ARGUMENTS` as a placeholder for the hook input JSON. Escape with a backslash to include literal text: `\$1.00` renders as `$1.00` |
| `model` | no | Model to use for evaluation. Defaults to a fast model |

### [​](#reference-scripts-by-path) Reference scripts by path

Use these placeholders to reference hook scripts relative to the project or plugin root, regardless of the working directory when the hook runs:

* `${CLAUDE_PROJECT_DIR}`: the project root. Claude Code also sets this variable in the environment of [stdio MCP servers](/docs/en/mcp#option-3-add-a-local-stdio-server) and plugin LSP servers.
* `${CLAUDE_PLUGIN_ROOT}`: the plugin’s installation directory, for scripts bundled with a [plugin](/docs/en/plugins). Changes on each plugin update.
* `${CLAUDE_PLUGIN_DATA}`: the plugin’s [persistent data directory](/docs/en/plugins-reference#persistent-data-directory), for dependencies and state that should survive plugin updates.

Prefer [exec form](#exec-form-and-shell-form) for any hook that references a path placeholder. Exec form passes each `args` element as one argument with no shell tokenization, so paths with spaces or special characters need no quoting. In shell form, wrap each placeholder in double quotes.

* Project scripts
* Plugin scripts

This example uses `${CLAUDE_PROJECT_DIR}` to run a style checker from the project’s `.claude/hooks/` directory after any `Write` or `Edit` tool call:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Define plugin hooks in `hooks/hooks.json` with an optional top-level `description` field. When a plugin is enabled, its hooks merge with your user and project hooks.This example runs a formatting script bundled with the plugin:

```
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "args": [],
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

See the [plugin components reference](/docs/en/plugins-reference#hooks) for details on creating plugin hooks.

### [​](#hooks-in-skills-and-agents) Hooks in skills and agents

In addition to settings files and plugins, hooks can be defined directly in [skills](/docs/en/skills) and [subagents](/docs/en/sub-agents) using frontmatter. These hooks are scoped to the component’s lifecycle and only run when that component is active.
All hook events are supported. For subagents, `Stop` hooks are automatically converted to `SubagentStop` since that is the event that fires when a subagent completes.
Hooks use the same configuration format as settings-based hooks but are scoped to the component’s lifetime and cleaned up when it finishes.
This skill defines a `PreToolUse` hook that runs a security validation script before each `Bash` command:

```
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Agents use the same format in their YAML frontmatter.

### [​](#the-/hooks-menu) The `/hooks` menu

Type `/hooks` in Claude Code to open a read-only browser for your configured hooks. The menu shows every hook event with a count of configured hooks, lets you drill into matchers, and shows the full details of each hook handler. Use it to verify configuration, check which settings file a hook came from, or inspect a hook’s command, prompt, or URL.
The menu displays all five hook types: `command`, `prompt`, `agent`, `http`, and `mcp_tool`. Each hook is labeled with a `[type]` prefix and a source indicating where it was defined:

* `User`: from `~/.claude/settings.json`
* `Project`: from `.claude/settings.json`
* `Local`: from `.claude/settings.local.json`
* `Plugin`: from a plugin’s `hooks/hooks.json`
* `Session`: registered in memory for the current session
* `Built-in`: registered internally by Claude Code

Selecting a hook opens a detail view showing its event, matcher, type, source file, and the full command, prompt, or URL. The menu is read-only: to add, modify, or remove hooks, edit the settings JSON directly or ask Claude to make the change.

### [​](#disable-or-remove-hooks) Disable or remove hooks

To remove a hook, delete its entry from the settings JSON file.
To temporarily disable all hooks without removing them, set `"disableAllHooks": true` in your settings file. There is no way to disable an individual hook while keeping it in the configuration.
The `disableAllHooks` setting respects the managed settings hierarchy. If an administrator has configured hooks through managed policy settings, `disableAllHooks` set in user, project, or local settings cannot disable those managed hooks. Only `disableAllHooks` set at the managed settings level can disable managed hooks.
Direct edits to hooks in settings files are normally picked up automatically by the file watcher.

## [​](#hook-input-and-output) Hook input and output

Command hooks receive JSON data via stdin and communicate results through exit codes, stdout, and stderr. HTTP hooks receive the same JSON as the POST request body and communicate results through the HTTP response body. This section covers fields and behavior common to all events. Each event’s section under [Hook events](#hook-events) includes its specific input schema and decision control options.
On macOS and Linux, command hooks run in their own session without a controlling terminal as of v2.1.139. The hook process and any child processes cannot open `/dev/tty` or send escape sequences directly to the Claude Code interface. Windows has no `/dev/tty`. To surface a message to the user on any platform, return [`systemMessage`](#json-output) in JSON output. To trigger a desktop notification, set a window title, or ring the bell, return [`terminalSequence`](#emit-terminal-notifications) instead.

### [​](#common-input-fields) Common input fields

Hook events receive these fields as JSON, in addition to event-specific fields documented in each [hook event](#hook-events) section. For command hooks, this JSON arrives via stdin. For HTTP hooks, it arrives as the POST request body.

| Field | Description |
| --- | --- |
| `session_id` | Current session identifier |
| `transcript_path` | Path to conversation JSON |
| `cwd` | Current working directory when the hook is invoked |
| `permission_mode` | Current [permission mode](/docs/en/permissions#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"`, or `"bypassPermissions"`. Not all events receive this field: see each event’s JSON example below to check |
| `effort` | Object with a `level` field holding the active [effort level](/docs/en/model-config#adjust-effort-level) for the turn: `"low"`, `"medium"`, `"high"`, `"xhigh"`, or `"max"`. If the requested model effort exceeds what the current model supports, this is the downgraded level the model actually used. Ultracode is not a distinct level and reports as `"xhigh"`. The object matches the [status line](/docs/en/statusline#available-data) `effort` field. Present for events that fire within a tool-use context, such as `PreToolUse`, `PostToolUse`, `Stop`, and `SubagentStop`, when the current model supports the effort parameter. The level is also available to hook commands and the Bash tool as the `$CLAUDE_EFFORT` environment variable. |
| `hook_event_name` | Name of the event that fired |

When running with `--agent` or inside a subagent, two additional fields are included:

| Field | Description |
| --- | --- |
| `agent_id` | Unique identifier for the subagent. Present only when the hook fires inside a subagent call. Use this to distinguish subagent hook calls from main-thread calls. |
| `agent_type` | Agent name (for example, `"Explore"` or `"security-reviewer"`). Present when the session uses `--agent` or the hook fires inside a subagent. For subagents, the subagent’s type takes precedence over the session’s `--agent` value. For [custom subagents](/docs/en/sub-agents), this is the `name` field from the agent’s frontmatter, not the filename. |

Only [`SessionStart`](#sessionstart) hooks can receive a `model` field, and it is not guaranteed to be present. There is no `$CLAUDE_MODEL` environment variable. A hook process inherits the parent environment, so it can read `$ANTHROPIC_MODEL` if you set it in your shell, but that value does not change when you switch models with `/model` during a session.
For example, a `PreToolUse` hook for a Bash command receives this on stdin:

```
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

The `tool_name` and `tool_input` fields are event-specific. Each [hook event](#hook-events) section documents the additional fields for that event.

### [​](#exit-code-output) Exit code output

The exit code from your hook command tells Claude Code whether the action should proceed, be blocked, or be ignored.
**Exit 0** means success. Claude Code parses stdout for [JSON output fields](#json-output). JSON output is only processed on exit 0. For most events, stdout is written to the debug log but not shown in the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart`, where stdout is added as context that Claude can see and act on.
**Exit 2** means a blocking error. Claude Code ignores stdout and any JSON in it. Instead, stderr text is fed back to Claude as an error message. The effect depends on the event: `PreToolUse` blocks the tool call, `UserPromptSubmit` rejects the prompt, and so on. See [exit code 2 behavior](#exit-code-2-behavior-per-event) for the full list.
**Any other exit code** is a non-blocking error for most hook events. The transcript shows a `<hook name> hook error` notice followed by the first line of stderr, so you can identify the cause without `--debug`. Execution continues and the full stderr is written to the debug log.
For example, a hook command script that blocks dangerous Bash commands:

```
#!/bin/bash