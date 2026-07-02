---
title: Catch security issues as Claude writes code - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Catch security issues as Claude writes code - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/security-guidance](https://code.claude.com/docs/en/security-guidance)

The security guidance plugin makes Claude review its own code changes for common vulnerabilities while it works and fix what it finds in the same session. The plugin catches issues such as injection, unsafe deserialization, and unsafe DOM APIs before the code reaches a pull request, reducing how much security review falls to human reviewers downstream.
Once installed, the plugin runs automatically. There is nothing to invoke and no separate command to remember.
The plugin is the in-session companion to [Code Review](/docs/en/code-review), which runs on pull requests. This plugin reduces what reaches the PR. Code Review catches what does. For how the plugin layers with on-demand review and CI scanning, see [How this fits with other security tools](#how-this-fits-with-other-security-tools).

## [​](#prerequisites) Prerequisites

* Claude Code CLI version 2.1.144 or later
* Python 3.8 or later on your `PATH`. The plugin tries `python3`, `python`, and `py -3` in that order
* A git repository for the directory you work in. The end-of-turn and commit reviews diff against git state and skip silently outside a repository. The per-edit pattern check works anywhere

On first run the plugin creates a virtual environment under `~/.claude/security/` and installs the Claude Agent SDK into it, which requires `pip` and network access. If that install fails, the commit review falls back to a single-shot review instead of the agentic one. On Windows the virtual environment step is skipped, so the agentic commit review runs only if `claude-agent-sdk` is already importable and otherwise falls back the same way.

## [​](#install-the-plugin) Install the plugin

In a Claude Code session, install from the [official Anthropic marketplace](/docs/en/discover-plugins#official-anthropic-marketplace):

```
/plugin install security-guidance@claude-plugins-official
```

The install prompts for a scope. Choose user scope to write the plugin to your user settings, so it loads in every new local session you start on this machine. If Claude Code reports that the marketplace is not found, run `/plugin marketplace add anthropics/claude-plugins-official` first, then retry the install.
Then activate it in the current session with `/reload-plugins`, which applies pending plugin changes without a restart:

```
/reload-plugins
```

### [​](#enable-in-cloud-sessions-and-shared-repositories) Enable in cloud sessions and shared repositories

User-scoped plugins do not carry into [Claude Code on the web](/docs/en/claude-code-on-the-web), because those sessions run on Anthropic infrastructure rather than your machine. To enable the plugin there, or to turn it on for everyone who clones a repository, declare it in the project’s checked-in settings:

.claude/settings.json

```
{
  "enabledPlugins": {
    "security-guidance@claude-plugins-official": true
  }
}
```

Administrators can enable the plugin organization-wide by setting [`enabledPlugins`](/docs/en/settings#plugin-settings) in [managed settings](/docs/en/admin-setup).

## [​](#what-the-plugin-checks) What the plugin checks

The plugin reviews Claude’s work at three points, each at a different depth:

* [On each file edit](#on-each-file-edit): a fast pattern match for risky calls, with no model call
* [At the end of each turn](#at-the-end-of-each-turn): a background model review of everything that turn changed
* [On each commit or push Claude makes](#on-each-commit-or-push-claude-makes): a deeper agentic review that reads surrounding code

You can extend each layer by [adding your own rules](#add-your-own-rules). Built-in checks cannot be removed individually, but you can [disable each layer](#disable-or-uninstall) independently.

### [​](#on-each-file-edit) On each file edit

When Claude writes to a file, the plugin scans the new content for known risky patterns. This is a pattern match with no model call, so it adds no usage cost.
Example pattern categories:

* Dynamic code execution: `eval(`, `new Function`, `os.system`, `child_process.exec`
* Unsafe deserialization: `pickle`
* DOM injection: `dangerouslySetInnerHTML`, `.innerHTML =`, `document.write`
* Workflow files: edits under `.github/workflows/`, which can grant repository-level permissions

The check runs after the edit lands and appends the warning to Claude’s context for the next step. Each warning fires once per pattern per file per session, so repeat matches in the same file do not flood the conversation.
You can [add your own patterns](#add-custom-per-edit-patterns) to this layer with a `security-patterns.yaml` file.

### [​](#at-the-end-of-each-turn) At the end of each turn

A turn is one round of Claude responding: you send a message, Claude works and replies, and the turn ends. After each turn, the plugin computes a git diff of everything that changed in the working tree during the turn, including changes from Claude’s edit tools, Bash commands, and subagents, and sends it to a separate Claude review focused on security. The review runs in the background, so Claude’s reply is not delayed. If the review finds issues, Claude is re-prompted with the findings and addresses them as a follow-up.
This catches issues a string match cannot, such as:

* Authorization bypass
* Insecure direct object references
* Injection
* Server-side request forgery
* Weak cryptography

You see both the finding and Claude’s resolution directly in your session. The review covers up to 30 changed files per turn and fires at most three times in a row before yielding back to you.

### [​](#on-each-commit-or-push-claude-makes) On each commit or push Claude makes

When Claude runs `git commit` or `git push` through its Bash tool, the plugin runs a deeper agentic review of the change in the background. This review reads surrounding code, including callers, sanitizers, and related files, to decide whether a finding is real before reporting it. The extra context keeps false positives low on patterns that look dangerous in isolation but are safe in your codebase.
This layer fires only on commits and pushes Claude makes through its Bash tool. Commits you run from your own shell, including the `!` shell escape inside a session, are not reviewed. Commit and push reviews are capped at 20 per rolling hour. If the commit review’s findings duplicate what the end-of-turn review already reported, Claude is not re-prompted, so a clean commit produces no visible output from this layer.

### [​](#review-independence-and-limits) Review independence and limits

The plugin does not ask the same Claude instance that wrote the code to grade itself. The per-edit check is a deterministic string match with no model involved. The end-of-turn and commit reviews run as a separate Claude call with a fresh context and a security-focused prompt: the reviewer starts from the diff, has no investment in the original approach, and is instructed only to find problems.
None of the layers block writes or commits. Findings reach the writing Claude as instructions, Claude addresses them in the conversation, and the review model can miss issues. Treat the plugin as one layer of defense in depth, not a complete security solution. See [How this fits with other security tools](#how-this-fits-with-other-security-tools).

## [​](#add-your-own-rules) Add your own rules

The plugin has two extension points: a Markdown guidance file for the model-backed reviews, and a YAML or JSON patterns file for the per-edit string match. Both are additive. You can add checks but cannot disable built-in ones from these files.

### [​](#add-guidance-for-the-model-backed-reviews) Add guidance for the model-backed reviews

Create `.claude/claude-security-guidance.md` in your project and describe your threat model and review checklist in plain language. The model-backed reviews load it as additional context alongside the built-in vulnerability checklist.
The following example is for a web service with role-gated admin routes and a customer-data logging policy:

.claude/claude-security-guidance.md

```