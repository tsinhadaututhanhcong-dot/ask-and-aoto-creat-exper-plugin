---
type: Reference
title: Replace your-repo-file-index with your own file search command
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Replace your-repo-file-index with your own file search command
your-repo-file-index --query "$query" | head -20
```

### [​](#footer-link-badges) Footer link badges

The `footerLinksRegexes` setting renders extra clickable badges in the footer below the input box. Use it to turn IDs printed by project CLIs, such as review tools and issue trackers, into session links.
Each entry’s `pattern` regex is matched against turn output: tool results, including file contents and fetched pages, and Claude’s own responses. `{name}` placeholders in `url` and `label` are filled from named capture groups in the pattern.
The following example renders a badge whenever an issue key like `PROJ-1234` appears in turn output. The `(?<key>...)` named group captures the key, and `{key}` substitutes it into the URL and label:

~/.claude/settings.json

```
{
  "footerLinksRegexes": [
    {
      "type": "regex",
      "pattern": "\\b(?<key>PROJ-\\d+)\\b",
      "url": "https://issues.example.com/browse/{key}",
      "label": "{key}"
    }
  ]
}
```

With this configured, when `PROJ-1234` appears in a tool result or in Claude’s reply, a `PROJ-1234` badge appears in the footer linking to `https://issues.example.com/browse/PROJ-1234`.
The following constraints apply to each entry:

| Constraint | Behavior |
| --- | --- |
| URL origin | Captured values are URL-encoded and the constructed URL must share the template’s literal origin. A capture can fill a path segment or query value but cannot change where the link points |
| URL length | Constructed URLs longer than 2048 characters are dropped |
| URL scheme | Must be `https`, `http`, or a recognized editor or workspace deep-link scheme: `vscode`, `vscode-insiders`, `cursor`, `windsurf`, `zed`, `jetbrains`, `idea`, `slack`, `linear`, `notion`, `figma` |
| Label | Defaults to the matched text and is truncated to 28 display columns |
| Badge count | At most 5 badges render. The oldest is displaced by newer matches and `/clear` removes them |
| Settings scope | Read from user settings, the `--settings` flag, and managed settings only. Ignored in project `.claude/settings.json` and local `.claude/settings.local.json` |

When a turn completes, Claude Code matches each entry’s `pattern` regex against the turn output on the main thread, so a slow regex blocks the UI until it finishes. Nested quantifiers such as `(a+)+$` can take exponentially long against certain inputs and freeze the session, so keep each `pattern` linear and avoid nesting `+` or `*`.
Footer badges render alongside a [custom status line](/docs/en/statusline) when one is configured; neither replaces the other. Use a status line for a script-driven row that computes its own content from session data, and footer badges to turn IDs from the conversation into links without a script.

### [​](#hook-configuration) Hook configuration

These settings control which hooks are allowed to run and what HTTP hooks can access. The `allowManagedHooksOnly` setting can only be configured in [managed settings](#settings-files). The URL and env var allowlists can be set at any settings level and merge across sources.
**Behavior when `allowManagedHooksOnly` is `true`:**

* Managed hooks and SDK hooks are loaded
* Hooks from plugins force-enabled in managed settings `enabledPlugins` are loaded. This lets administrators distribute vetted hooks through an organization marketplace while blocking everything else. Trust is granted by full `plugin@marketplace` ID, so a plugin with the same name from a different marketplace stays blocked
* User hooks, project hooks, and all other plugin hooks are blocked

**Restrict HTTP hook URLs:**
Limit which URLs HTTP hooks can target. Supports `*` as a wildcard for matching. When the array is defined, HTTP hooks targeting non-matching URLs are silently blocked. Hostname matching is case-insensitive and ignores a trailing FQDN dot, matching DNS semantics.

```
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restrict HTTP hook environment variables:**
Limit which environment variable names HTTP hooks can interpolate into header values. Each hook’s effective `allowedEnvVars` is the intersection of its own list and this setting.

```
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### [​](#compute-managed-settings-with-a-policy-helper) Compute managed settings with a policy helper

The `policyHelper` setting points at an executable that computes managed settings at startup, so admins can derive policy from device posture, identity, or a remote service instead of a static file. Configure it from MDM or a system `managed-settings.json` file. Claude Code ignores `policyHelper` when it appears in any other scope, including user settings, project settings, the HKCU registry hive, and [server-managed settings](/docs/en/server-managed-settings).
The setting accepts these keys:

| Key | Type | Description |
| --- | --- | --- |
| `path` | string | Absolute path to the helper executable |
| `timeoutMs` | number | How long to wait for the helper before treating the run as failed |
| `refreshIntervalMs` | number | How often to re-run the helper in the background. Set to `0` to disable refresh, or to at least `60000` |

The helper writes a JSON envelope to stdout. Put the settings under a `managedSettings` key rather than at the top level, since a bare settings object parses with `managedSettings` undefined and applies nothing:

```
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  },
  "claudeMd": "# Organization context\n...",
  "appendSystemPrompt": "Always cite the internal style guide."
}
```

When the helper emits `managedSettings`, that object replaces the file-based managed settings for the run. When the helper exits non-zero at startup, Claude Code prints the error and refuses to start, so a helper that needs outage resilience should serve from its own cache and exit `0`.

### [​](#settings-precedence) Settings precedence

Settings apply in order of precedence. From highest to lowest:

1. **Managed settings** ([server-managed](/docs/en/server-managed-settings), [MDM/OS-level policies](#configuration-scopes), or [managed settings](/docs/en/settings#settings-files))
   * Policies deployed by IT through server delivery, MDM configuration profiles, registry policies, or managed settings files
   * Cannot be overridden by any other level, including command line arguments
   * Within the managed tier, precedence is: server-managed > MDM/OS-level policies > file-based (`managed-settings.d/*.json` + `managed-settings.json`) > HKCU registry (Windows only). Only one managed source is used; sources do not merge across tiers. Within the file-based tier, drop-in files and the base file are merged together.
   * Embedding hosts such as Claude Desktop can supply policy via the SDK `managedSettings` option. By default this is ignored when an admin-deployed managed source is present: server-managed settings, an MDM or OS-level policy, or a managed settings file. The user-writable HKCU registry fallback does not count as an admin-deployed source. Administrators can opt in by setting [`parentSettingsBehavior`](#available-settings) to `"merge"`. The embedder’s values are filtered so they can tighten managed policy but not loosen it.
2. **Command line arguments**
   * Temporary overrides for a specific session. JSON passed via `--settings <file-or-json>` merges with file-based settings using the same rules as the other layers: a key set here overrides the same key in local, project, or user settings, and omitting a key leaves the lower-layer value in place
3. **Local project settings** (`.claude/settings.local.json`)
   * Personal project-specific settings
4. **Shared project settings** (`.claude/settings.json`)
   * Team-shared project settings in source control
5. **User settings** (`~/.claude/settings.json`)
   * Personal global settings

This hierarchy ensures that organizational policies are always enforced while still allowing teams and individuals to customize their experience. The same precedence applies whether you run Claude Code from the CLI, the [VS Code extension](/docs/en/vs-code), or a [JetBrains IDE](/docs/en/jetbrains).
For example, if your user settings set `permissions.defaultMode` to `acceptEdits` and a project’s shared settings set it to `default`, the project value applies. The example below covers how array-valued settings such as permission rules combine instead.

**Array settings merge across scopes.** When the same array-valued setting (such as `sandbox.filesystem.allowWrite` or `permissions.allow`) appears in multiple scopes, the arrays are **concatenated and deduplicated**, not replaced. This means lower-priority scopes can add entries without overriding those set by higher-priority scopes, and vice versa. For example, if managed settings set `allowWrite` to `["/opt/company-tools"]` and a user adds `["~/.kube"]`, both paths are included in the final configuration.Two array settings do not merge this way:

* [`fallbackModel`](#available-settings) is an ordered chain where position carries meaning: the highest-precedence file that defines it supplies the entire value.
* [`availableModels`](#available-settings): when the [highest-precedence managed source](/docs/en/server-managed-settings#settings-precedence) defines it, that list applies as-is and user, project, and local entries cannot extend it. Across non-managed scopes the arrays merge as usual. See [Merge behavior](/docs/en/model-config#merge-behavior).

### [​](#verify-active-settings) Verify active settings

Run `/status` inside Claude Code to see which settings sources are active. Inside the menu, the **Status** tab includes a `Setting sources` line that lists each layer Claude Code loaded for the current session, such as `User settings` or `Project local settings`. When [managed settings](/docs/en/admin-setup#decide-how-settings-reach-devices) are in effect, the entry shows the delivery channel in parentheses, for example `Enterprise managed settings (remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, or `(file)`. A layer appears in the list only when that source is loaded with at least one key, so an empty list means no settings sources were found.
The `Setting sources` line confirms which sources are being read. It does not show which layer supplied each individual key. The **Config** tab in the same dialog is an editor for a fixed set of toggles such as theme and verbose output, not a view of your `settings.json` contents.
If a settings file contains errors, such as invalid JSON or a value that fails validation, `/status` lists the affected files. Run `/doctor` to see the details for each error.

### [​](#key-points-about-the-configuration-system) Key points about the configuration system

* **Memory files (`CLAUDE.md`)**: Contain instructions and context that Claude loads at startup
* **Settings files (JSON)**: Configure permissions, environment variables, and tool behavior
* **Skills**: Custom prompts that can be invoked with `/skill-name` or loaded by Claude automatically
* **MCP servers**: Extend Claude Code with additional tools and integrations
* **Precedence**: Higher-level configurations (Managed) override lower-level ones (User/Project)
* **Inheritance**: Settings merge across scopes; scalar values from higher-priority scopes override, and arrays concatenate, with two exceptions described in the [array-merge Note](#settings-precedence)

### [​](#system-prompt) System prompt

Claude Code’s internal system prompt is not published. To add custom instructions, use `CLAUDE.md` files or the `--append-system-prompt` flag.

### [​](#exclude-sensitive-files) Exclude sensitive files

To prevent Claude Code from accessing files containing sensitive information like API keys, secrets, and environment files, use the `permissions.deny` setting in your `.claude/settings.json` file:

```
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

This replaces the deprecated `ignorePatterns` configuration. Files matching these patterns are excluded from file discovery and search results, and read operations on these files are denied.

## [​](#subagent-configuration) Subagent configuration

Claude Code supports custom AI subagents that can be configured at both user and project levels. These subagents are stored as Markdown files with YAML frontmatter:

* **User subagents**: `~/.claude/agents/`, available across all your projects
* **Project subagents**: `.claude/agents/`, specific to your project and shareable with your team

Subagent files define specialized AI assistants with custom prompts and tool permissions. Learn more about creating and using subagents in the [subagents documentation](/docs/en/sub-agents).

## [​](#plugin-configuration) Plugin configuration

Claude Code supports a plugin system that lets you extend functionality with skills, agents, hooks, and MCP servers. Plugins are distributed through marketplaces and can be configured at both user and repository levels.

### [​](#plugin-settings) Plugin settings

Plugin-related settings in `settings.json`:

```
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  }
}
```

#### [​](#enabledplugins) `enabledPlugins`

Controls which plugins are enabled. Format: `"plugin-name@marketplace-name": true/false`. A plugin with no entry at any scope falls back to its [`defaultEnabled`](/docs/en/plugins-reference#default-enablement) value.
**Scopes**:

* **User settings** (`~/.claude/settings.json`): Personal plugin preferences
* **Project settings** (`.claude/settings.json`): Project-specific plugins shared with team
* **Local settings** (`.claude/settings.local.json`): Per-machine overrides, gitignored when Claude Code creates it
* **Managed settings** (`managed-settings.json`): Organization-wide policy overrides that block installation at all scopes and hide the plugin from the marketplace

Project settings take precedence over user settings, so setting a plugin to `false` in `~/.claude/settings.json` does not disable a plugin that the project’s `.claude/settings.json` enables. To opt out of a project-enabled plugin on your machine, set it to `false` in `.claude/settings.local.json` instead.Plugins force-enabled by managed settings cannot be disabled this way, since managed settings override local settings.

**Example**:

```
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### [​](#extraknownmarketplaces) `extraKnownMarketplaces`

Defines additional marketplaces that should be made available for the repository. Typically used in repository-level settings to ensure team members have access to required plugin sources.
**When a repository includes `extraKnownMarketplaces`**:

1. Team members are prompted to install the marketplace when they trust the folder
2. Team members are then prompted to install plugins from that marketplace
3. Users can skip unwanted marketplaces or plugins (stored in user settings)
4. Installation respects trust boundaries and requires explicit consent

**Example**:

```
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Marketplace source types**:

* `github`: GitHub repository (uses `repo`)
* `git`: Any git URL (uses `url`)
* `directory`: Local filesystem path (uses `path`, for development only)
* `hostPattern`: regex pattern to match marketplace hosts (uses `hostPattern`)
* `settings`: inline marketplace declared directly in settings.json without a separate hosted repository (uses `name` and `plugins`)

The `git` source type works with any git hosting service, including self-hosted GitLab and Bitbucket. Claude Code clones the repository with the same authentication that `git clone` would use on that machine: configured credential helpers, SSH keys, or a host-specific token environment variable. See [Private repositories](/docs/en/plugin-marketplaces#private-repositories) for setup details.
For `github` and `git` sources, set `"skipLfs": true` inside the `source` object (alongside `repo` or `url`) to skip Git LFS downloads when Claude Code clones or updates the marketplace repository. LFS pointer files remain as pointers instead of downloading their content. Use this when the repository contains large LFS objects unrelated to plugin content. Requires Claude Code v2.1.153 or later.
Each marketplace entry also accepts an optional `autoUpdate` Boolean. Set `"autoUpdate": true` alongside `source` to make Claude Code refresh that marketplace and update its installed plugins at startup. When omitted, official Anthropic marketplaces default to `true` and all other marketplaces default to `false`. See [Configure auto-updates](/docs/en/discover-plugins#configure-auto-updates).
Use `source: 'settings'` to declare a small set of plugins inline without setting up a hosted marketplace repository. Plugins listed here must reference external sources such as GitHub or npm. You still need to enable each plugin separately in `enabledPlugins`.

```
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### [​](#strictknownmarketplaces) `strictKnownMarketplaces`

**Managed settings only**: Controls which plugin marketplaces users are allowed to add and install plugins from. This setting can only be configured in [managed settings](/docs/en/settings#settings-files) and provides administrators with strict control over marketplace sources.
**Managed settings file locations**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux and WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Key characteristics**:

* Only available in managed settings (`managed-settings.json`)
* Cannot be overridden by user or project settings (highest precedence)
* Enforced before network and filesystem operations, so blocked sources never run
* Uses exact matching for source specifications (including `ref`, `path` for git sources), except `hostPattern` and `pathPattern`, which use regex matching

**Allowlist behavior**:

* `undefined` (default): no restrictions, so users can add any marketplace
* Empty array `[]`: complete lockdown, so users can’t add any new marketplaces
* List of sources: users can only add marketplaces that match exactly

**All supported source types**:
The allowlist supports multiple marketplace source types. Most sources use exact matching, while `hostPattern` and `pathPattern` use regex matching against the marketplace host and filesystem path respectively.

1. **GitHub repositories**:

```
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Fields: `repo` (required), `ref` (optional: branch/tag/SHA), `path` (optional: subdirectory)

2. **Git repositories**:

```
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Fields: `url` (required), `ref` (optional: branch/tag/SHA), `path` (optional: subdirectory)

3. **URL-based marketplaces**:

```
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Fields: `url` (required), `headers` (optional: HTTP headers for authenticated access)

URL-based marketplaces only download the `marketplace.json` file. They do not download plugin files from the server. Plugins in URL-based marketplaces must use external sources (GitHub, npm, or git URLs) rather than relative paths. For plugins with relative paths, use a Git-based marketplace instead. See [Troubleshooting](/docs/en/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) for details.

4. **NPM packages**:

```
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Fields: `package` (required, supports scoped packages)

5. **File paths**:

```
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Fields: `path` (required: absolute path to marketplace.json file)

6. **Directory paths**:

```
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Fields: `path` (required: absolute path to directory containing `.claude-plugin/marketplace.json`)

7. **Host pattern matching**:

```
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Fields: `hostPattern` (required: regex pattern to match against the marketplace host)
Use host pattern matching when you want to allow all marketplaces from a specific host without enumerating each repository individually. This is useful for organizations with internal GitHub Enterprise or GitLab servers where developers create their own marketplaces.
Host extraction by source type:

* `github`: always matches against `github.com`
* `git`: extracts hostname from the URL (supports both HTTPS and SSH formats)
* `url`: extracts hostname from the URL
* `npm`, `file`, `directory`: not supported for host pattern matching

8. **Path pattern matching**:

```
{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }
{ "source": "pathPattern", "pathPattern": ".*" }
```

Fields: `pathPattern` (required: regex pattern matched against the `path` field of `file` and `directory` sources)
Use path pattern matching to allow filesystem-based marketplaces alongside `hostPattern` restrictions for network sources. Set `".*"` to allow all local paths, or a narrower pattern to restrict to specific directories.
**Configuration examples**:
Example: allow specific marketplaces only:

```
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Example: disable all marketplace additions:

```
{
  "strictKnownMarketplaces": []
}
```

Example: allow all marketplaces from an internal git server:

```
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Exact matching requirements**:
Marketplace sources must match exactly for a user’s addition to be allowed. For git-based sources (`github` and `git`), this includes all optional fields:

* The `repo` or `url` must match exactly
* The `ref` field must match exactly (or both be undefined)
* The `path` field must match exactly (or both be undefined)

Examples of sources that don’t match:

```
// These are DIFFERENT sources:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// These are also DIFFERENT:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparison with `extraKnownMarketplaces`**:

| Aspect | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| --- | --- | --- |
| **Purpose** | Organizational policy enforcement | Team convenience |
| **Settings file** | `managed-settings.json` only | Any settings file |
| **Behavior** | Blocks non-allowlisted additions | Auto-installs missing marketplaces |
| **When enforced** | Before network/filesystem operations | After user trust prompt |
| **Can be overridden** | No (highest precedence) | Yes (by higher precedence settings) |
| **Source format** | Direct source object | Named marketplace with nested source |
| **Use case** | Compliance, security restrictions | Onboarding, standardization |

**Format difference**:
`strictKnownMarketplaces` uses direct source objects:

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` requires named marketplaces:

```
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Using both together**:
`strictKnownMarketplaces` is a policy gate: it controls what users may add but does not register any marketplaces. To both restrict and pre-register a marketplace for all users, set both in `managed-settings.json`:

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

With only `strictKnownMarketplaces` set, users can still add the allowed marketplace manually via `/plugin marketplace add`, but it is not available automatically.
**Important notes**:

* Restrictions are checked before any network requests or filesystem operations
* When blocked, users see clear error messages indicating the source is blocked by managed policy
* The restriction is enforced on marketplace add and on plugin install, update, refresh, and auto-update. A marketplace added before the policy was set cannot be used to install or update plugins once its source no longer matches the allowlist
* Managed settings have the highest precedence and cannot be overridden

See [Managed marketplace restrictions](/docs/en/plugin-marketplaces#managed-marketplace-restrictions) for user-facing documentation.

#### [​](#strictpluginonlycustomization) `strictPluginOnlyCustomization`

**Managed settings only**: blocks skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings. Combine it with `strictKnownMarketplaces` to control the full customization supply chain: the marketplace allowlist controls which plugins users can install, and this setting blocks everything that doesn’t come from a plugin or from managed settings.

`strictPluginOnlyCustomization` requires Claude Code v2.1.82 or later. Earlier versions ignore the key and keep loading user and project customizations, so the lockdown isn’t enforced until clients update.

The value is either `true` to lock all four surfaces, or an array naming the surfaces to lock:

```
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
```

For each locked surface, Claude Code skips user-level and project-level sources and loads only plugin-provided and managed sources:

| Surface | Blocked when locked | Still loads |
| --- | --- | --- |
| `skills` | `~/.claude/skills/`, `.claude/skills/` | Plugin skills, bundled skills, skills in the managed policy directory |
| `agents` | `~/.claude/agents/`, `.claude/agents/` | Plugin agents, built-in agents, agents in the managed policy directory |
| `hooks` | Hooks in user, project, and local `settings.json` | Plugin hooks, hooks in managed settings |
| `mcp` | Servers in `~/.claude.json` and `.mcp.json` | Plugin MCP servers, [`managed-mcp.json`](/docs/en/managed-mcp) servers |

Surface names that a Claude Code version doesn’t recognize are ignored rather than failing the settings file, so you can add new surface names before all clients have updated.

### [​](#manage-plugins) Manage plugins

Use the `/plugin` command to manage plugins interactively:

* Browse available plugins from marketplaces
* Install/uninstall plugins
* Enable/disable plugins
* View plugin details (skills, agents, hooks provided)
* Add/remove marketplaces

Learn more about the plugin system in the [plugins documentation](/docs/en/plugins).

## [​](#environment-variables) Environment variables

Environment variables let you control Claude Code behavior without editing settings files. Any variable can also be configured in [`settings.json`](#available-settings) under the `env` key to apply it to every session or roll it out to your team.
See the [environment variables reference](/docs/en/env-vars) for the full list.

## [​](#tools-available-to-claude) Tools available to Claude

Claude Code has access to a set of tools for reading, editing, searching, running commands, and orchestrating subagents. Tool names are the exact strings you use in permission rules and hook matchers.
See the [tools reference](/docs/en/tools-reference) for the full list and Bash tool behavior details.

## [​](#see-also) See also

* [Permissions](/docs/en/permissions): permission system, rule syntax, tool-specific patterns, and managed policies
* [Authentication](/docs/en/authentication): set up user access to Claude Code
* [Debug your configuration](/docs/en/debug-your-config): diagnose why a setting, hook, or MCP server isn’t taking effect
* [Troubleshoot installation and login](/docs/en/troubleshoot-install): installation, authentication, and platform issues

Was this page helpful?

YesNo

[Permissions](/docs/en/permissions)

⌘I

---