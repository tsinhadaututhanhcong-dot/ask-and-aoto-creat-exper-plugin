---
type: Reference
title: Summary instructions
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Summary instructions

When summarizing this conversation, always preserve:
- The current task objective and acceptance criteria
- File paths that have been read or modified
- Test results and error messages
- Decisions made and the reasoning behind them
```

### [​](#keep-context-efficient) Keep context efficient

A few strategies for long-running agents:

* **Use subagents for subtasks.** Each subagent starts with a fresh conversation (no prior message history, though it does load its own system prompt and project-level context like CLAUDE.md). It does not see the parent’s turns, and only its final response returns to the parent as a tool result. The main agent’s context grows by that summary, not by the full subtask transcript. See [What subagents inherit](/docs/en/agent-sdk/subagents#what-subagents-inherit) for details.
* **Be selective with tools.** Every tool definition takes context space. Use the `tools` field on [`AgentDefinition`](/docs/en/agent-sdk/subagents#agentdefinition-configuration) to scope subagents to the minimum set they need.
* **Watch MCP server costs.** [MCP tool search](/docs/en/agent-sdk/mcp#mcp-tool-search) defers MCP tool schemas by default and loads them on demand. When tool search is off, on Vertex AI, or behind a non-first-party `ANTHROPIC_BASE_URL`, each MCP server adds all its tool schemas to every request, so a few servers with many tools can consume significant context before the agent does any work.
* **Use lower effort for routine tasks.** Set [effort](#effort-level) to `"low"` for agents that only need to read files or list directories. This reduces token usage and cost.

For a detailed breakdown of per-feature context costs, see [Understand context costs](/docs/en/features-overview#understand-context-costs).

## [​](#sessions-and-continuity) Sessions and continuity

Each interaction with the SDK creates or continues a session. Capture the session ID from `ResultMessage.session_id` (available in both SDKs) to resume later. The TypeScript SDK also exposes it as a direct field on the init `SystemMessage`; in Python it’s nested in `SystemMessage.data`.
When you resume, the full context from previous turns is restored: files that were read, analysis that was performed, and actions that were taken. You can also fork a session to branch into a different approach without modifying the original.
See [Session management](/docs/en/agent-sdk/sessions) for the full guide on resume, continue, and fork patterns.

In Python, `ClaudeSDKClient` handles session IDs automatically across multiple calls. See the [Python SDK reference](/docs/en/agent-sdk/python#choosing-between-query-and-claudesdkclient) for details.

## [​](#handle-the-result) Handle the result

When the loop ends, the `ResultMessage` tells you what happened and gives you the output. The `subtype` field (available in both SDKs) is the primary way to check termination state.

| Result subtype | What happened | `result` field available? |
| --- | --- | --- |
| `success` | Claude finished the task normally | Yes |
| `error_max_turns` | Hit the `maxTurns` limit before finishing | No |
| `error_max_budget_usd` | Hit the `maxBudgetUsd` limit before finishing | No |
| `error_during_execution` | An error interrupted the loop (for example, an API failure or cancelled request) | No |
| `error_max_structured_output_retries` | No valid structured output was produced within the configured retry limit: every attempt failed validation, or a model fallback retracted the completed output with no successful retry | No |

The `result` field (the final text output) is only present on the `success` variant, so always check the subtype before reading it. All result subtypes carry `total_cost_usd`, `usage`, `num_turns`, and `session_id` so you can track cost and resume even after errors. In Python, `total_cost_usd` and `usage` are typed as optional and may be `None` on some error paths, so guard before formatting them. See [Tracking costs and usage](/docs/en/agent-sdk/cost-tracking) for details on interpreting the `usage` fields.
The result also includes a `stop_reason` field (`string | null` in TypeScript, `str | None` in Python) indicating why the model stopped generating on its final turn. Common values are `end_turn` (model finished normally), `max_tokens` (hit the output token limit), and `refusal` (the model declined the request). On error result subtypes, `stop_reason` carries the value from the last assistant response before the loop ended. To detect refusals, check `stop_reason === "refusal"` (TypeScript) or `stop_reason == "refusal"` (Python). See [`SDKResultMessage`](/docs/en/agent-sdk/typescript#sdkresultmessage) (TypeScript) or [`ResultMessage`](/docs/en/agent-sdk/python#resultmessage) (Python) for the full type.

## [​](#hooks) Hooks

[Hooks](/docs/en/agent-sdk/hooks) are callbacks that fire at specific points in the loop: before a tool runs, after it returns, when the agent finishes, and so on. Some commonly used hooks are:

| Hook | When it fires | Common uses |
| --- | --- | --- |
| `PreToolUse` | Before a tool executes | Validate inputs, block dangerous commands |
| `PostToolUse` | After a tool returns | Audit outputs, trigger side effects |
| `UserPromptSubmit` | When a prompt is sent | Inject additional context into prompts |
| `Stop` | When the agent finishes | Validate the result, save session state |
| `SubagentStart` / `SubagentStop` | When a subagent spawns or completes | Track and aggregate parallel task results |
| `PreCompact` | Before context compaction | Archive full transcript before summarizing |

Hooks run in your application process, not inside the agent’s context window, so they don’t consume context. Hooks can also short-circuit the loop: a `PreToolUse` hook that rejects a tool call prevents it from executing, and Claude receives the rejection message instead.
Both SDKs support all the events above. The TypeScript SDK includes additional events that Python does not yet support. See [Control execution with hooks](/docs/en/agent-sdk/hooks) for the complete event list, per-SDK availability, and the full callback API.

## [​](#put-it-all-together) Put it all together

This example combines the key concepts from this page into a single agent that fixes failing tests. It configures the agent with allowed tools (auto-approved so the agent runs autonomously), project settings, and safety limits on turns and reasoning effort. As the loop runs, it captures the session ID for potential resumption, handles the final result, and prints the total cost.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def run_agent():
    session_id = None

    async for message in query(
        prompt="Find and fix the bug causing test failures in the auth module",
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
            ],  # Listing tools here auto-approves them (no prompting)
            setting_sources=[
                "project"
            ],  # Load CLAUDE.md, skills, hooks from current directory
            max_turns=30,  # Prevent runaway sessions
            effort="high",  # Thorough reasoning for complex debugging
        ),
    ):
        # Handle the final result
        if isinstance(message, ResultMessage):
            session_id = message.session_id  # Save for potential resumption

            if message.subtype == "success":
                print(f"Done: {message.result}")
            elif message.subtype == "error_max_turns":
                # Agent ran out of turns. Resume with a higher limit.
                print(f"Hit turn limit. Resume session {session_id} to continue.")
            elif message.subtype == "error_max_budget_usd":
                print("Hit budget limit.")
            else:
                print(f"Stopped: {message.subtype}")
            if message.total_cost_usd is not None:
                print(f"Cost: ${message.total_cost_usd:.4f}")


asyncio.run(run_agent())
```

## [​](#next-steps) Next steps

Now that you understand the loop, here’s where to go depending on what you’re building:

* **Haven’t run an agent yet?** Start with the [quickstart](/docs/en/agent-sdk/quickstart) to get the SDK installed and see a full example running end to end.
* **Ready to hook into your project?** [Load CLAUDE.md, skills, and filesystem hooks](/docs/en/agent-sdk/claude-code-features) so the agent follows your project conventions automatically.
* **Building an interactive UI?** Enable [streaming](/docs/en/agent-sdk/streaming-output) to show live text and tool calls as the loop runs.
* **Need tighter control over what the agent can do?** Lock down tool access with [permissions](/docs/en/agent-sdk/permissions), and use [hooks](/docs/en/agent-sdk/hooks) to audit, block, or transform tool calls before they execute.
* **Running long or expensive tasks?** Offload isolated work to [subagents](/docs/en/agent-sdk/subagents) to keep your main context lean.

For the broader conceptual picture of the agentic loop (not SDK-specific), see [How Claude Code works](/docs/en/how-claude-code-works).

Was this page helpful?

YesNo

[Quickstart](/docs/en/agent-sdk/quickstart)[Use Claude Code features](/docs/en/agent-sdk/claude-code-features)

⌘I

---