---
title: Intercept and control agent behavior with hooks - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Intercept and control agent behavior with hooks - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

Hooks are callback functions that run your code in response to agent events, like a tool being called, a session starting, or execution stopping. With hooks, you can:

* **Block dangerous operations** before they execute, like destructive shell commands or unauthorized file access
* **Log and audit** every tool call for compliance, debugging, or analytics
* **Transform inputs and outputs** to sanitize data, inject credentials, or redirect file paths
* **Require human approval** for sensitive actions like database writes or API calls
* **Track session lifecycle** to manage state, clean up resources, or send notifications

This guide covers how hooks work and how to configure them, with examples for common patterns like blocking tools, modifying inputs, and forwarding notifications.

## [​](#how-hooks-work) How hooks work

1

An event fires

Something happens during agent execution and the SDK fires an event: a tool is about to be called (`PreToolUse`), a tool returned a result (`PostToolUse`), a subagent started or stopped, the agent is idle, or execution finished. See the [full list of events](#available-hooks).

2

The SDK collects registered hooks

The SDK checks for hooks registered for that event type. This includes callback hooks you pass in `options.hooks` and shell command hooks from settings files when the corresponding [`settingSources`](/docs/en/agent-sdk/typescript#settingsource) or [`setting_sources`](/docs/en/agent-sdk/python#settingsource) entry is enabled, which it is for default `query()` options.

3

Matchers filter which hooks run

If a hook has a [`matcher`](#matchers) pattern (like `"Write|Edit"`), the SDK tests it against the event’s target (for example, the tool name). Hooks without a matcher run for every event of that type.

4

Callback functions execute

Each matching hook’s [callback function](#callback-functions) receives input about what’s happening: the tool name, its arguments, the session ID, and other event-specific details.

5

Your callback returns a decision

After performing any operations (logging, API calls, validation), your callback returns an [output object](#outputs) that tells the agent what to do: allow the operation, block it, modify the input, or inject context into the conversation.

The following example puts these steps together. It registers a `PreToolUse` hook (step 1) with a `"Write|Edit"` matcher (step 3) so the callback only fires for file-writing tools. When triggered, the callback receives the tool’s input (step 4), checks if the file path targets a `.env` file, and returns `permissionDecision: "deny"` to block the operation (step 5):

Python

TypeScript

```
import asyncio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
)