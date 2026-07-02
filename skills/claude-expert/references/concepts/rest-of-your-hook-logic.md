---
title: ... rest of your hook logic
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# ... rest of your hook logic
```

If your hook legitimately needs more than eight iterations to converge, raise the cap with [`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](/docs/en/env-vars).

### [​](#json-validation-failed) JSON validation failed

Claude Code shows a JSON parsing error even though your hook script outputs valid JSON.
When Claude Code runs a shell-form command hook (one without `args`), it spawns `sh -c` on macOS and Linux or Git Bash on Windows by default. This shell is non-interactive, but Git Bash and some configurations (such as `BASH_ENV` pointing at `~/.bashrc`) still source your profile. If that profile contains unconditional `echo` statements, the output gets prepended to your hook’s JSON:

```
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code tries to parse this as JSON and fails. To fix this, wrap echo statements in your shell profile so they only run in interactive shells:

```