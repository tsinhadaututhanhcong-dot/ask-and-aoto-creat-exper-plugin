---
type: Reference
title: Read hook input from stdin
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')