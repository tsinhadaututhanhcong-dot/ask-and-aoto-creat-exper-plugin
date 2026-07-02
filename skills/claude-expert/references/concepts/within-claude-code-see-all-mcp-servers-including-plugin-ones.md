---
title: Within Claude Code, see all MCP servers including plugin ones
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Within Claude Code, see all MCP servers including plugin ones
/mcp
```

Plugin servers appear in the list with indicators showing they come from plugins.
**Plugin MCP tool names**:
Tools from a plugin-bundled MCP server include both the plugin name and the server key in their callable name. The full form is `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`, where any character outside `A-Z`, `a-z`, `0-9`, `_`, and `-` is replaced with `_`. For the `database-tools` server bundled in a plugin named `my-plugin`, a `query` tool is callable as:

```
mcp__plugin_my-plugin_database-tools__query
```

Use this full name when referencing the tool in [permission rules](/docs/en/permissions), a skill’s `allowed-tools` list, or a [subagent’s `tools` field](/docs/en/sub-agents#available-tools).
**Benefits of plugin MCP servers**:

* **Bundled distribution**: tools and servers packaged together
* **Automatic setup**: no manual MCP configuration needed
* **Team consistency**: everyone gets the same tools when the plugin is installed

See the [plugin components reference](/docs/en/plugins-reference#mcp-servers) for details on bundling MCP servers with plugins.

## [​](#mcp-installation-scopes) MCP installation scopes

MCP servers can be configured at three scopes. The scope you choose controls which projects the server loads in and whether the configuration is shared with your team. Administrators can also deploy servers at the enterprise level via [managed configuration](#managed-mcp-configuration).

| Scope | Loads in | Shared with team | Stored in |
| --- | --- | --- | --- |
| [Local](#local-scope) | Current project only | No | `~/.claude.json` |
| [Project](#project-scope) | Current project only | Yes, via version control | `.mcp.json` in project root |
| [User](#user-scope) | All your projects | No | `~/.claude.json` |

### [​](#local-scope) Local scope

Local scope is the default. A local-scoped server loads only in the project where you added it and stays private to you. Claude Code stores it in `~/.claude.json` under that project’s path, so the same server won’t appear in your other projects. Use local scope for personal development servers, experimental configurations, or servers with credentials you don’t want in version control.

The term “local scope” for MCP servers differs from general local settings. MCP local-scoped servers are stored in `~/.claude.json` (your home directory), while general local settings use `.claude/settings.local.json` (in the project directory). See [Settings](/docs/en/settings#settings-files) for details on settings file locations.

```