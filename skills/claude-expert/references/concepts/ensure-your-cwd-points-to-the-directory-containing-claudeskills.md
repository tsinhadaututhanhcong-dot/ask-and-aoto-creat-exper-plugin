---
type: Reference
title: Ensure your cwd points to the directory containing .claude/skills/
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Ensure your cwd points to the directory containing .claude/skills/
options = ClaudeAgentOptions(
    cwd="/path/to/project",  # .claude/skills/ here or in a parent directory
    setting_sources=["user", "project"],  # Loads skills from these sources
    skills="all",
)
```

See the “Using Skills with the SDK” section above for the complete pattern.
**Verify filesystem location**:

```