---
title: Do not load user, project, or local settings from disk
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Do not load user, project, or local settings from disk
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Analyze this code",
    options=ClaudeAgentOptions(
        setting_sources=[]
    ),
):
    print(message)
```

In Python SDK 0.1.59 and earlier, an empty list was treated the same as omitting the option, so `setting_sources=[]` did not disable filesystem settings. Upgrade to a newer release if you need an empty list to take effect. The TypeScript SDK is not affected.

**Load all filesystem settings explicitly:**

```
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Analyze this code",
    options=ClaudeAgentOptions(
        setting_sources=["user", "project", "local"]
    ),
):
    print(message)
```

**Load only specific setting sources:**

```