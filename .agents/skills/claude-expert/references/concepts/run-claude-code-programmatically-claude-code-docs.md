---
type: Reference
title: Run Claude Code programmatically - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Run Claude Code programmatically - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

The [Agent SDK](/docs/en/agent-sdk/overview) gives you the same tools, agent loop, and context management that power Claude Code. It’s available as a CLI for scripts and CI/CD, or as [Python](/docs/en/agent-sdk/python) and [TypeScript](/docs/en/agent-sdk/typescript) packages for full programmatic control.
To run Claude Code in non-interactive mode, pass `-p` with your prompt and any [CLI options](/docs/en/cli-reference):

```
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

This page covers using the Agent SDK via the CLI (`claude -p`). For the Python and TypeScript SDK packages with structured outputs, tool approval callbacks, and native message objects, see the [full Agent SDK documentation](/docs/en/agent-sdk/overview).

## [​](#basic-usage) Basic usage

Add the `-p` (or `--print`) flag to any `claude` command to run it non-interactively. All [CLI options](/docs/en/cli-reference) work with `-p`, including:

* `--continue` for [continuing conversations](#continue-conversations)
* `--allowedTools` for [auto-approving tools](#auto-approve-tools)
* `--output-format` for [structured output](#get-structured-output)

This example asks Claude a question about your codebase and prints the response:

```
claude -p "What does the auth module do?"
```

### [​](#start-faster-with-bare-mode) Start faster with bare mode

Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Without it, `claude -p` loads the same [context](/docs/en/how-claude-code-works#the-context-window) an interactive session would, including anything configured in the working directory or `~/.claude`.
Bare mode is useful for CI and scripts where you need the same result on every machine. A hook in a teammate’s `~/.claude` or an MCP server in the project’s `.mcp.json` won’t run, because bare mode never reads them. Only flags you pass explicitly take effect.
This example runs a one-off summarize task in bare mode and pre-approves the Read tool so the call completes without a permission prompt:

```
claude --bare -p "Summarize this file" --allowedTools "Read"
```

In bare mode Claude has access to the Bash, file read, and file edit tools. Pass any context you need with a flag:

| To load | Use |
| --- | --- |
| System prompt additions | `--append-system-prompt`, `--append-system-prompt-file` |
| Settings | `--settings <file-or-json>` |
| MCP servers | `--mcp-config <file-or-json>` |
| Custom agents | `--agents <json>` |
| A plugin | `--plugin-dir <path>`, `--plugin-url <url>` |

Bare mode skips OAuth and keychain reads. Anthropic authentication must come from `ANTHROPIC_API_KEY` or an `apiKeyHelper` in the JSON passed to `--settings`. Bedrock, Vertex, and Foundry use their usual provider credentials.

`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release.

### [​](#background-tasks-at-exit) Background tasks at exit

If Claude starts a [background Bash task](/docs/en/tools-reference#bash-tool-behavior) during a `claude -p` run, for example a dev server or a watch build, that shell is terminated about five seconds after Claude has returned its final result and stdin has closed. The grace period lets a task that finishes right after the result still deliver its output. Before v2.1.163, a never-exiting background process would hold the `claude -p` invocation open indefinitely.
Background [subagents](/docs/en/sub-agents) and workflows are exempt from the five-second grace because their result is part of the final output, so `claude -p` waits for them to complete. From v2.1.182, that wait is capped at ten minutes by default so a stuck background agent cannot hold the process open indefinitely. Adjust the cap with [`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`](/docs/en/env-vars), or set it to `0` to wait without a limit.

## [​](#examples) Examples

These examples highlight common CLI patterns. For CI and other scripted calls, add [`--bare`](#start-faster-with-bare-mode) so they don’t pick up whatever happens to be configured locally.

### [​](#pipe-data-through-claude) Pipe data through Claude

Non-interactive mode reads stdin, so you can pipe data in and redirect the response out like any other command-line tool.
This example pipes a build log into Claude and writes the explanation to a file:

```
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown, so scripted callers can track spend per invocation without consulting the [usage dashboard](/docs/en/costs).

As of Claude Code v2.1.128, piped stdin is capped at 10MB. If you exceed the cap, Claude Code exits with a clear error and a non-zero status. To work with larger inputs, write the content to a file and reference the file path in your prompt instead of piping it.

### [​](#add-claude-to-a-build-script) Add Claude to a build script

You can wrap a non-interactive call in a script to use Claude as a project-specific linter or reviewer.
This `package.json` script pipes the diff against `main` into Claude and asks it to report typos. Piping the diff means Claude doesn’t need Bash permission to read it, and the escaped double quotes keep the script portable to Windows:

```
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### [​](#get-structured-output) Get structured output

Use `--output-format` to control how responses are returned:

* `text` (default): plain text output
* `json`: structured JSON with result, session ID, and metadata
* `stream-json`: newline-delimited JSON for real-time streaming

This example returns a project summary as JSON with session metadata, with the text result in the `result` field:

```
claude -p "Summarize this project" --output-format json
```

To get output conforming to a specific schema, use `--output-format json` with `--json-schema` and a [JSON Schema](https://json-schema.org/) definition. The response includes metadata about the request (session ID, usage, etc.) with the structured output in the `structured_output` field.
This example extracts function names and returns them as an array of strings:

```
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Use a tool like [jq](https://jqlang.github.io/jq/) to parse the response and extract specific fields:

```