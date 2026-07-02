---
title: Example: Adding a stdio server with JSON configuration
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'