---
type: Reference
title: Create plugins - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Create plugins - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. This guide covers creating your own plugins with skills, agents, hooks, and MCP servers.
Looking to install existing plugins? See [Discover and install plugins](/docs/en/discover-plugins). For complete technical specifications, see [Plugins reference](/docs/en/plugins-reference).

## [​](#when-to-use-plugins-vs-standalone-configuration) When to use plugins vs standalone configuration

Claude Code supports two ways to add custom skills, agents, and hooks:

| Approach | Skill names | Best for |
| --- | --- | --- |
| **Standalone** (`.claude/` directory) | `/hello` | Personal workflows, project-specific customizations, quick experiments |
| **Plugins** (self-contained directories with skills, agents, hooks, or a `.claude-plugin/plugin.json` manifest) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

**Use standalone configuration when**:

* You’re customizing Claude Code for a single project
* The configuration is personal and doesn’t need to be shared
* You’re experimenting with skills or hooks before packaging them
* You want short skill names like `/hello` or `/deploy`

**Use plugins when**:

* You want to share functionality with your team or community
* You need the same skills/agents across multiple projects
* You want version control and easy updates for your extensions
* You’re distributing through a marketplace
* You’re okay with namespaced skills like `/my-plugin:hello` (namespacing prevents conflicts between plugins)

Start with standalone configuration in `.claude/` for quick iteration, then [convert to a plugin](#convert-existing-configurations-to-plugins) when you’re ready to share.

## [​](#quickstart) Quickstart

This quickstart walks you through creating a plugin with a custom skill. You’ll create a manifest (the configuration file that defines your plugin), add a skill, and test it locally using the `--plugin-dir` flag.

### [​](#prerequisites) Prerequisites

* Claude Code [installed and authenticated](/docs/en/quickstart#step-1-install-claude-code)

If you don’t see the `/plugin` command, update Claude Code to the latest version. See [Troubleshooting](/docs/en/troubleshooting) for upgrade instructions.

### [​](#create-your-first-plugin) Create your first plugin

1

Create the plugin directory

Every plugin lives in its own directory containing your skills, agents, or hooks, optionally alongside a `.claude-plugin/plugin.json` manifest. Create one now:

```
mkdir my-first-plugin
```

2

Create the plugin manifest

The manifest file at `.claude-plugin/plugin.json` defines your plugin’s identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.Create the `.claude-plugin` directory inside your plugin folder:

```
mkdir my-first-plugin/.claude-plugin
```

Then create `my-first-plugin/.claude-plugin/plugin.json` with this content:

my-first-plugin/.claude-plugin/plugin.json

```
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

| Field | Purpose |
| --- | --- |
| `name` | Unique identifier and skill namespace. Skills are prefixed with this (e.g., `/my-first-plugin:hello`). |
| `description` | Shown in the plugin manager when browsing or installing plugins. |
| `version` | Optional. If set, users only receive updates when you bump this field. If omitted and your plugin is distributed via git, the commit SHA is used and every commit counts as a new version. See [version management](/docs/en/plugins-reference#version-management). |
| `author` | Optional. Helpful for attribution. |

For additional fields like `homepage`, `repository`, and `license`, see the [full manifest schema](/docs/en/plugins-reference#plugin-manifest-schema).

3

Add a skill

Skills live in the `skills/` directory. Each skill is a folder containing a `SKILL.md` file. The folder name becomes the skill name, prefixed with the plugin’s namespace (`hello/` in a plugin named `my-first-plugin` creates `/my-first-plugin:hello`).Create a skill directory in your plugin folder:

```
mkdir -p my-first-plugin/skills/hello
```

Then create `my-first-plugin/skills/hello/SKILL.md` with this content:

my-first-plugin/skills/hello/SKILL.md

```
---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.
```

4

Test your plugin

Run Claude Code with the `--plugin-dir` flag to load your plugin:

```
claude --plugin-dir ./my-first-plugin
```

Once Claude Code starts, try your new skill:

```
/my-first-plugin:hello
```

You’ll see Claude respond with a greeting. Run `/help` to see your skill listed under the plugin namespace.

**Why namespacing?** Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name.To change the namespace prefix, update the `name` field in `plugin.json`.

5

Add skill arguments

Make your skill dynamic by accepting user input. The `$ARGUMENTS` placeholder captures any text the user provides after the skill name.Update your `SKILL.md` file:

my-first-plugin/skills/hello/SKILL.md

```
---
description: Greet the user with a personalized message
---