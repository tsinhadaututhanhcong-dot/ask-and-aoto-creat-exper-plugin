---
title: "// empty" produces no output when rate_limits is absent
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# "// empty" produces no output when rate_limits is absent
FIVE_H=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
WEEK=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

LIMITS=""
[ -n "$FIVE_H" ] && LIMITS="5h: $(printf '%.0f' "$FIVE_H")%"
[ -n "$WEEK" ] && LIMITS="${LIMITS:+$LIMITS }7d: $(printf '%.0f' "$WEEK")%"

[ -n "$LIMITS" ] && echo "[$MODEL] | $LIMITS" || echo "[$MODEL]"
```

### [​](#cache-expensive-operations) Cache expensive operations

Your status line script runs frequently during active sessions. Commands like `git status` or `git diff` can be slow, especially in large repositories. This example caches git information to a temp file and only refreshes it every 5 seconds.
The cache filename needs to be stable across status line invocations within a session, but unique across sessions so concurrent sessions in different repositories don’t read each other’s cached git state. Process-based identifiers like `$$`, `os.getpid()`, or `process.pid` change on every invocation and defeat the cache. Use the `session_id` from the JSON input instead: it’s stable for the lifetime of a session and unique per session.
Each script checks if the cache file is missing or older than 5 seconds before running git commands:

Bash

Python

Node.js

```
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
SESSION_ID=$(echo "$input" | jq -r '.session_id')

CACHE_FILE="/tmp/statusline-git-cache-$SESSION_ID"
CACHE_MAX_AGE=5  # seconds

cache_is_stale() {
    [ ! -f "$CACHE_FILE" ] || \
    # stat -f %m is macOS, stat -c %Y is Linux
    [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
}

if cache_is_stale; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        BRANCH=$(git branch --show-current 2>/dev/null)
        STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
    else
        echo "||" > "$CACHE_FILE"
    fi
fi

IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

if [ -n "$BRANCH" ]; then
    echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
else
    echo "[$MODEL] 📁 ${DIR##*/}"
fi
```

### [​](#windows-configuration) Windows configuration

On Windows, Claude Code runs status line commands through Git Bash when Git Bash is installed, or through PowerShell when Git Bash is absent.
Git Bash treats unquoted backslashes as escape characters, so a Windows-style path such as `C:\Users\username\script.mjs` reaches the script runner with its separators removed and the command fails without a visible error. Write file paths in the `command` string with forward slashes, as shown in the examples below. The `~` shorthand also works and expands to your Windows home directory.
To run a PowerShell script as your status line, invoke it via `powershell`. This works whether Claude Code routes the command through Git Bash or PowerShell:

settings.json

statusline.ps1

```
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File C:/Users/username/.claude/statusline.ps1"
  }
}
```

Or, when Git Bash is installed, run a Bash script directly:

settings.json

statusline.sh

```
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

## [​](#subagent-status-lines) Subagent status lines

The `subagentStatusLine` setting renders a custom row body for each [subagent](/docs/en/sub-agents) shown in the agent panel below the prompt. Use it to replace the default `name · description · token count` row with your own formatting.

```
{
  "subagentStatusLine": {
    "type": "command",
    "command": "~/.claude/subagent-statusline.sh"
  }
}
```

The command runs once per refresh tick with all visible subagent rows passed as a single JSON object on stdin. The input includes the [base hook fields](/docs/en/hooks#common-input-fields) plus `columns` (the usable row width) and a `tasks` array, where each task has `id`, `name`, `type`, `status`, `description`, `label`, `startTime`, `tokenCount`, `tokenSamples`, and `cwd`.
Write one JSON line to stdout per row you want to override, in the form `{"id": "<task id>", "content": "<row body>"}`. The `content` string is rendered as-is, including ANSI colors and OSC 8 hyperlinks. Omit a task’s `id` to keep the default rendering for that row; emit an empty `content` string to hide it.
The same trust and `disableAllHooks` gates that apply to `statusLine` apply here. Plugins can ship a default `subagentStatusLine` in their [`settings.json`](/docs/en/plugins-reference#standard-plugin-layout).

## [​](#tips) Tips

* **Test with mock input**: `echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/home/user/project"},"context_window":{"used_percentage":25},"session_id":"test-session-abc"}' | ./statusline.sh`
* **Keep output short**: the status bar has limited width, so long output may get truncated or wrap awkwardly
* **Cache slow operations**: your script runs frequently during active sessions, so commands like `git status` can cause lag. See the [caching example](#cache-expensive-operations) for how to handle this.

Community projects like [ccstatusline](https://github.com/sirmalloc/ccstatusline) and [starship-claude](https://github.com/martinemde/starship-claude) provide pre-built configurations with themes and additional features.

## [​](#troubleshooting) Troubleshooting

**Status line not appearing**

* Verify your script is executable: `chmod +x ~/.claude/statusline.sh`
* Check that your script outputs to stdout, not stderr
* Run your script manually to verify it produces output
* On Windows with Git Bash installed, backslashes in the `command` path are likely being consumed as escape characters before the script runs. Use forward slashes in the path. See [Windows configuration](#windows-configuration).
* If `disableAllHooks` is set to `true` in your settings, the status line is also disabled. Remove this setting or set it to `false` to re-enable.
* Run `claude --debug` to log the exit code and stderr from the first status line invocation in a session
* Ask Claude to read your settings file and execute the `statusLine` command directly to surface errors

**Status line shows `--` or empty values**

* Fields may be `null` before the first API response completes
* Handle null values in your script with fallbacks such as `// 0` in jq
* Restart Claude Code if values remain empty after multiple messages

**Context percentage shows unexpected values**

* Use `used_percentage` for the simplest accurate context state
* Context percentage may differ from `/context` output due to when each is calculated

**OSC 8 links not clickable**

* Verify your terminal supports OSC 8 hyperlinks (iTerm2, Kitty, WezTerm)
* Terminal.app does not support clickable links
* If link text appears but isn’t clickable, Claude Code may not have detected hyperlink support in your terminal. This commonly affects Windows Terminal and other emulators not in the auto-detection list. Set the `FORCE_HYPERLINK` environment variable to override detection before launching Claude Code:

  ```
  FORCE_HYPERLINK=1 claude
  ```

  In PowerShell, set the variable in the current session first:

  ```
  $env:FORCE_HYPERLINK = "1"; claude
  ```
* SSH and tmux sessions may strip OSC sequences depending on configuration
* If escape sequences appear as literal text like `\e]8;;`, use `printf '%b'` instead of `echo -e` for more reliable escape handling

**Display glitches with escape sequences**

* Complex escape sequences (ANSI colors, OSC 8 links) can occasionally cause garbled output if they overlap with other UI updates
* If you see corrupted text, try simplifying your script to plain text output
* Multi-line status lines with escape codes are more prone to rendering issues than single-line plain text

**Workspace trust required**

* The status line command only runs if you’ve accepted the workspace trust dialog for the current directory. Because `statusLine` executes a shell command, it requires the same trust acceptance as hooks and other shell-executing settings.
* If trust isn’t accepted, you’ll see the notification `statusline skipped · restart to fix` instead of your status line output. Restart Claude Code and accept the trust prompt to enable it.

**Script errors or hangs**

* Scripts that exit with non-zero codes or produce no output cause the status line to go blank
* Slow scripts block the status line from updating until they complete. Keep scripts fast to avoid stale output.
* If a new update triggers while a slow script is running, the in-flight script is cancelled
* Test your script independently with mock input before configuring it

**Notifications share the status line row**

* System notifications like MCP server errors and auto-updates display on the right side of the same row as your status line. Transient notifications such as the context-low warning also cycle through this area.
* Enabling verbose mode adds a token counter to this area
* On narrow terminals, these notifications may truncate your status line output

Was this page helpful?

YesNo

[Voice dictation](/docs/en/voice-dictation)[Customize keyboard shortcuts](/docs/en/keybindings)

⌘I

---