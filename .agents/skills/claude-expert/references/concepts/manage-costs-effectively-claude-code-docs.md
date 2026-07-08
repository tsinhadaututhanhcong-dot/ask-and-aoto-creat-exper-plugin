---
type: Reference
title: Manage costs effectively - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Manage costs effectively - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs)

Claude Code charges by API token consumption. For subscription plan pricing (Pro, Max, Team, Enterprise), see [claude.com/pricing](https://claude.com/pricing). Per-developer costs vary widely based on model selection, codebase size, and usage patterns such as running multiple instances or automation.
Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users. To estimate spend for your own team, start with a small pilot group and use the tracking tools below to establish a baseline before wider rollout.
This page covers how to [track your costs](#track-your-costs), [manage costs for teams](#managing-costs-for-teams), and [reduce token usage](#reduce-token-usage).

## [​](#track-your-costs) Track your costs

### [​](#using-the-/usage-command) Using the `/usage` command

The Session block in `/usage` shows API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure isn’t relevant for billing purposes. Subscribers see plan usage bars, activity stats, and a usage breakdown on the same screen.

The Session block at the top of `/usage` shows detailed token usage statistics for your current session. The dollar figure is an estimate computed locally from token counts and may differ from your actual bill. For authoritative billing, see the Usage page in the [Claude Console](https://platform.claude.com/usage).

```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

On a Pro, Max, Team, or Enterprise plan, `/usage` also shows a breakdown of what counts against your plan limits. It attributes recent usage to skills, subagents, plugins, and individual MCP servers, with each shown as a percentage of the total. Press `d` or `w` to switch between the last 24 hours and the last 7 days. The figures are approximate and computed from local session history on this machine, so usage from other devices or claude.ai is not included.
In the [VS Code extension](/docs/en/vs-code#check-account-and-usage), the same breakdown appears in the Account & usage dialog with a Day and Week toggle. Requires Claude Code v2.1.174 or later.

## [​](#managing-costs-for-teams) Managing costs for teams

When using Claude API, you can [set workspace spend limits](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits) on the total Claude Code workspace spend. Admins can [view cost and usage reporting](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking) in the Console.
On Pro and Max plans, you can set a monthly spend limit on usage credits with the `/usage-credits` command. If you reach that limit while you still have usage credits available, Claude Code prompts you to raise or remove the limit so you can continue without leaving the CLI. Changing the limit requires billing access on the account.

When you first authenticate Claude Code with your Claude Console account, a workspace called “Claude Code” is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace; it is exclusively for Claude Code authentication and usage.For organizations with custom rate limits, Claude Code traffic in this workspace counts toward your organization’s overall API rate limits. You can set a [workspace rate limit](https://platform.claude.com/docs/en/api/rate-limits#setting-lower-limits-for-workspaces) on this workspace’s Limits page in the Claude Console to cap Claude Code’s share and protect other production workloads.

On Bedrock, Vertex, and Foundry, Claude Code does not send metrics from your cloud. Organizations that already route Claude Code through an [LLM gateway](/docs/en/llm-gateway) can track spend there, since the gateway sees every request.

### [​](#rate-limit-recommendations) Rate limit recommendations

When setting up Claude Code for teams, consider these Token Per Minute (TPM) and Request Per Minute (RPM) per-user recommendations based on your organization size:

| Team size | TPM per user | RPM per user |
| --- | --- | --- |
| 1-5 users | 200k-300k | 5-7 |
| 5-20 users | 100k-150k | 2.5-3.5 |
| 20-50 users | 50k-75k | 1.25-1.75 |
| 50-100 users | 25k-35k | 0.62-0.87 |
| 100-500 users | 15k-20k | 0.37-0.47 |
| 500+ users | 10k-15k | 0.25-0.35 |

For example, if you have 200 users, you might request 20k TPM for each user, or 4 million total TPM (200\*20,000 = 4 million).
The TPM per user decreases as team size grows because fewer users tend to use Claude Code concurrently in larger organizations. These rate limits apply at the organization level, not per individual user, which means individual users can temporarily consume more than their calculated share when others aren’t actively using the service.

If you anticipate scenarios with unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.

### [​](#agent-team-token-costs) Agent team token costs

[Agent teams](/docs/en/agent-teams) spawn multiple Claude Code instances, each with its own context window. Token usage scales with the number of active teammates and how long each one runs.
To keep agent team costs manageable:

* Use Sonnet for teammates. It balances capability and cost for coordination tasks.
* Keep teams small. Each teammate runs its own context window, so token usage is roughly proportional to team size.
* Keep spawn prompts focused. Teammates load CLAUDE.md, MCP servers, and skills automatically, but everything in the spawn prompt adds to their context from the start.
* Shut down teammates when their work is done. Each active teammate continues consuming tokens until it exits or the session ends.
* Agent teams are disabled by default. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your [settings.json](/docs/en/settings) or environment to enable them. See [enable agent teams](/docs/en/agent-teams#enable-agent-teams).

## [​](#reduce-token-usage) Reduce token usage

Token costs scale with context size: the more context Claude processes, the more tokens you use. Claude Code automatically optimizes costs through [prompt caching](/docs/en/prompt-caching), which reduces costs for repeated content like system prompts, and auto-compaction, which summarizes conversation history when approaching context limits.
The following strategies help you keep context small and reduce per-message costs.

### [​](#manage-context-proactively) Manage context proactively

Use `/usage` to check your current token usage, or [configure your status line](/docs/en/statusline#context-window-usage) to display it continuously.

* **Clear between tasks**: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message. Use `/rename` before clearing so you can easily find the session later, then `/resume` to return to it.
* **Add custom compaction instructions**: `/compact Focus on code samples and API usage` tells Claude what to preserve during summarization.

You can also customize compaction behavior in your CLAUDE.md:

```