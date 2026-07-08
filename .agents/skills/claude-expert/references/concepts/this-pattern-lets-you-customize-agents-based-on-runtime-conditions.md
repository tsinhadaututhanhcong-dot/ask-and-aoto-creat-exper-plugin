---
type: Reference
title: This pattern lets you customize agents based on runtime conditions
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# This pattern lets you customize agents based on runtime conditions
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        # Customize the prompt based on strictness level
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        # Key insight: use a more capable model for high-stakes reviews
        model="opus" if is_strict else "sonnet",
    )


async def main():
    # The agent is created at query time, so each request can use different settings
    async for message in query(
        prompt="Review this PR for security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                # Call the factory with your desired configuration
                "security-reviewer": create_security_agent("strict")
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

## [​](#detecting-subagent-invocation) Detecting subagent invocation

Subagents are invoked via the Agent tool. To detect when a subagent is invoked, check for `tool_use` blocks where `name` is `"Agent"`. Messages from within a subagent’s context include a `parent_tool_use_id` field.

The tool name was renamed from `"Task"` to `"Agent"` in Claude Code v2.1.63. Current SDK releases emit `"Agent"` in `tool_use` blocks but still use `"Task"` in the `system:init` tools list and in `result.permission_denials[].tool_name`. Checking both values in `block.name` ensures compatibility across SDK versions.

The message structure differs between SDKs. In Python, content blocks are accessed directly via `message.content`. In TypeScript, `SDKAssistantMessage` wraps the Claude API message, so content is accessed via `message.message.content`.
This example iterates through streamed messages, logging when a subagent is invoked and when subsequent messages originate from within that subagent’s execution context.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ToolUseBlock


async def main():
    async for message in query(
        prompt="Use the code-reviewer agent to review this codebase",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer.",
                    prompt="Analyze code quality and suggest improvements.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        # Check for subagent invocation. Match both names: older SDK
        # versions emitted "Task", current versions emit "Agent".
        if hasattr(message, "content") and message.content:
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in (
                    "Task",
                    "Agent",
                ):
                    print(f"Subagent invoked: {block.input.get('subagent_type')}")

        # Check if this message is from within a subagent's context
        if hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id:
            print("  (running inside subagent)")

        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

## [​](#resuming-subagents) Resuming subagents

Subagents can be resumed to continue where they left off. Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.
When a subagent completes, the Agent tool result includes a text block containing `agentId: <id>`. The built-in [`Explore` and `Plan` agents](/docs/en/sub-agents#built-in-subagents) are one-shot and do not return an `agentId`, so use a custom agent or `general-purpose` when you need to resume. To resume a subagent programmatically:

1. **Capture the session ID**: Extract `session_id` from messages during the first query
2. **Extract the agent ID**: Parse `agentId` from the Agent tool result text
3. **Resume the session**: Pass `resume: sessionId` in the second query’s options, and include the agent ID in your prompt

You must resume the same session to access the subagent’s transcript. Each `query()` call starts a new session by default, so pass `resume: sessionId` to continue in the same session.When using a custom agent, pass the same agent definition in the `agents` parameter for both queries.

The example below defines a custom `endpoint-finder` agent. The first query runs it and captures the session ID and agent ID from the Agent tool result, then the second query resumes the session to ask a follow-up question that requires context from the first analysis.

Python

TypeScript

```
import asyncio
import re
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ToolResultBlock

AGENTS = {
    "endpoint-finder": AgentDefinition(
        description="Locates and catalogs API endpoints in a codebase.",
        prompt="You find and document API endpoints. Report each endpoint's path, method, and handler.",
        tools=["Read", "Grep", "Glob"],
    )
}


def extract_agent_id(block: ToolResultBlock) -> str | None:
    """Extract agentId from an Agent tool result's text content."""
    parts = block.content if isinstance(block.content, list) else [{"text": block.content}]
    for part in parts:
        if match := re.search(r"agentId:\s*([\w-]+)", part.get("text") or ""):
            return match.group(1)
    return None


async def main():
    agent_id = None
    session_id = None

    # First invocation - run the endpoint-finder subagent
    try:
        async for message in query(
            prompt="Use the endpoint-finder agent to find all API endpoints in this codebase",
            options=ClaudeAgentOptions(allowed_tools=["Read", "Grep", "Glob", "Agent"], agents=AGENTS),
        ):
            # Capture session_id from ResultMessage (needed to resume this session)
            if hasattr(message, "session_id"):
                session_id = message.session_id
            # Search tool results for the agentId trailer
            for block in getattr(message, "content", None) or []:
                if isinstance(block, ToolResultBlock):
                    agent_id = extract_agent_id(block) or agent_id
            # Print the final result
            if hasattr(message, "result"):
                print(message.result)
    except Exception as error:
        # A single-shot query() raises after yielding an error result,
        # so session_id and agent_id have already been captured by the loop above.
        print(f"Session ended with an error: {error}")

    # Second invocation - resume and ask follow-up
    if agent_id and session_id:
        async for message in query(
            prompt=f"Resume agent {agent_id} and list the top 3 most complex endpoints",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Grep", "Glob", "Agent"], agents=AGENTS, resume=session_id
            ),
        ):
            if hasattr(message, "result"):
                print(message.result)
    else:
        print("No agentId found in the first query, so there is no subagent to resume.")


asyncio.run(main())
```

Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: When the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.
* **Session persistence**: Subagent transcripts persist within their session. You can resume a subagent after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: Transcripts are cleaned up based on the `cleanupPeriodDays` setting (default: 30 days).

## [​](#tool-restrictions-2) Tool restrictions

Subagents can have restricted tool access via the `tools` field:

* **Omit the field**: agent inherits all available tools (default)
* **Specify tools**: agent can only use listed tools

This example creates a read-only analysis agent that can examine code but cannot modify files or run commands.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


async def main():
    async for message in query(
        prompt="Analyze the architecture of this codebase",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "code-analyzer": AgentDefinition(
                    description="Static code analysis and architecture review",
                    prompt="""You are a code architecture analyst. Analyze code structure,
identify patterns, and suggest improvements without making changes.""",
                    # Read-only tools: no Edit, Write, or Bash access
                    tools=["Read", "Grep", "Glob"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

### [​](#common-tool-combinations) Common tool combinations

| Use case | Tools | Description |
| --- | --- | --- |
| Read-only analysis | `Read`, `Grep`, `Glob` | Can examine code but not modify or execute |
| Test execution | `Bash`, `Read`, `Grep` | Can run commands and analyze output |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` | Full read/write access without command execution |
| Full access | All tools | Inherits all tools from parent (omit `tools` field) |

## [​](#scale-up-with-dynamic-workflows) Scale up with dynamic workflows

Subagents work well for a few delegated tasks per turn. For runs that coordinate dozens to hundreds of agents, use the `Workflow` tool, which moves the orchestration into a script the runtime executes outside the conversation context. See [dynamic workflows](/docs/en/workflows) for how workflows differ from turn-by-turn subagent delegation.
The `Workflow` tool is available in the TypeScript Agent SDK v0.3.149 and later. Include `Workflow` in `allowedTools` to auto-approve workflow runs. The tool input and output schemas are listed in the [TypeScript reference](/docs/en/agent-sdk/typescript#workflow).

## [​](#troubleshooting) Troubleshooting

### [​](#claude-not-delegating-to-subagents) Claude not delegating to subagents

If Claude completes tasks directly instead of delegating to your subagent:

1. **Check Agent invocations are approved**: include `Agent` in `allowedTools` to auto-approve subagent calls. Without it, Agent invocations fall through to your `canUseTool` callback or, in `dontAsk` mode, are denied
2. **Use explicit prompting**: mention the subagent by name in your prompt (for example, “Use the code-reviewer agent to…”)
3. **Write a clear description**: explain exactly when the subagent should be used so Claude can match tasks appropriately

### [​](#filesystem-based-agents-not-loading) Filesystem-based agents not loading

Agents defined in `.claude/agents/` are loaded at startup only. If you create a new agent file while Claude Code is running, restart the session to load it.

### [​](#windows-long-prompt-failures) Windows: long prompt failures

On Windows, subagents with very long prompts may fail due to command line length limits (8191 chars). Keep prompts concise or use filesystem-based agents for complex instructions.

## [​](#related-documentation) Related documentation

* [Claude Code subagents](/docs/en/sub-agents): comprehensive subagent documentation including filesystem-based definitions
* [Dynamic workflows](/docs/en/workflows): orchestrate many subagents from a script for jobs too large for one conversation
* [SDK overview](/docs/en/agent-sdk/overview): getting started with the Claude Agent SDK

Was this page helpful?

YesNo

[Scale to many tools with tool search](/docs/en/agent-sdk/tool-search)[Modifying system prompts](/docs/en/agent-sdk/modifying-system-prompts)

⌘I

---