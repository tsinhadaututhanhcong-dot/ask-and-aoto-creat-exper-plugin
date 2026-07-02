---
title: Example with authentication header
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### [​](#option-3-add-a-local-stdio-server) Option 3: Add a local stdio server

Stdio servers run as local processes on your machine. They’re ideal for tools that need direct system access or custom scripts.
Claude Code sets `CLAUDE_PROJECT_DIR` in the spawned server’s environment to the project root, so your server can resolve project-relative paths without depending on the working directory. This is the same directory hooks receive in their `CLAUDE_PROJECT_DIR` variable. Read it from inside your server process, for example `process.env.CLAUDE_PROJECT_DIR` in Node or `os.environ["CLAUDE_PROJECT_DIR"]` in Python.
Your server can also call the MCP `roots/list` request, which returns the directory Claude Code was launched from.
This variable is set in the server’s environment, not in Claude Code’s own environment, so referencing it via `${VAR}` expansion in a project- or user-scoped `.mcp.json` `command` or `args` requires a default such as `${CLAUDE_PROJECT_DIR:-.}`. Plugin-provided MCP configurations substitute `${CLAUDE_PROJECT_DIR}` directly and don’t need the default.

```