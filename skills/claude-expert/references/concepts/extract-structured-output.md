---
type: Reference
title: Extract structured output
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Extract structured output
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

### [​](#stream-responses) Stream responses

Use `--output-format stream-json` with `--verbose` and `--include-partial-messages` to receive tokens as they’re generated. Each line is a JSON object representing an event:

```
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

The following example uses [jq](https://jqlang.github.io/jq/) to filter for text deltas and display just the streaming text. The `-r` flag outputs raw strings (no quotes) and `-j` joins without newlines so tokens stream continuously:

```
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

When an API request fails with a retryable error, Claude Code emits a `system/api_retry` event before retrying. You can use this to surface retry progress or implement custom backoff logic.

| Field | Type | Description |
| --- | --- | --- |
| `type` | `"system"` | message type |
| `subtype` | `"api_retry"` | identifies this as a retry event |
| `attempt` | integer | current attempt number, starting at 1 |
| `max_retries` | integer | total retries permitted |
| `retry_delay_ms` | integer | milliseconds until the next attempt |
| `error_status` | integer or null | HTTP status code, or `null` for connection errors with no HTTP response |
| `error` | string | error category: `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `overloaded`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, or `unknown` |
| `uuid` | string | unique event identifier |
| `session_id` | string | session the event belongs to |

The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins. It is the first event in the stream unless [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/docs/en/env-vars) is set, in which case `plugin_install` events precede it. Use the plugin fields to fail CI when a plugin did not load:

| Field | Type | Description |
| --- | --- | --- |
| `plugins` | array | plugins that loaded successfully, each with `name` and `path` |
| `plugin_errors` | array | plugin load-time errors, each with `plugin`, `type`, and `message`. Includes unsatisfied dependency versions and `--plugin-dir` load failures such as a missing path or invalid archive. Affected plugins are demoted and absent from `plugins`. The key is omitted when there are no errors |

When [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/docs/en/env-vars) is set, Claude Code emits `system/plugin_install` events while marketplace plugins install before the first turn. Use these to surface install progress in your own UI.

| Field | Type | Description |
| --- | --- | --- |
| `type` | `"system"` | message type |
| `subtype` | `"plugin_install"` | identifies this as a plugin install event |
| `status` | `"started"`, `"installed"`, `"failed"`, or `"completed"` | `started` and `completed` bracket the overall install; `installed` and `failed` report individual marketplaces |
| `name` | string, optional | marketplace name, present on `installed` and `failed` |
| `error` | string, optional | failure message, present on `failed` |
| `uuid` | string | unique event identifier |
| `session_id` | string | session the event belongs to |

For programmatic streaming with callbacks and message objects, see [Stream responses in real-time](/docs/en/agent-sdk/streaming-output) in the Agent SDK documentation.

### [​](#auto-approve-tools) Auto-approve tools

Use `--allowedTools` to let Claude use certain tools without prompting. This example runs a test suite and fixes failures, allowing Claude to execute Bash commands and read/edit files without asking for permission:

```
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

To set a baseline for the whole session instead of listing individual tools, pass a [permission mode](/docs/en/permission-modes). `dontAsk` denies anything not in your `permissions.allow` rules or the [read-only command set](/docs/en/permissions#read-only-commands), which is useful for locked-down CI runs. `acceptEdits` lets Claude write files without prompting and also auto-approves common filesystem commands such as `mkdir`, `touch`, `mv`, and `cp`. Other shell commands and network requests still need an `--allowedTools` entry or a `permissions.allow` rule, otherwise the run aborts when one is attempted:

```
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### [​](#create-a-commit) Create a commit

This example reviews staged changes and creates a commit with an appropriate message:

```
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

The `--allowedTools` flag uses [permission rule syntax](/docs/en/settings#permission-rule-syntax). The trailing  `*` enables prefix matching, so `Bash(git diff *)` allows any command starting with `git diff`. The space before `*` is important: without it, `Bash(git diff*)` would also match `git diff-index`.

User-invoked [skills](/docs/en/skills) and custom commands work in `-p` mode: include `/skill-name` in the prompt string and Claude Code expands it before running. Built-in commands that open an interactive dialog, such as `/login`, are not available in `-p` mode. To change a setting from a `-p` invocation, pass `key=value` to `/config`, for example `/config thinking=false`.

### [​](#customize-the-system-prompt) Customize the system prompt

Use `--append-system-prompt` to add instructions while keeping Claude Code’s default behavior. This example pipes a PR diff to Claude and instructs it to review for security vulnerabilities:

```
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

See [system prompt flags](/docs/en/cli-reference#system-prompt-flags) for more options including `--system-prompt` to fully replace the default prompt.

### [​](#continue-conversations) Continue conversations

Use `--continue` to continue the most recent conversation, or `--resume` with a session ID to continue a specific conversation. This example runs a review, then sends follow-up prompts:

```