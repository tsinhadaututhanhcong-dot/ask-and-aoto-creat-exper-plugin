---
type: Reference
title: "Migrating from Gemini CLI"
description: "> Nguồn: Google Antigravity Master Corpus"
timestamp: 2026-07-06T03:34:16Z
---
# Migrating from Gemini CLI

> Nguồn: Google Antigravity Master Corpus
> Phân loại: concept
> Trạng thái: active
> Ngày tạo: 2026-06-21


*Source URL*: https://antigravity.google/docs/gcli-migration

If you are an existing Gemini CLI user looking to migrate your workflow to Antigravity CLI, you have come to the right place. The guide below will help you get familiar with and up and running quickly in Antigravity CLI.

info**TL;DR**: Antigravity CLI supports the majority of features from Gemini CLI. While there is not 100% feature parity, workflow defining features like *Gemini CLI extensions* (Antigravity plugins), *Agent Skills*, *MCP servers*, *hooks*, and *subagents* are all supported in Antigravity CLI.

On the first launch of Antigravity CLI, you should see **Migration Options** where you can choose to migrate your existing Gemini CLI extensions to the equivalent *Antigravity Plugins*.

info**Note**: Some Gemini CLI extensions cannot be migrated 1:1 to Antigravity plugins as some components (e.g., custom themes) are not currently supported.

For the majority of users, you can now get started using Antigravity CLI with the workflows you have come to love in Gemini CLI. Antigravity CLI loads in the same context files and global Agent Skills as Gemini CLI does.

If you notice something not working the way it should or how you expect, refer to the specific details below.

## Gemini CLI Extensions → Antigravity Plugins

Since Gemini CLI launched extensions (a way to extend the CLI by bundling and sharing capabilities), the industry has standardized on the term **plugins**. Antigravity plugins are supported in Antigravity CLI.

Users should be prompted on the first launch of Antigravity CLI to have their extensions automatically migrated to plugins. You can also run an explicit command from your terminal to migrate them:

content\_copy

```
            agy plugin import gemini
```

Running the `agy plugin import` command will search for each locally installed extension and convert them to an Antigravity plugin:

content\_copy

```
              [ok]    conductor
          - skills      : skipped (not found)
          - agents      : skipped (not found)
          ✔ commands    : 6 processed (converted to skills)
          - mcpServers  : skipped (not found)
          - hooks       : skipped (not found)
  [ok]    google-workspace
          ✔ skills      : 6 processed
          - agents      : skipped (not found)
          ✔ commands    : 4 processed (converted to skills)
          ✔ mcpServers  : 1 processed
          - hooks       : skipped (not found)
```

## Context Files (Rules)

Antigravity CLI supports the same context files as Gemini CLI:

* **Workspace Context**: Reads both `GEMINI.md` and `AGENTS.md` from your active workspace directory.
* **Global Context**: Automatically loads and enforces global constraints located at `~/.gemini/GEMINI.md`.

## Agent Skills

Agent Skills work in Antigravity CLI just as they do in Gemini CLI. They can be managed with the same `/skills` command and are also converted into slash commands allowing them to be manually invoked.

Global skills for Gemini CLI were located in `~/.gemini/skills/` and are shared with Antigravity CLI across all workspaces. No action is needed for global skills; they are picked up automatically.

Workspace-specific skills for Antigravity CLI are stored in `.agents/skills`, which means if you have project/workspace skills in a given project within the `.gemini/skills` folder, they will need to be moved to `.agents/skills`.

| Attribute | Gemini CLI | Antigravity CLI |
| --- | --- | --- |
| **Location** | Global: `~/.gemini/skills/`Workspace: `.gemini/skills/` or `.agents/skills/` | Global: `~/.gemini/antigravity-cli/skills/`Workspace: `.agents/skills/` |
| **Management** | `/skills` | `/skills` |
| **Behavior** | Skills become slash commands | Skills become slash commands |

info**Note**: Antigravity CLI does not currently have an equivalent to the `gemini skills` command for managing Agent Skills on your terminal. You can create your own skills files manually or use `npx skills install`.

## MCP Servers

Antigravity CLI supports both local and remote MCP servers and provides the same `/mcp` command to manage them. The main difference from Gemini CLI is the file location where `mcpServers` are defined.

Antigravity and Antigravity CLI store MCP server configurations in a distinct `mcp_config.json` file, whereas Gemini CLI stores them inline in your `settings.json`.

warning**Important**: Antigravity CLI uses the `serverUrl` field instead of `url` (or the deprecated `httpUrl`) for remote MCP servers.

| Attribute | Gemini CLI | Antigravity CLI |
| --- | --- | --- |
| **Location** | Global: `~/.gemini/settings.json`Workspace: `.gemini/settings.json` | Global: `~/.gemini/antigravity-cli/mcp_config.json`Workspace: `.agents/mcp_config.json` |
| **Management** | `/mcp` | `/mcp` |



---