---
title: API Development Rules
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Rules without a `paths` field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.
Use glob patterns in the `paths` field to match files by extension, directory, or any combination:

| Pattern | Matches |
| --- | --- |
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` directory |
| `*.md` | Markdown files in the project root |
| `src/components/*.tsx` | React components in a specific directory |

You can specify multiple patterns and use brace expansion to match multiple extensions in one pattern:

```
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### [​](#share-rules-across-projects-with-symlinks) Share rules across projects with symlinks

The `.claude/rules/` directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and circular symlinks are detected and handled gracefully.
This example links both a shared directory and an individual file:

```
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### [​](#user-level-rules) User-level rules

Personal rules in `~/.claude/rules/` apply to every project on your machine. Use them for preferences that aren’t project-specific:

```
~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows
```

User-level rules are loaded before project rules, giving project rules higher priority.

### [​](#manage-claude-md-for-large-teams) Manage CLAUDE.md for large teams

For organizations deploying Claude Code across teams, you can centralize instructions and control which CLAUDE.md files are loaded.

#### [​](#deploy-organization-wide-claude-md) Deploy organization-wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.

1

Create the file at the managed policy location

* macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
* Linux and WSL: `/etc/claude-code/CLAUDE.md`
* Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`

2

Deploy with your configuration management system

Use MDM, Group Policy, Ansible, or similar tools to distribute the file across developer machines. See [managed settings](/docs/en/permissions#managed-settings) for other organization-wide configuration options.

The `claudeMd` key lets you put managed CLAUDE.md content directly inside `managed-settings.json` instead of deploying a separate file.
**Scope**: every Claude Code session on the machine, in every repository. For repository-specific guidance, commit a project CLAUDE.md instead.
**Precedence**: same as a managed CLAUDE.md file. Loads before user and project CLAUDE.md.
**Where it’s honored**: managed and policy settings only. Setting `claudeMd` in user, project, or local settings has no effect.
The example below adds behavioral instructions directly in a managed settings file:

```
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

A managed CLAUDE.md and [managed settings](/docs/en/settings#settings-files) serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance:

| Concern | Configure in |
| --- | --- |
| Block specific tools, commands, or file paths | Managed settings: `permissions.deny` |
| Enforce sandbox isolation | Managed settings: `sandbox.enabled` |
| Environment variables and API provider routing | Managed settings: `env` |
| Authentication method and organization lock | Managed settings: `forceLoginMethod`, `forceLoginOrgUUID` |
| Code style and quality guidelines | Managed CLAUDE.md |
| Data handling and compliance reminders | Managed CLAUDE.md |
| Behavioral instructions for Claude | Managed CLAUDE.md |

Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude’s behavior but are not a hard enforcement layer.

#### [​](#exclude-specific-claude-md-files) Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren’t relevant to your work. The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern.
This example excludes a top-level CLAUDE.md and a rules directory from a parent folder. Add it to `.claude/settings.local.json` so the exclusion stays local to your machine:

```
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Patterns are matched against absolute file paths using glob syntax. You can configure `claudeMdExcludes` at any [settings layer](/docs/en/settings#settings-files): user, project, local, or managed policy. Arrays merge across layers.
Managed policy CLAUDE.md files cannot be excluded. This ensures organization-wide instructions always apply regardless of individual settings.

## [​](#auto-memory) Auto memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Claude doesn’t save something every session. It decides what’s worth remembering based on whether the information would be useful in a future conversation.

Auto memory requires Claude Code v2.1.59 or later. Check your version with `claude --version`.

### [​](#enable-or-disable-auto-memory) Enable or disable auto memory

Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings:

```
{
  "autoMemoryEnabled": false
}
```

To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### [​](#storage-location) Storage location

Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.
To store auto memory in a different location, set `autoMemoryDirectory` in your `settings.json`. It is read from any [settings scope](/docs/en/settings#settings-precedence): user, project, local, policy, or `--settings`.

```
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

The value must be an absolute path or start with `~/`. When set in a project’s `.claude/settings.json` or `.claude/settings.local.json`, the value is honored only after you accept the workspace trust dialog for that folder, the same gate that governs hooks.
The directory contains a `MEMORY.md` entrypoint and optional topic files:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what’s stored where.
Auto memory is machine-local. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.

### [​](#how-it-works) How it works

The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.
This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.
Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.
Claude reads and writes memory files during your session. When you see “Writing memory” or “Recalled memory” in the Claude Code interface, Claude is actively updating or reading from `~/.claude/projects/<project>/memory/`.

### [​](#audit-and-edit-your-memory) Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. Run [`/memory`](#view-and-edit-with-%2Fmemory) to browse and open memory files from within a session.

## [​](#view-and-edit-with-/memory) View and edit with `/memory`

The `/memory` command lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.
When you ask Claude to remember something, like “always use pnpm, not npm” or “remember that the API tests require a local Redis instance,” Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly, like “add this to CLAUDE.md,” or edit the file yourself via `/memory`.

## [​](#troubleshoot-memory-issues) Troubleshoot memory issues

These are the most common issues with CLAUDE.md and auto memory, along with steps to debug them.

### [​](#claude-isn’t-following-my-claude-md) Claude isn’t following my CLAUDE.md

CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there’s no guarantee of strict compliance, especially for vague or conflicting instructions.
To debug:

* Run `/memory` to verify your CLAUDE.md and CLAUDE.local.md files are being loaded. If a file isn’t listed, Claude can’t see it.
* Check that the relevant CLAUDE.md is in a location that gets loaded for your session (see [Choose where to put CLAUDE.md files](#choose-where-to-put-claude-md-files)).
* Make instructions more specific. “Use 2-space indentation” works better than “format code nicely.”
* Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily.

If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a [hook](/docs/en/hooks-guide) instead. Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.
For instructions you want at the system prompt level, use [`--append-system-prompt`](/docs/en/cli-reference#system-prompt-flags). This must be passed every invocation, so it’s better suited to scripts and automation than interactive use.

Use the [`InstructionsLoaded` hook](/docs/en/hooks#instructionsloaded) to log exactly which instruction files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories.

### [​](#i-don’t-know-what-auto-memory-saved) I don’t know what auto memory saved

Run `/memory` and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete.

### [​](#my-claude-md-is-too-large) My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Use [path-scoped rules](#path-specific-rules) to load instructions only when Claude works with matching files, or trim content that isn’t needed in every session. Splitting into [`@path` imports](#import-additional-files) helps organization but does not reduce context, since imported files load at launch.

### [​](#instructions-seem-lost-after-/compact) Instructions seem lost after `/compact`

Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory.
If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn’t reloaded yet. Add conversation-only instructions to CLAUDE.md to make them persist. See [What survives compaction](/docs/en/context-window#what-survives-compaction) for the full breakdown.
See [Write effective instructions](#write-effective-instructions) for guidance on size, structure, and specificity.

## [​](#related-resources) Related resources

* [Debug your configuration](/docs/en/debug-your-config): diagnose why CLAUDE.md or settings aren’t taking effect
* [Skills](/docs/en/skills): package repeatable workflows that load on demand
* [Settings](/docs/en/settings): configure Claude Code behavior with settings files
* [Subagent memory](/docs/en/sub-agents#enable-persistent-memory): let subagents maintain their own auto memory

Was this page helpful?

YesNo

[Prompt caching](/docs/en/prompt-caching)[Permission modes](/docs/en/permission-modes)

⌘I

---