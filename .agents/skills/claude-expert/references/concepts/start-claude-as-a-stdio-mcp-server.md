---
title: Start Claude as a stdio MCP server
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Start Claude as a stdio MCP server
claude mcp serve
```

You can use this in Claude Desktop by adding this configuration to claude\_desktop\_config.json:

```
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Configuring the executable path**: the `command` field must reference the Claude Code executable. If the `claude` command is not in your system’s PATH, you’ll need to specify the full path to the executable.To find the full path:

```
which claude
```

Then use the full path in your configuration:

```
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "/full/path/to/claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

Without the correct executable path, you’ll encounter errors like `spawn claude ENOENT`.

Tips:

* The server provides access to Claude’s tools like View, Edit, LS, etc.
* In Claude Desktop, try asking Claude to read files in a directory, make edits, and more.
* This MCP server only exposes Claude Code’s tools to your MCP client, so your own client is responsible for implementing user confirmation for individual tool calls.

## [​](#mcp-output-limits-and-warnings) MCP output limits and warnings

When MCP tools produce large outputs, Claude Code helps manage the token usage to prevent overwhelming your conversation context:

* **Output warning threshold**: Claude Code displays a warning when any MCP tool output exceeds 10,000 tokens
* **Configurable limit**: you can adjust the maximum allowed MCP output tokens using the `MAX_MCP_OUTPUT_TOKENS` environment variable
* **Default limit**: the default maximum is 25,000 tokens
* **Scope**: the environment variable applies to tools that don’t declare their own limit. Tools that set [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) use that value instead for text content, regardless of what `MAX_MCP_OUTPUT_TOKENS` is set to. Tools that return image data are still subject to `MAX_MCP_OUTPUT_TOKENS`

To increase the limit for tools that produce large outputs:

```
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

This is particularly useful when working with MCP servers that:

* Query large datasets or databases
* Generate detailed reports or documentation
* Process extensive log files or debugging information

### [​](#raise-the-limit-for-a-specific-tool) Raise the limit for a specific tool

If you’re building an MCP server, you can allow individual tools to return results larger than the default persist-to-disk threshold by setting `_meta["anthropic/maxResultSizeChars"]` in the tool’s `tools/list` response entry. Claude Code raises that tool’s threshold to the annotated value, up to a hard ceiling of 500,000 characters.
This is useful for tools that return inherently large but necessary outputs, such as database schemas or full file trees. Without the annotation, results that exceed the default threshold are persisted to disk and replaced with a file reference in the conversation.

```
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

The annotation applies independently of `MAX_MCP_OUTPUT_TOKENS` for text content, so users don’t need to raise the environment variable for tools that declare it. Tools that return image data are still subject to the token limit.

If you frequently encounter output warnings with specific MCP servers you don’t control, consider increasing the `MAX_MCP_OUTPUT_TOKENS` limit. You can also ask the server author to add the `anthropic/maxResultSizeChars` annotation or to paginate their responses. The annotation has no effect on tools that return image content; for those, raising `MAX_MCP_OUTPUT_TOKENS` is the only option.

## [​](#respond-to-mcp-elicitation-requests) Respond to MCP elicitation requests

MCP servers can request structured input from you mid-task using elicitation. When a server needs information it can’t get on its own, Claude Code displays an interactive dialog and passes your response back to the server. No configuration is required on your side: elicitation dialogs appear automatically when a server requests them.
Servers can request input in two ways:

* **Form mode**: Claude Code shows a dialog with form fields defined by the server (for example, a username and password prompt). Fill in the fields and submit.
* **URL mode**: Claude Code opens a browser URL for authentication or approval. Complete the flow in the browser, then confirm in the CLI.

To auto-respond to elicitation requests without showing a dialog, use the [`Elicitation` hook](/docs/en/hooks#elicitation).
If you’re building an MCP server that uses elicitation, see the [MCP elicitation specification](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) for protocol details and schema examples.

## [​](#use-mcp-resources) Use MCP resources

MCP servers can expose resources that you can reference using @ mentions, similar to how you reference files.

### [​](#reference-mcp-resources) Reference MCP resources

1

List available resources

Type `@` in your prompt to see available resources from all connected MCP servers. Resources appear alongside files in the autocomplete menu.

2

Reference a specific resource

Use the format `@server:protocol://resource/path` to reference a resource:

```
Can you analyze @github:issue://123 and suggest a fix?
```

```
Please review the API documentation at @docs:file://api/authentication
```

3

Multiple resource references

You can reference multiple resources in a single prompt:

```
Compare @postgres:schema://users with @docs:file://database/user-model
```

Tips:

* Resources are automatically fetched and included as attachments when referenced
* Resource paths are fuzzy-searchable in the @ mention autocomplete
* Claude Code automatically provides tools to list and read MCP resources when servers support them
* Resources can contain any type of content that the MCP server provides (text, JSON, structured data, etc.)

## [​](#scale-with-mcp-tool-search) Scale with MCP tool search

Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them. Only tool names and server instructions load at session start, so adding more MCP servers has minimal impact on your context window. Claude Code doesn’t impose a fixed per-server tool cap; the practical limit is your context window budget.

### [​](#how-it-works) How it works

Tool search is enabled by default. MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context. From your perspective, MCP tools work exactly as before.
If you prefer threshold-based loading, set `ENABLE_TOOL_SEARCH=auto` to load schemas upfront when they fit within 10% of the context window and defer only the overflow. See [Configure tool search](#configure-tool-search) for all options.

### [​](#for-mcp-server-authors) For MCP server authors

If you’re building an MCP server, the server instructions field becomes more useful with tool search enabled. Server instructions help Claude understand when to search for your tools, similar to how [skills](/docs/en/skills) work.
Add clear, descriptive server instructions that explain:

* What category of tasks your tools handle
* When Claude should search for your tools
* Key capabilities your server provides

Claude Code truncates tool descriptions and server instructions at 2KB each. Keep them concise to avoid truncation, and put critical details near the start.

### [​](#configure-tool-search) Configure tool search

Tool search is enabled by default: MCP tools are deferred and discovered on demand. Claude Code disables it by default on Vertex AI. It is also disabled when `ANTHROPIC_BASE_URL` points to a non-first-party host, since most proxies don’t forward `tool_reference` blocks. Set `ENABLE_TOOL_SEARCH` explicitly to override either fallback.
Tool search requires a model that supports `tool_reference` blocks. Haiku models don’t support it. On Vertex AI, tool search is supported for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later.
Control tool search behavior with the `ENABLE_TOOL_SEARCH` environment variable:

| Value | Behavior |
| --- | --- |
| (unset) | All MCP tools deferred and loaded on demand. Falls back to loading upfront on Vertex AI or when `ANTHROPIC_BASE_URL` is a non-first-party host |
| `true` | All MCP tools deferred. Claude Code sends the beta header even on Vertex AI and through proxies. Requests fail on Vertex AI models earlier than Sonnet 4.5 or Opus 4.5, or on proxies that don’t support `tool_reference` blocks |
| `auto` | Threshold mode: tools load upfront if they fit within 10% of the context window, deferred otherwise |
| `auto:N` | Threshold mode with a custom percentage, where `N` is 0-100. For example, `auto:5` for 5% |
| `false` | All MCP tools loaded upfront, no deferral |

```