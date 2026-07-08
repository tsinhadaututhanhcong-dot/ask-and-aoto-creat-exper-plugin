---
type: Reference
title: Block SQL write operations (case-insensitive)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

See [Hook input](/docs/en/hooks#pretooluse-input) for the complete input schema and [exit codes](/docs/en/hooks#exit-code-output) for how exit codes affect behavior. On Windows, write hook scripts in PowerShell and add `shell: powershell` to the hook entry as shown in [running hooks in PowerShell](/docs/en/hooks#windows-powershell-tool).

#### [​](#disable-specific-subagents) Disable specific subagents

You can prevent Claude from using specific subagents by adding them to the `deny` array in your [settings](/docs/en/settings#permission-settings). Use the format `Agent(subagent-name)` where `subagent-name` matches the subagent’s name field.

```
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

This works for both built-in and custom subagents. You can also use the `--disallowedTools` CLI flag:

```
claude --disallowedTools "Agent(Explore)"
```

See [Permissions documentation](/docs/en/permissions#tool-specific-permission-rules) for more details on permission rules.

### [​](#define-hooks-for-subagents) Define hooks for subagents

Subagents can define [hooks](/docs/en/hooks) that run during the subagent’s lifecycle. There are two ways to configure hooks:

* **In the subagent’s frontmatter**: define hooks that run only while that subagent is active
* **In `settings.json`**: define hooks that run in the main session when subagents start or stop

#### [​](#hooks-in-subagent-frontmatter) Hooks in subagent frontmatter

Define hooks directly in the subagent’s markdown file. These hooks only run while that specific subagent is active and are cleaned up when it finishes.

Frontmatter hooks fire when the agent is spawned as a subagent through the Agent tool or an @-mention, and when the agent runs as the main session via [`--agent`](#invoke-subagents-explicitly) or the `agent` setting. In the main-session case they run alongside any hooks defined in [`settings.json`](/docs/en/hooks).

All [hook events](/docs/en/hooks#hook-events) are supported. The most common events for subagents are:

| Event | Matcher input | When it fires |
| --- | --- | --- |
| `PreToolUse` | Tool name | Before the subagent uses a tool |
| `PostToolUse` | Tool name | After the subagent uses a tool |
| `Stop` | (none) | When the subagent finishes (converted to `SubagentStop` at runtime) |

This example validates Bash commands with the `PreToolUse` hook and runs a linter after file edits with `PostToolUse`:

```
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

When the agent is invoked as a subagent, `Stop` hooks in frontmatter are automatically converted to `SubagentStop` events.

#### [​](#project-level-hooks-for-subagent-events) Project-level hooks for subagent events

Configure hooks in `settings.json` that respond to subagent lifecycle events in the main session.

| Event | Matcher input | When it fires |
| --- | --- | --- |
| `SubagentStart` | Agent type name | When a subagent begins execution |
| `SubagentStop` | Agent type name | When a subagent completes |

Both events support matchers to target specific agent types by name. This example runs a setup script only when the `db-agent` subagent starts, and a cleanup script when any subagent stops:

```
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

See [Hooks](/docs/en/hooks) for the complete hook configuration format.

## [​](#work-with-subagents) Work with subagents

### [​](#understand-automatic-delegation) Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like “use proactively” in your subagent’s description field.

### [​](#invoke-subagents-explicitly) Invoke subagents explicitly

When automatic delegation isn’t enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

* **Natural language**: name the subagent in your prompt; Claude decides whether to delegate
* **@-mention**: guarantees the subagent runs for one task
* **Session-wide**: the whole session uses that subagent’s system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

For natural language, there’s no special syntax. Name the subagent and Claude typically delegates:

```
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention the subagent.** Type `@` and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:

```
@"code-reviewer (agent)" look at the auth changes
```

Your full message still goes to Claude, which writes the subagent’s task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives.
Subagents provided by an enabled [plugin](/docs/en/plugins) appear in the typeahead under their scoped name, such as `my-plugin:code-reviewer` or `my-plugin:review:security` when the plugin [organizes agents into subfolders](#choose-the-subagent-scope). Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name.
You can also type the mention manually without using the picker: `@agent-<name>` for local subagents, or `@agent-` followed by the scoped name for plugin subagents, for example `@agent-my-plugin:code-reviewer`.
**Run the whole session as a subagent.** Pass [`--agent <name>`](/docs/en/cli-reference) to start a session where the main thread itself takes on that subagent’s system prompt, tool restrictions, and model:

```
claude --agent code-reviewer
```

The subagent’s system prompt replaces the default Claude Code system prompt entirely, the same way [`--system-prompt`](/docs/en/cli-reference) does. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header so you can confirm it’s active.
This works with built-in and custom subagents, and the choice persists when you resume the session.
For a plugin-provided subagent, you can pass only the agent name and Claude Code finds it:

```
claude --agent security-reviewer
```

If multiple plugins provide agents with the same name, pass the scoped name to disambiguate:

```
claude --agent my-plugin:security-reviewer
```

If the plugin places the agent in a subfolder of its `agents/` directory, include the subfolder in the scoped name, for example `claude --agent my-plugin:review:security`.
To make it the default for every session in a project, set `agent` in `.claude/settings.json`:

```
{
  "agent": "code-reviewer"
}
```

The CLI flag overrides the setting if both are present.

### [​](#run-subagents-in-foreground-or-background) Run subagents in foreground or background

Subagents can run in the foreground or the background:

* **Foreground subagents** block the main conversation until complete. Permission prompts are passed through to you as they come up.
* **Background subagents** run concurrently while you continue working. As of v2.1.186, when a background subagent reaches a tool call that needs permission, the prompt surfaces in your main session and names the subagent that is asking. Approve to let the subagent continue, or press Esc to deny that one tool call without stopping the subagent. Before v2.1.186, background subagents auto-denied any tool call that would have prompted.

Claude decides whether to run subagents in the foreground or background based on the task. You can also:

* Ask Claude to “run this in the background”
* Press **Ctrl+B** to background a running task

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](/docs/en/env-vars).
When [`CLAUDE_CODE_FORK_SUBAGENT`](#fork-the-current-conversation) is set to `1`, every subagent spawn runs in the background regardless of the `background` field. Permission prompts from these background subagents surface in your main session as described above.

### [​](#common-patterns) Common patterns

#### [​](#isolate-high-volume-operations) Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent’s context while only the relevant summary returns to your main conversation.

```
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### [​](#run-parallel-research) Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:

```
Research the authentication, database, and API modules in parallel using separate subagents
```

Each subagent explores its area independently, then Claude synthesizes the findings. This works best when the research paths don’t depend on each other.

When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context.

For tasks that need sustained parallelism or exceed your context window, [agent teams](/docs/en/agent-teams) give each worker its own independent context.

#### [​](#chain-subagents) Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.

```
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### [​](#choose-between-subagents-and-main-conversation) Choose between subagents and main conversation

Use the **main conversation** when:

* The task needs frequent back-and-forth or iterative refinement
* Multiple phases share significant context, such as planning, implementation, and testing
* You’re making a quick, targeted change
* Latency matters. Subagents start fresh and may need time to gather context

Use **subagents** when:

* The task produces verbose output you don’t need in your main context
* You want to enforce specific tool restrictions or permissions
* The work is self-contained and can return a summary

Consider [Skills](/docs/en/skills) instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context.
For a quick question about something already in your conversation, use [`/btw`](/docs/en/interactive-mode#side-questions-with-%2Fbtw) instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.

### [​](#spawn-nested-subagents) Spawn nested subagents

As of Claude Code v2.1.172, a subagent can spawn its own subagents. Use this when a delegated task itself splits into parallel subtasks, such as a reviewer subagent that dispatches a verifier per finding, so the intermediate output never reaches your main conversation. Only the top-level subagent’s summary returns to you.
A nested subagent is configured the same way as a top-level one and resolves from the same [scopes](#choose-the-subagent-scope). The subagent panel below the prompt input shows the full tree: each row displays a `(+N)` count of descendants, and opening a row shows that subagent’s direct children with a path back to `main`. The Running tab in [`/agents`](#use-the-%2Fagents-command) lists running subagents as a flat list.
Depth is counted as the number of subagent levels below the main conversation, regardless of whether each level runs in the [foreground or background](#run-subagents-in-foreground-or-background). A subagent at depth five doesn’t receive the Agent tool and can’t spawn further. The limit is fixed and not configurable.
As of Claude Code v2.1.187, a background subagent’s depth is fixed when it is first spawned, and [resuming](#resume-subagents) it later doesn’t change that depth. For example, if your main conversation spawns subagent A, and A spawns a background subagent B at depth two, B is still at depth two when you resume it directly from the main conversation. Resuming a subagent from a shallower context doesn’t let it spawn additional levels that the depth limit already prevented.
To prevent a specific subagent from spawning others, omit `Agent` from its [`tools`](#available-tools) list or add it to `disallowedTools`.
A [fork](#fork-the-current-conversation) still can’t spawn another fork. It can spawn other subagent types, and those count toward the depth limit.

### [​](#manage-subagent-context) Manage subagent context

#### [​](#what-loads-at-startup) What loads at startup

Each subagent starts with a fresh, isolated context window. It doesn’t see your conversation history, the skills you’ve already invoked, or the files Claude has already read. Claude composes a delegation message that summarizes the task, and the subagent works from there. The exception is a [fork](#fork-the-current-conversation), which inherits the parent conversation instead of starting fresh.
A non-fork subagent’s initial context contains:

* **System prompt**: the agent’s own prompt plus environment details that Claude Code appends, not the full Claude Code system prompt. Custom subagents define theirs in the [markdown body](#write-subagent-files) or `prompt` field. Built-in agents have predefined prompts.
* **Task message**: the delegation prompt Claude writes when it hands off the work.
* **CLAUDE.md and memory**: every level of the [memory hierarchy](/docs/en/memory#how-claude-md-files-load) the main conversation loads, including `~/.claude/CLAUDE.md`, project rules, `CLAUDE.local.md`, and managed policy files. The built-in Explore and Plan agents skip this.
* **Git status**: a snapshot taken at the start of the parent session. Absent when the working directory isn’t a Git repository or when [`includeGitInstructions`](/docs/en/settings#available-settings) is `false`. Explore and Plan skip it regardless.
* **Preloaded skills**: full content of any skill named in the agent’s [`skills` field](#preload-skills-into-subagents). Built-in agents don’t preload skills.

Explore and Plan are the only subagents that omit CLAUDE.md and git status. There is no frontmatter field or per-agent setting to change which agents skip them.
The main conversation reads Explore and Plan results with full CLAUDE.md context, so most rules don’t need to reach the subagent itself. If a rule must, such as “ignore the `vendor/` directory,” restate it in the prompt you give Claude when delegating.

#### [​](#resume-subagents) Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent’s work instead of starting over, ask Claude to resume it.
Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.
When a subagent completes, Claude receives its agent ID. The built-in Explore and Plan agents are one-shot and return no agent ID, so they can’t be resumed; use `general-purpose` or a custom subagent when you need to continue the work.
Claude uses the `SendMessage` tool with the agent’s ID as the `to` field to resume it. The `SendMessage` tool is always available for resuming subagents by agent ID or name. Structured team-protocol messages such as `shutdown_request` and `plan_approval_response` require [agent teams](/docs/en/agent-teams) to be enabled.
To resume a subagent, ask Claude to continue the previous work:

```
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

If a stopped subagent receives a `SendMessage`, it auto-resumes in the background without requiring a new `Agent` invocation.
You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at `~/.claude/projects/{project}/{sessionId}/subagents/`. Each transcript is stored as `agent-{agentId}.jsonl`.
Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: when the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.
* **Session persistence**: subagent transcripts persist within their session. You can [resume a subagent](#resume-subagents) after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: transcripts are cleaned up based on the `cleanupPeriodDays` setting, which defaults to 30 days.

#### [​](#auto-compaction) Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. Compaction triggers under the same conditions, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` applies to subagents as well. See [environment variables](/docs/en/env-vars) for when the override takes effect.
Compaction events are logged in subagent transcript files:

```
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

The `preTokens` value shows how many tokens were used before compaction occurred.

## [​](#fork-the-current-conversation) Fork the current conversation

Forked subagents require Claude Code v2.1.117 or later. From v2.1.161 the `/fork` command is enabled by default; on earlier versions it requires setting the [`CLAUDE_CODE_FORK_SUBAGENT`](/docs/en/env-vars) environment variable to `1`. Letting Claude itself spawn forks is experimental and may change in future releases. This capability may also be enabled in interactive sessions as part of a staged rollout.

A fork is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation. The fork’s own tool calls still stay out of your conversation and only its final result comes back, so your main context window stays clean. Use a fork when a named subagent would need too much background to be useful, or when you want to try several approaches in parallel from the same starting point.
To control fork mode regardless of the staged rollout, set [`CLAUDE_CODE_FORK_SUBAGENT`](/docs/en/env-vars) to `1` to enable it explicitly or to `0` to disable it. The variable is honored in interactive mode and via the SDK or `claude -p`.
Enabling fork mode changes Claude Code in two ways:

* Claude can spawn a fork by requesting the `fork` subagent type explicitly. Spawns without a subagent type still use the [general-purpose](#built-in-subagents) subagent, and named subagents such as Explore still spawn as before.
* Every subagent spawn runs in the [background](#run-subagents-in-foreground-or-background), whether it is a fork or a named subagent. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to `1` to keep spawns synchronous.

You can start a fork yourself with `/fork` followed by a directive, with or without the variable set. Claude Code names the fork from the first words of the directive. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

```
/fork draft unit tests for the parser changes so far
```

The fork appears in a panel below your prompt and runs in the background while you keep working. When it finishes, its result arrives as a message in your main conversation. The next section covers the panel controls for watching and steering forks while they run.

### [​](#observe-and-steer-running-forks) Observe and steer running forks

Running forks appear in a panel below the prompt input, with one row for the main session and one for each fork. Use these keys to interact with the panel:

| Key | Action |
| --- | --- |
| `↑` / `↓` | Move between rows |
| `Enter` | Open the selected fork’s transcript and send it follow-up messages |
| `x` | Dismiss a finished fork or stop a running one |
| `Esc` | Return focus to the prompt input |

### [​](#how-forks-differ-from-named-subagents) How forks differ from named subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

|  | Fork | Named subagent |
| --- | --- | --- |
| Context | Full conversation history | Fresh context with the prompt you pass |
| System prompt and tools | Same as main session | From the subagent’s [definition file](#write-subagent-files) |
| Model | Same as main session | From the subagent’s `model` field |
| Permissions | Prompts surface in your terminal | [Prompts surface in your main session](#run-subagents-in-foreground-or-background) when running in the background |
| Prompt cache | Shared with main session | Separate cache |

Because a fork’s system prompt and tool definitions are identical to the parent, its first request reuses the parent’s [prompt cache](/docs/en/prompt-caching#subagents-and-the-cache). This makes forking cheaper than spawning a fresh subagent for tasks that need the same context.
When Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` so the fork’s file edits are written to a separate git worktree instead of your checkout.

### [​](#limitations) Limitations

Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, [non-interactive mode](/docs/en/headless), and the Agent SDK; setting it to `0` disables fork mode everywhere, including any server-side rollout. A fork can’t spawn further forks.

## [​](#example-subagents) Example subagents

These examples demonstrate effective patterns for building subagents. Use them as starting points, or generate a customized version with Claude.

**Best practices:**

* **Design focused subagents:** each subagent should excel at one specific task
* **Write detailed descriptions:** Claude uses the description to decide when to delegate
* **Limit tool access:** grant only necessary permissions for security and focus
* **Check into version control:** share project subagents with your team

### [​](#code-reviewer) Code reviewer

A read-only subagent that reviews code without modifying it. This example shows how to design a focused subagent with limited tool access (no Edit or Write) and a detailed prompt that specifies exactly what to look for and how to format output.

```
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### [​](#debugger) Debugger

A subagent that can both analyze and fix issues. Unlike the code reviewer, this one includes Edit because fixing bugs requires modifying code. The prompt provides a clear workflow from diagnosis to verification.

```
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### [​](#data-scientist) Data scientist

A domain-specific subagent for data analysis work. This example shows how to create subagents for specialized workflows outside of typical coding tasks. It explicitly sets `model: sonnet` for more capable analysis.

```
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### [​](#database-query-validator) Database query validator

A subagent that allows Bash access but validates commands to permit only read-only SQL queries. This example shows how to use `PreToolUse` hooks for conditional validation when you need finer control than the `tools` field provides.

```
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [passes hook input as JSON](/docs/en/hooks#pretooluse-input) via stdin to hook commands. The validation script reads this JSON, extracts the command being executed, and checks it against a list of SQL write operations. If a write operation is detected, the script [exits with code 2](/docs/en/hooks#exit-code-2-behavior-per-event) to block execution and returns an error message to Claude via stderr.
Create the validation script anywhere in your project. The path must match the `command` field in your hook configuration:

```
#!/bin/bash