---
title: Real example: Add Airtable server
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Real example: Add Airtable server
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

**Important: Separate server arguments with `--`**For stdio servers, the `--` (double dash) separates Claude’s own options, such as `--transport`, `--env`, and `--scope`, from the command and arguments that run the server. Everything after `--` is passed to the server untouched.For example:

* `claude mcp add --transport stdio myserver -- npx server` → runs `npx server`
* `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080` → runs `python server.py --port 8080` with `KEY=value` in environment

Without `--`, Claude Code would try to parse the server’s flags, like `--port` above, as its own options.`--env` accepts multiple `KEY=value` pairs. If the server name comes directly after `--env`, the CLI reads the name as another pair and rejects it, so place at least one other option between `--env` and the server name, as in the examples above.

### [​](#option-4-add-a-remote-websocket-server) Option 4: Add a remote WebSocket server

WebSocket servers hold a persistent bidirectional connection, which suits remote MCP servers that push events to Claude unprompted. Use HTTP instead when your server only responds to requests, since HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither.
Configure WebSocket servers in `.mcp.json` or with `claude mcp add-json`:

```
claude mcp add-json events-server \
  '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'
```

The `type: "ws"` entry accepts the same `url`, `headers`, `headersHelper`, `timeout`, and `alwaysLoad` fields as `http`. Authentication is header-only, so pass a static token in `headers` or generate one at connect time with [`headersHelper`](#use-dynamic-headers-for-custom-authentication). The `claude mcp add --transport` flag doesn’t accept `ws`.

### [​](#managing-your-servers) Managing your servers

Once configured, you can manage your MCP servers with these commands:

```