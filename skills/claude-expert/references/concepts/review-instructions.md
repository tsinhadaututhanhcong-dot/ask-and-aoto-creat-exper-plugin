---
title: Review instructions
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: integration
---

# Review instructions

## What Important means here

Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, and migrations that aren't backward
compatible. Style, naming, and refactoring suggestions are Nit at
most.

## Cap the nits

Report at most five Nits per review. If you found more, say "plus N
similar items" in the summary instead of posting them inline. If
everything you found is a Nit, lead the summary with "No blocking
issues."

## Do not report

- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file
- Test-only code that intentionally violates production rules

## Always check

- New API routes have an integration test
- Log lines don't include email addresses, user IDs, or request bodies
- Database queries are scoped to the caller's tenant
```

#### [​](#keep-it-focused) Keep it focused

Length has a cost: a long `REVIEW.md` dilutes the rules that matter most. Keep it to instructions that change review behavior, and leave general project context in `CLAUDE.md`.

## [​](#view-usage) View usage

Go to [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) to see Code Review activity across your organization. The dashboard shows:

| Section | What it shows |
| --- | --- |
| PRs reviewed | Daily count of pull requests reviewed over the selected time range |
| Cost weekly | Weekly spend on Code Review |
| Feedback | Count of review comments that were auto-resolved because a developer addressed the issue |
| Repository breakdown | Per-repo counts of PRs reviewed and comments resolved |

The repositories table in admin settings also shows average cost per review for each repo. Dashboard cost figures are estimates for monitoring activity; for invoice-accurate spend, refer to your Anthropic bill.

## [​](#pricing) Pricing

Code Review is billed based on token usage. Each review averages $15-25 in cost, scaling with PR size, codebase complexity, and how many issues require verification. Code Review usage is billed separately through [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) and does not count against your plan’s included usage.
The review trigger you choose affects total cost:

* **Once after PR creation**: runs once per PR
* **After every push**: runs on each push, multiplying cost by the number of pushes
* **Manual**: no reviews until someone comments `@claude review` on a PR

In any mode, commenting `@claude review` [opts the PR into push-triggered reviews](#manually-trigger-reviews), so additional cost accrues per push after that comment. To run a single review without subscribing to future pushes, comment `@claude review once` instead.
Costs appear on your Anthropic bill regardless of whether your organization uses Amazon Bedrock or Google Vertex AI for other Claude Code features. To set a monthly spend cap for Code Review, go to [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) and configure the limit for the Claude Code Review service.
Monitor spend via the weekly cost chart in [analytics](#view-usage) or the per-repo average cost column in admin settings.

## [​](#troubleshooting) Troubleshooting

Review runs are best-effort. A failed run never blocks your PR, but it also doesn’t retry on its own. This section covers how to recover from a failed run and where to look when the check run reports issues you can’t find.

### [​](#retrigger-a-failed-or-timed-out-review) Retrigger a failed or timed-out review

When the review infrastructure hits an internal error or exceeds its time limit, the check run completes with a title of **Code review encountered an error** or **Code review timed out**. The conclusion is still neutral, so nothing blocks your merge, but no findings are posted.
To run the review again, comment `@claude review once` on the PR. This starts a fresh review without subscribing the PR to future pushes. If the PR is already subscribed to push-triggered reviews, pushing a new commit also starts a new review.
The **Re-run** button in GitHub’s Checks tab does not retrigger Code Review. Use the comment command or a new push instead.

### [​](#review-didn’t-run-and-the-pr-shows-a-spend-cap-message) Review didn’t run and the PR shows a spend-cap message

When your organization’s monthly spend cap is reached, Code Review posts a single comment on the PR explaining that the review was skipped. Reviews resume automatically at the start of the next billing period, or immediately when an admin raises the cap at [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage).

### [​](#find-issues-that-aren’t-showing-as-inline-comments) Find issues that aren’t showing as inline comments

If the check run title says issues were found but you don’t see inline review comments on the diff, look in these other locations where findings are surfaced:

* **Check run Details**: click **Details** next to the Claude Code Review check in the Checks tab. The severity table lists every finding with its file, line, and summary regardless of whether the inline comment was accepted.
* **Files changed annotations**: open the **Files changed** tab on the PR. Findings render as annotations attached directly to the diff lines, separate from review comments.
* **Review body**: if you pushed to the PR while a review was running, some findings may reference lines that no longer exist in the current diff. Those appear under an **Additional findings** heading in the review body text rather than as inline comments.

## [​](#review-a-diff-locally) Review a diff locally

The [`/code-review` command](/docs/en/commands) reviews a diff in your terminal without installing the GitHub App. Run it in any Claude Code session: it reports correctness bugs and reuse, simplification, and efficiency cleanups. By default the local review covers your branch’s commits ahead of its upstream plus any uncommitted changes in the working tree. Pass `--comment` to post findings as inline PR comments, or `--fix` to apply the findings to your working tree after the review.
Lower [effort levels](/docs/en/model-config#adjust-effort-level) return fewer, higher-confidence findings, while `high` through `max` give broader coverage and may include uncertain findings. Without an effort argument, the review uses the session’s current effort. To review something other than the default diff, pass a target: a file path, a PR number, a branch name, or a ref range such as `main...my-feature`. The ref range form reviews the committed diff a pull request from `my-feature` into `main` would contain, regardless of how the branch’s upstream is configured.
`/code-review ultra --fix` runs the deeper [ultrareview](/docs/en/ultrareview) in the cloud, then applies its findings to your working tree when they arrive back in your session. Ultrareview uses its own scope: your current branch against the repository’s default branch, plus any uncommitted and staged changes in the working tree.
The command was named `/simplify` before v2.1.147, when it applied fixes by default. From v2.1.154, `/simplify` runs a separate cleanup-only review that applies fixes without hunting for bugs. If you scripted `/simplify` for bug-finding, switch to `/code-review --fix`, which is unchanged.

## [​](#related-resources) Related resources

Code Review is designed to work alongside the rest of Claude Code. If you want to run reviews locally before opening a PR, need a self-hosted setup, or want to go deeper on how `CLAUDE.md` shapes Claude’s behavior across tools, these pages are good next stops:

* [Commands](/docs/en/commands): run `/code-review` in a local Claude Code session to check a diff before pushing
* [GitHub Actions](/docs/en/github-actions): run Claude in your own GitHub Actions workflows for custom automation beyond code review
* [GitLab CI/CD](/docs/en/gitlab-ci-cd): self-hosted Claude integration for GitLab pipelines
* [Memory](/docs/en/memory): how `CLAUDE.md` files work across Claude Code
* [Analytics](/docs/en/analytics): track Claude Code usage beyond code review

Was this page helpful?

YesNo

[Security guidance plugin](/docs/en/security-guidance)[GitHub Actions](/docs/en/github-actions)

⌘I

---