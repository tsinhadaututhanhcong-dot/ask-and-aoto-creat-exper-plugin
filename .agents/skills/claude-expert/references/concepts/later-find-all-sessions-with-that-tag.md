---
title: Later: find all sessions with that tag
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Later: find all sessions with that tag
for session in list_sessions(directory="/path/to/project"):
    if session.tag == "needs-review":
        print(session.summary)
```

## [​](#classes) Classes

### [​](#claudesdkclient) `ClaudeSDKClient`

**Maintains a conversation session across multiple exchanges.** This is the Python equivalent of how the TypeScript SDK’s `query()` function works internally - it creates a client object that can continue conversations.

#### [​](#key-features) Key Features

* **Session continuity**: Maintains conversation context across multiple `query()` calls
* **Same conversation**: The session retains previous messages
* **Interrupt support**: Can stop execution mid-task
* **Explicit lifecycle**: You control when the session starts and ends
* **Response-driven flow**: Can react to responses and send follow-ups
* **Custom tools and hooks**: Supports custom tools (created with `@tool` decorator) and hooks

```
class ClaudeSDKClient:
    def __init__(self, options: ClaudeAgentOptions | None = None, transport: Transport | None = None)
    async def connect(self, prompt: str | AsyncIterable[dict] | None = None) -> None
    async def query(self, prompt: str | AsyncIterable[dict], session_id: str = "default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def set_permission_mode(self, mode: str) -> None
    async def set_model(self, model: str | None = None) -> None
    async def rewind_files(self, user_message_id: str) -> None
    async def get_mcp_status(self) -> McpStatusResponse
    async def reconnect_mcp_server(self, server_name: str) -> None
    async def toggle_mcp_server(self, server_name: str, enabled: bool) -> None
    async def stop_task(self, task_id: str) -> None
    async def get_server_info(self) -> dict[str, Any] | None
    async def disconnect(self) -> None
```

#### [​](#methods) Methods

| Method | Description |
| --- | --- |
| `__init__(options)` | Initialize the client with optional configuration |
| `connect(prompt)` | Connect to Claude with an optional initial prompt or message stream |
| `query(prompt, session_id)` | Send a new request in streaming mode |
| `receive_messages()` | Receive all messages from Claude as an async iterator |
| `receive_response()` | Receive messages until and including a ResultMessage |
| `interrupt()` | Send interrupt signal (only works in streaming mode) |
| `set_permission_mode(mode)` | Change the permission mode for the current session |
| `set_model(model)` | Change the model for the current session. Pass `None` to reset to default |
| `rewind_files(user_message_id)` | Restore files to their state at the specified user message. Requires `enable_file_checkpointing=True`. See [File checkpointing](/docs/en/agent-sdk/file-checkpointing) |
| `get_mcp_status()` | Get the status of all configured MCP servers. Returns [`McpStatusResponse`](#mcpstatusresponse) |
| `reconnect_mcp_server(server_name)` | Retry connecting to an MCP server that failed or was disconnected |
| `toggle_mcp_server(server_name, enabled)` | Enable or disable an MCP server mid-session. Disabling removes its tools |
| `stop_task(task_id)` | Stop a running background task. A [`TaskNotificationMessage`](#tasknotificationmessage) with status `"stopped"` follows in the message stream |
| `get_server_info()` | Get server information including session ID and capabilities |
| `disconnect()` | Disconnect from Claude |

#### [​](#context-manager-support) Context Manager Support

The client can be used as an async context manager for automatic connection management:

```
async with ClaudeSDKClient() as client:
    await client.query("Hello Claude")
    async for message in client.receive_response():
        print(message)
```

> **Important:** When iterating over messages, avoid using `break` to exit early as this can cause asyncio cleanup issues. Instead, let the iteration complete naturally or use flags to track when you’ve found what you need.

#### [​](#example-continuing-a-conversation) Example - Continuing a conversation

```
import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage


async def main():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")

        # Process response
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up question - the session retains the previous context
        await client.query("What's the population of that city?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Another follow-up - still in the same conversation
        await client.query("What are some famous landmarks there?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")


asyncio.run(main())
```

#### [​](#example-streaming-input-with-claudesdkclient) Example - Streaming input with ClaudeSDKClient

```
import asyncio
from claude_agent_sdk import ClaudeSDKClient


async def message_stream():
    """Generate messages dynamically."""
    yield {
        "type": "user",
        "message": {"role": "user", "content": "Analyze the following data:"},
    }
    await asyncio.sleep(0.5)
    yield {
        "type": "user",
        "message": {"role": "user", "content": "Temperature: 25°C, Humidity: 60%"},
    }
    await asyncio.sleep(0.5)
    yield {
        "type": "user",
        "message": {"role": "user", "content": "What patterns do you see?"},
    }


async def main():
    async with ClaudeSDKClient() as client:
        # Stream input to Claude
        await client.query(message_stream())

        # Process response
        async for message in client.receive_response():
            print(message)

        # Follow-up in same session
        await client.query("Should we be concerned about these readings?")

        async for message in client.receive_response():
            print(message)


asyncio.run(main())
```

#### [​](#example-using-interrupts) Example - Using interrupts

```
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ResultMessage


async def interruptible_task():
    options = ClaudeAgentOptions(allowed_tools=["Bash"], permission_mode="acceptEdits")

    async with ClaudeSDKClient(options=options) as client:
        # Start a long-running task
        await client.query("Count from 1 to 100 slowly, using the bash sleep command")

        # Let it run for a bit
        await asyncio.sleep(2)

        # Interrupt the task
        await client.interrupt()
        print("Task interrupted!")

        # Drain the interrupted task's messages (including its ResultMessage)
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                print(f"Interrupted task finished with subtype={message.subtype!r}")
                # subtype is "error_during_execution" for interrupted tasks

        # Send a new command
        await client.query("Just say hello instead")

        # Now receive the new response
        async for message in client.receive_response():
            if isinstance(message, ResultMessage) and message.subtype == "success":
                print(f"New result: {message.result}")


asyncio.run(interruptible_task())
```

**Buffer behavior after interrupt:** `interrupt()` sends a stop signal but does not clear the message buffer. Messages already produced by the interrupted task, including its `ResultMessage` (with `subtype="error_during_execution"`), remain in the stream. You must drain them with `receive_response()` before reading the response to a new query. If you send a new query immediately after `interrupt()` and call `receive_response()` only once, you’ll receive the interrupted task’s messages, not the new query’s response.

#### [​](#example-advanced-permission-control) Example - Advanced permission control

```
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


async def custom_permission_handler(
    tool_name: str, input_data: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Custom logic for tool permissions."""

    # Block writes to system directories
    if tool_name == "Write" and input_data.get("file_path", "").startswith("/system/"):
        return PermissionResultDeny(
            message="System directory write not allowed", interrupt=True
        )

    # Redirect sensitive file operations
    if tool_name in ["Write", "Edit"] and "config" in input_data.get("file_path", ""):
        safe_path = f"./sandbox/{input_data['file_path']}"
        return PermissionResultAllow(
            updated_input={**input_data, "file_path": safe_path}
        )

    # Allow everything else
    return PermissionResultAllow(updated_input=input_data)


async def main():
    options = ClaudeAgentOptions(
        can_use_tool=custom_permission_handler, allowed_tools=["Read", "Write", "Edit"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Update the system config file")

        async for message in client.receive_response():
            # Will use sandbox path instead
            print(message)


asyncio.run(main())
```

## [​](#types) Types

**`@dataclass` vs `TypedDict`:** This SDK uses two kinds of types. Classes decorated with `@dataclass` (such as `ResultMessage`, `AgentDefinition`, `TextBlock`) are object instances at runtime and support attribute access: `msg.result`. Classes defined with `TypedDict` (such as `ThinkingConfigEnabled`, `McpStdioServerConfig`, `SyncHookJSONOutput`) are **plain dicts at runtime** and require key access: `config["budget_tokens"]`, not `config.budget_tokens`. The `ClassName(field=value)` call syntax works for both, but only dataclasses produce objects with attributes.

### [​](#sdkmcptool) `SdkMcpTool`

Definition for an SDK MCP tool created with the `@tool` decorator.

```
@dataclass
class SdkMcpTool(Generic[T]):
    name: str
    description: str
    input_schema: type[T] | dict[str, Any]
    handler: Callable[[T], Awaitable[dict[str, Any]]]
    annotations: ToolAnnotations | None = None
```

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Unique identifier for the tool |
| `description` | `str` | Human-readable description |
| `input_schema` | `type[T] | dict[str, Any]` | Schema for input validation |
| `handler` | `Callable[[T], Awaitable[dict[str, Any]]]` | Async function that handles tool execution |
| `annotations` | `ToolAnnotations | None` | Optional MCP tool annotations (e.g., `readOnlyHint`, `destructiveHint`, `openWorldHint`). From `mcp.types` |

### [​](#transport) `Transport`

Abstract base class for custom transport implementations. Use this to communicate with the Claude process over a custom channel (for example, a remote connection instead of a local subprocess).

This is a low-level internal API. The interface may change in future releases. Custom implementations must be updated to match any interface changes.

```
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class Transport(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def write(self, data: str) -> None: ...

    @abstractmethod
    def read_messages(self) -> AsyncIterator[dict[str, Any]]: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    def is_ready(self) -> bool: ...

    @abstractmethod
    async def end_input(self) -> None: ...
```

| Method | Description |
| --- | --- |
| `connect()` | Connect the transport and prepare for communication |
| `write(data)` | Write raw data (JSON + newline) to the transport |
| `read_messages()` | Async iterator that yields parsed JSON messages |
| `close()` | Close the connection and clean up resources |
| `is_ready()` | Returns `True` if the transport can send and receive |
| `end_input()` | Close the input stream (for example, close stdin for subprocess transports) |

Import: `from claude_agent_sdk import Transport`

### [​](#claudeagentoptions) `ClaudeAgentOptions`

Configuration dataclass for Claude Code queries.

```
@dataclass
class ClaudeAgentOptions:
    tools: list[str] | ToolsPreset | None = None
    allowed_tools: list[str] = field(default_factory=list)
    system_prompt: str | SystemPromptPreset | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    strict_mcp_config: bool = False
    permission_mode: PermissionMode | None = None
    continue_conversation: bool = False
    resume: str | None = None
    max_turns: int | None = None
    max_budget_usd: float | None = None
    disallowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    fallback_model: str | None = None
    betas: list[SdkBeta] = field(default_factory=list)
    output_format: dict[str, Any] | None = None
    permission_prompt_tool_name: str | None = None
    cwd: str | Path | None = None
    cli_path: str | Path | None = None
    settings: str | None = None
    add_dirs: list[str | Path] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, str | None] = field(default_factory=dict)
    max_buffer_size: int | None = None
    debug_stderr: Any = sys.stderr  # Deprecated
    stderr: Callable[[str], None] | None = None
    can_use_tool: CanUseTool | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    user: str | None = None
    include_partial_messages: bool = False
    include_hook_events: bool = False
    fork_session: bool = False
    agents: dict[str, AgentDefinition] | None = None
    setting_sources: list[SettingSource] | None = None
    sandbox: SandboxSettings | None = None
    plugins: list[SdkPluginConfig] = field(default_factory=list)
    max_thinking_tokens: int | None = None  # Deprecated: use thinking instead
    thinking: ThinkingConfig | None = None
    effort: EffortLevel | None = None
    enable_file_checkpointing: bool = False
    session_store: SessionStore | None = None
    session_store_flush: SessionStoreFlushMode = "batched"
```

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `tools` | `list[str] | ToolsPreset | None` | `None` | Tools configuration. Use `{"type": "preset", "preset": "claude_code"}` for Claude Code’s default tools |
| `allowed_tools` | `list[str]` | `[]` | Tools to auto-approve without prompting. This does not restrict Claude to only these tools; unlisted tools fall through to `permission_mode` and `can_use_tool`. Use `disallowed_tools` to block tools. See [Permissions](/docs/en/agent-sdk/permissions#allow-and-deny-rules) |
| `system_prompt` | `str | SystemPromptPreset | None` | `None` | System prompt configuration. Pass a string for custom prompt, or use `{"type": "preset", "preset": "claude_code"}` for Claude Code’s system prompt. Add `"append"` to extend the preset |
| `mcp_servers` | `dict[str, McpServerConfig] | str | Path` | `{}` | MCP server configurations or path to config file |
| `strict_mcp_config` | `bool` | `False` | When `True`, use only the servers passed in `mcp_servers` and ignore project `.mcp.json`, user settings, plugin-provided MCP servers, and [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai). Maps to the CLI `--strict-mcp-config` flag |
| `permission_mode` | `PermissionMode | None` | `None` | Permission mode for tool usage |
| `continue_conversation` | `bool` | `False` | Continue the most recent conversation |
| `resume` | `str | None` | `None` | Session ID to resume |
| `max_turns` | `int | None` | `None` | Maximum agentic turns (tool-use round trips) |
| `max_budget_usd` | `float | None` | `None` | Stop the query when the client-side cost estimate reaches this USD value. Compared against the same estimate as `total_cost_usd`; see [Track cost and usage](/docs/en/agent-sdk/cost-tracking) for accuracy caveats |
| `disallowed_tools` | `list[str]` | `[]` | Tools to deny. A bare name such as `"Bash"` removes the tool from Claude’s context. A scoped rule such as `"Bash(rm *)"` leaves the tool available and denies matching calls in every permission mode, including `bypassPermissions`. See [Permissions](/docs/en/agent-sdk/permissions#allow-and-deny-rules) |
| `enable_file_checkpointing` | `bool` | `False` | Enable file change tracking for rewinding. See [File checkpointing](/docs/en/agent-sdk/file-checkpointing) |
| `model` | `str | None` | `None` | Claude model alias or full model name. See [accepted values and provider-specific IDs](/docs/en/model-config#available-models) |
| `fallback_model` | `str | None` | `None` | Fallback model to use if the primary model fails |
| `betas` | `list[SdkBeta]` | `[]` | Beta features to enable. See [`SdkBeta`](#sdkbeta) for available options |
| `output_format` | `dict[str, Any] | None` | `None` | Output format for structured responses (e.g., `{"type": "json_schema", "schema": {...}}`). See [Structured outputs](/docs/en/agent-sdk/structured-outputs) for details |
| `permission_prompt_tool_name` | `str | None` | `None` | MCP tool name for permission prompts |
| `cwd` | `str | Path | None` | `None` | Current working directory |
| `cli_path` | `str | Path | None` | `None` | Custom path to the Claude Code CLI executable |
| `settings` | `str | None` | `None` | Path to settings file |
| `add_dirs` | `list[str | Path]` | `[]` | Additional directories Claude can access |
| `env` | `dict[str, str]` | `{}` | Environment variables merged on top of the inherited process environment. See [Environment variables](/docs/en/env-vars) for variables the underlying CLI reads, and [Handle slow or stalled API responses](#handle-slow-or-stalled-api-responses) for timeout-related variables |
| `extra_args` | `dict[str, str | None]` | `{}` | Additional CLI arguments to pass directly to the CLI |
| `max_buffer_size` | `int | None` | `None` | Maximum bytes when buffering CLI stdout |
| `debug_stderr` | `Any` | `sys.stderr` | *Deprecated* - File-like object for debug output. Use `stderr` callback instead |
| `stderr` | `Callable[[str], None] | None` | `None` | Callback function for stderr output from CLI |
| `can_use_tool` | [`CanUseTool`](#canusetool)  `| None` | `None` | Tool permission callback function. See [Permission types](#canusetool) for details |
| `hooks` | `dict[HookEvent, list[HookMatcher]] | None` | `None` | Hook configurations for intercepting events |
| `user` | `str | None` | `None` | User identifier |
| `include_partial_messages` | `bool` | `False` | Include partial message streaming events. When enabled, [`StreamEvent`](#streamevent) messages are yielded |
| `include_hook_events` | `bool` | `False` | Include hook lifecycle events in the message stream as `HookEventMessage` objects |
| `fork_session` | `bool` | `False` | When resuming with `resume`, fork to a new session ID instead of continuing the original session |
| `agents` | `dict[str, AgentDefinition] | None` | `None` | Programmatically defined subagents |
| `plugins` | `list[SdkPluginConfig]` | `[]` | Load custom plugins from local paths. See [Plugins](/docs/en/agent-sdk/plugins) for details |
| `sandbox` | [`SandboxSettings`](#sandboxsettings)  `| None` | `None` | Configure sandbox behavior programmatically. See [Sandbox settings](#sandboxsettings) for details |
| `setting_sources` | `list[SettingSource] | None` | `None` (CLI defaults: all sources) | Control which filesystem settings to load. Pass `[]` to disable user, project, and local settings. Endpoint-managed policy loads regardless; server-managed settings are fetched when the session authenticates with an organization credential on an [eligible configuration](/docs/en/server-managed-settings#platform-availability). See [Use Claude Code features](/docs/en/agent-sdk/claude-code-features#what-settingsources-does-not-control) |
| `skills` | `list[str] | Literal["all"] | None` | `None` | Skills available to the session. Pass `"all"` to enable every discovered skill, or a list of skill names. When set, the SDK adds the Skill tool to `allowed_tools` automatically. If you also pass `tools`, include `"Skill"` in that list. See [Skills](/docs/en/agent-sdk/skills) |
| `max_thinking_tokens` | `int | None` | `None` | *Deprecated* - Maximum tokens for thinking blocks. Use `thinking` instead |
| `thinking` | [`ThinkingConfig`](#thinkingconfig)  `| None` | `None` | Controls extended thinking behavior. Takes precedence over `max_thinking_tokens` |
| `effort` | [`EffortLevel`](#effortlevel)  `| None` | `None` | Effort level for thinking depth. See [adjust the effort level](/docs/en/model-config#adjust-effort-level) |
| `session_store` | [`SessionStore`](/docs/en/agent-sdk/session-storage#the-sessionstore-interface)  `| None` | `None` | Mirror session transcripts to an external backend so any host can resume them. See [Persist sessions to external storage](/docs/en/agent-sdk/session-storage) |
| `session_store_flush` | `Literal["batched", "eager"]` | `"batched"` | When to flush mirrored transcript entries to `session_store`. `"batched"` flushes once per turn or when the buffer fills; `"eager"` triggers a background flush after every frame. Ignored when `session_store` is `None` |

#### [​](#handle-slow-or-stalled-api-responses) Handle slow or stalled API responses

The CLI subprocess reads several environment variables that control API timeouts and stall detection. Pass them through `ClaudeAgentOptions.env`:

```
options = ClaudeAgentOptions(
    env={
        "API_TIMEOUT_MS": "120000",
        "CLAUDE_CODE_MAX_RETRIES": "2",
        "CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS": "120000",
    },
)
```

* `API_TIMEOUT_MS`: per-request timeout on the Anthropic client, in milliseconds. Default `600000`. Applies to the main loop and all subagents.
* `CLAUDE_CODE_MAX_RETRIES`: maximum API retries. Default `10`, capped at `15`. Each retry gets its own `API_TIMEOUT_MS` window, so worst-case wall time is roughly `API_TIMEOUT_MS × (CLAUDE_CODE_MAX_RETRIES + 1)` plus backoff. For unattended runs that need to wait through longer outages, set `CLAUDE_CODE_RETRY_WATCHDOG=1` to retry capacity errors indefinitely.
* `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`: stall watchdog for subagents launched with `run_in_background`. Default `600000`. Resets on each stream event; on stall it aborts the subagent, marks the task failed, and surfaces the error to the parent with any partial result. Does not apply to synchronous subagents.
* `CLAUDE_ENABLE_STREAM_WATCHDOG=1` with `CLAUDE_STREAM_IDLE_TIMEOUT_MS`: aborts the request when headers have arrived but the response body stops streaming. When `CLAUDE_ENABLE_STREAM_WATCHDOG` is unset, the default is server-controlled on the direct Anthropic API and off on other providers. `CLAUDE_STREAM_IDLE_TIMEOUT_MS` defaults to `300000` and is clamped to that minimum. The aborted request goes through the normal retry path.

### [​](#outputformat) `OutputFormat`

Configuration for structured output validation. Pass this as a `dict` to the `output_format` field on `ClaudeAgentOptions`:

```