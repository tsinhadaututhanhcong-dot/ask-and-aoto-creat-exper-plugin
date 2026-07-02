---
title: After
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# After
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(model="claude-opus-4-7")
```

**5. Review [breaking changes](#breaking-changes)**
Make any code changes needed to complete the migration.

## [​](#breaking-changes) Breaking changes

To improve isolation and explicit configuration, Claude Agent SDK v0.1.0 introduces breaking changes for users migrating from Claude Code SDK. Review this section carefully before migrating.

### [​](#python-claudecodeoptions-renamed-to-claudeagentoptions) Python: ClaudeCodeOptions renamed to ClaudeAgentOptions

**What changed:** The Python SDK type `ClaudeCodeOptions` has been renamed to `ClaudeAgentOptions`.
**Migration:**

```