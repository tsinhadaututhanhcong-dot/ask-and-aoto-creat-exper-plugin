---
title: Skills loaded: user and project sources included
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Skills loaded: user and project sources included
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],
    skills="all",
)
```

For more details on `settingSources`/`setting_sources`, see the [TypeScript SDK reference](/docs/en/agent-sdk/typescript#settingsource) or [Python SDK reference](/docs/en/agent-sdk/python#settingsource).
**Check working directory**: The SDK loads Skills from `.claude/skills/` in the `cwd` option and in every parent directory up to the repository root. Ensure `cwd` points at or below the directory containing `.claude/skills/`, within the same repository:

Python

TypeScript

```