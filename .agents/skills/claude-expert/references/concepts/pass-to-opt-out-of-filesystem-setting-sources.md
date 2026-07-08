---
type: Reference
title: Pass [] to opt out of filesystem setting sources.
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Pass [] to opt out of filesystem setting sources.
async for message in query(
    prompt="Review this PR",
    options=ClaudeAgentOptions(
        setting_sources=[],
        agents={...},
        mcp_servers={...},
        allowed_tools=["Read", "Grep", "Glob"],
    ),
):
    print(message)
```

**Loading CLAUDE.md project instructions:**

```