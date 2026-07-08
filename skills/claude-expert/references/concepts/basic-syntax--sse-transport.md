---
type: Reference
title: Basic syntax (SSE transport, deprecated)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Basic syntax (SSE transport, deprecated)
```bash
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```
