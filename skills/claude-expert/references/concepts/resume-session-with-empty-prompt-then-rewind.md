---
type: Reference
title: Resume session with empty prompt, then rewind
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Resume session with empty prompt, then rewind
async with ClaudeSDKClient(
    ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
) as client:
    await client.query("")
    async for message in client.receive_response():
        await client.rewind_files(checkpoint_id)
        break
```

## [​](#next-steps) Next steps

* **[Sessions](/docs/en/agent-sdk/sessions)**: learn how to resume sessions, which is required for rewinding after the stream completes. Covers session IDs, resuming conversations, and session forking.
* **[Permissions](/docs/en/agent-sdk/permissions)**: configure which tools Claude can use and how file modifications are approved. Useful if you want more control over when edits happen.
* **[TypeScript SDK reference](/docs/en/agent-sdk/typescript)**: complete API reference including all options for `query()` and the `rewindFiles()` method.
* **[Python SDK reference](/docs/en/agent-sdk/python)**: complete API reference including all options for `ClaudeAgentOptions` and the `rewind_files()` method.

Was this page helpful?

YesNo

[Intercept and control agent behavior with hooks](/docs/en/agent-sdk/hooks)[Track cost and usage](/docs/en/agent-sdk/cost-tracking)

⌘I

---