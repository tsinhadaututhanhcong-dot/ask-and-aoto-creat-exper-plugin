---
title: Convert git SSH URL to HTTPS
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Convert git SSH URL to HTTPS
REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

if [ -n "$REMOTE" ]; then
    REPO_NAME=$(basename "$REMOTE")
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    # printf %b interprets escape sequences reliably across shells
    printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
else
    echo "[$MODEL]"
fi
```

### [​](#rate-limit-usage) Rate limit usage

Display Claude.ai subscription rate limit usage in the status line. The `rate_limits` object contains `five_hour` (5-hour rolling window) and `seven_day` (weekly) windows. Each window provides `used_percentage` (0-100) and `resets_at` (Unix epoch seconds when the window resets).
This field is only present for Claude.ai subscribers (Pro/Max) after the first API response. Each script handles the absent field gracefully:

Bash

Python

Node.js

```
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')