---
title: Security guidance for this repo
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Security guidance for this repo

- Do not log `customer_id` or `account_number` at INFO level or above.
- All routes under `/admin` must call `require_role("admin")` before any database read.
- Use `crypto.timingSafeEqual` for token comparison instead of `===`.
```

These rules are guidance for the reviewer, not deterministic guardrails. The plugin surfaces violations as findings for Claude to fix, but it does not block writes or guarantee every violation is caught. The guidance is additive only: a rule that says to ignore a vulnerability class does not suppress those findings. For hard enforcement, pair the plugin with a [hook that blocks the edit](/docs/en/hooks-guide#block-edits-to-protected-files) or a CI check.

### [​](#add-custom-per-edit-patterns) Add custom per-edit patterns

Create `.claude/security-patterns.yaml` to add regex or substring rules to the [per-edit pattern check](#on-each-file-edit). These run as deterministic string matches alongside the built-in patterns:

.claude/security-patterns.yaml

```
patterns:
  - rule_name: internal_api_key
    substrings: ["sk_live_", "AKIA"]
    reminder: "Hardcoded API key prefix. Load credentials from the secret manager."
  - rule_name: tenant_unfiltered_query
    regex: "\\.objects\\.all\\(\\)"
    paths: ["**/src/tenants/**"]
    reminder: "Multi-tenant code must filter by org_id."
```

| Field | Type | Description |
| --- | --- | --- |
| `rule_name` | string | Identifier shown in the warning |
| `reminder` | string | Warning text appended to Claude’s context, capped at 1 KB |
| `regex` | string | Python regex matched against the edited content |
| `substrings` | list | Literal substrings; provide this or `regex` |
| `paths` | list | Optional glob patterns; the rule applies only to matching files. Globs match against the full file path, so prefix project-relative patterns with `**/` |
| `exclude_paths` | list | Optional glob patterns to skip; same matching as `paths` |

The plugin also reads `.claude/security-patterns.yml` and `.claude/security-patterns.json` with the same schema. JSON works on any Python install. The YAML forms require PyYAML to be importable, which the plugin does not install for you. The plugin loads up to 50 custom rules and skips regexes that look prone to catastrophic backtracking.

### [​](#rule-file-lookup-locations) Rule file lookup locations

The plugin looks for `claude-security-guidance.md` and `security-patterns.yaml` in the same locations, independently of how the plugin was enabled:

| Scope | Path | Notes |
| --- | --- | --- |
| User | `~/.claude/claude-security-guidance.md` | Applies to every project on your machine |
| Project | `.claude/claude-security-guidance.md` | Checked in with the repository |
| Project local | `.claude/claude-security-guidance.local.md` | Gitignored, for personal overrides |

The plugin loads all locations that exist and concatenates them, with a combined cap of 8 KB for the guidance file. Administrators can distribute organization-wide rules by pushing the user-scope file to `~/.claude/` through device management. The same paths apply to `security-patterns.yaml`.

## [​](#usage-cost) Usage cost

The [per-edit pattern check](#on-each-file-edit) makes no model call and adds no cost. The [end-of-turn](#at-the-end-of-each-turn) and [commit](#on-each-commit-or-push-claude-makes) reviews each spend additional model usage that counts toward your [usage](/docs/en/costs) like any other Claude request. The commit review is agentic and may take several model turns per commit, capped at 20 reviews per rolling hour. Expect roughly one review call per turn that changes files and one deeper review per commit, both subject to the caps above.
Both model-backed reviews use Claude Opus 4.7 by default. Set `SECURITY_REVIEW_MODEL` to choose a different model for the end-of-turn review and `SG_AGENTIC_MODEL` for the commit review.
The plugin is available on all plans.

## [​](#disable-or-uninstall) Disable or uninstall

To turn off individual layers while keeping the rest, set the matching environment variable:

| Variable | Effect |
| --- | --- |
| `ENABLE_PATTERN_RULES=0` | Disable the [per-edit pattern check](#on-each-file-edit) |
| `ENABLE_STOP_REVIEW=0` | Disable the [end-of-turn diff review](#at-the-end-of-each-turn) |
| `ENABLE_COMMIT_REVIEW=0` | Disable the [commit and push review](#on-each-commit-or-push-claude-makes) |
| `ENABLE_CODE_SECURITY_REVIEW=0` | Disable all model-backed reviews at once |
| `SECURITY_GUIDANCE_DISABLE=1` | Disable the plugin entirely without uninstalling |

To pause the plugin in your user scope:

```
/plugin disable security-guidance@claude-plugins-official
```

To remove it from your user scope:

```
/plugin uninstall security-guidance@claude-plugins-official
```

If the plugin was enabled through a project’s `.claude/settings.json`, disabling it from `/plugin` writes an override to your `.claude/settings.local.json` rather than editing the checked-in file, so the plugin stays off for you while teammates are unaffected. If it was enabled through [managed settings](/docs/en/admin-setup), only an administrator can disable it.

## [​](#how-the-plugin-integrates-with-claude-code) How the plugin integrates with Claude Code

The plugin is built entirely on [hooks](/docs/en/hooks), the mechanism for running your own code at specific points in Claude’s loop. It registers:

| Hook event | Purpose |
| --- | --- |
| `SessionStart` | Bootstrap the plugin’s Python environment |
| `UserPromptSubmit` | Capture the working-tree baseline that the end-of-turn review diffs against |
| `PostToolUse` on `Edit`, `Write`, and `NotebookEdit` | Per-edit pattern match |
| `Stop` | End-of-turn diff review, run in the background |
| `PostToolUse` on `Bash`, filtered to `git commit` and `git push` | Commit and push review, run in the background |

If you build your own hooks, the [plugin’s source](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) is a working example of running a separate model call from a hook and feeding the result back to the session.

## [​](#how-this-fits-with-other-security-tools) How this fits with other security tools

The plugin is one layer in a defense-in-depth approach. It catches issues earliest, while code is still in the editor, but it is not a guarantee and does not replace later checks. A typical stack:

| Stage | Tool | What it covers |
| --- | --- | --- |
| In session | Security guidance plugin | Common vulnerabilities in code Claude writes, fixed in the same session |
| On demand | [`/security-review`](/docs/en/commands#all-commands) | One-time security pass on the current branch, run when you ask |
| On pull request | [Code Review](/docs/en/code-review), Team and Enterprise plans | Multi-agent correctness and security review with full codebase context |
| In CI | Your existing static analysis and dependency scanners | Language-specific rules, supply-chain checks, and policy enforcement the plugin does not attempt |

Each later stage catches what earlier ones miss. The plugin’s value is reducing the volume that reaches them, not eliminating the need for them.

## [​](#troubleshooting) Troubleshooting

The plugin writes runtime diagnostics to `~/.claude/security/log.txt`. Check there first if reviews are not appearing.
Common reasons a review layer skips without a message in the conversation:

* The directory is not a git repository: the end-of-turn and commit reviews require git state and skip outside a repository
* The session has no Anthropic authentication: the model-backed reviews skip and only the per-edit pattern check runs
* A `security-patterns.yaml` file is present but PyYAML is not importable: the file is ignored. Use `security-patterns.json` instead

## [​](#related-resources) Related resources

To go deeper on the pieces this page touches:

* [Code Review](/docs/en/code-review): set up the PR-time multi-agent review
* [Automate actions with hooks](/docs/en/hooks-guide): build your own checks at the same lifecycle points
* [Discover and install plugins](/docs/en/discover-plugins#official-anthropic-marketplace): browse other official plugins

Was this page helpful?

YesNo

[JetBrains IDEs](/docs/en/jetbrains)[Code Review](/docs/en/code-review)

⌘I

---