---
title: Basic syntax (HTTP transport)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Basic syntax (HTTP transport)
```bash
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```
