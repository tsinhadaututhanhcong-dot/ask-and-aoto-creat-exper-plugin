---
title: Basic syntax (stdio transport)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Basic syntax (stdio transport)
```bash
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \
  -- npx -y airtable-mcp-server
```
