---
type: Reference
title: Earlier session analyzed the code; now build on that analysis
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Earlier session analyzed the code; now build on that analysis
async for message in query(
    prompt="Now implement the refactoring you suggested",
    options=ClaudeAgentOptions(
        resume=session_id,
        allowed_tools=["Read", "Edit", "Write", "Glob", "Grep"],
    ),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

You should see a response that builds on the earlier analysis instead of starting fresh. That confirms the agent resumed the session with its prior context intact.

If a `resume` call returns a fresh session instead of the expected history, the most common cause is a mismatched `cwd`. Sessions are stored under `~/.claude/projects/<encoded-cwd>/*.jsonl`, or under `$CLAUDE_CONFIG_DIR/projects/<encoded-cwd>/*.jsonl` if you set the `CLAUDE_CONFIG_DIR` environment variable, where `<encoded-cwd>` is the absolute working directory with every non-alphanumeric character replaced by `-` (so `/Users/me/proj` becomes `-Users-me-proj`). If your resume call runs from a different directory, the SDK looks in the wrong place. The session file also needs to exist on the current machine.

To resume sessions across machines or in serverless environments, mirror transcripts to shared storage with a [`SessionStore` adapter](/docs/en/agent-sdk/session-storage).

### [​](#fork-to-explore-alternatives) Fork to explore alternatives

Forking creates a new session that starts with a copy of the original’s history but diverges from that point. The fork gets its own session ID; the original’s ID and history stay unchanged. You end up with two independent sessions you can resume separately.

Forking branches the conversation history, not the filesystem. If a forked agent edits files, those changes are real and visible to any session working in the same directory. To branch and revert file changes, use [file checkpointing](/docs/en/agent-sdk/file-checkpointing).

This example builds on [Capture the session ID](#capture-the-session-id): you’ve already analyzed an auth module in `session_id` and want to explore OAuth2 without losing the JWT-focused thread. The first block forks the session and captures the fork’s ID (`forked_id`); the second block resumes the original `session_id` to continue down the JWT path. You now have two session IDs pointing at two separate histories:

Python

TypeScript

```