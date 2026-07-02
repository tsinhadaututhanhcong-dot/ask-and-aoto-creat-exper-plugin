---
title: Original session is untouched; resuming it continues the JWT thread
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Original session is untouched; resuming it continues the JWT thread
async for message in query(
    prompt="Continue with the JWT approach",
    options=ClaudeAgentOptions(resume=session_id),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

You should see that `forkedId` differs from the original session ID. Resuming the original session still continues the JWT thread, which confirms the fork did not modify the original history.

## [​](#resume-across-hosts) Resume across hosts

Session files are local to the machine that created them. To resume a session on a different host (CI workers, ephemeral containers, serverless), you have two options:

* **Move the session file.** Persist `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` from the first run and restore it to the same path on the new host before calling `resume`. The `cwd` must match.
* **Don’t rely on session resume.** Capture the results you need (analysis output, decisions, file diffs) as application state and pass them into a fresh session’s prompt. This is often more robust than shipping transcript files around.

Both SDKs expose functions for enumerating sessions on disk and reading their messages: [`listSessions()`](/docs/en/agent-sdk/typescript#listsessions) and [`getSessionMessages()`](/docs/en/agent-sdk/typescript#getsessionmessages) in TypeScript, [`list_sessions()`](/docs/en/agent-sdk/python#list_sessions) and [`get_session_messages()`](/docs/en/agent-sdk/python#get_session_messages) in Python. Use them to build custom session pickers, cleanup logic, or transcript viewers.
Both SDKs also expose functions for looking up and mutating individual sessions: [`get_session_info()`](/docs/en/agent-sdk/python#get_session_info), [`rename_session()`](/docs/en/agent-sdk/python#rename_session), and [`tag_session()`](/docs/en/agent-sdk/python#tag_session) in Python, and [`getSessionInfo()`](/docs/en/agent-sdk/typescript#getsessioninfo), [`renameSession()`](/docs/en/agent-sdk/typescript#renamesession), and [`tagSession()`](/docs/en/agent-sdk/typescript#tagsession) in TypeScript. Use them to organize sessions by tag or give them human-readable titles.

## [​](#related-resources) Related resources

* [How the agent loop works](/docs/en/agent-sdk/agent-loop): Understand turns, messages, and context accumulation within a session
* [File checkpointing](/docs/en/agent-sdk/file-checkpointing): Snapshot and revert file changes the agent made within a session
* [Python `ClaudeAgentOptions`](/docs/en/agent-sdk/python#claudeagentoptions): Full session option reference for Python
* [TypeScript `Options`](/docs/en/agent-sdk/typescript#options): Full session option reference for TypeScript

Was this page helpful?

YesNo

[Use Claude Code features](/docs/en/agent-sdk/claude-code-features)[Persist sessions to external storage](/docs/en/agent-sdk/session-storage)

⌘I

---