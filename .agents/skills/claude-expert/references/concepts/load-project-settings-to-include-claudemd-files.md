---
type: Reference
title: Load project settings to include CLAUDE.md files
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Load project settings to include CLAUDE.md files
async for message in query(
    prompt="Add a new feature following project conventions",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",  # Use Claude Code's system prompt
        },
        setting_sources=["project"],  # Loads CLAUDE.md from project
        allowed_tools=["Read", "Write", "Edit"],
    ),
):
    print(message)
```

#### [​](#settings-precedence) Settings precedence

When multiple sources are loaded, settings are merged with this precedence (highest to lowest):

1. Local settings (`.claude/settings.local.json`)
2. Project settings (`.claude/settings.json`)
3. User settings (`~/.claude/settings.json`)

Programmatic options such as `agents` and `allowed_tools` override user, project, and local filesystem settings. Managed policy settings take precedence over programmatic options.

### [​](#agentdefinition) `AgentDefinition`

Configuration for a subagent defined programmatically.

```
@dataclass
class AgentDefinition:
    description: str
    prompt: str
    tools: list[str] | None = None
    disallowedTools: list[str] | None = None
    model: str | None = None
    skills: list[str] | None = None
    memory: Literal["user", "project", "local"] | None = None
    mcpServers: list[str | dict[str, Any]] | None = None
    initialPrompt: str | None = None
    maxTurns: int | None = None
    background: bool | None = None
    effort: EffortLevel | int | None = None
    permissionMode: PermissionMode | None = None
```

| Field | Required | Description |
| --- | --- | --- |
| `description` | Yes | Natural language description of when to use this agent |
| `prompt` | Yes | The agent’s system prompt |
| `tools` | No | Array of allowed tool names. If omitted, inherits all tools |
| `disallowedTools` | No | Array of tool names to remove from the agent’s tool set. MCP server-level patterns are also accepted: `mcp__server` or `mcp__server__*` removes every tool from that server, and `mcp__*` removes every MCP tool from any server |
| `model` | No | Model override for this agent. Accepts an alias such as `"sonnet"`, `"opus"`, `"haiku"`, or `"inherit"`, or a full model ID. If omitted, uses the main model |
| `skills` | No | List of skill names to preload into the agent’s context at startup. Unlisted skills remain invocable through the Skill tool |
| `memory` | No | Memory source for this agent: `"user"`, `"project"`, or `"local"` |
| `mcpServers` | No | MCP servers available to this agent. Each entry is a server name or an inline `{name: config}` dict |
| `initialPrompt` | No | Auto-submitted as the first user turn when this agent runs as the main thread agent |
| `maxTurns` | No | Maximum number of agentic turns before the agent stops |
| `background` | No | Run this agent as a non-blocking background task when invoked |
| `effort` | No | Reasoning effort level for this agent. Accepts a named level or an integer. See [`EffortLevel`](#effortlevel) |
| `permissionMode` | No | Permission mode for tool execution within this agent. See [`PermissionMode`](#permissionmode) |

`AgentDefinition` field names use camelCase, such as `disallowedTools`, `permissionMode`, and `maxTurns`. These names map directly to the wire format shared with the TypeScript SDK. This differs from `ClaudeAgentOptions`, which uses Python snake\_case for the equivalent top-level fields such as `disallowed_tools` and `permission_mode`. Because `AgentDefinition` is a dataclass, passing a snake\_case keyword raises a `TypeError` at construction time.

### [​](#permissionmode) `PermissionMode`

Permission modes for controlling tool execution.

```
PermissionMode = Literal[
    "default",  # Standard permission behavior
    "acceptEdits",  # Auto-accept file edits
    "plan",  # Planning mode - explore without editing
    "dontAsk",  # Deny anything not pre-approved instead of prompting
    "bypassPermissions",  # Bypass permission checks; explicit ask rules still prompt (use with caution)
]
```

### [​](#effortlevel) `EffortLevel`

Effort levels for guiding thinking depth.

```
EffortLevel = Literal[
    "low",  # Minimal thinking, fastest responses
    "medium",  # Moderate thinking
    "high",  # Deep reasoning
    "xhigh",  # Extended reasoning (Opus 4.8 and Opus 4.7; falls back to "high" on other models)
    "max",  # Maximum effort
]
```

### [​](#canusetool) `CanUseTool`

Type alias for tool permission callback functions.

```
CanUseTool = Callable[
    [str, dict[str, Any], ToolPermissionContext], Awaitable[PermissionResult]
]
```

The callback receives:

* `tool_name`: Name of the tool being called
* `input_data`: The tool’s input parameters
* `context`: A `ToolPermissionContext` with additional information

Returns a `PermissionResult` (either `PermissionResultAllow` or `PermissionResultDeny`).

### [​](#toolpermissioncontext) `ToolPermissionContext`

Context information passed to tool permission callbacks.

```
@dataclass
class ToolPermissionContext:
    signal: Any | None = None  # Future: abort signal support
    suggestions: list[PermissionUpdate] = field(default_factory=list)
    blocked_path: str | None = None
    decision_reason: str | None = None
    title: str | None = None
    display_name: str | None = None
    description: str | None = None
```

| Field | Type | Description |
| --- | --- | --- |
| `signal` | `Any | None` | Reserved for future abort signal support |
| `suggestions` | `list[PermissionUpdate]` | Permission update suggestions from the CLI. Bash prompts include a suggestion with the `localSettings` destination, so returning it in `updated_permissions` writes the rule to `.claude/settings.local.json` and persists across sessions. |
| `blocked_path` | `str | None` | File path that triggered the permission request, when applicable. For example, when a Bash command tries to access a path outside allowed directories |
| `decision_reason` | `str | None` | Reason this permission request was triggered. Forwarded from a PreToolUse hook’s `permissionDecisionReason` when the hook returned `"ask"` |
| `title` | `str | None` | Full permission prompt sentence, such as `Claude wants to read foo.txt`. Use as the primary prompt text when present |
| `display_name` | `str | None` | Short noun phrase for the tool action, such as `Read file`, suitable for button labels |
| `description` | `str | None` | Human-readable subtitle for the permission UI |

### [​](#permissionresult) `PermissionResult`

Union type for permission callback results.

```
PermissionResult = PermissionResultAllow | PermissionResultDeny
```

### [​](#permissionresultallow) `PermissionResultAllow`

Result indicating the tool call should be allowed.

```
@dataclass
class PermissionResultAllow:
    behavior: Literal["allow"] = "allow"
    updated_input: dict[str, Any] | None = None
    updated_permissions: list[PermissionUpdate] | None = None
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `behavior` | `Literal["allow"]` | `"allow"` | Must be “allow” |
| `updated_input` | `dict[str, Any] | None` | `None` | Modified input to use instead of original |
| `updated_permissions` | `list[PermissionUpdate] | None` | `None` | Permission updates to apply |

### [​](#permissionresultdeny) `PermissionResultDeny`

Result indicating the tool call should be denied.

```
@dataclass
class PermissionResultDeny:
    behavior: Literal["deny"] = "deny"
    message: str = ""
    interrupt: bool = False
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `behavior` | `Literal["deny"]` | `"deny"` | Must be “deny” |
| `message` | `str` | `""` | Message explaining why the tool was denied |
| `interrupt` | `bool` | `False` | Whether to interrupt the current execution |

### [​](#permissionupdate) `PermissionUpdate`

Configuration for updating permissions programmatically.

```
@dataclass
class PermissionUpdate:
    type: Literal[
        "addRules",
        "replaceRules",
        "removeRules",
        "setMode",
        "addDirectories",
        "removeDirectories",
    ]
    rules: list[PermissionRuleValue] | None = None
    behavior: Literal["allow", "deny", "ask"] | None = None
    mode: PermissionMode | None = None
    directories: list[str] | None = None
    destination: (
        Literal["userSettings", "projectSettings", "localSettings", "session"] | None
    ) = None
```

| Field | Type | Description |
| --- | --- | --- |
| `type` | `Literal[...]` | The type of permission update operation |
| `rules` | `list[PermissionRuleValue] | None` | Rules for add/replace/remove operations |
| `behavior` | `Literal["allow", "deny", "ask"] | None` | Behavior for rule-based operations |
| `mode` | `PermissionMode | None` | Mode for setMode operation |
| `directories` | `list[str] | None` | Directories for add/remove directory operations |
| `destination` | `Literal[...] | None` | Where to apply the permission update |

### [​](#permissionrulevalue) `PermissionRuleValue`

A rule to add, replace, or remove in a permission update.

```
@dataclass
class PermissionRuleValue:
    tool_name: str
    rule_content: str | None = None
```

### [​](#toolspreset) `ToolsPreset`

Preset tools configuration for using Claude Code’s default tool set.

```
class ToolsPreset(TypedDict):
    type: Literal["preset"]
    preset: Literal["claude_code"]
```

### [​](#thinkingconfig) `ThinkingConfig`

Controls extended thinking behavior. A union of three configurations:

```
ThinkingDisplay = Literal["summarized", "omitted"]


class ThinkingConfigAdaptive(TypedDict):
    type: Literal["adaptive"]
    display: NotRequired[ThinkingDisplay]


class ThinkingConfigEnabled(TypedDict):
    type: Literal["enabled"]
    budget_tokens: int
    display: NotRequired[ThinkingDisplay]


class ThinkingConfigDisabled(TypedDict):
    type: Literal["disabled"]


ThinkingConfig = ThinkingConfigAdaptive | ThinkingConfigEnabled | ThinkingConfigDisabled
```

| Variant | Fields | Description |
| --- | --- | --- |
| `adaptive` | `type`, `display` | Claude adaptively decides when to think |
| `enabled` | `type`, `budget_tokens`, `display` | Enable thinking with a specific token budget |
| `disabled` | `type` | Disable thinking |

The optional `display` field controls whether thinking text is returned `"summarized"` or `"omitted"`. On Claude Opus 4.7 and later, the API default is `"omitted"`, so set `"summarized"` to receive thinking content in [`ThinkingBlock`](#thinkingblock) outputs.
Because these are `TypedDict` classes, they’re plain dicts at runtime. Either construct them as dict literals or call the class like a constructor; both produce a `dict`. Access fields with `config["budget_tokens"]`, not `config.budget_tokens`:

```
from claude_agent_sdk import ClaudeAgentOptions, ThinkingConfigEnabled