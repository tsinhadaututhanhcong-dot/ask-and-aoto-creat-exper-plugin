---
title: Bulk operations across files
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

See the [CLI reference](/docs/en/cli-reference) for the full set of commands and flags.

Schedule recurring tasks

Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

* [Routines](/docs/en/routines) run on Anthropic-managed infrastructure, so they keep running even when your computer is off. They can also trigger on API calls or GitHub events. Create them from the web, the Desktop app, or by running `/schedule` in the CLI.
* [Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks) run on your machine, with direct access to your local files and tools
* [`/loop`](/docs/en/scheduled-tasks) repeats a prompt within a CLI session for quick polling

Work from anywhere

Sessions aren’t tied to a single surface. Move work between environments as your context changes:

* Step away from your desk and keep working from your phone or any browser with [Remote Control](/docs/en/remote-control)
* Message [Dispatch](/docs/en/desktop#sessions-from-dispatch) a task from your phone and open the Desktop session it creates
* Kick off a long-running task on the [web](/docs/en/claude-code-on-the-web) or [iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684), then pull it into your terminal with `claude --teleport`. Teleport requires a claude.ai subscription.
* Hand off a terminal session to the [Desktop app](/docs/en/desktop) with `/desktop` for visual diff review
* Route tasks from team chat: mention `@Claude` in [Slack](/docs/en/slack) with a bug report and get a pull request back

## [​](#use-claude-code-everywhere) Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.
Beyond the [Terminal](/docs/en/quickstart), [VS Code](/docs/en/vs-code), [JetBrains](/docs/en/jetbrains), [Desktop](/docs/en/desktop), and [Web](/docs/en/claude-code-on-the-web) environments above, Claude Code integrates with CI/CD, chat, and browser workflows:

| I want to… | Best option |
| --- | --- |
| Continue a local session from my phone or another device | [Remote Control](/docs/en/remote-control) |
| Push events from Telegram, Discord, iMessage, or my own webhooks into a session | [Channels](/docs/en/channels) |
| Start a task locally, continue on mobile | [Web](/docs/en/claude-code-on-the-web) or [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Run Claude on a recurring schedule | [Routines](/docs/en/routines) or [Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks) |
| Automate PR reviews and issue triage | [GitHub Actions](/docs/en/github-actions) or [GitLab CI/CD](/docs/en/gitlab-ci-cd) |
| Get automatic code review on every PR | [GitHub Code Review](/docs/en/code-review) |
| Route bug reports from Slack to pull requests | [Slack](/docs/en/slack) |
| Debug live web applications | [Chrome](/docs/en/chrome) |
| Build custom agents for your own workflows | [Agent SDK](/docs/en/agent-sdk/overview) |

## [​](#next-steps) Next steps

Once you’ve installed Claude Code, these guides help you go deeper.

* [Quickstart](/docs/en/quickstart): walk through your first real task, from exploring a codebase to committing a fix
* [Store instructions and memories](/docs/en/memory): give Claude persistent instructions with CLAUDE.md files and auto memory
* [Common workflows](/docs/en/common-workflows) and [best practices](/docs/en/best-practices): patterns for getting the most out of Claude Code
* [Settings](/docs/en/settings): customize Claude Code for your workflow
* [Troubleshooting](/docs/en/troubleshooting): solutions for common issues
* [code.claude.com](https://code.claude.com/): demos, pricing, and product details

Was this page helpful?

YesNo

[Quickstart](/docs/en/quickstart)

⌘I

---