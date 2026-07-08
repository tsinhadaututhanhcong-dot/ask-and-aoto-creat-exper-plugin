---
type: Reference
title: Automate actions with hooks - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Automate actions with hooks - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)

Hooks are user-defined shell commands that execute at specific points in Claude Code’s lifecycle. They provide deterministic control over Claude Code’s behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them. Use hooks to enforce project rules, automate repetitive tasks, and integrate Claude Code with your existing tools.
For decisions that require judgment rather than deterministic rules, you can also use [prompt-based hooks](#prompt-based-hooks) or [agent-based hooks](#agent-based-hooks) that use a Claude model to evaluate conditions.
For other ways to extend Claude Code, see [skills](/docs/en/skills) for giving Claude additional instructions and executable commands, [subagents](/docs/en/sub-agents) for running tasks in isolated contexts, and [plugins](/docs/en/plugins) for packaging extensions to share across projects.

This guide covers common use cases and how to get started. For full event schemas, JSON input/output formats, and advanced features like async hooks and MCP tool hooks, see the [Hooks reference](/docs/en/hooks).

## [​](#set-up-your-first-hook) Set up your first hook

To create a hook, add a `hooks` block to a [settings file](#configure-hook-location). This walkthrough creates a desktop notification hook, so you get alerted whenever Claude is waiting for your input instead of watching the terminal.

1

Add the hook to your settings

Open `~/.claude/settings.json` and add a `Notification` hook. The example below uses `osascript` for macOS; see [Get notified when Claude needs input](#get-notified-when-claude-needs-input) for Linux and Windows commands.

```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

If your settings file already has a `hooks` key, add `Notification` as a sibling of the existing event keys rather than replacing the whole object. Each event name is a key inside the single `hooks` object:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" }]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'" }]
      }
    ]
  }
}
```

You can also ask Claude to write the hook for you by describing what you want in the CLI.

2

Verify the configuration

Type `/hooks` to open the hooks browser. You’ll see a list of all available hook events, with a count next to each event that has hooks configured. Select `Notification` to confirm your new hook appears in the list. Selecting the hook shows its details: the event, matcher, type, source file, and command.

3

Test the hook

Press `Esc` to return to the CLI. Ask Claude to do something that requires permission, then switch away from the terminal. You should receive a desktop notification.

The `/hooks` menu is read-only. To add, modify, or remove hooks, edit your settings JSON directly or ask Claude to make the change.

## [​](#what-you-can-automate) What you can automate

Hooks let you run code at key points in Claude Code’s lifecycle: format files after edits, block commands before they execute, send notifications when Claude needs input, inject context at session start, and more. For the full list of hook events, see the [Hooks reference](/docs/en/hooks#hook-lifecycle).
Each example includes a ready-to-use configuration block that you add to a [settings file](#configure-hook-location). The most common patterns:

* [Get notified when Claude needs input](#get-notified-when-claude-needs-input)
* [Auto-format code after edits](#auto-format-code-after-edits)
* [Block edits to protected files](#block-edits-to-protected-files)
* [Re-inject context after compaction](#re-inject-context-after-compaction)
* [Audit configuration changes](#audit-configuration-changes)
* [Reload environment when directory or files change](#reload-environment-when-directory-or-files-change)
* [Auto-approve specific permission prompts](#auto-approve-specific-permission-prompts)

For a production example of hooks that run a separate model review and feed findings back into the session, see [how the `security-guidance` plugin integrates with Claude Code](/docs/en/security-guidance#how-the-plugin-integrates-with-claude-code).

### [​](#get-notified-when-claude-needs-input) Get notified when Claude needs input

Get a desktop notification whenever Claude finishes working and needs your input, so you can switch to other tasks without checking the terminal.
This hook uses the `Notification` event, which fires when Claude is waiting for input or permission. Each tab below uses the platform’s native notification command. Add this to `~/.claude/settings.json`:

* macOS
* Linux
* Windows (PowerShell)

```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

If no notification appears

`osascript` routes notifications through the built-in Script Editor app. If Script Editor doesn’t have notification permission, the command fails silently, and macOS won’t prompt you to grant it. Run this in Terminal once to make Script Editor appear in your notification settings:

```
osascript -e 'display notification "test"'
```

Nothing will appear yet. Open **System Settings > Notifications**, find **Script Editor** in the list, and turn on **Allow Notifications**. Run the command again to confirm the test notification appears.

```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

The empty `matcher` fires on all notification types. To fire only on specific events, set it to one of these values:

| Matcher | Fires when |
| --- | --- |
| `permission_prompt` | Claude needs you to approve a tool use |
| `idle_prompt` | Claude is done and waiting for your next prompt |
| `auth_success` | Authentication completes |
| `elicitation_dialog` | An MCP server opens an elicitation form |
| `elicitation_complete` | An MCP elicitation form is submitted or dismissed |
| `elicitation_response` | An MCP elicitation response is sent back to the server |

Type `/hooks` and select `Notification` to confirm the hook is registered. For the full event schema, see the [Notification reference](/docs/en/hooks#notification).

### [​](#auto-format-code-after-edits) Auto-format code after edits

Automatically run [Prettier](https://prettier.io/) on every file Claude edits, so formatting stays consistent without manual intervention.
This hook uses the `PostToolUse` event with an `Edit|Write` matcher, so it runs only after file-editing tools. On Claude Code v2.1.191 or later you can also write the matcher as `Edit,Write`, since `|` and `,` are interchangeable list separators for tool-name matchers on those versions. The command extracts the edited file path with [`jq`](https://jqlang.github.io/jq/) and passes it to Prettier. Add this to `.claude/settings.json` in your project root:

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

The Bash examples on this page use `jq` for JSON parsing. Install it with `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), or see [`jq` downloads](https://jqlang.github.io/jq/download/).

### [​](#block-edits-to-protected-files) Block edits to protected files

Prevent Claude from modifying sensitive files like `.env`, `package-lock.json`, or anything in `.git/`. Claude receives feedback explaining why the edit was blocked, so it can adjust its approach.
This example uses a separate script file that the hook calls. The script checks the target file path against a list of protected patterns and exits with code 2 to block the edit.

1

Create the hook script

Save this to `.claude/hooks/protect-files.sh`:

```
#!/bin/bash