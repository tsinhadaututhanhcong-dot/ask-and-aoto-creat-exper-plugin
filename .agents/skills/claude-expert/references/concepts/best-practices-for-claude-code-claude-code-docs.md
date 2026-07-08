---
type: Reference
title: Best practices for Claude Code - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Best practices for Claude Code - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

Claude Code is an agentic coding environment. Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely.
This changes how you work. Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements.
But this autonomy still comes with a learning curve. Claude works within certain constraints you need to understand.
This guide covers patterns that have proven effective across Anthropic’s internal teams and for engineers using Claude Code across various codebases, languages, and environments. For how the agentic loop works under the hood, see [How Claude Code works](/docs/en/how-claude-code-works).


---

Most best practices are based on one constraint: Claude’s context window fills up fast, and performance degrades as it fills.
Claude’s context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.
This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start “forgetting” earlier instructions or making more mistakes. The context window is the most important resource to manage. To see how a session fills up in practice, [watch an interactive walkthrough](/docs/en/context-window) of what loads at startup and what each file read costs. Track context usage continuously with a [custom status line](/docs/en/statusline), and see [Reduce token usage](/docs/en/costs#reduce-token-usage) for strategies on reducing token usage.


---

## [​](#give-claude-a-way-to-verify-its-work) Give Claude a way to verify its work

Give Claude a check it can run: tests, a build, a screenshot to compare. It’s the difference between a session you watch and one you walk away from.

Claude stops when the work looks done. Without a check it can run, “looks done” is the only signal available, and you become the verification loop: every mistake waits for you to notice it. Give Claude something that produces a pass or fail, and the loop closes on its own. Claude does the work, runs the check, reads the result, and iterates until the check passes.
The check is anything that returns a signal Claude can read in the conversation: a test suite, a build exit code, a linter, a script that diffs output against a fixture, or a [browser screenshot](/docs/en/chrome) compared against a design.

| Strategy | Before | After |
| --- | --- | --- |
| **Provide verification criteria** | *”implement a function that validates email addresses"* | *"write a validateEmail function. example test cases: [user@example.com](mailto:user@example.com) is true, invalid is false, [user@.com](mailto:user@.com) is false. run the tests after implementing”* |
| **Verify UI changes visually** | *”make the dashboard look better"* | *"[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them”* |
| **Address root causes, not symptoms** | *”the build is failing"* | *"the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don’t suppress the error”* |

Once the check exists, decide how hard it gates the stop:

* **In one prompt**: ask Claude to run the check and iterate in the same message, as in the table above.
* **Across a session**: set the check as a [`/goal` condition](/docs/en/goal). A separate evaluator re-checks it after every turn and Claude keeps working until it holds.
* **As a deterministic gate**: a [Stop hook](/docs/en/hooks#stop) runs your check as a script and blocks the turn from ending until it passes. Claude Code overrides the hook and ends the turn after 8 consecutive blocks.
* **By a second opinion**: a [verification subagent](/docs/en/sub-agents) or a [dynamic workflow](/docs/en/workflows) that checks its own findings has a fresh model try to refute the result, so the agent doing the work isn’t the one grading it.

Each step trades setup for attention. The prompt version works on any task today. The `/goal` and Stop hook versions are what let an unattended run finish correctly without you.
Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot of the result. Reviewing evidence is faster than re-running the verification yourself, and it works for sessions you weren’t watching.


---

## [​](#explore-first-then-plan-then-code) Explore first, then plan, then code

Separate research and planning from implementation to avoid solving the wrong problem.

Letting Claude jump straight to coding can produce code that solves the wrong problem. Use [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) to separate exploration from execution.
The recommended workflow has four phases:

1

Explore

Enter plan mode. Claude reads files and answers questions without making changes.

claude (plan mode)

```
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```

2

Plan

Ask Claude to create a detailed implementation plan.

claude (plan mode)

```
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```

Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.

3

Implement

Switch out of plan mode and let Claude code, verifying against its plan.

claude (default mode)

```
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```

4

Commit

Ask Claude to commit with a descriptive message and create a PR.

claude (default mode)

```
commit with a descriptive message and open a PR
```

Plan mode is useful, but also adds overhead.For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly.Planning is most useful when you’re uncertain about the approach, when the change modifies multiple files, or when you’re unfamiliar with the code being modified. If you could describe the diff in one sentence, skip the plan.

---

## [​](#provide-specific-context-in-your-prompts) Provide specific context in your prompts

The more precise your instructions, the fewer corrections you’ll need.

Claude can infer intent, but it can’t read your mind. Reference specific files, mention constraints, and point to example patterns.

| Strategy | Before | After |
| --- | --- | --- |
| **Scope the task.** Specify which file, what scenario, and testing preferences. | *”add tests for foo.py"* | *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks.”* |
| **Point to sources.** Direct Claude to the source that can answer a question. | *”why does ExecutionFactory have such a weird api?"* | *"look through ExecutionFactory’s git history and summarize how its api came to be”* |
| **Reference existing patterns.** Point Claude to patterns in your codebase. | *”add a calendar widget"* | *"look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase.”* |
| **Describe the symptom.** Provide the symptom, the likely location, and what “fixed” looks like. | *”fix the login bug"* | *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it”* |

Vague prompts can be useful when you’re exploring and can afford to course-correct. A prompt like `"what would you improve in this file?"` can surface things you wouldn’t have thought to ask about.

### [​](#provide-rich-content) Provide rich content

Use `@` to reference files, paste screenshots/images, or pipe data directly.

You can provide rich data to Claude in several ways:

* **Reference files with `@`** instead of describing where code lives. Claude reads the file before responding.
* **Paste images directly**. Copy/paste or drag and drop images into the prompt.
* **Give URLs** for documentation and API references. Use `/permissions` to allowlist frequently-used domains.
* **Pipe in data** by running `cat error.log | claude` to send file contents directly.
* **Let Claude fetch what it needs**. Tell Claude to pull context itself using Bash commands, MCP tools, or by reading files.

---

## [​](#configure-your-environment) Configure your environment

A few setup steps make Claude Code significantly more effective across all your sessions. For a full overview of extension features and when to use each one, see [Extend Claude Code](/docs/en/features-overview).

### [​](#write-an-effective-claude-md) Write an effective CLAUDE.md

Run `/init` to generate a starter CLAUDE.md file based on your current project structure, then refine over time.

CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can’t infer from code alone.
The `/init` command analyzes your codebase to detect build systems, test frameworks, and code patterns, giving you a solid foundation to refine.
There’s no required format for CLAUDE.md files, but keep it short and human-readable. For example:

CLAUDE.md

```