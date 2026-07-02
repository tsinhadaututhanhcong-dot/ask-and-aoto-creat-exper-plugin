---
title: (within Claude Code) Check server status
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# (within Claude Code) Check server status
/mcp
```

Project-scoped servers from `.mcp.json` that are awaiting your approval appear in `claude mcp list` as `⏸ Pending approval`. Run `claude` interactively to review and approve them. `claude mcp get <name>` shows pending servers as `⏸ Pending approval` and rejected servers as `✗ Rejected`.
The `/mcp` panel shows the tool count next to each connected server and flags servers that advertise the tools capability but expose no tools.
If your request needs tools from a server that is still connecting in the background, Claude waits for that server before continuing. With [tool search](#scale-with-mcp-tool-search) enabled, which is the default, the wait happens inside the `ToolSearch` call. In configurations without tool search, such as Vertex AI, a custom `ANTHROPIC_BASE_URL`, or `ENABLE_TOOL_SEARCH=false`, Claude uses the `WaitForMcpServers` tool instead.
The server name `workspace` is reserved for internal use. If your configuration defines a server with that name, Claude Code skips it at load time and shows a warning asking you to rename it.

### [​](#dynamic-tool-updates) Dynamic tool updates

Claude Code supports MCP `list_changed` notifications, allowing MCP servers to dynamically update their available tools, prompts, and resources without requiring you to disconnect and reconnect. When an MCP server sends a `list_changed` notification, Claude Code automatically refreshes the available capabilities from that server.

### [​](#automatic-reconnection) Automatic reconnection

If an HTTP or SSE server disconnects mid-session, Claude Code automatically reconnects with exponential backoff: up to five attempts, starting at a one-second delay and doubling each time. The server appears as pending in `/mcp` while reconnection is in progress. After five failed attempts the server is marked as failed and you can retry manually from `/mcp`. Stdio servers are local processes and are not reconnected automatically.
The same backoff applies when an HTTP or SSE server fails its initial connection at startup. As of v2.1.121, Claude Code retries the initial connection up to three times on transient errors such as a 5xx response, a connection refused, or a timeout, then marks the server as failed if it still can’t connect. Authentication and not-found errors are not retried because they require a configuration change to resolve.
As of v2.1.191, the capability discovery requests that run after a successful connection, such as `tools/list`, `prompts/list`, and `resources/list`, also retry transient network and server errors up to three times with short backoff. Authentication errors, 4xx responses, and request timeouts are not retried.

### [​](#push-messages-with-channels) Push messages with channels

An MCP server can also push messages directly into your session so Claude can react to external events like CI results, monitoring alerts, or chat messages. To enable this, your server declares the `claude/channel` capability and you opt it in with the `--channels` flag at startup. See [Channels](/docs/en/channels) to use an officially supported channel, or [Channels reference](/docs/en/channels-reference) to build your own.

Tips:

* Use the `--scope` flag to specify where the configuration is stored:
  + `local` (default): available only to you in the current project. Older versions called this scope `project`
  + `project`: shared with everyone in the project via the `.mcp.json` file
  + `user`: available to you across all projects. Older versions called this scope `global`
* Set environment variables with `--env` flags (for example, `--env KEY=value`)
* Configure MCP server startup timeout using the `MCP_TIMEOUT` environment variable (for example, `MCP_TIMEOUT=10000 claude` sets a 10-second timeout)
* Set a per-server tool execution timeout by adding a `timeout` field in milliseconds to that server’s `.mcp.json` entry, for example `"timeout": 600000` for ten minutes. This overrides the `MCP_TOOL_TIMEOUT` environment variable for that server only
* Claude Code displays a warning when MCP tool output exceeds 10,000 tokens. To increase this limit, set the `MAX_MCP_OUTPUT_TOKENS` environment variable (for example, `MAX_MCP_OUTPUT_TOKENS=50000`)
* Use `/mcp` to authenticate with remote servers that require OAuth 2.0 authentication

The per-server `timeout` is a hard wall-clock limit per tool call, and progress notifications from the server don’t extend it. Values below 1000 are ignored and fall through to `MCP_TOOL_TIMEOUT`, or to its default of about 28 hours when that variable is unset. Before v2.1.162, values below 1000 were floored to one second instead.
For HTTP and SSE servers, the per-request fetch first-byte budget has a 60-second minimum.
As of v2.1.187, a tool call to a remote HTTP, SSE, WebSocket, or [claude.ai connector](#use-mcp-servers-from-claude-ai) server that sends no response and no progress notification for 5 minutes aborts with an error instead of waiting for the wall-clock limit. Set the [`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`](/docs/en/env-vars) environment variable in milliseconds to change the idle window, or set it to `0` to disable the check. Stdio servers are local processes and are not subject to the idle timeout.

### [​](#plugin-provided-mcp-servers) Plugin-provided MCP servers

[Plugins](/docs/en/plugins) can bundle MCP servers, automatically providing tools and integrations when the plugin is enabled. Plugin MCP servers work identically to user-configured servers.
**How plugin MCP servers work**:

* Plugins define MCP servers in `.mcp.json` at the plugin root or inline in `plugin.json`
* When a plugin is enabled, its MCP servers start automatically
* Plugin MCP tools appear alongside manually configured MCP tools
* Plugin servers are managed through plugin installation, not `/mcp` commands

**Example plugin MCP configuration**:
In `.mcp.json` at plugin root:

```
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Or inline in `plugin.json`:

```
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Plugin MCP features**:

* **Automatic lifecycle**: at session startup, servers for enabled plugins connect automatically. If you enable or disable a plugin during a session, run `/reload-plugins` to connect or disconnect its MCP servers
* **Environment variables**: use `${CLAUDE_PLUGIN_ROOT}` for bundled plugin files, `${CLAUDE_PLUGIN_DATA}` for [persistent state](/docs/en/plugins-reference#persistent-data-directory) that survives plugin updates, and `${CLAUDE_PROJECT_DIR}` for the stable project root
* **User environment access**: access to the same environment variables as manually configured servers
* **Multiple transport types**: support for stdio, SSE, HTTP, and WebSocket transports, though transport support may vary by server

**Viewing plugin MCP servers**:

```