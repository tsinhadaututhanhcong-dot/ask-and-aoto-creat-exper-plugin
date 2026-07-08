---
type: Reference
title: Customize your status line - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Customize your status line - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/statusline](https://code.claude.com/docs/en/statusline)

The status line is a customizable bar at the bottom of Claude Code that runs any shell script you configure. It receives JSON session data on stdin and displays whatever your script prints, giving you a persistent, at-a-glance view of context usage, costs, git status, or anything else you want to track.
Status lines are useful when you:

* Want to monitor context window usage as you work
* Need to track session costs
* Work across multiple sessions and need to distinguish them
* Want git branch and status always visible

The status line renders in its own row above the built-in footer badges and does not replace them. To add clickable link badges to the footer when an ID appears in the conversation, without writing a script, configure [`footerLinksRegexes`](/docs/en/settings#footer-link-badges) instead.
Here’s an example of a [multi-line status line](#display-multiple-lines) that displays git info on the first line and a color-coded context bar on the second.

![A multi-line status line showing model name, directory, git branch on the first line, and a context usage progress bar with cost and duration on the second line](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87)

This page walks through [setting up a basic status line](#set-up-a-status-line), explains [how the data flows](#how-status-lines-work) from Claude Code to your script, lists [all the fields you can display](#available-data), and provides [ready-to-use examples](#examples) for common patterns like git status, cost tracking, and progress bars.

## [​](#set-up-a-status-line) Set up a status line

Use the [`/statusline` command](#use-the-%2Fstatusline-command) to have Claude Code generate a script for you, or [manually create a script](#manually-configure-a-status-line) and add it to your settings.

### [​](#use-the-/statusline-command) Use the /statusline command

The `/statusline` command accepts natural language instructions describing what you want displayed. Claude Code generates a script file in `~/.claude/` and updates your settings automatically:

```
/statusline show model name and context percentage with a progress bar
```

### [​](#manually-configure-a-status-line) Manually configure a status line

Add a `statusLine` field to your user settings (`~/.claude/settings.json`, where `~` is your home directory) or [project settings](/docs/en/settings#settings-files). Set `type` to `"command"` and point `command` to a script path or an inline shell command. For a full walkthrough of creating a script, see [Build a status line step by step](#build-a-status-line-step-by-step).

```
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

The `command` field runs in a shell, so you can also use inline commands instead of a script file. This example uses `jq` to parse the JSON input and display the model name and context percentage:

```
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

The optional `padding` field adds extra horizontal spacing (in characters) to the status line content. Defaults to `0`. This padding is in addition to the interface’s built-in spacing, so it controls relative indentation rather than absolute distance from the terminal edge.
The optional `refreshInterval` field re-runs your command every N seconds in addition to the [event-driven updates](#how-status-lines-work). The minimum is `1`. Set this when your status line shows time-based data such as a clock, or when background subagents change git state while the main session is idle. Leave it unset to run only on events.
The optional `hideVimModeIndicator` field suppresses the built-in `-- INSERT --` text below the prompt. Set this to `true` when your script renders [`vim.mode`](#available-data) itself, so the mode is not shown twice.

### [​](#disable-the-status-line) Disable the status line

Run `/statusline` and ask it to remove or clear your status line (e.g., `/statusline delete`, `/statusline clear`, `/statusline remove it`). You can also manually delete the `statusLine` field from your settings.json.

## [​](#build-a-status-line-step-by-step) Build a status line step by step

This walkthrough shows what’s happening under the hood by manually creating a status line that displays the current model, working directory, and context window usage percentage.

Running [`/statusline`](#use-the-%2Fstatusline-command) with a description of what you want configures all of this for you automatically.

These examples use Bash scripts, which work on macOS and Linux. On Windows, see [Windows configuration](#windows-configuration) for PowerShell and Git Bash examples.

![A status line showing model name, directory, and context percentage](https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=696445e59ca0059213250651ad23db6b)

1

Create a script that reads JSON and prints output

Claude Code sends JSON data to your script via stdin. This script uses [`jq`](https://jqlang.github.io/jq/), a command-line JSON parser you may need to install, to extract the model name, directory, and context percentage, then prints a formatted line.Save this to `~/.claude/statusline.sh` (where `~` is your home directory, such as `/Users/username` on macOS or `/home/username` on Linux):

```
#!/bin/bash