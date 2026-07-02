---
title: Hello Skill
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Hello Skill

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
```

Run `/reload-plugins` to pick up the changes, then try the skill with your name:

```
/my-first-plugin:hello Alex
```

Claude will greet you by name. For more on passing arguments to skills, see [Skills](/docs/en/skills#pass-arguments-to-skills).

You’ve successfully created and tested a plugin with these key components:

* **Plugin manifest** (`.claude-plugin/plugin.json`): describes your plugin’s metadata
* **Skills directory** (`skills/`): contains your custom skills
* **Skill arguments** (`$ARGUMENTS`): captures user input for dynamic behavior

The `--plugin-dir` flag is useful for development and testing. When you’re ready to share your plugin with others, see [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces).

## [​](#develop-a-plugin-in-your-skills-directory) Develop a plugin in your skills directory

Instead of passing `--plugin-dir` on every launch, you can keep a plugin in your skills directory and have Claude Code load it automatically. `claude plugin init` scaffolds one:

```
claude plugin init my-tool
```

This creates `~/.claude/skills/my-tool/` with a `.claude-plugin/plugin.json` manifest and a starter `SKILL.md`. On the next session it loads as `my-tool@skills-dir` with no marketplace or install step.
For the auto-load rules, personal vs. project scope, the workspace-trust requirement, and how to update or remove one, see [Skills-directory plugins](/docs/en/plugins-reference#skills-directory-plugins).

## [​](#plugin-structure-overview) Plugin structure overview

You’ve created a plugin with a skill, but plugins can include much more: custom agents, hooks, MCP servers, LSP servers, and background monitors.

**Common mistake**: Don’t put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level.

| Directory | Location | Purpose |
| --- | --- | --- |
| `.claude-plugin/` | Plugin root | Contains `plugin.json` manifest (optional if components use default locations) |
| `skills/` | Plugin root | Skills as `<name>/SKILL.md` directories |
| `commands/` | Plugin root | Skills as flat Markdown files. Use `skills/` for new plugins |
| `agents/` | Plugin root | Custom agent definitions |
| `hooks/` | Plugin root | Event handlers in `hooks.json` |
| `.mcp.json` | Plugin root | MCP server configurations |
| `.lsp.json` | Plugin root | LSP server configurations for code intelligence |
| `monitors/` | Plugin root | Background monitor configurations in `monitors.json` |
| `bin/` | Plugin root | Executables added to the Bash tool’s `PATH` while the plugin is enabled |
| `settings.json` | Plugin root | Default [settings](/docs/en/settings) applied when the plugin is enabled |

A plugin that ships exactly one skill can place `SKILL.md` directly at the plugin root instead of creating a `skills/` directory. Claude Code loads it as a single skill and uses the frontmatter `name` field for the invocation name. Use the `skills/` layout for plugins that may grow to more than one skill.

**Next steps**: Ready to add more features? Jump to [Develop more complex plugins](#develop-more-complex-plugins) to add agents, hooks, MCP servers, and LSP servers. For complete technical specifications of all plugin components, see [Plugins reference](/docs/en/plugins-reference).

## [​](#develop-more-complex-plugins) Develop more complex plugins

Once you’re comfortable with basic plugins, you can create more sophisticated extensions.

### [​](#add-skills-to-your-plugin) Add Skills to your plugin

Plugins can include [Agent Skills](/docs/en/skills) to extend Claude’s capabilities. Skills are model-invoked: Claude automatically uses them based on the task context.
Add a `skills/` directory at your plugin root with Skill folders containing `SKILL.md` files:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Each `SKILL.md` contains YAML frontmatter and instructions. Include a `description` so Claude knows when to use the skill:

```
---
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

After installing the plugin, run `/reload-plugins` to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see [Agent Skills](/docs/en/skills).

### [​](#add-lsp-servers-to-your-plugin) Add LSP servers to your plugin

For common languages like TypeScript, Python, and Rust, install the pre-built LSP plugins from the official marketplace. Create custom LSP plugins only when you need support for languages not already covered.

LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn’t have an official LSP plugin, you can create your own by adding an `.lsp.json` file to your plugin:

.lsp.json

```
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Users installing your plugin must have the language server binary installed on their machine.
For complete LSP configuration options, see [LSP servers](/docs/en/plugins-reference#lsp-servers).

### [​](#add-background-monitors-to-your-plugin) Add background monitors to your plugin

Background monitors let your plugin watch logs, files, or external status in the background and notify Claude as events arrive. Claude Code starts each monitor automatically when the plugin is active, so you don’t need to instruct Claude to start the watch.
Add a `monitors/monitors.json` file at the plugin root with an array of monitor entries:

monitors/monitors.json

```
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Each stdout line from `command` is delivered to Claude as a notification during the session. For the full schema, including the `when` trigger and variable substitution, see [Monitors](/docs/en/plugins-reference#monitors).

### [​](#ship-default-settings-with-your-plugin) Ship default settings with your plugin

Plugins can include a `settings.json` file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the `agent` and `subagentStatusLine` keys are supported.
Setting `agent` activates one of the plugin’s [custom agents](/docs/en/sub-agents) as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.

settings.json

```
{
  "agent": "security-reviewer"
}
```

This example activates the `security-reviewer` agent defined in the plugin’s `agents/` directory. Settings from `settings.json` take priority over `settings` declared in `plugin.json`. Unknown keys are silently ignored.

### [​](#organize-complex-plugins) Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see [Plugin directory structure](/docs/en/plugins-reference#plugin-directory-structure).

### [​](#test-your-plugins-locally) Test your plugins locally

Use the `--plugin-dir` flag to test plugins during development. This loads your plugin directly without requiring installation.

```
claude --plugin-dir ./my-plugin
```

The flag also accepts a `.zip` archive of the plugin directory, which requires Claude Code v2.1.128 or later.

```
claude --plugin-dir ./my-plugin.zip
```

When a `--plugin-dir` plugin has the same name as an installed marketplace plugin, the local copy takes precedence for that session. This lets you test changes to a plugin you already have installed without uninstalling it first. The exception is plugins that managed settings force-enable or force-disable: `--plugin-dir` cannot override those.
As you make changes to your plugin, run `/reload-plugins` to pick up the updates without restarting. This reloads plugins, skills, agents, hooks, plugin MCP servers, and plugin LSP servers. Test your plugin components:

* Try your skills with `/plugin-name:skill-name`
* Check that agents appear in `/agents`
* Verify hooks work as expected

You can load multiple plugins at once by specifying the flag multiple times:

```
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

To test a plugin that is already packaged as a `.zip` archive and hosted at a URL, such as a CI build artifact, use `--plugin-url` instead. Claude Code fetches the archive at startup and loads it for that session only. If the fetch fails or the archive is invalid, Claude Code reports a plugin load error and starts without it. The same [trust considerations](/docs/en/discover-plugins#security) apply as for any plugin source: only point this flag at archives you control or trust.
To load multiple plugins, repeat the flag for each URL:

```
claude --plugin-url https://example.com/my-plugin.zip --plugin-url https://example.com/other.zip
```

Or pass space-separated URLs as one quoted argument:

```
claude --plugin-url "https://example.com/my-plugin.zip https://example.com/other.zip"
```

### [​](#debug-plugin-issues) Debug plugin issues

If your plugin isn’t working as expected:

1. **Check the structure**: Ensure your directories are at the plugin root, not inside `.claude-plugin/`
2. **Test components individually**: Check each skill, agent, and hook separately
3. **Use validation and debugging tools**: See [Debugging and development tools](/docs/en/plugins-reference#debugging-and-development-tools) for CLI commands and troubleshooting techniques

### [​](#share-your-plugins) Share your plugins

When your plugin is ready to share:

1. **Add documentation**: Include a `README.md` with installation and usage instructions
2. **Choose a versioning strategy**: Decide whether to set an explicit `version` or rely on the git commit SHA. See [version management](/docs/en/plugins-reference#version-management)
3. **Create or use a marketplace**: Distribute through [plugin marketplaces](/docs/en/plugin-marketplaces) for installation
4. **Test with others**: Have team members test the plugin before wider distribution

Once your plugin is in a marketplace, others can install it using the instructions in [Discover and install plugins](/docs/en/discover-plugins). To keep a plugin internal to your team, host the marketplace in a [private repository](/docs/en/plugin-marketplaces#private-repositories).

### [​](#submit-your-plugin-to-the-community-marketplace) Submit your plugin to the community marketplace

Anthropic maintains two public marketplaces for Claude Code plugins:

* **`claude-plugins-official`**: a curated set of plugins maintained by Anthropic. Registered automatically the first time you start Claude Code interactively. A non-interactive script that runs before that first launch must add it explicitly with `claude plugin marketplace add anthropics/claude-plugins-official`.
* **`claude-community`**: the public community marketplace where third-party submissions land after review. Users add it with `/plugin marketplace add anthropics/claude-plugins-community` and install from it as `@claude-community`.

To submit your plugin for community-marketplace review, use one of the in-app forms:

* **claude.ai**: [claude.ai/admin-settings/directory/submissions/plugins/new](https://claude.ai/admin-settings/directory/submissions/plugins/new)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

The claude.ai form requires a Team or Enterprise organization and directory management access; organization Owners have this access by default. Individual authors who aren’t part of a Team or Enterprise organization can use the Console form instead.
Run `claude plugin validate` locally before you submit. The review pipeline runs the same check on every submission, along with automated safety screening.
Approved plugins are pinned to a specific commit SHA in the [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) catalog, and CI bumps the pin automatically as you push new commits to your repository. The public catalog syncs nightly from the review pipeline, so there can be a delay between approval and your plugin appearing in `marketplace.json`. To check whether your plugin is installable yet, search for its name in the [community catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json).
The official marketplace, `claude-plugins-official`, is curated separately. Anthropic decides which plugins to include at its discretion. There is no application process, and the submission form does not add plugins to the official marketplace.
If Anthropic lists your plugin in the official marketplace, your CLI can prompt Claude Code users to install it. See [Recommend your plugin from your CLI](/docs/en/plugin-hints).

For complete technical specifications, debugging techniques, and distribution strategies, see [Plugins reference](/docs/en/plugins-reference).

## [​](#convert-existing-configurations-to-plugins) Convert existing configurations to plugins

If you already have skills or hooks in your `.claude/` directory, you can convert them into a plugin for easier sharing and distribution.

### [​](#migration-steps) Migration steps

1

Create the plugin structure

Create a new plugin directory:

```
mkdir -p my-plugin/.claude-plugin
```

Create the manifest file at `my-plugin/.claude-plugin/plugin.json`:

my-plugin/.claude-plugin/plugin.json

```
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

2

Copy your existing files

Copy your existing configurations to the plugin directory:

```