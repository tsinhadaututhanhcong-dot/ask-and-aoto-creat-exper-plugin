---
type: Reference
title: If running tests, filter to show only failures
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# If running tests, filter to show only failures
if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
  filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
else
  echo "{}"
fi
```

### [​](#move-instructions-from-claude-md-to-skills) Move instructions from CLAUDE.md to skills

Your [CLAUDE.md](/docs/en/memory) file is loaded into context at session start. If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you’re doing unrelated work. [Skills](/docs/en/skills) load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under 200 lines by including only essentials.

### [​](#adjust-extended-thinking) Adjust extended thinking

Extended thinking is enabled by default because it significantly improves performance on complex planning and reasoning tasks. Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request depending on the model. For simpler tasks where deep reasoning isn’t needed, you can reduce costs by lowering the [effort level](/docs/en/model-config#adjust-effort-level) with `/effort` or in `/model`, disabling thinking in `/config`, or, on models with a [fixed thinking budget](/docs/en/model-config#adaptive-reasoning-and-fixed-thinking-budgets), lowering the budget with `MAX_THINKING_TOKENS=8000`. Adaptive-reasoning models ignore nonzero budgets, so use effort levels there instead. Disabling thinking is not available on Fable 5, which always uses extended thinking.

### [​](#delegate-verbose-operations-to-subagents) Delegate verbose operations to subagents

Running tests, fetching documentation, or processing log files can consume significant context. Delegate these to [subagents](/docs/en/sub-agents#isolate-high-volume-operations) so the verbose output stays in the subagent’s context while only a summary returns to your main conversation.

### [​](#manage-agent-team-costs) Manage agent team costs

Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance. Keep team tasks small and self-contained to limit per-teammate token usage. See [agent teams](/docs/en/agent-teams) for details.

### [​](#write-specific-prompts) Write specific prompts

Vague requests like “improve this codebase” trigger broad scanning. Specific requests like “add input validation to the login function in auth.ts” let Claude work efficiently with minimal file reads.

### [​](#work-efficiently-on-complex-tasks) Work efficiently on complex tasks

For longer or more complex work, these habits help avoid wasted tokens from going down the wrong path:

* **Use plan mode for complex tasks**: Press Shift+Tab to enter [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) before implementation. Claude explores the codebase and proposes an approach for your approval, preventing expensive re-work when the initial direction is wrong.
* **Course-correct early**: If Claude starts heading the wrong direction, press Escape to stop immediately. Use `/rewind` or double-tap Escape to restore conversation and code to a previous checkpoint.
* **Give verification targets**: Include test cases, paste screenshots, or define expected output in your prompt. When Claude can verify its own work, it catches issues before you need to request fixes.
* **Test incrementally**: Write one file, test it, then continue. This catches issues early when they’re cheap to fix.

## [​](#background-token-usage) Background token usage

Claude Code uses tokens for some background functionality even when idle:

* **Conversation summarization**: Background jobs that summarize previous conversations for the `claude --resume` feature
* **Command processing**: Some commands like `/usage` may generate requests to check status

These background processes consume a small amount of tokens (typically under $0.04 per session) even without active interaction.

## [​](#understanding-changes-in-claude-code-behavior) Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting. Run `claude --version` to check your current version. For specific billing questions, contact Anthropic support through your [Console account](https://platform.claude.com/login).

Was this page helpful?

YesNo

[Monitoring](/docs/en/monitoring-usage)[Track team usage with analytics](/docs/en/analytics)

⌘I

---