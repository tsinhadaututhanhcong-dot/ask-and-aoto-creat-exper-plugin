---
title: Continue the most recent conversation
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

If you’re running multiple conversations, capture the session ID to resume a specific one:

```
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

Run both commands from the same directory: session ID lookup is scoped to the current project directory and its git worktrees. See [Resume a session](/docs/en/sessions#resume-a-session) for the full scope rules.

## [​](#next-steps) Next steps

* [Agent SDK quickstart](/docs/en/agent-sdk/quickstart): build your first agent with Python or TypeScript
* [CLI reference](/docs/en/cli-reference): all CLI flags and options
* [GitHub Actions](/docs/en/github-actions): use the Agent SDK in GitHub workflows
* [GitLab CI/CD](/docs/en/gitlab-ci-cd): use the Agent SDK in GitLab pipelines

Was this page helpful?

YesNo

[Goals](/docs/en/goal)[Launch sessions from links](/docs/en/deep-links)

⌘I

---