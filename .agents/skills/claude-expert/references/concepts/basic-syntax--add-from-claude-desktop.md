---
type: Reference
title: Basic syntax (import from Claude Desktop)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Basic syntax (import from Claude Desktop)
```bash
claude mcp add-from-claude-desktop
```

Tips:
* This feature only works on macOS and Windows Subsystem for Linux (WSL)
* It reads the Claude Desktop configuration file from its standard location on those platforms
* Use the `--scope user` flag to add servers to your user configuration
* Imported servers keep the same names as in Claude Desktop
* If servers with the same names already exist, they get a numerical suffix (for example, `server_1`)
