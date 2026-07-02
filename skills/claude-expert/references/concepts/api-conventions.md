---
title: API Conventions
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly:

.claude/skills/fix-issue/SKILL.md

```
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Run `/fix-issue 1234` to invoke it. Use `disable-model-invocation: true` for workflows with side effects that you want to trigger manually.

### [​](#create-custom-subagents) Create custom subagents

Define specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks.

[Subagents](/docs/en/sub-agents) run in their own context with their own set of allowed tools. They’re useful for tasks that read many files or need specialized focus without cluttering your main conversation.

.claude/agents/security-reviewer.md

```
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Tell Claude to use subagents explicitly: *“Use a subagent to review this code for security issues.”*

### [​](#install-plugins) Install plugins

Run `/plugin` to browse the marketplace. Plugins add skills, tools, and integrations without configuration.

[Plugins](/docs/en/plugins) bundle skills, hooks, subagents, and MCP servers into a single installable unit from the community and Anthropic. If you work with a typed language, install a [code intelligence plugin](/docs/en/discover-plugins#code-intelligence) to give Claude precise symbol navigation and automatic error detection after edits.
For guidance on choosing between skills, subagents, hooks, and MCP, see [Extend Claude Code](/docs/en/features-overview#match-features-to-your-goal).


---

## [​](#communicate-effectively) Communicate effectively

The way you communicate with Claude Code significantly impacts the quality of results.

### [​](#ask-codebase-questions) Ask codebase questions

Ask Claude questions you’d ask a senior engineer.

When onboarding to a new codebase, use Claude Code for learning and exploration. You can ask Claude the same sorts of questions you would ask another engineer:

* How does logging work?
* How do I make a new API endpoint?
* What does `async move { ... }` do on line 134 of `foo.rs`?
* What edge cases does `CustomerOnboardingFlowImpl` handle?
* Why does this code call `foo()` instead of `bar()` on line 333?

Using Claude Code this way is an effective onboarding workflow, improving ramp-up time and reducing load on other engineers. No special prompting required: ask questions directly.

### [​](#let-claude-interview-you) Let Claude interview you

For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool.

Claude asks about things you might not have considered yet, including technical implementation, UI/UX, edge cases, and tradeoffs.

```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a fresh session to execute it. The new session has clean context focused entirely on implementation, and you have a written spec to reference.
The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works. Time spent making the spec precise pays off more than time spent watching the implementation.


---

## [​](#manage-your-session) Manage your session

Conversations are persistent and reversible. Use this to your advantage!

### [​](#course-correct-early-and-often) Course-correct early and often

Correct Claude as soon as you notice it going off track.

The best results come from tight feedback loops. Though Claude occasionally solves problems perfectly on the first attempt, correcting it quickly generally produces better solutions faster.

* **`Esc`**: stop Claude mid-action with the `Esc` key. Context is preserved, so you can redirect.
* **`Esc + Esc` or `/rewind`**: press `Esc` twice or run `/rewind` to open the rewind menu and restore previous conversation and code state, or summarize from a selected message.
* **`"Undo that"`**: have Claude revert its changes.
* **`/clear`**: reset context between unrelated tasks. Long sessions with irrelevant context can reduce performance.

If you’ve corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

### [​](#manage-context-aggressively) Manage context aggressively

Run `/clear` between unrelated tasks to reset context.

Claude Code automatically compacts conversation history when you approach context limits, which preserves important code and decisions while freeing space.
During long sessions, Claude’s context window can fill with irrelevant conversation, file contents, and commands. This can reduce performance and sometimes distract Claude.

* Use `/clear` frequently between tasks to reset the context window entirely
* When auto compaction triggers, Claude summarizes what matters most, including code patterns, file states, and key decisions
* For more control, run `/compact <instructions>`, like `/compact Focus on the API changes`
* To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here** or **Summarize up to here**. The first condenses messages from that point forward while keeping earlier context intact; the second condenses earlier messages while keeping recent ones in full. See [Restore vs. summarize](/docs/en/checkpointing#restore-vs-summarize).
* Customize compaction behavior in CLAUDE.md with instructions like `"When compacting, always preserve the full list of modified files and any test commands"` to ensure critical context survives summarization
* For quick questions that don’t need to stay in context, use [`/btw`](/docs/en/interactive-mode#side-questions-with-%2Fbtw). The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context.

### [​](#use-subagents-for-investigation) Use subagents for investigation

Delegate research with `"use subagents to investigate X"`. They explore in a separate context, keeping your main conversation clean for implementation.

Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries:

```
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent explores the codebase, reads relevant files, and reports back with findings, all without cluttering your main conversation.
You can also use subagents for verification after Claude implements something:

```
use a subagent to review this code for edge cases
```

### [​](#rewind-with-checkpoints) Rewind with checkpoints

Every prompt you send creates a checkpoint. You can restore conversation, code, or both to any previous checkpoint.

Claude automatically snapshots files before each change so a checkpoint can restore them. Double-tap `Escape` or run `/rewind` to open the rewind menu. You can restore conversation only, restore code only, restore both, or summarize from a selected message. See [Checkpointing](/docs/en/checkpointing) for details.
Instead of carefully planning every move, you can tell Claude to try something risky. If it doesn’t work, rewind and try a different approach. Checkpoints persist across sessions, so you can close your terminal and still rewind later.

Checkpoints only track changes made *by Claude*, not external processes. This isn’t a replacement for git.

### [​](#resume-conversations) Resume conversations

Name sessions with `/rename` and treat them like branches: each workstream gets its own persistent context.

Claude Code saves conversations locally, so when a task spans multiple sittings you don’t have to re-explain the context. Run `claude --continue` to pick up the most recent session, or `claude --resume` to choose from a list. Give sessions descriptive names like `oauth-migration` so you can find them later. See [Manage sessions](/docs/en/sessions) for the full set of resume, branch, and naming controls.


---

## [​](#automate-and-scale) Automate and scale

Once you’re effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns.
Everything so far assumes one human, one Claude, and one conversation. But Claude Code scales horizontally. The techniques in this section show how you can get more done.

### [​](#run-non-interactive-mode) Run non-interactive mode

Use `claude -p "prompt"` in CI, pre-commit hooks, or scripts. Add `--output-format stream-json --verbose` for streaming JSON output.

With `claude -p "your prompt"`, you can run Claude non-interactively, without a session. [Non-interactive mode](/docs/en/headless) is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow. The output formats let you parse results programmatically: plain text, JSON, or streaming JSON.

```