---
title: ./scripts/validate-readonly-query.sh
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')