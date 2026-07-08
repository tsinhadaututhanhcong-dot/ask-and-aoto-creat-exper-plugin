---
type: Reference
title: Extract the command field from tool_input using jq
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi