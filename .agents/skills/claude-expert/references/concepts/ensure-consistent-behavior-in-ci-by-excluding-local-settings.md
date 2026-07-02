---
title: Ensure consistent behavior in CI by excluding local settings
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Ensure consistent behavior in CI by excluding local settings
async for message in query(
    prompt="Run tests",
    options=ClaudeAgentOptions(
        setting_sources=["project"],  # Only team-shared settings
        permission_mode="bypassPermissions",
    ),
):
    print(message)
```

**SDK-only applications:**

```