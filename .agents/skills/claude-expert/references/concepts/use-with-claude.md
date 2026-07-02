---
title: Use with Claude
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Use with Claude
options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add", "mcp__calc__multiply"],
)
```

### [​](#list_sessions) `list_sessions()`

Lists past sessions with metadata. Filter by project directory or list sessions across all projects. Synchronous; returns immediately.

```
def list_sessions(
    directory: str | None = None,
    limit: int | None = None,
    include_worktrees: bool = True
) -> list[SDKSessionInfo]
```

#### [​](#parameters-4) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `directory` | `str | None` | `None` | Directory to list sessions for. When omitted, returns sessions across all projects |
| `limit` | `int | None` | `None` | Maximum number of sessions to return |
| `include_worktrees` | `bool` | `True` | When `directory` is inside a git repository, include sessions from all worktree paths |

#### [​](#return-type-sdksessioninfo) Return type: `SDKSessionInfo`

| Property | Type | Description |
| --- | --- | --- |
| `session_id` | `str` | Unique session identifier |
| `summary` | `str` | Display title: custom title, auto-generated summary, or first prompt |
| `last_modified` | `int` | Last modified time in milliseconds since epoch |
| `file_size` | `int | None` | Session file size in bytes (`None` for remote storage backends) |
| `custom_title` | `str | None` | User-set session title |
| `first_prompt` | `str | None` | First meaningful user prompt in the session |
| `git_branch` | `str | None` | Git branch at the end of the session |
| `cwd` | `str | None` | Working directory for the session |
| `tag` | `str | None` | User-set session tag (see [`tag_session()`](#tag_session)) |
| `created_at` | `int | None` | Session creation time in milliseconds since epoch |

#### [​](#example-3) Example

Print the 10 most recent sessions for a project. Results are sorted by `last_modified` descending, so the first item is the newest. Omit `directory` to search across all projects.

```
from claude_agent_sdk import list_sessions

for session in list_sessions(directory="/path/to/project", limit=10):
    print(f"{session.summary} ({session.session_id})")
```

### [​](#get_session_messages) `get_session_messages()`

Retrieves messages from a past session. Synchronous; returns immediately.

```
def get_session_messages(
    session_id: str,
    directory: str | None = None,
    limit: int | None = None,
    offset: int = 0
) -> list[SessionMessage]
```

#### [​](#parameters-5) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `session_id` | `str` | required | The session ID to retrieve messages for |
| `directory` | `str | None` | `None` | Project directory to look in. When omitted, searches all projects |
| `limit` | `int | None` | `None` | Maximum number of messages to return |
| `offset` | `int` | `0` | Number of messages to skip from the start |

#### [​](#return-type-sessionmessage) Return type: `SessionMessage`

| Property | Type | Description |
| --- | --- | --- |
| `type` | `Literal["user", "assistant"]` | Message role |
| `uuid` | `str` | Unique message identifier |
| `session_id` | `str` | Session identifier |
| `message` | `Any` | Raw message content |
| `parent_tool_use_id` | `None` | Reserved for future use |

#### [​](#example-4) Example

```
from claude_agent_sdk import list_sessions, get_session_messages

sessions = list_sessions(limit=1)
if sessions:
    messages = get_session_messages(sessions[0].session_id)
    for msg in messages:
        print(f"[{msg.type}] {msg.uuid}")
```

### [​](#get_session_info) `get_session_info()`

Reads metadata for a single session by ID without scanning the full project directory. Synchronous; returns immediately.

```
def get_session_info(
    session_id: str,
    directory: str | None = None,
) -> SDKSessionInfo | None
```

#### [​](#parameters-6) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `session_id` | `str` | required | UUID of the session to look up |
| `directory` | `str | None` | `None` | Project directory path. When omitted, searches all project directories |

Returns [`SDKSessionInfo`](#return-type-sdksessioninfo), or `None` if the session is not found.

#### [​](#example-5) Example

Look up a single session’s metadata without scanning the project directory. Useful when you already have a session ID from a previous run.

```
from claude_agent_sdk import get_session_info

info = get_session_info("550e8400-e29b-41d4-a716-446655440000")
if info:
    print(f"{info.summary} (branch: {info.git_branch}, tag: {info.tag})")
```

### [​](#rename_session) `rename_session()`

Renames a session by appending a custom-title entry. Repeated calls are safe; the most recent title wins. Synchronous.

```
def rename_session(
    session_id: str,
    title: str,
    directory: str | None = None,
) -> None
```

#### [​](#parameters-7) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `session_id` | `str` | required | UUID of the session to rename |
| `title` | `str` | required | New title. Must be non-empty after stripping whitespace |
| `directory` | `str | None` | `None` | Project directory path. When omitted, searches all project directories |

Raises `ValueError` if `session_id` is not a valid UUID or `title` is empty; `FileNotFoundError` if the session cannot be found.

#### [​](#example-6) Example

Rename the most recent session so it’s easier to find later. The new title appears in [`SDKSessionInfo.custom_title`](#return-type-sdksessioninfo) on subsequent reads.

```
from claude_agent_sdk import list_sessions, rename_session

sessions = list_sessions(directory="/path/to/project", limit=1)
if sessions:
    rename_session(sessions[0].session_id, "Refactor auth module")
```

### [​](#tag_session) `tag_session()`

Tags a session. Pass `None` to clear the tag. Repeated calls are safe; the most recent tag wins. Synchronous.

```
def tag_session(
    session_id: str,
    tag: str | None,
    directory: str | None = None,
) -> None
```

#### [​](#parameters-8) Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `session_id` | `str` | required | UUID of the session to tag |
| `tag` | `str | None` | required | Tag string, or `None` to clear. Unicode-sanitized before storing |
| `directory` | `str | None` | `None` | Project directory path. When omitted, searches all project directories |

Raises `ValueError` if `session_id` is not a valid UUID or `tag` is empty after sanitization; `FileNotFoundError` if the session cannot be found.

#### [​](#example-7) Example

Tag a session, then filter by that tag on a later read. Pass `None` to clear an existing tag.

```
from claude_agent_sdk import list_sessions, tag_session