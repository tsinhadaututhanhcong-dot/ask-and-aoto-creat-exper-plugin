---
type: Reference
title: Expected dict shape for output_format
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Expected dict shape for output_format
{
    "type": "json_schema",
    "schema": {...},  # Your JSON Schema definition
}
```

| Field | Required | Description |
| --- | --- | --- |
| `type` | Yes | Must be `"json_schema"` for JSON Schema validation |
| `schema` | Yes | JSON Schema definition for output validation |

### [​](#systempromptpreset) `SystemPromptPreset`

Configuration for using Claude Code’s preset system prompt with optional additions.

```
class SystemPromptPreset(TypedDict):
    type: Literal["preset"]
    preset: Literal["claude_code"]
    append: NotRequired[str]
    exclude_dynamic_sections: NotRequired[bool]
```

| Field | Required | Description |
| --- | --- | --- |
| `type` | Yes | Must be `"preset"` to use a preset system prompt |
| `preset` | Yes | Must be `"claude_code"` to use Claude Code’s system prompt |
| `append` | No | Additional instructions to append to the preset system prompt |
| `exclude_dynamic_sections` | No | Move per-session context such as working directory, the git-repo flag, and auto-memory paths from the system prompt into the first user message. Improves prompt-cache reuse across users and machines. See [Modify system prompts](/docs/en/agent-sdk/modifying-system-prompts#improve-prompt-caching-across-users-and-machines) |

### [​](#settingsource) `SettingSource`

Controls which filesystem-based configuration sources the SDK loads settings from.

```
SettingSource = Literal["user", "project", "local"]
```

| Value | Description | Location |
| --- | --- | --- |
| `"user"` | Global user settings | `~/.claude/settings.json` |
| `"project"` | Shared project settings (version controlled) | `.claude/settings.json` |
| `"local"` | Local project settings (not version controlled) | `.claude/settings.local.json` |

#### [​](#default-behavior) Default behavior

When `setting_sources` is omitted or `None`, `query()` loads the same filesystem settings as the Claude Code CLI: user, project, and local. Endpoint-managed policy is loaded in all cases; server-managed settings are fetched when the session authenticates with an organization credential on an [eligible configuration](/docs/en/server-managed-settings#platform-availability). See [What settingSources does not control](/docs/en/agent-sdk/claude-code-features#what-settingsources-does-not-control) for inputs that are read regardless of this option, and how to disable them.

#### [​](#why-use-setting_sources) Why use setting\_sources

**Disable filesystem settings:**

```