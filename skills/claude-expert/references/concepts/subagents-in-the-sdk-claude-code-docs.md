---
type: Reference
title: Subagents in the SDK - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Subagents in the SDK - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

Subagents are separate agent instances that your main agent can spawn to handle focused subtasks.
Use subagents to isolate context for focused subtasks, run multiple analyses in parallel, and apply specialized instructions without adding to the main agent’s prompt.
This guide explains how to define and use subagents in the SDK using the `agents` parameter.

## [​](#overview) Overview

You can create subagents in three ways:

* **Programmatically**: use the `agents` parameter in your `query()` options ([TypeScript](/docs/en/agent-sdk/typescript#agentdefinition), [Python](/docs/en/agent-sdk/python#agentdefinition))
* **Filesystem-based**: define agents as markdown files in `.claude/agents/` directories (see [defining subagents as files](/docs/en/sub-agents))
* **Built-in general-purpose**: Claude can invoke the built-in `general-purpose` subagent at any time via the Agent tool without you defining anything

This guide focuses on the programmatic approach, which is recommended for SDK applications.
When you define subagents, Claude determines whether to invoke them based on each subagent’s `description` field. Write clear descriptions that explain when the subagent should be used, and Claude will automatically delegate appropriate tasks. You can also explicitly request a subagent by name in your prompt (for example, “Use the code-reviewer agent to…”).

## [​](#benefits-of-using-subagents) Benefits of using subagents

### [​](#context-isolation) Context isolation

Each subagent runs in its own fresh conversation. Intermediate tool calls and results stay inside the subagent; only its final message returns to the parent. See [What subagents inherit](#what-subagents-inherit) for exactly what’s in the subagent’s context.
**Example:** a `research-assistant` subagent can explore dozens of files without any of that content accumulating in the main conversation. The parent receives a concise summary, not every file the subagent read.

### [​](#parallelization) Parallelization

Multiple subagents can run concurrently, so independent subtasks finish in the time of the slowest one rather than the sum of all of them.
**Example:** during a code review, you can run `style-checker`, `security-scanner`, and `test-coverage` subagents simultaneously instead of sequentially.

### [​](#specialized-instructions-and-knowledge) Specialized instructions and knowledge

Each subagent can have tailored system prompts with specific expertise, best practices, and constraints.
**Example:** a `database-migration` subagent can have detailed knowledge about SQL best practices, rollback strategies, and data integrity checks that would be unnecessary noise in the main agent’s instructions.

### [​](#tool-restrictions) Tool restrictions

Subagents can be limited to specific tools, reducing the risk of unintended actions.
**Example:** a `doc-reviewer` subagent might only have access to Read and Grep tools, ensuring it can analyze but never accidentally modify your documentation files.

## [​](#creating-subagents) Creating subagents

### [​](#programmatic-definition-recommended) Programmatic definition (recommended)

Define subagents directly in your code using the `agents` parameter. This example creates two subagents: a code reviewer with read-only access and a test runner that can execute commands. Claude invokes subagents through the `Agent` tool, so include `Agent` in `allowedTools` to auto-approve subagent invocations without a permission prompt.
Most examples on this page print only the final result. To confirm that Claude delegated to a subagent rather than answering directly, see [Detecting subagent invocation](#detecting-subagent-invocation).

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Auto-approve these tools, including Agent for subagent invocation
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    # description tells Claude when to use this subagent
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    # prompt defines the subagent's behavior and expertise
                    prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
                    # tools restricts what the subagent can do (read-only here)
                    tools=["Read", "Grep", "Glob"],
                    # model overrides the default model for this subagent
                    model="sonnet",
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
                    prompt="""You are a test execution specialist. Run tests and provide clear analysis of results.

Focus on:
- Running test commands
- Analyzing test output
- Identifying failing tests
- Suggesting fixes for failures""",
                    # Bash access lets this subagent run test commands
                    tools=["Bash", "Read", "Grep"],
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

### [​](#agentdefinition-configuration) AgentDefinition configuration

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `description` | `string` | Yes | Natural language description of when to use this agent |
| `prompt` | `string` | Yes | The agent’s system prompt defining its role and behavior |
| `tools` | `string[]` | No | Array of allowed tool names. If omitted, inherits all tools |
| `disallowedTools` | `string[]` | No | Array of tool names to remove from the agent’s tool set. MCP server-level patterns are also accepted: `mcp__server` or `mcp__server__*` removes every tool from that server, and `mcp__*` removes every MCP tool from any server |
| `model` | `string` | No | Model override for this agent. Accepts an alias such as `'fable'`, `'opus'`, `'sonnet'`, `'haiku'`, `'inherit'`, or a full model ID. Defaults to main model if omitted |
| `skills` | `string[]` | No | List of skill names to preload into the agent’s context at startup. Unlisted skills remain invocable through the Skill tool |
| `memory` | `'user' | 'project' | 'local'` | No | Memory source for this agent |
| `mcpServers` | `(string | object)[]` | No | MCP servers available to this agent, by name or inline config |
| `initialPrompt` | `string` | No | Auto-submitted as the first user turn when this agent runs as the main thread agent. Ignored when the agent is invoked as a subagent |
| `maxTurns` | `number` | No | Maximum number of agentic turns before the agent stops |
| `background` | `boolean` | No | Run this agent as a non-blocking background task when invoked |
| `effort` | `'low' | 'medium' | 'high' | 'xhigh' | 'max' | number` | No | Reasoning effort level for this agent |
| `permissionMode` | `PermissionMode` | No | Permission mode for tool execution within this agent |

In the Python SDK, multi-word field names such as `disallowedTools` and `mcpServers` keep their camelCase spelling to match the wire format rather than following Python’s snake\_case convention. See the [`AgentDefinition` reference](/docs/en/agent-sdk/python#agentdefinition) for details.

As of Claude Code v2.1.172, subagents can spawn their own subagents. A subagent five levels below the main agent cannot spawn further subagents, regardless of whether it runs in the foreground or background. To prevent a subagent from spawning others, omit `Agent` from its `tools` array or add it to `disallowedTools`. See [nested subagents](/docs/en/sub-agents#spawn-nested-subagents) for the full depth rules.

### [​](#filesystem-based-definition-alternative) Filesystem-based definition (alternative)

You can also define subagents as markdown files in `.claude/agents/` directories. See the [Claude Code subagents documentation](/docs/en/sub-agents) for details on this approach. Programmatically defined agents take precedence over filesystem-based agents with the same name.

Even without defining custom subagents, Claude can spawn the built-in `general-purpose` subagent. This is useful for delegating research or exploration tasks without creating specialized agents. Include `Agent` in `allowedTools` so these invocations auto-approve without a permission prompt.

## [​](#what-subagents-inherit) What subagents inherit

A subagent’s context window starts fresh (no parent conversation) but isn’t empty. The only channel from parent to subagent is the Agent tool’s prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt.

| The subagent receives | The subagent does not receive |
| --- | --- |
| Its own system prompt (`AgentDefinition.prompt`) and the Agent tool’s prompt | The parent’s conversation history or tool results |
| Project CLAUDE.md (loaded via [`settingSources`](/docs/en/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources)) | Preloaded skill content, unless listed in `AgentDefinition.skills` |
| Tool definitions (inherited from parent, or the subset in `tools`) | The parent’s system prompt |

The parent receives the subagent’s final message verbatim as the Agent tool result, but may summarize it in its own response. To preserve subagent output verbatim in the user-facing response, include an instruction to do so in the prompt or `systemPrompt` option you pass to the **main** `query()` call.

## [​](#invoking-subagents) Invoking subagents

### [​](#automatic-invocation) Automatic invocation

Claude automatically decides when to invoke subagents based on the task and each subagent’s `description`. For example, if you define a `performance-optimizer` subagent with the description “Performance optimization specialist for query tuning”, Claude will invoke it when your prompt mentions optimizing queries.
Write clear, specific descriptions so Claude can match tasks to the right subagent.

### [​](#explicit-invocation) Explicit invocation

To guarantee Claude uses a specific subagent, mention it by name in your prompt:

```
"Use the code-reviewer agent to check the authentication module"
```

This bypasses automatic matching and directly invokes the named subagent.

### [​](#dynamic-agent-configuration) Dynamic agent configuration

You can create agent definitions dynamically based on runtime conditions. This example creates a security reviewer with different strictness levels, using a more powerful model for strict reviews.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition