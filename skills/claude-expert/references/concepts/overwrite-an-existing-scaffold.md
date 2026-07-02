---
title: Overwrite an existing scaffold
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Overwrite an existing scaffold
claude plugin init my-helper --force
```

### [​](#plugin-install) plugin install

Install a plugin from available marketplaces.

```
claude plugin install <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name` for a specific marketplace

**Options:**

| Option | Description | Default |
| --- | --- | --- |
| `-s, --scope <scope>` | Installation scope: `user`, `project`, or `local` | `user` |
| `-h, --help` | Display help for command |  |

Scope determines which settings file the installed plugin is added to. For example, `--scope project` writes to `enabledPlugins` in .claude/settings.json, making the plugin available to everyone who clones the project repository.
**Examples:**

```