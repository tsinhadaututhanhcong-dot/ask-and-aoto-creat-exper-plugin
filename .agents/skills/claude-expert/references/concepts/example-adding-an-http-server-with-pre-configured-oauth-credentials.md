---
type: Reference
title: Example: Adding an HTTP server with pre-configured OAuth credentials
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Example: Adding an HTTP server with pre-configured OAuth credentials
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
```

2

Verify the server was added

```
claude mcp get weather-api
```

Tips:

* Make sure the JSON is properly escaped in your shell
* The JSON must conform to the MCP server configuration schema
* You can use `--scope user` to add the server to your user configuration instead of the project-specific one

## [​](#import-mcp-servers-from-claude-desktop) Import MCP servers from Claude Desktop

If you’ve already configured MCP servers in Claude Desktop, you can import them:

1

Import servers from Claude Desktop

```