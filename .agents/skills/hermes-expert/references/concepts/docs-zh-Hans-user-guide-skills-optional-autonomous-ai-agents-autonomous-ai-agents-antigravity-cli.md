# Antigravity Cli — Operate the Antigravity CLI (agy): plugins, auth, sandbox | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-antigravity-cli](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-antigravity-cli)

本页总览

Operate the Antigravity CLI (agy): plugins, auth, sandbox.

## Skill metadata[​](#skill-metadata "Skill metadata的直接链接")

|  |  |
| --- | --- |
| Source | Optional — install with `hermes skills install official/autonomous-ai-agents/antigravity-cli` |
| Path | `optional-skills/autonomous-ai-agents/antigravity-cli` |
| Version | `0.2.0` |
| Author | Tony Simons (asimons81), Hermes Agent |
| License | MIT |
| Platforms | linux, macos, windows |
| Tags | `Coding-Agent`, `Antigravity`, `CLI`, `Auth`, `Plugins`, `Sandbox` |
| Related skills | [`grok`](/docs/zh-Hans/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-grok), [`codex`](/docs/zh-Hans/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex), [`claude-code`](/docs/zh-Hans/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code), [`hermes-agent`](/docs/zh-Hans/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent) |

## Reference: full SKILL.md[​](#reference-full-skillmd "Reference: full SKILL.md的直接链接")

信息

The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.

# Antigravity CLI (`agy`)

Operator guide for the Antigravity CLI, invoked as `agy`. Run all `agy`
commands through the Hermes `terminal` tool; inspect its config and logs with
`read_file`. This skill is reference + procedure — it does not wrap a network
API, so there is nothing to authenticate from Hermes itself.

## When to Use[​](#when-to-use "When to Use的直接链接")

* Installing, updating, or smoke-testing the `agy` binary
* Driving non-interactive `agy --print` / `agy -p` one-shots
* Debugging Antigravity auth, sandbox, permissions, or plugin state
* Reading Antigravity settings, keybindings, conversations, or logs

## Mental model[​](#mental-model "Mental model的直接链接")

Antigravity has two layers — keep them distinct or the guidance will be wrong:

1. **Shell wrapper commands** — `agy help`, `agy install`, `agy plugin`,
   `agy update`, `agy changelog`. Run these through the `terminal` tool.
2. **Interactive in-session slash commands** — `/config`, `/permissions`,
   `/skills`, `/agents`, etc. These only exist inside a running `agy` TUI
   session, not on the shell wrapper.

`agy help` shows the shell wrapper surface, NOT the in-session slash commands.

## Prerequisites[​](#prerequisites "Prerequisites的直接链接")

* The `agy` binary on PATH. Verify through the `terminal` tool:
  `command -v agy && agy --version`.
* No env vars or API keys required by this skill — Antigravity manages its own
  auth via the OS keyring / browser sign-in (see Authentication below).

## How to Run[​](#how-to-run "How to Run的直接链接")

Invoke every `agy` command through the `terminal` tool. Examples:

```
terminal(command="agy --version")  
terminal(command="agy help")  
terminal(command="agy plugin list")  
terminal(command="agy --print 'Summarize the repo in 3 bullets'", workdir="/path/to/project")
```

For an interactive multi-turn TUI session, launch `agy` with `pty=true` (and
tmux for capture/monitoring), the same pattern the `codex` / `claude-code`
skills use. For one-shot smoke tests and scripted prompts, prefer
`agy --print` (non-interactive).

To inspect Antigravity's own files, use `read_file` on the paths under Core
paths below — do not `cat` them through the terminal.

## Delegation patterns[​](#delegation-patterns "Delegation patterns的直接链接")

`agy` is a coding-agent backend in the same family as `codex` / `claude-code`,
so the same delegation shapes apply. Use these when handing real work (features,
fixes, reviews, second opinions) to Antigravity rather than just smoke-testing.

### One-shot (preferred for scripted prompts and second opinions)[​](#one-shot-preferred-for-scripted-prompts-and-second-opinions "One-shot (preferred for scripted prompts and second opinions)的直接链接")

```
terminal(command="agy -p 'Review this diff for bugs and security issues' --model 'Gemini 3.1 Pro (High)'", workdir="/path/to/repo", timeout=300)
```

`-p` is non-interactive: it runs the prompt and exits. Pick the engine with
`--model` (run `agy models` for the exact display strings, e.g.
`'Gemini 3.1 Pro (High)'`, `'Claude Opus 4.6 (Thinking)'`). Add extra context
roots with repeatable `--add-dir`.

### Long / bounded runs (tests, builds, multi-file changes)[​](#long--bounded-runs-tests-builds-multi-file-changes "Long / bounded runs (tests, builds, multi-file changes)的直接链接")

Background it and get notified on completion, the same as the `codex` skill:

```
terminal(command="agy -p 'Implement the change described in TASK.md and run the tests' --dangerously-skip-permissions", workdir="/path/to/repo", background=true, notify_on_complete=true)  
# then: process(action="poll"/"log"/"wait", session_id=<id>)
```

### Interactive multi-turn (PTY + tmux)[​](#interactive-multi-turn-pty--tmux "Interactive multi-turn (PTY + tmux)的直接链接")

For a conversational session, launch `agy -i` (or bare `agy`) under `pty=true`
with tmux for `capture-pane` / `send-keys`, exactly the pattern documented in
the `codex` / `claude-code` skills. Resume later with `--continue` / `-c` or a
specific `--conversation <id>`.

### Parallel instances (batch sub-issue / worktree fan-out)[​](#parallel-instances-batch-sub-issue--worktree-fan-out "Parallel instances (batch sub-issue / worktree fan-out)的直接链接")

Create one git worktree per task and launch an independent `agy -p` in each
(background), then collect results — same worktree fan-out the `codex` skill
uses for batch issue fixing. Bound concurrency to what the machine and your
review capacity can absorb.

### Output + bounding caveat (differs from Claude Code)[​](#output--bounding-caveat-differs-from-claude-code "Output + bounding caveat (differs from Claude Code)的直接链接")

* `agy -p` returns **plain text** — there is **no `--output-format json`** and
  no result envelope with `session_id` / cost / turn count. Parse stdout
  directly; don't expect a JSON object.
* There is **no `--max-turns`**. A print run is bounded by **`--print-timeout`**
  (default `5m`). Raise it for long tasks: `--print-timeout 20m`. Pair with the
  `terminal` `timeout=` so the outer call doesn't cut the run short.

### Orchestration boundary[​](#orchestration-boundary "Orchestration boundary的直接链接")

Antigravity is a **worker execution backend or third-opinion reviewer** — an
execution detail owned by the agent/profile running a task, NOT a first-class
orchestration primitive. Do not put `agy` on a kanban board as its own card or
treat it as a coordination layer; route work through the normal task graph and
let the assigned worker choose `agy` (vs. codex/claude-code/direct tools) as its
method. Reach for it explicitly only when the user asks, when a worker is
configured to wrap it, or when you want a Gemini-family cross-check against
another agent's plan or diff.

## Core paths[​](#core-paths "Core paths的直接链接")

* Binary / entrypoint: `agy`
* App data dir: `~/.gemini/antigravity-cli/`
* Settings file: `~/.gemini/antigravity-cli/settings.json`
* Keybindings file: `~/.gemini/antigravity-cli/keybindings.json`
* Logs: `~/.gemini/antigravity-cli/log/cli-*.log`
* Conversations: `~/.gemini/antigravity-cli/conversations/`
* Brain artifacts: `~/.gemini/antigravity-cli/brain/`
* History: `~/.gemini/antigravity-cli/history.jsonl`
* Plugin staging: `~/.gemini/antigravity-cli/plugins/<plugin_name>/`

## Quick Reference[​](#quick-reference "Quick Reference的直接链接")

### Wrapper commands[​](#wrapper-commands "Wrapper commands的直接链接")

* `agy changelog`
* `agy help`
* `agy install`
* `agy plugin` / `agy plugins`
* `agy update`

### Useful flags[​](#useful-flags "Useful flags的直接链接")

* `--add-dir`
* `--continue` / `-c`
* `--conversation`
* `--dangerously-skip-permissions`
* `--print` / `-p`
* `--print-timeout`
* `--prompt`
* `--prompt-interactive` / `-i`
* `--sandbox`
* `--log-file`
* `--version`

### Plugin subcommands (`agy plugin --help`)[​](#plugin-subcommands-agy-plugin---help "plugin-subcommands-agy-plugin---help的直接链接")

* `list`, `import [source]`, `install <target>`, `uninstall <name>`,
  `enable <name>`, `disable <name>`, `validate [path]`, `link <mp> <target>`,
  `help`

### Install flags (`agy install --help`)[​](#install-flags-agy-install---help "install-flags-agy-install---help的直接链接")

* `--dir`, `--skip-aliases`, `--skip-path`

### In-session slash commands[​](#in-session-slash-commands "In-session slash commands的直接链接")

* **Conversation control:** `/resume` (`/switch`), `/rewind` (`/undo`),
  `/rename <name>`, `/clear`, `/fork`, `/reset`, `/new`
* **Settings & tools:** `/config`, `/settings`, `/permissions`, `/model`,
  `/keybindings`, `/statusline`, `/tasks`, `/skills`, `/mcp`, `/open <path>`,
  `/usage`, `/logout`, `/agents`
* **Prompt helpers:** `@` path autocomplete, `esc esc` clears the prompt (when
  not streaming), `!` runs a terminal command directly, `?` opens help

## Settings and permissions[​](#settings-and-permissions "Settings and permissions的直接链接")

### Common settings keys (`settings.json`)[​](#common-settings-keys-settingsjson "common-settings-keys-settingsjson的直接链接")

* `allowNonWorkspaceAccess`
* `colorScheme`
* `permissions.allow`
* `trustedWorkspaces`

### Permission modes[​](#permission-modes "Permission modes的直接链接")

`request-review`, `always-proceed`, `strict`, `proceed-in-sandbox`.

### Sandbox behavior[​](#sandbox-behavior "Sandbox behavior的直接链接")

* `enableTerminalSandbox` is a boolean in `settings.json`; default `false`.
* Launch-time overrides (`--sandbox`, `--dangerously-skip-permissions`) can
  supersede persistent settings for the current session.

## Authentication behavior[​](#authentication-behavior "Authentication behavior的直接链接")

* The CLI tries the OS secure keyring first.
* With no saved session, it falls back to browser-based Google sign-in.
* Locally it opens the default browser; over SSH it prints an authorization URL
  and expects the auth code pasted back.
* `/logout` removes saved credentials.

## Plugins[​](#plugins "Plugins的直接链接")

* Plugins stage under `~/.gemini/antigravity-cli/plugins/<plugin_name>/`.
* They can bundle skills, agents, rules, MCP servers, and hooks.
* `agy plugin list` returning no imported plugins is a valid empty state.

## Pitfalls[​](#pitfalls "Pitfalls的直接链接")

* `agy help` shows wrapper commands, not interactive slash commands.
* `agy --version` is the safe non-interactive version check; `agy version` is
  interactive and can fail without a real TTY.
* First place to look for failures: `~/.gemini/antigravity-cli/log/cli-*.log`
  (read with `read_file`).
* Don't confuse persistent JSON settings with launch-time overrides.
* `~/.gemini/antigravity-cli/bin/agentapi` is a thin wrapper to `agy agentapi`.
* On WSL, token storage is file-based, so auth issues are usually local-file /
  session-state problems, not browser-only problems.
* Workspace identity can depend on launch directory and the `.antigravitycli`
  project marker.
* `agy -p` prints plain text only — no `--output-format json`, no result
  envelope. Don't try to parse a JSON object out of it (unlike `claude-code`).
* Bound print runs with `--print-timeout` (default `5m`), not `--max-turns`
  (which does not exist on `agy`).

## Verification[​](#verification "Verification的直接链接")

Confirm the install is real and usable, all through the `terminal` tool (read
files with `read_file`):

1. `terminal(command="command -v agy")`
2. `terminal(command="agy --version")`
3. `terminal(command="agy help")`
4. `terminal(command="agy plugin list")`
5. `read_file` on `~/.gemini/antigravity-cli/settings.json`
6. `read_file` on the latest `~/.gemini/antigravity-cli/log/cli-*.log`
7. If needed, `read_file` on `~/.gemini/antigravity-cli/keybindings.json`

## Support files[​](#support-files "Support files的直接链接")

* `references/cli-docs.md` — condensed notes from the getting-started, usage,
  and features docs.

* [Skill metadata](#skill-metadata)
* [Reference: full SKILL.md](#reference-full-skillmd)
* [When to Use](#when-to-use)
* [Mental model](#mental-model)
* [Prerequisites](#prerequisites)
* [How to Run](#how-to-run)
* [Delegation patterns](#delegation-patterns)
  + [One-shot (preferred for scripted prompts and second opinions)](#one-shot-preferred-for-scripted-prompts-and-second-opinions)
  + [Long / bounded runs (tests, builds, multi-file changes)](#long--bounded-runs-tests-builds-multi-file-changes)
  + [Interactive multi-turn (PTY + tmux)](#interactive-multi-turn-pty--tmux)
  + [Parallel instances (batch sub-issue / worktree fan-out)](#parallel-instances-batch-sub-issue--worktree-fan-out)
  + [Output + bounding caveat (differs from Claude Code)](#output--bounding-caveat-differs-from-claude-code)
  + [Orchestration boundary](#orchestration-boundary)
* [Core paths](#core-paths)
* [Quick Reference](#quick-reference)
  + [Wrapper commands](#wrapper-commands)
  + [Useful flags](#useful-flags)
  + [Plugin subcommands (`agy plugin --help`)](#plugin-subcommands-agy-plugin---help)
  + [Install flags (`agy install --help`)](#install-flags-agy-install---help)
  + [In-session slash commands](#in-session-slash-commands)
* [Settings and permissions](#settings-and-permissions)
  + [Common settings keys (`settings.json`)](#common-settings-keys-settingsjson)
  + [Permission modes](#permission-modes)
  + [Sandbox behavior](#sandbox-behavior)
* [Authentication behavior](#authentication-behavior)
* [Plugins](#plugins)
* [Pitfalls](#pitfalls)
* [Verification](#verification)
* [Support files](#support-files)