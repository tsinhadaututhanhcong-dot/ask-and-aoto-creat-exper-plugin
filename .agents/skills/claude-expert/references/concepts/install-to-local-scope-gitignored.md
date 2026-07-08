---
type: Reference
title: Install to local scope (gitignored)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Install to local scope (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### [​](#plugin-uninstall) plugin uninstall

Remove an installed plugin.

```
claude plugin uninstall <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Uninstall from scope: `user`, `project`, or `local` | `user` |
| `--keep-data` | Preserve the plugin’s [persistent data directory](#persistent-data-directory) |  |
| `--prune` | Also remove auto-installed dependencies that no other plugin requires. See [plugin prune](#plugin-prune) |  |
| `-y, --yes` | Skip the `--prune` confirmation prompt. Required when stdin or stdout is not a TTY |  |
| `-h, --help` | Display help for command |  |

**Aliases:** `remove`, `rm`
By default, uninstalling from the last remaining scope also deletes the plugin’s `${CLAUDE_PLUGIN_DATA}` directory. Use `--keep-data` to preserve it, for example when reinstalling after testing a new version.

### [​](#plugin-prune) plugin prune

Remove auto-installed plugin dependencies that are no longer required by any installed plugin. Dependencies that Claude Code pulled in to satisfy another plugin’s [`dependencies`](/docs/en/plugin-dependencies) field are removed; plugins you installed directly are never touched.

```
claude plugin prune [options]
```

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Prune at scope: `user`, `project`, or `local` | `user` |
| `--dry-run` | List what would be removed without removing anything |  |
| `-y, --yes` | Skip the confirmation prompt. Required when stdin or stdout is not a TTY |  |
| `-h, --help` | Display help for command |  |

**Aliases:** `autoremove`
The command lists orphaned dependencies and asks for confirmation before removing them. To remove a plugin and clean up its dependencies in one step, run `claude plugin uninstall <plugin> --prune`.

`claude plugin prune` requires Claude Code v2.1.121 or later.

### [​](#plugin-enable) plugin enable

Enable a disabled plugin. If the plugin declares [dependencies](/docs/en/plugin-dependencies), Claude Code enables them transitively at the same scope, and the command fails when a dependency is not installed.

```
claude plugin enable <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Scope to enable: `user`, `project`, or `local` | `user` |
| `-h, --help` | Display help for command |  |

### [​](#plugin-disable) plugin disable

Disable a plugin without uninstalling it. Fails when another enabled plugin [depends on](/docs/en/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies) the target. The error message includes a chained command that disables every dependent first.

```
claude plugin disable <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Scope to disable: `user`, `project`, or `local` | `user` |
| `-h, --help` | Display help for command |  |

### [​](#plugin-update) plugin update

Update a plugin to the latest version.

```
claude plugin update <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Scope to update: `user`, `project`, `local`, or `managed` | `user` |
| `-h, --help` | Display help for command |  |

---

### [​](#plugin-list) plugin list

List installed plugins with their version, source marketplace, and enable status.

```
claude plugin list [options]
```

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `--json` | Output as JSON |  |
| `--available` | Include available plugins from marketplaces. Requires `--json` |  |
| `-h, --help` | Display help for command |  |

Within an interactive session, `/plugin list` prints the same listing inline. The interactive form accepts `--enabled` or `--disabled` to show only plugins in that state, and `ls` as a shorthand for `list`.

### [​](#plugin-details) plugin details

Show a plugin’s component inventory and projected token cost. The output lists all components the plugin contributes, grouped as Skills, Agents, Hooks, MCP servers, and LSP servers, along with an estimate of how many tokens it adds to each session. The Skills group includes both `skills/` and `commands/` entries.

```
claude plugin details <name>
```

**Arguments:**

* `<name>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-h, --help` | Display help for command |  |

The output shows two cost figures for each component:

* **Always-on:** tokens added to every session by the plugin’s listing text, such as skill descriptions, agent descriptions, and command names, regardless of whether any component fires.
* **On-invoke:** tokens a component costs when it fires. Shown per component, not as a plugin total, because a typical session invokes only a subset of components.

This example shows what the output looks like for a plugin with two skills:

```
dependency-guard 1.2.0
  Dependency analysis for Claude Code sessions
  Source: dependency-guard@example-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

The always-on total is computed via the `count_tokens` API for your active model. Per-component numbers are proportionally scaled from that total. If the API is unreachable, the command falls back to a character-based estimate.

### [​](#plugin-tag) plugin tag

Create a release git tag for the plugin in the current directory. Run from inside the plugin’s folder. See [Tag plugin releases](/docs/en/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```
claude plugin tag [options]
```

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `--push` | Push the tag to the remote after creating it |  |
| `--dry-run` | Print what would be tagged without creating the tag |  |
| `-f, --force` | Create the tag even if the working tree is dirty or the tag already exists |  |
| `-h, --help` | Display help for command |  |

---

## [​](#debugging-and-development-tools) Debugging and development tools

### [​](#debugging-commands) Debugging commands

Use `claude --debug` to see plugin loading details:
This shows:

* Which plugins are being loaded
* Any errors in plugin manifests
* Skill, agent, and hook registration
* MCP server initialization

### [​](#common-issues) Common issues

| Issue | Cause | Solution |
| --- | --- | --- |
| Plugin not loading | Invalid `plugin.json` | Run `claude plugin validate` or `/plugin validate` to check `plugin.json`, skill/agent/command frontmatter, and `hooks/hooks.json` for syntax and schema errors |
| Skills not appearing | Wrong directory structure | Ensure `skills/` or `commands/` is at the plugin root, not inside `.claude-plugin/` |
| Hooks not firing | Script not executable | Run `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths |
| Path errors | Absolute paths used | All paths must be relative and start with `./` |
| LSP `Executable not found in $PATH` | Language server not installed | Install the binary (e.g., `npm install -g typescript-language-server typescript`) |

### [​](#example-error-messages) Example error messages

**Manifest validation errors**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: check for missing commas, extra commas, or unquoted strings
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: a required field is missing
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON syntax error

**Plugin loading errors**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: command path exists but contains no valid command files
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: the `source` path in marketplace.json points to a non-existent directory
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: remove duplicate component definitions or remove `strict: false` in marketplace entry

### [​](#hook-troubleshooting) Hook troubleshooting

**Hook script not executing**:

1. Check the script is executable: `chmod +x ./scripts/your-script.sh`
2. Verify the shebang line: First line should be `#!/bin/bash` or `#!/usr/bin/env bash`
3. Check the path uses `${CLAUDE_PLUGIN_ROOT}`: `"command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/your-script.sh"`
4. Test the script manually: `./scripts/your-script.sh`

**Hook not triggering on expected events**:

1. Verify the event name is correct (case-sensitive): `PostToolUse`, not `postToolUse`
2. Check the matcher pattern matches your tools: `"matcher": "Write|Edit"` for file operations
3. Confirm the hook type is valid: `command`, `http`, `mcp_tool`, `prompt`, or `agent`

### [​](#mcp-server-troubleshooting) MCP server troubleshooting

**Server not starting**:

1. Check the command exists and is executable
2. Verify all paths use `${CLAUDE_PLUGIN_ROOT}` variable
3. Check the MCP server logs: `claude --debug` shows initialization errors
4. Test the server manually outside of Claude Code

**Server tools not appearing**:

1. Ensure the server is properly configured in `.mcp.json` or `plugin.json`
2. Verify the server implements the MCP protocol correctly
3. Check for connection timeouts in debug output

### [​](#directory-structure-mistakes) Directory structure mistakes

**Symptoms**: Plugin loads but components (skills, agents, hooks) are missing.
**Correct structure**: Components must be at the plugin root, not inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Only manifest here
├── commands/            ← At root level
├── agents/              ← At root level
└── hooks/               ← At root level
```

If your components are inside `.claude-plugin/`, move them to the plugin root.
**Debug checklist**:

1. Run `claude --debug` and look for “loading plugin” messages
2. Check that each component directory is listed in the debug output
3. Verify file permissions allow reading the plugin files

---

## [​](#distribution-and-versioning-reference) Distribution and versioning reference

### [​](#version-management) Version management

Claude Code uses the plugin’s version as the cache key that determines whether an update is available. When you run `/plugin update` or auto-update fires, Claude Code computes the current version and skips the update if it matches what’s already installed.
The version is resolved from the first of these that is set:

1. The `version` field in the plugin’s `plugin.json`
2. The `version` field in the plugin’s marketplace entry in `marketplace.json`
3. The git commit SHA of the plugin’s source, for `github`, `url`, `git-subdir`, and relative-path sources in a git-hosted marketplace
4. `unknown`, for `npm` sources or local directories not inside a git repository

This gives you two ways to version a plugin:

| Approach | How | Update behavior | Best for |
| --- | --- | --- | --- |
| **Explicit version** | Set `"version": "2.1.0"` in `plugin.json` | Users get updates only when you bump this field. Pushing new commits without bumping it has no effect, and `/plugin update` reports “already at the latest version”. | Published plugins with stable release cycles |
| **Commit-SHA version** | Omit `version` from both `plugin.json` and the marketplace entry | Users get updates on every new commit to the plugin’s git source | Internal or team plugins under active development |

If you set `version` in `plugin.json`, you must bump it every time you want users to receive changes. Pushing new commits alone is not enough, because Claude Code sees the same version string and keeps the cached copy. If you’re iterating quickly, leave `version` unset so the git commit SHA is used instead.

If you use explicit versions, follow [semantic versioning](https://semver.org) (`MAJOR.MINOR.PATCH`): bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Document changes in a `CHANGELOG.md`.


---

## [​](#see-also) See also

* [Plugins](/docs/en/plugins) - Tutorials and practical usage
* [Plugin marketplaces](/docs/en/plugin-marketplaces) - Creating and managing marketplaces
* [Skills](/docs/en/skills) - Skill development details
* [Subagents](/docs/en/sub-agents) - Agent configuration and capabilities
* [Hooks](/docs/en/hooks) - Event handling and automation
* [MCP](/docs/en/mcp) - External tool integration
* [Settings](/docs/en/settings) - Configuration options for plugins

Was this page helpful?

YesNo

[Hooks reference](/docs/en/hooks)[Channels reference](/docs/en/channels-reference)

⌘I

---