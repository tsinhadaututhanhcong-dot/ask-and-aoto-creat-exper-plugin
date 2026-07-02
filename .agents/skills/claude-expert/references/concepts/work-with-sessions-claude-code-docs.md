---
title: Work with sessions - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Work with sessions - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

A session is the conversation history the SDK accumulates while your agent works. It contains your prompt, every tool call the agent made, every tool result, and every response. The SDK writes it to disk automatically so you can return to it later.
Returning to a session means the agent has full context from before: files it already read, analysis it already performed, decisions it already made. You can ask a follow-up question, recover from an interruption, or branch off to try a different approach.

Sessions persist the **conversation**, not the filesystem. To snapshot and revert file changes the agent made, use [file checkpointing](/docs/en/agent-sdk/file-checkpointing).

This guide covers how to pick the right approach for your app, the SDK interfaces that track sessions automatically, how to capture session IDs and use `resume` and `fork` manually, and what to know about resuming sessions across hosts.

## [​](#choose-an-approach) Choose an approach

How much session handling you need depends on your application’s shape. Session management comes into play when you send multiple prompts that should share context. Within a single `query()` call, the agent already takes as many turns as it needs, and permission prompts and `AskUserQuestion` are [handled in-loop](/docs/en/agent-sdk/user-input) (they don’t end the call).

| What you’re building | What to use |
| --- | --- |
| One-shot task: single prompt, no follow-up | Nothing extra. One `query()` call handles it. |
| Multi-turn chat in one process | [`ClaudeSDKClient` (Python) or `continue: true` (TypeScript)](#automatic-session-management). The SDK tracks the session for you with no ID handling. |
| Pick up where you left off after a process restart | `continue_conversation=True` (Python) / `continue: true` (TypeScript). Resumes the most recent session in the directory, no ID needed. |
| Resume a specific past session (not the most recent) | Capture the session ID and pass it to `resume`. |
| Try an alternative approach without losing the original | Fork the session. |
| Stateless task, don’t want anything written to disk (TypeScript only) | Set [`persistSession: false`](/docs/en/agent-sdk/typescript#options). The session exists only in memory for the duration of the call. Python always persists to disk. |

### [​](#continue-resume-and-fork) Continue, resume, and fork

Continue, resume, and fork are option fields you set on `query()` ([`ClaudeAgentOptions`](/docs/en/agent-sdk/python#claudeagentoptions) in Python, [`Options`](/docs/en/agent-sdk/typescript#options) in TypeScript).
**Continue** and **resume** both pick up an existing session and add to it. The difference is how they find that session:

* **Continue** finds the most recent session in the current directory. You don’t track anything. Works well when your app runs one conversation at a time.
* **Resume** takes a specific session ID. You track the ID. Required when you have multiple sessions (for example, one per user in a multi-user app) or want to return to one that isn’t the most recent.

**Fork** is different: it creates a new session that starts with a copy of the original’s history. The original stays unchanged. Use fork to try a different direction while keeping the option to go back.

## [​](#automatic-session-management) Automatic session management

Both SDKs offer an interface that tracks session state for you across calls, so you don’t pass IDs around manually. Use these for multi-turn conversations within a single process.

### [​](#python-claudesdkclient) Python: `ClaudeSDKClient`

[`ClaudeSDKClient`](/docs/en/agent-sdk/python#claudesdkclient) handles session IDs internally. Each call to `client.query()` automatically continues the same session. Call [`client.receive_response()`](/docs/en/agent-sdk/python#claudesdkclient) to iterate over the messages for the current query. Use the client as an async context manager so connection setup and teardown are handled for you, or call `connect()` and `disconnect()` manually.
This example runs two queries against the same `client`. The first asks the agent to analyze a module; the second asks it to refactor that module. Because both calls go through the same client instance, the second query has full context from the first without any explicit `resume` or session ID:

Python

```
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)


def print_response(message):
    """Print only the human-readable parts of a message."""
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
    elif isinstance(message, ResultMessage):
        cost = (
            f"${message.total_cost_usd:.4f}"
            if message.total_cost_usd is not None
            else "N/A"
        )
        print(f"[done: {message.subtype}, cost: {cost}]")


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Glob", "Grep"],
    )

    async with ClaudeSDKClient(options=options) as client:
        # First query: client captures the session ID internally
        await client.query("Analyze the auth module")
        async for message in client.receive_response():
            print_response(message)

        # Second query: automatically continues the same session
        await client.query("Now refactor it to use JWT")
        async for message in client.receive_response():
            print_response(message)


asyncio.run(main())
```

See the [Python SDK reference](/docs/en/agent-sdk/python#choosing-between-query-and-claudesdkclient) for details on when to use `ClaudeSDKClient` vs the standalone `query()` function.

### [​](#typescript-continue-true) TypeScript: `continue: true`

The TypeScript SDK doesn’t have a session-holding client object like Python’s `ClaudeSDKClient`. Instead, pass `continue: true` on each subsequent `query()` call and the SDK picks up the most recent session in the current directory. No ID tracking required.
This example makes two separate `query()` calls. The first creates a fresh session; the second sets `continue: true`, which tells the SDK to find and resume the most recent session on disk. The agent has full context from the first call:

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// First query: creates a new session
for await (const message of query({
  prompt: "Analyze the auth module",
  options: { allowedTools: ["Read", "Glob", "Grep"] }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}

// Second query: continue: true resumes the most recent session
for await (const message of query({
  prompt: "Now refactor it to use JWT",
  options: {
    continue: true,
    allowedTools: ["Read", "Edit", "Write", "Glob", "Grep"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

The experimental [V2 session API](/docs/en/agent-sdk/typescript-v2-preview), which provided `createSession()` with a `send` / `stream` pattern, was removed in TypeScript Agent SDK 0.3.142. Use the `query()` function and the session options described on this page instead.

## [​](#use-session-options-with-query) Use session options with `query()`

### [​](#capture-the-session-id) Capture the session ID

Resume and fork require a session ID. Read it from the `session_id` field on the result message ([`ResultMessage`](/docs/en/agent-sdk/python#resultmessage) in Python, [`SDKResultMessage`](/docs/en/agent-sdk/typescript#sdkresultmessage) in TypeScript), which is present on every result regardless of success or error. In TypeScript the ID is also available earlier as a direct field on the init `SystemMessage`; in Python it’s nested inside `SystemMessage.data`.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    session_id = None

    async for message in query(
        prompt="Analyze the auth module and suggest improvements",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep"],
        ),
    ):
        if isinstance(message, ResultMessage):
            session_id = message.session_id
            if message.subtype == "success":
                print(message.result)

    print(f"Session ID: {session_id}")
    return session_id


session_id = asyncio.run(main())
```

### [​](#resume-by-id) Resume by ID

Pass a session ID to `resume` to return to that specific session. The agent picks up with full context from wherever the session left off. Common reasons to resume:

* **Follow up on a completed task.** The agent already analyzed something; now you want it to act on that analysis without re-reading files.
* **Recover from a limit.** The first run ended with `error_max_turns` or `error_max_budget_usd` (see [Handle the result](/docs/en/agent-sdk/agent-loop#handle-the-result)); resume with a higher limit.
* **Restart your process.** You captured the ID before shutdown and want to restore the conversation.

This example resumes the session from [Capture the session ID](#capture-the-session-id) with a follow-up prompt. Because you’re resuming, the agent already has the prior analysis in context:

Python

TypeScript

```