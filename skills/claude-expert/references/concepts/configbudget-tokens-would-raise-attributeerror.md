---
title: config.budget_tokens would raise AttributeError
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# config.budget_tokens would raise AttributeError
```

### [​](#sdkbeta) `SdkBeta`

Literal type for SDK beta features.

```
SdkBeta = Literal["context-1m-2025-08-07"]
```

Use with the `betas` field in `ClaudeAgentOptions` to enable beta features.

The `context-1m-2025-08-07` beta is retired as of April 30, 2026. Passing this header with Claude Sonnet 4.5 or Sonnet 4 has no effect, and requests that exceed the standard 200k-token context window return an error. To use a 1M-token context window, migrate to [Claude Sonnet 4.6, Claude Opus 4.6, Claude Opus 4.7, or Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/overview), which include 1M context at standard pricing with no beta header required.

### [​](#mcpsdkserverconfig) `McpSdkServerConfig`

Configuration for SDK MCP servers created with `create_sdk_mcp_server()`.

```
class McpSdkServerConfig(TypedDict):
    type: Literal["sdk"]
    name: str
    instance: Any  # MCP Server instance
```

### [​](#mcpserverconfig) `McpServerConfig`

Union type for MCP server configurations.

```
McpServerConfig = (
    McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig
)
```

#### [​](#mcpstdioserverconfig) `McpStdioServerConfig`

```
class McpStdioServerConfig(TypedDict):
    type: NotRequired[Literal["stdio"]]  # Optional for backwards compatibility
    command: str
    args: NotRequired[list[str]]
    env: NotRequired[dict[str, str]]
```

#### [​](#mcpsseserverconfig) `McpSSEServerConfig`

```
class McpSSEServerConfig(TypedDict):
    type: Literal["sse"]
    url: str
    headers: NotRequired[dict[str, str]]
```

#### [​](#mcphttpserverconfig) `McpHttpServerConfig`

```
class McpHttpServerConfig(TypedDict):
    type: Literal["http"]
    url: str
    headers: NotRequired[dict[str, str]]
```

### [​](#mcpserverstatusconfig) `McpServerStatusConfig`

The configuration of an MCP server as reported by [`get_mcp_status()`](#methods). This is the union of all [`McpServerConfig`](#mcpserverconfig) transport variants plus an output-only `claudeai-proxy` variant for servers proxied through claude.ai.

```
McpServerStatusConfig = (
    McpStdioServerConfig
    | McpSSEServerConfig
    | McpHttpServerConfig
    | McpSdkServerConfigStatus
    | McpClaudeAIProxyServerConfig
)
```

`McpSdkServerConfigStatus` is the serializable form of [`McpSdkServerConfig`](#mcpsdkserverconfig) with only `type` (`"sdk"`) and `name` (`str`) fields; the in-process `instance` is omitted. `McpClaudeAIProxyServerConfig` has `type` (`"claudeai-proxy"`), `url` (`str`), and `id` (`str`) fields.

### [​](#mcpstatusresponse) `McpStatusResponse`

Response from [`ClaudeSDKClient.get_mcp_status()`](#methods). Wraps the list of server statuses under the `mcpServers` key.

```
class McpStatusResponse(TypedDict):
    mcpServers: list[McpServerStatus]
```

### [​](#mcpserverstatus) `McpServerStatus`

Status of a connected MCP server, contained in [`McpStatusResponse`](#mcpstatusresponse).

```
class McpServerStatus(TypedDict):
    name: str
    status: McpServerConnectionStatus  # "connected" | "failed" | "needs-auth" | "pending" | "disabled"
    serverInfo: NotRequired[McpServerInfo]
    error: NotRequired[str]
    config: NotRequired[McpServerStatusConfig]
    scope: NotRequired[str]
    tools: NotRequired[list[McpToolInfo]]
```

| Field | Type | Description |
| --- | --- | --- |
| `name` | `str` | Server name |
| `status` | `str` | One of `"connected"`, `"failed"`, `"needs-auth"`, `"pending"`, or `"disabled"` |
| `serverInfo` | `dict` (optional) | Server name and version (`{"name": str, "version": str}`) |
| `error` | `str` (optional) | Error message if the server failed to connect |
| `config` | [`McpServerStatusConfig`](#mcpserverstatusconfig) (optional) | Server configuration. Same shape as [`McpServerConfig`](#mcpserverconfig) (stdio, SSE, HTTP, or SDK), plus a `claudeai-proxy` variant for servers connected through claude.ai |
| `scope` | `str` (optional) | Configuration scope |
| `tools` | `list` (optional) | Tools provided by this server, each with `name`, `description`, and `annotations` fields |

### [​](#sdkpluginconfig) `SdkPluginConfig`

Configuration for loading plugins in the SDK.

```
class SdkPluginConfig(TypedDict):
    type: Literal["local"]
    path: str
```

| Field | Type | Description |
| --- | --- | --- |
| `type` | `Literal["local"]` | Must be `"local"` (only local plugins currently supported) |
| `path` | `str` | Absolute or relative path to the plugin directory |

**Example:**

```
plugins = [
    {"type": "local", "path": "./my-plugin"},
    {"type": "local", "path": "/absolute/path/to/plugin"},
]
```

For complete information on creating and using plugins, see [Plugins](/docs/en/agent-sdk/plugins).

## [​](#message-types) Message Types

### [​](#message) `Message`

Union type of all possible messages.

```
Message = (
    UserMessage
    | AssistantMessage
    | SystemMessage
    | ResultMessage
    | StreamEvent
    | RateLimitEvent
)
```

### [​](#usermessage) `UserMessage`

User input message.

```
@dataclass
class UserMessage:
    content: str | list[ContentBlock]
    uuid: str | None = None
    parent_tool_use_id: str | None = None
    tool_use_result: dict[str, Any] | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `content` | `str | list[ContentBlock]` | Message content as text or content blocks |
| `uuid` | `str | None` | Unique message identifier |
| `parent_tool_use_id` | `str | None` | Tool use ID if this message is a tool result response |
| `tool_use_result` | `dict[str, Any] | None` | Tool result data if applicable |

### [​](#assistantmessage) `AssistantMessage`

Assistant response message with content blocks.

```
@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str
    parent_tool_use_id: str | None = None
    error: AssistantMessageError | None = None
    usage: dict[str, Any] | None = None
    message_id: str | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `content` | `list[ContentBlock]` | List of content blocks in the response |
| `model` | `str` | Model that generated the response |
| `parent_tool_use_id` | `str | None` | Tool use ID if this is a nested response |
| `error` | [`AssistantMessageError`](#assistantmessageerror)  `| None` | Error type if the response encountered an error |
| `usage` | `dict[str, Any] | None` | Per-message token usage (same keys as [`ResultMessage.usage`](#resultmessage)) |
| `message_id` | `str | None` | API message ID. Multiple messages from one turn share the same ID |

### [​](#assistantmessageerror) `AssistantMessageError`

Possible error types for assistant messages.

```
AssistantMessageError = Literal[
    "authentication_failed",
    "billing_error",
    "rate_limit",
    "invalid_request",
    "server_error",
    "max_output_tokens",
    "unknown",
]
```

### [​](#systemmessage) `SystemMessage`

System message with metadata.

```
@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]
```

### [​](#resultmessage) `ResultMessage`

Final result message with cost and usage information.

```
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    stop_reason: str | None = None
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    structured_output: Any = None
    model_usage: dict[str, Any] | None = None
    permission_denials: list[Any] | None = None
    deferred_tool_use: DeferredToolUse | None = None
    errors: list[str] | None = None
    api_error_status: int | None = None
    uuid: str | None = None
```

The `subtype` field determines which other fields are populated. It is one of `"success"`, `"error_during_execution"`, `"error_max_turns"`, `"error_max_budget_usd"`, or `"error_max_structured_output_retries"`. The Python dataclass flattens all variants into one shape, so fields that don’t apply to the returned subtype are `None`.
Several fields carry diagnostic detail when the conversation ends on an error:

* `is_error`: `True` when the conversation ended in an error state. Always `True` on the `error_*` subtypes. On `subtype="success"` it is `True` when the final model request failed, meaning the agent loop completed but the last API call returned an error.
* `api_error_status`: the HTTP status code of the terminating API error. `None` when the turn ended without one. Populated only on `subtype="success"`.
* `result`: text of the final assistant message on `subtype="success"`, or `None` on the `error_*` subtypes. When `subtype="success"` and `is_error=True`, this holds the API error string if one is available but can be empty, so check `api_error_status` and the preceding `AssistantMessage` content for detail.
* `errors`: loop-level error strings such as the max-turns message. Populated only on the `error_*` subtypes.

The `usage` dict contains the following keys when present:

| Key | Type | Description |
| --- | --- | --- |
| `input_tokens` | `int` | Total input tokens consumed. |
| `output_tokens` | `int` | Total output tokens generated. |
| `cache_creation_input_tokens` | `int` | Tokens used to create new cache entries. |
| `cache_read_input_tokens` | `int` | Tokens read from existing cache entries. |

The `model_usage` dict maps model names to per-model usage. The inner dict keys use camelCase because the value is passed through unmodified from the underlying CLI process, matching the TypeScript [`ModelUsage`](/docs/en/agent-sdk/typescript#modelusage) type:

| Key | Type | Description |
| --- | --- | --- |
| `inputTokens` | `int` | Input tokens for this model. |
| `outputTokens` | `int` | Output tokens for this model. |
| `cacheReadInputTokens` | `int` | Cache read tokens for this model. |
| `cacheCreationInputTokens` | `int` | Cache creation tokens for this model. |
| `webSearchRequests` | `int` | Web search requests made by this model. |
| `costUSD` | `float` | Estimated cost in USD for this model, computed client-side. See [Track cost and usage](/docs/en/agent-sdk/cost-tracking) for billing caveats. |
| `contextWindow` | `int` | Context window size for this model. |
| `maxOutputTokens` | `int` | Maximum output token limit for this model. |

### [​](#streamevent) `StreamEvent`

Stream event for partial message updates during streaming. Only received when `include_partial_messages=True` in `ClaudeAgentOptions`. Import via `from claude_agent_sdk.types import StreamEvent`.

```
@dataclass
class StreamEvent:
    uuid: str
    session_id: str
    event: dict[str, Any]  # The raw Claude API stream event
    parent_tool_use_id: str | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `uuid` | `str` | Unique identifier for this event |
| `session_id` | `str` | Session identifier |
| `event` | `dict[str, Any]` | The raw Claude API stream event data |
| `parent_tool_use_id` | `str | None` | Parent tool use ID if this event is from a subagent |

### [​](#ratelimitevent) `RateLimitEvent`

Emitted when rate limit status changes (for example, from `"allowed"` to `"allowed_warning"`). Use this to warn users before they hit a hard limit, or to back off when status is `"rejected"`.

```
@dataclass
class RateLimitEvent:
    rate_limit_info: RateLimitInfo
    uuid: str
    session_id: str
```

| Field | Type | Description |
| --- | --- | --- |
| `rate_limit_info` | [`RateLimitInfo`](#ratelimitinfo) | Current rate limit state |
| `uuid` | `str` | Unique event identifier |
| `session_id` | `str` | Session identifier |

### [​](#ratelimitinfo) `RateLimitInfo`

Rate limit state carried by [`RateLimitEvent`](#ratelimitevent).

```
RateLimitStatus = Literal["allowed", "allowed_warning", "rejected"]
RateLimitType = Literal[
    "five_hour", "seven_day", "seven_day_opus", "seven_day_sonnet", "overage"
]


@dataclass
class RateLimitInfo:
    status: RateLimitStatus
    resets_at: int | None = None
    rate_limit_type: RateLimitType | None = None
    utilization: float | None = None
    overage_status: RateLimitStatus | None = None
    overage_resets_at: int | None = None
    overage_disabled_reason: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)
```

| Field | Type | Description |
| --- | --- | --- |
| `status` | `RateLimitStatus` | Current status. `"allowed_warning"` means approaching the limit; `"rejected"` means the limit was hit |
| `resets_at` | `int | None` | Unix timestamp when the rate limit window resets |
| `rate_limit_type` | `RateLimitType | None` | Which rate limit window applies |
| `utilization` | `float | None` | Fraction of the rate limit consumed (0.0 to 1.0) |
| `overage_status` | `RateLimitStatus | None` | Status of pay-as-you-go overage usage, if applicable |
| `overage_resets_at` | `int | None` | Unix timestamp when the overage window resets |
| `overage_disabled_reason` | `str | None` | Why overage is unavailable, if status is `"rejected"` |
| `raw` | `dict[str, Any]` | Full raw dict from the CLI, including fields not modeled above |

### [​](#taskstartedmessage) `TaskStartedMessage`

Emitted when a background task starts. A background task is anything tracked outside the main turn: a backgrounded Bash command, a [Monitor](#monitor) watch, a subagent spawned via the Agent tool, or a remote agent. The `task_type` field tells you which. This naming is unrelated to the `Task`-to-`Agent` tool rename.

```
@dataclass
class TaskStartedMessage(SystemMessage):
    task_id: str
    description: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    task_type: str | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `task_id` | `str` | Unique identifier for the task |
| `description` | `str` | Description of the task |
| `uuid` | `str` | Unique message identifier |
| `session_id` | `str` | Session identifier |
| `tool_use_id` | `str | None` | Associated tool use ID |
| `task_type` | `str | None` | Which kind of background task: `"local_bash"` for background Bash and Monitor watches, `"local_agent"`, or `"remote_agent"` |

### [​](#taskusage) `TaskUsage`

Token and timing data for a background task.

```
class TaskUsage(TypedDict):
    total_tokens: int
    tool_uses: int
    duration_ms: int
```

### [​](#taskprogressmessage) `TaskProgressMessage`

Emitted periodically with progress updates for a running background task.

```
@dataclass
class TaskProgressMessage(SystemMessage):
    task_id: str
    description: str
    usage: TaskUsage
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    last_tool_name: str | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `task_id` | `str` | Unique identifier for the task |
| `description` | `str` | Current status description |
| `usage` | `TaskUsage` | Token usage for this task so far |
| `uuid` | `str` | Unique message identifier |
| `session_id` | `str` | Session identifier |
| `tool_use_id` | `str | None` | Associated tool use ID |
| `last_tool_name` | `str | None` | Name of the last tool the task used |

### [​](#tasknotificationmessage) `TaskNotificationMessage`

Emitted when a background task completes, fails, or is stopped. Background tasks include `run_in_background` Bash commands, Monitor watches, and background subagents.

```
@dataclass
class TaskNotificationMessage(SystemMessage):
    task_id: str
    status: TaskNotificationStatus  # "completed" | "failed" | "stopped"
    output_file: str
    summary: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    usage: TaskUsage | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `task_id` | `str` | Unique identifier for the task |
| `status` | `TaskNotificationStatus` | One of `"completed"`, `"failed"`, or `"stopped"` |
| `output_file` | `str` | Path to the task output file |
| `summary` | `str` | Summary of the task result |
| `uuid` | `str` | Unique message identifier |
| `session_id` | `str` | Session identifier |
| `tool_use_id` | `str | None` | Associated tool use ID |
| `usage` | `TaskUsage | None` | Final token usage for the task |

## [​](#content-block-types) Content Block Types

### [​](#contentblock) `ContentBlock`

Union type of all content blocks.

```
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

### [​](#textblock) `TextBlock`

Text content block.

```
@dataclass
class TextBlock:
    text: str
```

### [​](#thinkingblock) `ThinkingBlock`

Thinking content block (for models with thinking capability).

```
@dataclass
class ThinkingBlock:
    thinking: str
    signature: str
```

### [​](#tooluseblock) `ToolUseBlock`

Tool use request block.

```
@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]
```

### [​](#toolresultblock) `ToolResultBlock`

Tool execution result block.

```
@dataclass
class ToolResultBlock:
    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
```

## [​](#error-types) Error Types

### [​](#claudesdkerror) `ClaudeSDKError`

Base exception class for all SDK errors.

```
class ClaudeSDKError(Exception):
    """Base error for Claude SDK."""
```

### [​](#clinotfounderror) `CLINotFoundError`

Raised when Claude Code CLI is not installed or not found.

```
class CLINotFoundError(CLIConnectionError):
    def __init__(
        self, message: str = "Claude Code not found", cli_path: str | None = None
    ):
        """
        Args:
            message: Error message (default: "Claude Code not found")
            cli_path: Optional path to the CLI that was not found
        """
```

### [​](#cliconnectionerror) `CLIConnectionError`

Raised when connection to Claude Code fails.

```
class CLIConnectionError(ClaudeSDKError):
    """Failed to connect to Claude Code."""
```

### [​](#processerror) `ProcessError`

Raised when the Claude Code process fails.

```
class ProcessError(ClaudeSDKError):
    def __init__(
        self, message: str, exit_code: int | None = None, stderr: str | None = None
    ):
        self.exit_code = exit_code
        self.stderr = stderr
```

### [​](#clijsondecodeerror) `CLIJSONDecodeError`

Raised when JSON parsing fails.

```
class CLIJSONDecodeError(ClaudeSDKError):
    def __init__(self, line: str, original_error: Exception):
        """
        Args:
            line: The line that failed to parse
            original_error: The original JSON decode exception
        """
        self.line = line
        self.original_error = original_error
```

## [​](#hook-types) Hook Types

For a comprehensive guide on using hooks with examples and common patterns, see the [Hooks guide](/docs/en/agent-sdk/hooks).

### [​](#hookevent) `HookEvent`

Supported hook event types.

```
HookEvent = Literal[
    "PreToolUse",  # Called before tool execution
    "PostToolUse",  # Called after tool execution
    "PostToolUseFailure",  # Called when a tool execution fails
    "UserPromptSubmit",  # Called when user submits a prompt
    "Stop",  # Called when stopping execution
    "SubagentStop",  # Called when a subagent stops
    "PreCompact",  # Called before message compaction
    "Notification",  # Called for notification events
    "SubagentStart",  # Called when a subagent starts
    "PermissionRequest",  # Called when a permission decision is needed
]
```

The TypeScript SDK supports additional hook events not yet available in Python: `SessionStart`, `SessionEnd`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`, `PostToolBatch`, and `MessageDisplay`.

### [​](#hookcallback) `HookCallback`

Type definition for hook callback functions.

```
HookCallback = Callable[[HookInput, str | None, HookContext], Awaitable[HookJSONOutput]]
```

Parameters:

* `input`: Strongly-typed hook input with discriminated unions based on `hook_event_name` (see [`HookInput`](#hookinput))
* `tool_use_id`: Optional tool use identifier (for tool-related hooks)
* `context`: Hook context with additional information

Returns a [`HookJSONOutput`](#hookjsonoutput) that may contain:

* `decision`: `"block"` to block the action
* `systemMessage`: warning message shown to the user
* `hookSpecificOutput`: Hook-specific output data

### [​](#hookcontext) `HookContext`

Context information passed to hook callbacks.

```
class HookContext(TypedDict):
    signal: Any | None  # Future: abort signal support
```

### [​](#hookmatcher) `HookMatcher`

Configuration for matching hooks to specific events or tools.

```
@dataclass
class HookMatcher:
    matcher: str | None = (
        None  # Tool name or pattern to match (e.g., "Bash", "Write|Edit")
    )
    hooks: list[HookCallback] = field(
        default_factory=list
    )  # List of callbacks to execute
    timeout: float | None = (
        None  # Timeout in seconds for all hooks in this matcher (default: 60)
    )
```

### [​](#hookinput) `HookInput`

Union type of all hook input types. The actual type depends on the `hook_event_name` field.

```
HookInput = (
    PreToolUseHookInput
    | PostToolUseHookInput
    | PostToolUseFailureHookInput
    | UserPromptSubmitHookInput
    | StopHookInput
    | SubagentStopHookInput
    | PreCompactHookInput
    | NotificationHookInput
    | SubagentStartHookInput
    | PermissionRequestHookInput
)
```

### [​](#basehookinput) `BaseHookInput`

Base fields present in all hook input types.

```
class BaseHookInput(TypedDict):
    session_id: str
    transcript_path: str
    cwd: str
    permission_mode: NotRequired[str]
```

| Field | Type | Description |
| --- | --- | --- |
| `session_id` | `str` | Current session identifier |
| `transcript_path` | `str` | Path to the session transcript file |
| `cwd` | `str` | Current working directory |
| `permission_mode` | `str` (optional) | Current permission mode |

### [​](#pretoolusehookinput) `PreToolUseHookInput`

Input data for `PreToolUse` hook events.

```
class PreToolUseHookInput(BaseHookInput):
    hook_event_name: Literal["PreToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["PreToolUse"]` | Always “PreToolUse” |
| `tool_name` | `str` | Name of the tool about to be executed |
| `tool_input` | `dict[str, Any]` | Input parameters for the tool |
| `tool_use_id` | `str` | Unique identifier for this tool use |
| `agent_id` | `str` (optional) | Subagent identifier, present when the hook fires inside a subagent |
| `agent_type` | `str` (optional) | Subagent type, present when the hook fires inside a subagent |

### [​](#posttoolusehookinput) `PostToolUseHookInput`

Input data for `PostToolUse` hook events.

```
class PostToolUseHookInput(BaseHookInput):
    hook_event_name: Literal["PostToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_response: Any
    tool_use_id: str
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["PostToolUse"]` | Always “PostToolUse” |
| `tool_name` | `str` | Name of the tool that was executed |
| `tool_input` | `dict[str, Any]` | Input parameters that were used |
| `tool_response` | `Any` | Response from the tool execution |
| `tool_use_id` | `str` | Unique identifier for this tool use |
| `agent_id` | `str` (optional) | Subagent identifier, present when the hook fires inside a subagent |
| `agent_type` | `str` (optional) | Subagent type, present when the hook fires inside a subagent |

### [​](#posttoolusefailurehookinput) `PostToolUseFailureHookInput`

Input data for `PostToolUseFailure` hook events. Called when a tool execution fails.

```
class PostToolUseFailureHookInput(BaseHookInput):
    hook_event_name: Literal["PostToolUseFailure"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    error: str
    is_interrupt: NotRequired[bool]
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["PostToolUseFailure"]` | Always “PostToolUseFailure” |
| `tool_name` | `str` | Name of the tool that failed |
| `tool_input` | `dict[str, Any]` | Input parameters that were used |
| `tool_use_id` | `str` | Unique identifier for this tool use |
| `error` | `str` | Error message from the failed execution |
| `is_interrupt` | `bool` (optional) | Whether the failure was caused by an interrupt |
| `agent_id` | `str` (optional) | Subagent identifier, present when the hook fires inside a subagent |
| `agent_type` | `str` (optional) | Subagent type, present when the hook fires inside a subagent |

### [​](#userpromptsubmithookinput) `UserPromptSubmitHookInput`

Input data for `UserPromptSubmit` hook events.

```
class UserPromptSubmitHookInput(BaseHookInput):
    hook_event_name: Literal["UserPromptSubmit"]
    prompt: str
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["UserPromptSubmit"]` | Always “UserPromptSubmit” |
| `prompt` | `str` | The user’s submitted prompt |

### [​](#stophookinput) `StopHookInput`

Input data for `Stop` hook events.

```
class StopHookInput(BaseHookInput):
    hook_event_name: Literal["Stop"]
    stop_hook_active: bool
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["Stop"]` | Always “Stop” |
| `stop_hook_active` | `bool` | Whether the stop hook is active |

### [​](#subagentstophookinput) `SubagentStopHookInput`

Input data for `SubagentStop` hook events.

```
class SubagentStopHookInput(BaseHookInput):
    hook_event_name: Literal["SubagentStop"]
    stop_hook_active: bool
    agent_id: str
    agent_transcript_path: str
    agent_type: str
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["SubagentStop"]` | Always “SubagentStop” |
| `stop_hook_active` | `bool` | Whether the stop hook is active |
| `agent_id` | `str` | Unique identifier for the subagent |
| `agent_transcript_path` | `str` | Path to the subagent’s transcript file |
| `agent_type` | `str` | Type of the subagent |

### [​](#precompacthookinput) `PreCompactHookInput`

Input data for `PreCompact` hook events.

```
class PreCompactHookInput(BaseHookInput):
    hook_event_name: Literal["PreCompact"]
    trigger: Literal["manual", "auto"]
    custom_instructions: str | None
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["PreCompact"]` | Always “PreCompact” |
| `trigger` | `Literal["manual", "auto"]` | What triggered the compaction |
| `custom_instructions` | `str | None` | Custom instructions for compaction |

### [​](#notificationhookinput) `NotificationHookInput`

Input data for `Notification` hook events.

```
class NotificationHookInput(BaseHookInput):
    hook_event_name: Literal["Notification"]
    message: str
    title: NotRequired[str]
    notification_type: str
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["Notification"]` | Always “Notification” |
| `message` | `str` | Notification message content |
| `title` | `str` (optional) | Notification title |
| `notification_type` | `str` | Type of notification |

### [​](#subagentstarthookinput) `SubagentStartHookInput`

Input data for `SubagentStart` hook events.

```
class SubagentStartHookInput(BaseHookInput):
    hook_event_name: Literal["SubagentStart"]
    agent_id: str
    agent_type: str
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["SubagentStart"]` | Always “SubagentStart” |
| `agent_id` | `str` | Unique identifier for the subagent |
| `agent_type` | `str` | Type of the subagent |

### [​](#permissionrequesthookinput) `PermissionRequestHookInput`

Input data for `PermissionRequest` hook events. Allows hooks to handle permission decisions programmatically.

```
class PermissionRequestHookInput(BaseHookInput):
    hook_event_name: Literal["PermissionRequest"]
    tool_name: str
    tool_input: dict[str, Any]
    permission_suggestions: NotRequired[list[Any]]
```

| Field | Type | Description |
| --- | --- | --- |
| `hook_event_name` | `Literal["PermissionRequest"]` | Always “PermissionRequest” |
| `tool_name` | `str` | Name of the tool requesting permission |
| `tool_input` | `dict[str, Any]` | Input parameters for the tool |
| `permission_suggestions` | `list[Any]` (optional) | Suggested permission updates from the CLI |

### [​](#hookjsonoutput) `HookJSONOutput`

Union type for hook callback return values.

```
HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput
```

#### [​](#synchookjsonoutput) `SyncHookJSONOutput`

Synchronous hook output with control and decision fields.

```
class SyncHookJSONOutput(TypedDict):
    # Control fields
    continue_: NotRequired[bool]  # Whether to proceed (default: True)
    suppressOutput: NotRequired[bool]  # Hide stdout from transcript
    stopReason: NotRequired[str]  # Message when continue is False

    # Decision fields
    decision: NotRequired[Literal["block"]]
    systemMessage: NotRequired[str]  # Warning message for user
    reason: NotRequired[str]  # Feedback for Claude

    # Hook-specific output
    hookSpecificOutput: NotRequired[HookSpecificOutput]
```

Use `continue_` (with underscore) in Python code. It is automatically converted to `continue` when sent to the CLI.

#### [​](#hookspecificoutput) `HookSpecificOutput`

A `TypedDict` containing the hook event name and event-specific fields. The shape depends on the `hookEventName` value. For full details on available fields per hook event, see [Control execution with hooks](/docs/en/agent-sdk/hooks#outputs).
A discriminated union of event-specific output types. The `hookEventName` field determines which fields are valid.

```
class PreToolUseHookSpecificOutput(TypedDict):
    hookEventName: Literal["PreToolUse"]
    permissionDecision: NotRequired[Literal["allow", "deny", "ask", "defer"]]
    permissionDecisionReason: NotRequired[str]
    updatedInput: NotRequired[dict[str, Any]]
    additionalContext: NotRequired[str]


class PostToolUseHookSpecificOutput(TypedDict):
    hookEventName: Literal["PostToolUse"]
    additionalContext: NotRequired[str]
    updatedToolOutput: NotRequired[Any]
    updatedMCPToolOutput: NotRequired[Any]  # Deprecated: use updatedToolOutput, which works for all tools


class PostToolUseFailureHookSpecificOutput(TypedDict):
    hookEventName: Literal["PostToolUseFailure"]
    additionalContext: NotRequired[str]


class UserPromptSubmitHookSpecificOutput(TypedDict):
    hookEventName: Literal["UserPromptSubmit"]
    additionalContext: NotRequired[str]


class NotificationHookSpecificOutput(TypedDict):
    hookEventName: Literal["Notification"]
    additionalContext: NotRequired[str]


class SubagentStartHookSpecificOutput(TypedDict):
    hookEventName: Literal["SubagentStart"]
    additionalContext: NotRequired[str]


class PermissionRequestHookSpecificOutput(TypedDict):
    hookEventName: Literal["PermissionRequest"]
    decision: dict[str, Any]


HookSpecificOutput = (
    PreToolUseHookSpecificOutput
    | PostToolUseHookSpecificOutput
    | PostToolUseFailureHookSpecificOutput
    | UserPromptSubmitHookSpecificOutput
    | NotificationHookSpecificOutput
    | SubagentStartHookSpecificOutput
    | PermissionRequestHookSpecificOutput
)
```

#### [​](#asynchookjsonoutput) `AsyncHookJSONOutput`

Async hook output that defers hook execution.

```
class AsyncHookJSONOutput(TypedDict):
    async_: Literal[True]  # Set to True to defer execution
    asyncTimeout: NotRequired[int]  # Timeout in milliseconds
```

Use `async_` (with underscore) in Python code. It is automatically converted to `async` when sent to the CLI.

### [​](#hook-usage-example) Hook Usage Example

This example registers two hooks: one that blocks dangerous bash commands like `rm -rf /`, and another that logs all tool usage for auditing. The security hook only runs on Bash commands (via the `matcher`), while the logging hook runs on all tools.

```
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, HookContext
from typing import Any


async def validate_bash_command(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Validate and potentially block dangerous bash commands."""
    if input_data["tool_name"] == "Bash":
        command = input_data["tool_input"].get("command", "")
        if "rm -rf /" in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Dangerous command blocked",
                }
            }
    return {}


async def log_tool_use(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Log all tool usage for auditing."""
    print(f"Tool used: {input_data.get('tool_name')}")
    return {}


options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="Bash", hooks=[validate_bash_command], timeout=120
            ),  # 2 min for validation
            HookMatcher(
                hooks=[log_tool_use]
            ),  # Applies to all tools (default 60s timeout)
        ],
        "PostToolUse": [HookMatcher(hooks=[log_tool_use])],
    }
)

async for message in query(prompt="Analyze this codebase", options=options):
    print(message)
```

## [​](#tool-input/output-types) Tool Input/Output Types

Documentation of input/output schemas for all built-in Claude Code tools. While the Python SDK doesn’t export these as types, they represent the structure of tool inputs and outputs in messages.

### [​](#agent) Agent

**Tool name:** `Agent` (previously `Task`, which is still accepted as an alias)
**Input:**

```
{
    "description": str,  # A short (3-5 word) description of the task
    "prompt": str,  # The task for the agent to perform
    "subagent_type": str,  # The type of specialized agent to use
}
```

**Output:**

```
{
    "result": str,  # Final result from the subagent
    "usage": dict | None,  # Token usage statistics
    "total_cost_usd": float | None,  # Estimated total cost in USD
    "duration_ms": int | None,  # Execution duration in milliseconds
}
```

### [​](#askuserquestion) AskUserQuestion

**Tool name:** `AskUserQuestion`
Asks the user clarifying questions during execution. See [Handle approvals and user input](/docs/en/agent-sdk/user-input#handle-clarifying-questions) for usage details.
**Input:**

```
{
    "questions": [  # Questions to ask the user (1-4 questions)
        {
            "question": str,  # The complete question to ask the user
            "header": str,  # Very short label displayed as a chip/tag (max 12 chars)
            "options": [  # The available choices (2-4 options)
                {
                    "label": str,  # Display text for this option (1-5 words)
                    "description": str,  # Explanation of what this option means
                }
            ],
            "multiSelect": bool,  # Set to true to allow multiple selections
        }
    ],
    "answers": dict[str, str | list[str]] | None,
    # User answers populated by the permission system. Multi-select
    # answers may be a list of labels or a comma-joined string
}
```

**Output:**

```
{
    "questions": [  # The questions that were asked
        {
            "question": str,
            "header": str,
            "options": [{"label": str, "description": str}],
            "multiSelect": bool,
        }
    ],
    "answers": dict[str, str],  # Maps question text to answer string
    # Multi-select answers are comma-separated
}
```

### [​](#bash) Bash

**Tool name:** `Bash`
**Input:**

```
{
    "command": str,  # The command to execute
    "timeout": int | None,  # Optional timeout in milliseconds (max 600000)
    "description": str | None,  # Clear, concise description (5-10 words)
    "run_in_background": bool | None,  # Set to true to run in background
}
```

**Output:**

```
{
    "output": str,  # Combined stdout and stderr output
    "exitCode": int,  # Exit code of the command
    "killed": bool | None,  # Whether command was killed due to timeout
    "shellId": str | None,  # Shell ID for background processes
}
```

### [​](#monitor) Monitor

**Tool name:** `Monitor`
Runs a background script and delivers each stdout line to Claude as an event so it can react without polling. Monitor follows the same permission rules as Bash. See the [Monitor tool reference](/docs/en/tools-reference#monitor-tool) for behavior and provider availability.
**Input:**

```
{
    "command": str,  # Shell script; each stdout line is an event, exit ends the watch
    "description": str,  # Short description shown in notifications
    "timeout_ms": int | None,  # Kill after this deadline (default 300000, max 3600000)
    "persistent": bool | None,  # Run for the lifetime of the session; stop with TaskStop
}
```

**Output:**

```
{
    "taskId": str,  # ID of the background monitor task
    "timeoutMs": int,  # Timeout deadline in milliseconds (0 when persistent)
    "persistent": bool | None,  # True when running until TaskStop or session end
}
```

### [​](#edit) Edit

**Tool name:** `Edit`
**Input:**

```
{
    "file_path": str,  # The absolute path to the file to modify
    "old_string": str,  # The text to replace
    "new_string": str,  # The text to replace it with
    "replace_all": bool | None,  # Replace all occurrences (default False)
}
```

**Output:**

```
{
    "message": str,  # Confirmation message
    "replacements": int,  # Number of replacements made
    "file_path": str,  # File path that was edited
}
```

### [​](#read) Read

**Tool name:** `Read`
**Input:**

```
{
    "file_path": str,  # The absolute path to the file to read
    "offset": int | None,  # The line number to start reading from
    "limit": int | None,  # The number of lines to read
}
```

**Output (Text files):**

```
{
    "content": str,  # File contents with line numbers
    "total_lines": int,  # Total number of lines in file
    "lines_returned": int,  # Lines actually returned
}
```

**Output (Images):**

```
{
    "image": str,  # Base64 encoded image data
    "mime_type": str,  # Image MIME type
    "file_size": int,  # File size in bytes
}
```

### [​](#write) Write

**Tool name:** `Write`
**Input:**

```
{
    "file_path": str,  # The absolute path to the file to write
    "content": str,  # The content to write to the file
}
```

**Output:**

```
{
    "message": str,  # Success message
    "bytes_written": int,  # Number of bytes written
    "file_path": str,  # File path that was written
}
```

### [​](#glob) Glob

**Tool name:** `Glob`
**Input:**

```
{
    "pattern": str,  # The glob pattern to match files against
    "path": str | None,  # The directory to search in (defaults to cwd)
}
```

**Output:**

```
{
    "matches": list[str],  # Array of matching file paths
    "count": int,  # Number of matches found
    "search_path": str,  # Search directory used
}
```

### [​](#grep) Grep

**Tool name:** `Grep`
**Input:**

```
{
    "pattern": str,  # The regular expression pattern
    "path": str | None,  # File or directory to search in
    "glob": str | None,  # Glob pattern to filter files
    "type": str | None,  # File type to search
    "output_mode": str | None,  # "content", "files_with_matches", or "count"
    "-i": bool | None,  # Case insensitive search
    "-n": bool | None,  # Show line numbers
    "-B": int | None,  # Lines to show before each match
    "-A": int | None,  # Lines to show after each match
    "-C": int | None,  # Lines to show before and after
    "head_limit": int | None,  # Limit output to first N lines/entries
    "multiline": bool | None,  # Enable multiline mode
}
```

**Output (content mode):**

```
{
    "matches": [
        {
            "file": str,
            "line_number": int | None,
            "line": str,
            "before_context": list[str] | None,
            "after_context": list[str] | None,
        }
    ],
    "total_matches": int,
}
```

**Output (files\_with\_matches mode):**

```
{
    "files": list[str],  # Files containing matches
    "count": int,  # Number of files with matches
}
```

### [​](#notebookedit) NotebookEdit

**Tool name:** `NotebookEdit`
**Input:**

```
{
    "notebook_path": str,  # Absolute path to the Jupyter notebook
    "cell_id": str | None,  # The ID of the cell to edit
    "new_source": str,  # The new source for the cell
    "cell_type": "code" | "markdown" | None,  # The type of the cell
    "edit_mode": "replace" | "insert" | "delete" | None,  # Edit operation type
}
```

**Output:**

```
{
    "message": str,  # Success message
    "edit_type": "replaced" | "inserted" | "deleted",  # Type of edit performed
    "cell_id": str | None,  # Cell ID that was affected
    "total_cells": int,  # Total cells in notebook after edit
}
```

### [​](#webfetch) WebFetch

**Tool name:** `WebFetch`
**Input:**

```
{
    "url": str,  # The URL to fetch content from
    "prompt": str,  # The prompt to run on the fetched content
}
```

**Output:**

```
{
    "bytes": int,  # Size of the fetched content in bytes
    "code": int,  # HTTP response code
    "codeText": str,  # HTTP response code text
    "result": str,  # Processed result from applying the prompt to the content
    "durationMs": int,  # Time to fetch and process the content, in milliseconds
    "url": str,  # URL that was fetched
}
```

### [​](#websearch) WebSearch

**Tool name:** `WebSearch`
**Input:**

```
{
    "query": str,  # The search query to use
    "allowed_domains": list[str] | None,  # Only include results from these domains
    "blocked_domains": list[str] | None,  # Never include results from these domains
}
```

**Output:**

```
{
    "query": str,  # The search query
    "results": list[str | {"tool_use_id": str, "content": list[{"title": str, "url": str}]}],
    "durationSeconds": float,  # Search duration in seconds
}
```

### [​](#todowrite) TodoWrite

**Tool name:** `TodoWrite`

As of Claude Code v2.1.142, `TodoWrite` is disabled by default. Use `TaskCreate`, `TaskGet`, `TaskUpdate`, and `TaskList` instead. See [Migrate to Task tools](/docs/en/agent-sdk/todo-tracking#migrate-to-task-tools) to update your monitoring code, or set `CLAUDE_CODE_ENABLE_TASKS=0` to revert to `TodoWrite`.

**Input:**

```
{
    "todos": [
        {
            "content": str,  # The task description
            "status": "pending" | "in_progress" | "completed",  # Task status
            "activeForm": str,  # Active form of the description
        }
    ]
}
```

**Output:**

```
{
    "message": str,  # Success message
    "stats": {"total": int, "pending": int, "in_progress": int, "completed": int},
}
```

### [​](#taskcreate) TaskCreate

**Tool name:** `TaskCreate`
**Input:**

```
{
    "subject": str,  # Short task title
    "description": str,  # Detailed task body
    "activeForm": str | None,  # Present-tense label shown while in progress
    "metadata": dict | None,  # Arbitrary caller metadata
}
```

**Output:**

```
{
    "task": {"id": str, "subject": str},  # Created task with assigned ID
}
```

### [​](#taskupdate) TaskUpdate

**Tool name:** `TaskUpdate`
**Input:**

```
{
    "taskId": str,  # ID of the task to patch
    "status": Literal["pending", "in_progress", "completed", "deleted"] | None,
    "subject": str | None,
    "description": str | None,
    "activeForm": str | None,
    "addBlocks": list[str] | None,  # Task IDs this task now blocks
    "addBlockedBy": list[str] | None,  # Task IDs that now block this task
    "owner": str | None,
    "metadata": dict | None,
}
```

**Output:**

```
{
    "success": bool,
    "taskId": str,
    "updatedFields": list[str],  # Names of fields that changed
    "error": str | None,
    "statusChange": {"from": str, "to": str} | None,
}
```

### [​](#taskget) TaskGet

**Tool name:** `TaskGet`
**Input:**

```
{
    "taskId": str,  # ID of the task to read
}
```

**Output:**

```
{
    "task": {
        "id": str,
        "subject": str,
        "description": str,
        "status": Literal["pending", "in_progress", "completed"],
        "blocks": list[str],
        "blockedBy": list[str],
    } | None,  # None when the ID is not found
}
```

### [​](#tasklist) TaskList

**Tool name:** `TaskList`
**Input:**

```
{}
```

**Output:**

```
{
    "tasks": [
        {
            "id": str,
            "subject": str,
            "status": Literal["pending", "in_progress", "completed"],
            "owner": str | None,
            "blockedBy": list[str],
        }
    ],
}
```

### [​](#bashoutput) BashOutput

**Tool name:** `BashOutput`
**Input:**

```
{
    "bash_id": str,  # The ID of the background shell
    "filter": str | None,  # Optional regex to filter output lines
}
```

**Output:**

```
{
    "output": str,  # New output since last check
    "status": "running" | "completed" | "failed",  # Current shell status
    "exitCode": int | None,  # Exit code when completed
}
```

### [​](#killbash) KillBash

**Tool name:** `KillBash`
**Input:**

```
{
    "shell_id": str  # The ID of the background shell to kill
}
```

**Output:**

```
{
    "message": str,  # Success message
    "shell_id": str,  # ID of the killed shell
}
```

### [​](#exitplanmode) ExitPlanMode

**Tool name:** `ExitPlanMode`
**Input:**

```
{
    "plan": str  # The plan to run by the user for approval
}
```

**Output:**

```
{
    "message": str,  # Confirmation message
    "approved": bool | None,  # Whether user approved the plan
}
```

### [​](#listmcpresources) ListMcpResources

**Tool name:** `ListMcpResourcesTool`
**Input:**

```
{
    "server": str | None  # Optional server name to filter resources by
}
```

**Output:**

```
{
    "resources": [
        {
            "uri": str,
            "name": str,
            "description": str | None,
            "mimeType": str | None,
            "server": str,
        }
    ],
    "total": int,
}
```

### [​](#readmcpresource) ReadMcpResource

**Tool name:** `ReadMcpResourceTool`
**Input:**

```
{
    "server": str,  # The MCP server name
    "uri": str,  # The resource URI to read
}
```

**Output:**

```
{
    "contents": [
        {"uri": str, "mimeType": str | None, "text": str | None, "blob": str | None}
    ],
    "server": str,
}
```

## [​](#advanced-features-with-claudesdkclient) Advanced Features with ClaudeSDKClient

### [​](#building-a-continuous-conversation-interface) Building a Continuous Conversation Interface

```
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
)
import asyncio


class ConversationSession:
    """Maintains a single conversation session with Claude."""

    def __init__(self, options: ClaudeAgentOptions | None = None):
        self.client = ClaudeSDKClient(options)
        self.turn_count = 0

    async def start(self):
        await self.client.connect()
        print("Starting conversation session. Claude will remember context.")
        print(
            "Commands: 'exit' to quit, 'interrupt' to stop current task, 'new' for new session"
        )

        while True:
            user_input = input(f"\n[Turn {self.turn_count + 1}] You: ")

            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "interrupt":
                await self.client.interrupt()
                print("Task interrupted!")
                continue
            elif user_input.lower() == "new":
                # Disconnect and reconnect for a fresh session
                await self.client.disconnect()
                await self.client.connect()
                self.turn_count = 0
                print("Started new conversation session (previous context cleared)")
                continue

            # Send message - the session retains all previous messages
            await self.client.query(user_input)
            self.turn_count += 1

            # Process response
            print(f"[Turn {self.turn_count}] Claude: ", end="")
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="")
            print()  # New line after response

        await self.client.disconnect()
        print(f"Conversation ended after {self.turn_count} turns.")


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"], permission_mode="acceptEdits"
    )
    session = ConversationSession(options)
    await session.start()