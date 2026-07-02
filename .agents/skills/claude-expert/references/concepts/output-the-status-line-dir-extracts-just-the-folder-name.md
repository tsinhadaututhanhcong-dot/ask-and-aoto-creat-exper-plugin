---
title: Output the status line - ${DIR##*/} extracts just the folder name
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Output the status line - ${DIR##*/} extracts just the folder name
echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
```

2

Make it executable

Mark the script as executable so your shell can run it:

```
chmod +x ~/.claude/statusline.sh
```

3

Add to settings

Tell Claude Code to run your script as the status line. Add this configuration to `~/.claude/settings.json`, which sets `type` to `"command"` (meaning “run this shell command”) and points `command` to your script:

```
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

Your status line appears at the bottom of the interface. Settings reload automatically, but changes won’t appear until your next interaction with Claude Code.

## [​](#how-status-lines-work) How status lines work

Claude Code runs your script and pipes [JSON session data](#available-data) to it via stdin. Your script reads the JSON, extracts what it needs, and prints text to stdout. Claude Code displays whatever your script prints.
**When it updates**
Your script runs after each new assistant message, after `/compact` finishes, when the permission mode changes, or when vim mode toggles. Updates are debounced at 300ms, meaning rapid changes batch together and your script runs once things settle. If a new update triggers while your script is still running, the in-flight execution is cancelled. If you edit your script, the changes won’t appear until your next interaction with Claude Code triggers an update.
These triggers can go quiet when the main session is idle, for example while a coordinator waits on background subagents. To keep time-based or externally-sourced segments current during idle periods, set [`refreshInterval`](#manually-configure-a-status-line) to also re-run the command on a fixed timer.
**What your script can output**

* **Multiple lines**: each `echo` or `print` statement displays as a separate row. See the [multi-line example](#display-multiple-lines).
* **Colors**: use [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) like `\033[32m` for green (terminal must support them). See the [git status example](#git-status-with-colors).
* **Links**: use [OSC 8 escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC) to make text clickable (Cmd+click on macOS, Ctrl+click on Windows/Linux). Requires a terminal that supports hyperlinks like iTerm2, Kitty, or WezTerm. See the [clickable links example](#clickable-links).

**Sizing output to the terminal**
Claude Code captures your script’s output instead of connecting it directly to the terminal, so `tput cols` and language-level width detection cannot read the terminal size from inside the script. Read the `COLUMNS` and `LINES` environment variables instead. Claude Code sets these to the current terminal dimensions before running your script. Requires Claude Code v2.1.153 or later.

The status line runs locally and does not consume API tokens. It temporarily hides during certain UI interactions, including autocomplete suggestions, the help menu, and permission prompts.

## [​](#available-data) Available data

Claude Code sends the following JSON fields to your script via stdin:

| Field | Description |
| --- | --- |
| `model.id`, `model.display_name` | Current model identifier and display name |
| `cwd`, `workspace.current_dir` | Current working directory. Both fields contain the same value; `workspace.current_dir` is preferred for consistency with `workspace.project_dir`. |
| `workspace.project_dir` | Directory where Claude Code was launched, which may differ from `cwd` if the working directory changes during a session |
| `workspace.added_dirs` | Additional directories added via `/add-dir` or `--add-dir`. Empty array if none have been added |
| `workspace.git_worktree` | Git worktree name when the current directory is inside a linked worktree created with `git worktree add`. Absent in the main working tree. Populated for any git worktree, unlike `worktree.*` which applies only to `--worktree` sessions |
| `workspace.repo.host`, `workspace.repo.owner`, `workspace.repo.name` | Repository identity parsed from the `origin` remote, for example `"github.com"`, `"anthropics"`, `"claude-code"`. Absent outside a git repository or when no `origin` remote is configured |
| `cost.total_cost_usd` | Estimated session cost in USD, computed client-side. May differ from your actual bill |
| `cost.total_duration_ms` | Total wall-clock time since the session started, in milliseconds |
| `cost.total_api_duration_ms` | Total time spent waiting for API responses in milliseconds |
| `cost.total_lines_added`, `cost.total_lines_removed` | Lines of code changed |
| `context_window.total_input_tokens`, `context_window.total_output_tokens` | Token counts currently in the context window, from the most recent API response. Input includes cache reads and writes. Before v2.1.132 these were cumulative session totals |
| `context_window.context_window_size` | Maximum context window size in tokens. 200000 by default, or 1000000 for models with extended context. |
| `context_window.used_percentage` | Pre-calculated percentage of context window used |
| `context_window.remaining_percentage` | Pre-calculated percentage of context window remaining |
| `context_window.current_usage` | Token counts from the last API call, described in [context window fields](#context-window-fields) |
| `exceeds_200k_tokens` | Whether the total token count (input, cache, and output tokens combined) from the most recent API response exceeds 200k. This is a fixed threshold regardless of actual context window size. |
| `effort.level` | Current reasoning effort (`low`, `medium`, `high`, `xhigh`, or `max`). Reflects the live session value, including mid-session `/effort` changes. Ultracode is not a distinct level and reports as `xhigh`. Absent when the current model does not support the effort parameter |
| `thinking.enabled` | Whether extended thinking is enabled for the session |
| `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` | Percentage of the 5-hour or 7-day rate limit consumed, from 0 to 100 |
| `rate_limits.five_hour.resets_at`, `rate_limits.seven_day.resets_at` | Unix epoch seconds when the 5-hour or 7-day rate limit window resets |
| `session_id` | Unique session identifier |
| `session_name` | Custom session name set with the `--name` flag or `/rename`. Absent if no custom name has been set |
| `transcript_path` | Path to conversation transcript file |
| `version` | Claude Code version |
| `output_style.name` | Name of the current output style |
| `vim.mode` | Current vim mode (`NORMAL`, `INSERT`, `VISUAL`, or `VISUAL LINE`) when [vim mode](/docs/en/interactive-mode#vim-editor-mode) is enabled |
| `agent.name` | Agent name when running with the `--agent` flag or agent settings configured |
| `pr.number`, `pr.url` | Open pull request for the current branch. Mirrors the PR badge in the bottom status bar. Absent until a PR is found, when not in a git repository, or once the PR merges or closes |
| `pr.review_state` | Review status of the open PR: `approved`, `pending`, `changes_requested`, or `draft`. May be independently absent even when `pr` is present |
| `worktree.name` | Name of the active worktree. Present only during `--worktree` sessions |
| `worktree.path` | Absolute path to the worktree directory |
| `worktree.branch` | Git branch name for the worktree (for example, `"worktree-my-feature"`). Absent for hook-based worktrees |
| `worktree.original_cwd` | The directory Claude was in before entering the worktree |
| `worktree.original_branch` | Git branch checked out before entering the worktree. Absent for hook-based worktrees |

Full JSON schema

Your status line command receives this JSON structure via stdin:

```
{
  "cwd": "/current/working/directory",
  "session_id": "abc123...",
  "session_name": "my-session",
  "transcript_path": "/path/to/transcript.jsonl",
  "model": {
    "id": "claude-opus-4-8",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory",
    "added_dirs": [],
    "git_worktree": "feature-xyz",
    "repo": {
      "host": "github.com",
      "owner": "anthropics",
      "name": "claude-code"
    }
  },
  "version": "2.1.90",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  },
  "context_window": {
    "total_input_tokens": 15500,
    "total_output_tokens": 1200,
    "context_window_size": 200000,
    "used_percentage": 8,
    "remaining_percentage": 92,
    "current_usage": {
      "input_tokens": 8500,
      "output_tokens": 1200,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  },
  "exceeds_200k_tokens": false,
  "effort": {
    "level": "high"
  },
  "thinking": {
    "enabled": true
  },
  "rate_limits": {
    "five_hour": {
      "used_percentage": 23.5,
      "resets_at": 1738425600
    },
    "seven_day": {
      "used_percentage": 41.2,
      "resets_at": 1738857600
    }
  },
  "vim": {
    "mode": "NORMAL"
  },
  "agent": {
    "name": "security-reviewer"
  },
  "pr": {
    "number": 1234,
    "url": "https://github.com/anthropics/claude-code/pull/1234",
    "review_state": "pending"
  },
  "worktree": {
    "name": "my-feature",
    "path": "/path/to/.claude/worktrees/my-feature",
    "branch": "worktree-my-feature",
    "original_cwd": "/path/to/project",
    "original_branch": "main"
  }
}
```

**Fields that may be absent** (not present in JSON):

* `session_name`: appears only when a custom name has been set with `--name` or `/rename`
* `workspace.git_worktree`: appears only when the current directory is inside a linked git worktree
* `workspace.repo`: appears only inside a git repository with an `origin` remote configured
* `effort`: appears only when the current model supports the reasoning effort parameter
* `vim`: appears only when vim mode is enabled
* `agent`: appears only when running with the `--agent` flag or agent settings configured
* `pr`: appears only while an open PR is found for the current branch, and is removed once the PR merges or closes. `pr.review_state` may be independently absent
* `worktree`: appears only during `--worktree` sessions. When present, `branch` and `original_branch` may also be absent for hook-based worktrees
* `rate_limits`: appears only for Claude.ai subscribers (Pro/Max) after the first API response in the session. Each window (`five_hour`, `seven_day`) may be independently absent. Use `jq -r '.rate_limits.five_hour.used_percentage // empty'` to handle absence gracefully.

**Fields that may be `null`**:

* `context_window.current_usage`: `null` before the first API call in a session, and again after `/compact` until the next API call repopulates it
* `context_window.used_percentage`, `context_window.remaining_percentage`: may be `null` early in the session

Handle missing fields with conditional access and null values with fallback defaults in your scripts.

### [​](#context-window-fields) Context window fields

The `context_window` object describes the live context window from the most recent API response. As of v2.1.132, `total_input_tokens` and `total_output_tokens` reflect current context usage, not cumulative session totals.

* **Combined totals** (`total_input_tokens`, `total_output_tokens`): tokens currently in the context window. `total_input_tokens` is the sum of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`; `total_output_tokens` is the output tokens from the most recent response. Both are `0` before the first API response.
* **Per-component usage** (`current_usage`): the same token counts broken out by category. Use this when you need cache hits separate from fresh input.

The `current_usage` object contains:

* `input_tokens`: input tokens in current context
* `output_tokens`: output tokens generated
* `cache_creation_input_tokens`: tokens written to cache
* `cache_read_input_tokens`: tokens read from cache

For what the cache fields mean and how they’re billed, see [check cache performance](/docs/en/prompt-caching#check-cache-performance).
The `used_percentage` field is calculated from input tokens only: `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. It does not include `output_tokens`.
If you calculate context percentage manually from `current_usage`, use the same input-only formula to match `used_percentage`.
The `current_usage` object is `null` before the first API call in a session, and again immediately after `/compact` until the next API call repopulates it.

## [​](#examples) Examples

These examples show common status line patterns. To use any example:

1. Save the script to a file like `~/.claude/statusline.sh` (or `.py`/`.js`)
2. Make it executable: `chmod +x ~/.claude/statusline.sh`
3. Add the path to your [settings](#manually-configure-a-status-line)

The Bash examples use [`jq`](https://jqlang.github.io/jq/) to parse JSON. Python and Node.js have built-in JSON parsing.

### [​](#context-window-usage) Context window usage

Display the current model and context window usage with a visual progress bar. Each script reads JSON from stdin, extracts the `used_percentage` field, and builds a 10-character bar where filled blocks (▓) represent usage:

![A status line showing model name and a progress bar with percentage](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=15b58ab3602f036939145dde3165c6f7)

Bash

Python

Node.js

```
#!/bin/bash