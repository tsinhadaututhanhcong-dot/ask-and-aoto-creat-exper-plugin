---
title: Streaming for real-time processing
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json --verbose
```

### [​](#run-multiple-claude-sessions) Run multiple Claude sessions

Run multiple Claude sessions in parallel to speed up development, run isolated experiments, or start complex workflows.

Pick the parallel approach that fits how much coordination you want to do yourself:

* [Worktrees](/docs/en/worktrees): run separate CLI sessions in isolated git checkouts so edits don’t collide
* [Desktop app](/docs/en/desktop#work-in-parallel-with-sessions): manage multiple local sessions visually, each in its own worktree
* [Claude Code on the web](/docs/en/claude-code-on-the-web): run sessions on Anthropic-managed cloud infrastructure in isolated VMs
* [Agent teams](/docs/en/agent-teams): automated coordination of multiple sessions with shared tasks, messaging, and a team lead

Beyond parallelizing work, multiple sessions enable quality-focused workflows. A fresh context improves code review since Claude won’t be biased toward code it just wrote.
For example, use a Writer/Reviewer pattern:

| Session A (Writer) | Session B (Reviewer) |
| --- | --- |
| `Implement a rate limiter for our API endpoints` |  |
|  | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |  |

You can do something similar with tests: have one Claude write tests, then another write code to pass them.

### [​](#fan-out-across-files) Fan out across files

Loop through tasks calling `claude -p` for each. Use `--allowedTools` to scope permissions for batch operations.

For large migrations or analyses, you can distribute work across many parallel Claude invocations:

1

Generate a task list

Have Claude list all files that need migrating (e.g., `list all 2,000 Python files that need migrating`)

2

Write a script to loop through the list

```
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

3

Test on a few files, then run at scale

Refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set. The `--allowedTools` flag restricts what Claude can do, which matters when you’re running unattended.

You can also integrate Claude into existing data/processing pipelines:

```
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` for debugging during development, and turn it off in production.

### [​](#run-autonomously-with-auto-mode) Run autonomously with auto mode

For uninterrupted execution with background safety checks, use [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode). A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts.

```
claude --permission-mode auto -p "fix all lint errors"
```

For non-interactive runs with the `-p` flag, auto mode aborts if the classifier repeatedly blocks actions, since there is no user to fall back to. See [when auto mode falls back](/docs/en/permission-modes#when-auto-mode-falls-back) for thresholds.

### [​](#add-an-adversarial-review-step) Add an adversarial review step

Before treating a task as done, have a subagent review the diff in a fresh context and report gaps.

The longer Claude works unattended, the more an independent check matters before you count the work as done. A reviewer running in a fresh [subagent](/docs/en/sub-agents) context sees only the diff and the criteria you give it, not the reasoning that produced the change, so it evaluates the result on its own terms.
For a correctness check, run the bundled [`/code-review` skill](/docs/en/commands), which reviews the current diff for bugs in a fresh subagent and returns findings to the session. To check the diff against your plan instead, write the review prompt yourself. Name the work to check, the plan to check it against, and what counts as a finding:

```
Use a subagent to review the rate limiter diff against PLAN.md. Check that
every requirement is implemented, the listed edge cases have tests, and
nothing outside the task's scope changed. Report gaps, not style preferences.
```

Because the reviewer runs as a subagent, the implementing session receives the gaps directly and can fix them and re-review without you copying findings between windows. For longer autonomous runs, an [agent team](/docs/en/agent-teams) can keep this loop going across many tasks while you spot-check the recorded findings.

A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that can’t happen. Tell the reviewer to flag only gaps that affect correctness or the stated requirements, and treat the rest as optional.

---

## [​](#avoid-common-failure-patterns) Avoid common failure patterns

These are common mistakes. Recognizing them early saves time:

* **The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information.
  > **Fix**: `/clear` between unrelated tasks.
* **Correcting over and over.** Claude does something wrong, you correct it, it’s still wrong, you correct again. Context is polluted with failed approaches.
  > **Fix**: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.
* **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
  > **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.
* **The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn’t handle edge cases.
  > **Fix**: Always provide verification (tests, scripts, screenshots). If you can’t verify it, don’t ship it.
* **The infinite exploration.** You ask Claude to “investigate” something without scoping it. Claude reads hundreds of files, filling the context.
  > **Fix**: Scope investigations narrowly or use subagents so the exploration doesn’t consume your main context.

---

## [​](#develop-your-intuition) Develop your intuition

The patterns in this guide aren’t set in stone. They’re starting points that work well in general, but might not be optimal for every situation.
Sometimes you *should* let context accumulate because you’re deep in one complex problem and the history is valuable. Sometimes you should skip planning and let Claude figure it out because the task is exploratory. Sometimes a vague prompt is exactly right because you want to see how Claude interprets the problem before constraining it.
Pay attention to what works. When Claude produces great output, notice what you did: the prompt structure, the context you provided, the mode you were in. When Claude struggles, ask why. Was the context too noisy? The prompt too vague? The task too big for one pass?
Over time, you’ll develop intuition that no guide can capture. You’ll know when to be specific and when to be open-ended, when to plan and when to explore, when to clear context and when to let it accumulate.

## [​](#related-resources) Related resources

* [How Claude Code works](/docs/en/how-claude-code-works): the agentic loop, tools, and context management
* [Extend Claude Code](/docs/en/features-overview): skills, hooks, MCP, subagents, and plugins
* [Common workflows](/docs/en/common-workflows): step-by-step recipes for debugging, testing, PRs, and more
* [CLAUDE.md](/docs/en/memory): store project conventions and persistent context

Was this page helpful?

YesNo

[Prompt library](/docs/en/prompt-library)[Overview](/docs/en/platforms)

⌘I

---