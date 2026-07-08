---
type: Reference
title: Agent SDK reference - Python - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Agent SDK reference - Python - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/python](https://code.claude.com/docs/en/agent-sdk/python)

## [​](#installation) Installation

```
pip install claude-agent-sdk
```

## [​](#choosing-between-query-and-claudesdkclient) Choosing between `query()` and `ClaudeSDKClient`

The Python SDK provides two ways to interact with Claude Code:

### [​](#quick-comparison) Quick comparison

| Feature | `query()` | `ClaudeSDKClient` |
| --- | --- | --- |
| **Session** | Creates a new session by default | Reuses same session |
| **Conversation** | Single exchange | Multiple exchanges in same context |
| **Connection** | Managed automatically | Manual control |
| **Streaming Input** | ✅ Supported | ✅ Supported |
| **Interrupts** | ❌ Not supported | ✅ Supported |
| **Hooks** | ✅ Supported | ✅ Supported |
| **Custom Tools** | ✅ Supported | ✅ Supported |
| **Continue Chat** | Manual via `continue_conversation` or `resume` | ✅ Automatic |
| **Use Case** | One-off tasks | Continuous conversations |

### [​](#when-to-use-query-one-off-tasks) When to use `query()` (one-off tasks)

**Best for:**

* One-off questions where you don’t need conversation history
* Independent tasks that don’t require context from previous exchanges
* Simple automation scripts
* When you want a fresh start each time

### [​](#when-to-use-claudesdkclient-continuous-conversation) When to use `ClaudeSDKClient` (continuous conversation)

**Best for:**

* **Continuing conversations** - When you need Claude to remember context
* **Follow-up questions** - Building on previous responses
* **Interactive applications** - Chat interfaces, REPLs
* **Response-driven logic** - When next action depends on Claude’s response
* **Session control** - Managing conversation lifecycle explicitly

## [​](#functions) Functions

### [​](#query) `query()`

Creates a new session for each interaction with Claude Code by default. Returns an async iterator that yields messages as they arrive. Each call to `query()` starts fresh with no memory of previous interactions unless you pass `continue_conversation=True` or `resume` in [`ClaudeAgentOptions`](#claudeagentoptions). See [Sessions](/docs/en/agent-sdk/sessions).

```
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None
) -> AsyncIterator[Message]
```

#### [​](#parameters) Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `prompt` | `str | AsyncIterable[dict]` | The input prompt as a string or async iterable for streaming mode |
| `options` | `ClaudeAgentOptions | None` | Optional configuration object (defaults to `ClaudeAgentOptions()` if None) |
| `transport` | `Transport | None` | Optional custom transport for communicating with the CLI process |

#### [​](#returns) Returns

Returns an `AsyncIterator[Message]` that yields messages from the conversation.

#### [​](#example-with-options) Example - With options

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode="acceptEdits",
        cwd="/home/user/project",
    )

    async for message in query(prompt="Create a Python web server", options=options):
        print(message)


asyncio.run(main())
```

### [​](#tool) `tool()`

Decorator for defining MCP tools with type safety.

```
def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any],
    annotations: ToolAnnotations | None = None
) -> Callable[[Callable[[Any], Awaitable[dict[str, Any]]]], SdkMcpTool[Any]]
```

#### [​](#parameters-2) Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `str` | Unique identifier for the tool |
| `description` | `str` | Human-readable description of what the tool does |
| `input_schema` | `type | dict[str, Any]` | Schema defining the tool’s input parameters (see below) |
| `annotations` | [`ToolAnnotations`](#toolannotations) `| None` | Optional MCP tool annotations providing behavioral hints to clients |

#### [​](#input-schema-options) Input schema options

1. **Simple type mapping** (recommended):

   ```
   {"text": str, "count": int, "enabled": bool}
   ```
2. **JSON Schema format** (for complex validation):

   ```
   {
       "type": "object",
       "properties": {
           "text": {"type": "string"},
           "count": {"type": "integer", "minimum": 0},
       },
       "required": ["text"],
   }
   ```

#### [​](#returns-2) Returns

A decorator function that wraps the tool implementation and returns an `SdkMcpTool` instance.

#### [​](#example) Example

```
from claude_agent_sdk import tool
from typing import Any


@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}
```

#### [​](#toolannotations) `ToolAnnotations`

Re-exported from `mcp.types` (also available as `from claude_agent_sdk import ToolAnnotations`). All fields are optional hints; clients should not rely on them for security decisions.

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `str | None` | `None` | Human-readable title for the tool |
| `readOnlyHint` | `bool | None` | `False` | If `True`, the tool does not modify its environment |
| `destructiveHint` | `bool | None` | `True` | If `True`, the tool may perform destructive updates (only meaningful when `readOnlyHint` is `False`) |
| `idempotentHint` | `bool | None` | `False` | If `True`, repeated calls with the same arguments have no additional effect (only meaningful when `readOnlyHint` is `False`) |
| `openWorldHint` | `bool | None` | `True` | If `True`, the tool interacts with external entities (for example, web search). If `False`, the tool’s domain is closed (for example, a memory tool) |

```
from claude_agent_sdk import tool, ToolAnnotations
from typing import Any


@tool(
    "search",
    "Search the web",
    {"query": str},
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
)
async def search(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Results for: {args['query']}"}]}
```

### [​](#create_sdk_mcp_server) `create_sdk_mcp_server()`

Create an in-process MCP server that runs within your Python application.

```
def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: list[SdkMcpTool[Any]] | None = None
) -> McpSdkServerConfig
```

#### [​](#parameters-3) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `name` | `str` | - | Unique identifier for the server |
| `version` | `str` | `"1.0.0"` | Server version string |
| `tools` | `list[SdkMcpTool[Any]] | None` | `None` | List of tool functions created with `@tool` decorator |

#### [​](#returns-3) Returns

Returns an `McpSdkServerConfig` object that can be passed to `ClaudeAgentOptions.mcp_servers`.

#### [​](#example-2) Example

```
from claude_agent_sdk import tool, create_sdk_mcp_server


@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}


@tool("multiply", "Multiply two numbers", {"a": float, "b": float})
async def multiply(args):
    return {"content": [{"type": "text", "text": f"Product: {args['a'] * args['b']}"}]}


calculator = create_sdk_mcp_server(
    name="calculator",
    version="2.0.0",
    tools=[add, multiply],  # Pass decorated functions
)