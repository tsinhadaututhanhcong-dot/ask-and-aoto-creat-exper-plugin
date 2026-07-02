---
title: Handle approvals and user input - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Handle approvals and user input - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/user-input](https://code.claude.com/docs/en/agent-sdk/user-input)

While working on a task, Claude sometimes needs to check in with users. It might need permission before deleting files, or need to ask which database to use for a new project. Your application needs to surface these requests to users so Claude can continue with their input.
Claude requests user input in two situations: when it needs **permission to use a tool** (like deleting files or running commands), and when it has **clarifying questions** (via the `AskUserQuestion` tool). Both trigger your `canUseTool` callback, which pauses execution until you return a response. This is different from normal conversation turns where Claude finishes and waits for your next message.
For clarifying questions, Claude generates the questions and options. Your role is to present them to users and return their selections. You can’t add your own questions to this flow; if you need to ask users something yourself, do that separately in your application logic.
The callback can stay pending indefinitely. Execution remains paused until your callback returns, and the SDK only cancels the wait when the query itself is cancelled. If a user might take longer to respond than your process can reasonably stay running, return the [`defer` hook decision](/docs/en/hooks#defer-a-tool-call-for-later), which lets the process exit and resume later from the persisted session.
This guide shows you how to detect each type of request and respond appropriately.

## [​](#detect-when-claude-needs-input) Detect when Claude needs input

Pass a `canUseTool` callback in your query options. The callback fires whenever Claude needs user input, receiving the tool name and input as arguments:

Python

TypeScript

```
async def handle_tool_request(tool_name, input_data, context):
    # Prompt user and return allow or deny
    ...


options = ClaudeAgentOptions(can_use_tool=handle_tool_request)
```

The callback fires in two cases:

1. **Tool needs approval**: Claude wants to use a tool that isn’t auto-approved by [permission rules](/docs/en/agent-sdk/permissions) or modes. Check `tool_name` for the tool (e.g., `"Bash"`, `"Write"`).
2. **Claude asks a question**: Claude calls the `AskUserQuestion` tool. Check if `tool_name == "AskUserQuestion"` to handle it differently. If you specify a `tools` array, include `AskUserQuestion` for this to work. See [Handle clarifying questions](#handle-clarifying-questions) for details.

To automatically allow or deny tools without prompting users, use [hooks](/docs/en/agent-sdk/hooks) instead. Hooks execute before `canUseTool` and can allow, deny, or modify requests based on your own logic. You can also use the [`PermissionRequest` hook](/docs/en/agent-sdk/hooks#available-hooks) to send external notifications (Slack, email, push) when Claude is waiting for approval.

## [​](#handle-tool-approval-requests) Handle tool approval requests

Once you’ve passed a `canUseTool` callback in your query options, it fires when Claude wants to use a tool that isn’t auto-approved. Your callback receives three arguments:

| Argument | Description |
| --- | --- |
| `toolName` | The name of the tool Claude wants to use (e.g., `"Bash"`, `"Write"`, `"Edit"`) |
| `input` | The parameters Claude is passing to the tool. Contents vary by tool. |
| `options` (TS) / `context` (Python) | Additional context including optional `suggestions` (proposed `PermissionUpdate` entries to avoid re-prompting) and a cancellation signal. In TypeScript, `signal` is an `AbortSignal`; in Python, the signal field is reserved for future use. See [`ToolPermissionContext`](/docs/en/agent-sdk/python#toolpermissioncontext) for Python. |

The `input` object contains tool-specific parameters. Common examples:

| Tool | Input fields |
| --- | --- |
| `Bash` | `command`, `description`, `timeout` |
| `Write` | `file_path`, `content` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Read` | `file_path`, `offset`, `limit` |

See the SDK reference for complete input schemas: [Python](/docs/en/agent-sdk/python#tool-input%2Foutput-types) | [TypeScript](/docs/en/agent-sdk/typescript#tool-input-types).
You can display this information to the user so they can decide whether to allow or reject the action, then return the appropriate response.
The following example asks Claude to create and delete a test file. When Claude attempts each operation, the callback prints the tool request to the terminal and prompts for y/n approval.

Python

TypeScript

```
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from claude_agent_sdk.types import (
    HookMatcher,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


async def can_use_tool(
    tool_name: str, input_data: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Display the tool request
    print(f"\nTool: {tool_name}")
    if tool_name == "Bash":
        print(f"Command: {input_data.get('command')}")
        if input_data.get("description"):
            print(f"Description: {input_data.get('description')}")
    else:
        print(f"Input: {input_data}")

    # Get user approval
    response = input("Allow this action? (y/n): ")

    # Return allow or deny based on user's response
    if response.lower() == "y":
        # Allow: tool executes with the original (or modified) input
        return PermissionResultAllow(updated_input=input_data)
    else:
        # Deny: tool doesn't execute, Claude sees the message
        return PermissionResultDeny(message="User denied this action")