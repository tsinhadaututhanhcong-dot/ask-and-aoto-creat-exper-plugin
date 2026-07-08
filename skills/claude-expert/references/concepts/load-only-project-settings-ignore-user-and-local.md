---
type: Reference
title: Load only project settings, ignore user and local
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Load only project settings, ignore user and local
async for message in query(
    prompt="Run CI checks",
    options=ClaudeAgentOptions(
        setting_sources=["project"]  # Only .claude/settings.json
    ),
):
    print(message)
```

**Testing and CI environments:**

```