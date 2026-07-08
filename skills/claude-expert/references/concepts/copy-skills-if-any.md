---
type: Reference
title: Copy skills (if any)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Copy skills (if any)
cp -r .claude/skills my-plugin/
```

3

Migrate hooks

If you have hooks in your settings, create a hooks directory:

```
mkdir my-plugin/hooks
```

Create `my-plugin/hooks/hooks.json` with your hooks configuration. Copy the `hooks` object from your `.claude/settings.json` or `settings.local.json`, since the format is the same. The command receives hook input as JSON on stdin, so use `jq` to extract the file path:

my-plugin/hooks/hooks.json

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
      }
    ]
  }
}
```

4

Test your migrated plugin

Load your plugin to verify everything works:

```
claude --plugin-dir ./my-plugin
```

Test each component: run your commands, check agents appear in `/agents`, and verify hooks trigger correctly.

### [​](#what-changes-when-migrating) What changes when migrating

| Standalone (`.claude/`) | Plugin |
| --- | --- |
| Only available in one project | Can be shared via marketplaces |
| Files in `.claude/commands/` | Files in `plugin-name/commands/` |
| Hooks in `settings.json` | Hooks in `hooks/hooks.json` |
| Must manually copy to share | Install with `/plugin install` |

After migrating, remove the original files from `.claude/` to avoid duplicates. Project and user `.claude/agents/` definitions override same-named plugin agents, so the plugin version only takes effect once the originals are removed.

## [​](#next-steps) Next steps

Now that you understand Claude Code’s plugin system, here are suggested paths for different goals:

### [​](#for-plugin-users) For plugin users

* [Discover and install plugins](/docs/en/discover-plugins): browse marketplaces and install plugins
* [Configure team marketplaces](/docs/en/discover-plugins#configure-team-marketplaces): set up repository-level plugins for your team

### [​](#for-plugin-developers) For plugin developers

* [Create and distribute a marketplace](/docs/en/plugin-marketplaces): package and share your plugins
* [Plugins reference](/docs/en/plugins-reference): complete technical specifications
* Dive deeper into specific plugin components:
  + [Skills](/docs/en/skills): skill development details
  + [Subagents](/docs/en/sub-agents): agent configuration and capabilities
  + [Hooks](/docs/en/hooks): event handling and automation
  + [MCP](/docs/en/mcp): external tool integration

Was this page helpful?

YesNo

[Discover and install prebuilt plugins](/docs/en/discover-plugins)[Share session output as artifacts](/docs/en/artifacts)

⌘I

---