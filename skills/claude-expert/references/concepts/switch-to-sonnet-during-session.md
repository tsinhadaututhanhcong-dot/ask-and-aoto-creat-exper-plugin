---
type: Reference
title: Switch to Sonnet during session
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Switch to Sonnet during session
/model sonnet
```

Example settings file:

```
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## [​](#restrict-model-selection) Restrict model selection

Enterprise administrators can use `availableModels` in [managed or policy settings](/docs/en/settings#settings-files) to restrict which models users can select. Entries match a model family such as `sonnet`, a version prefix such as `claude-sonnet-4-5`, or a full model ID such as `claude-sonnet-4-5-20250929`.
When `availableModels` is set, the allowlist applies everywhere a user can specify a model:

* **Main session model**: `/model`, the `--model` flag, the `ANTHROPIC_MODEL` environment variable, the `model` setting, and the model restored when [resuming a session](#setting-your-model)
* **Alias resolution**: the `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, and `ANTHROPIC_DEFAULT_FABLE_MODEL` environment variables cannot redirect an allowed alias to a model outside the list
* **Fast mode**: `/fast` refuses to toggle when it would implicitly switch to an Opus model outside the list, with the message “is not in your organization’s allowed models”
* **Subagent models**: the `model` field in [subagent](/docs/en/sub-agents#choose-a-model) frontmatter, the Agent tool’s `model` parameter, the model picker in `/agents`, and `CLAUDE_CODE_SUBAGENT_MODEL`
* **Skill and command models**: the `model` frontmatter in [skills and commands](/docs/en/skills)
* **Advisor model**: the configured [`advisorModel`](/docs/en/advisor) setting and the `--advisor` flag
* **Background agent model**: the model selected in the [dispatch picker](/docs/en/agent-view)

Switching to a blocked model with `/model` is rejected with an error, while a blocked `--model` flag, `ANTHROPIC_MODEL`, or `model` setting value is replaced at startup with a warning naming both the requested and substituted models, and the session starts on the default model. A blocked subagent, skill, or command override falls back to the inherited or default model rather than failing the request; a blocked `advisorModel` setting disables the advisor for the session, while a blocked `--advisor` flag value exits with an error at launch. Excluded models are hidden from the `/model` picker.
Automatic model changes are checked the same way: elements of a [fallback model chain](#fallback-model-chains) outside the allowlist are dropped, a plan-mode upgrade such as [`opusplan`](#opusplan-model-setting) to an excluded model is skipped so planning continues on the session’s model, and an [automatic model fallback](#automatic-model-fallback) whose target is excluded does not run, so the flagged request ends with a refusal instead. Enabling [fast mode](/docs/en/fast-mode) is refused when the model the session would run on afterward is outside the allowlist.

```
{
  "availableModels": ["sonnet", "haiku"]
}
```

### [​](#surface-coverage) Surface coverage

Every surface enforces the allowlist it receives. Which delivery mechanism reaches each surface differs:

| Delivery mechanism | CLI and IDE | Desktop local sessions | Web, mobile, and cloud sessions | Agent SDK and non-interactive | Cowork |
| --- | --- | --- | --- | --- | --- |
| [Server-managed settings](/docs/en/server-managed-settings) from the admin console | Enforced | Enforced | Enforced | Enforced | Not delivered |
| [MDM or managed settings files](/docs/en/settings#settings-files) | Enforced | Enforced | Not delivered | Enforced | Enforced where deployed |

* Cloud sessions, on [Claude Code on the web](/docs/en/claude-code-on-the-web) or in the Desktop app, run on Anthropic-managed VMs: settings deployed to your device do not reach them, so deliver the allowlist through server-managed settings. A mid-session model switch in a cloud session is rejected when the requested model is excluded by the allowlist. Server-side rejection at session creation applies to [organization model restrictions](#organization-model-restrictions), not the `availableModels` settings key.
* Cowork, the agentic-work tab in the Claude Desktop app, is not a Claude Code surface and does not receive server-managed settings by design. A managed settings file applies to Cowork sessions when it is present where the session runs; remote Cowork sessions run on Anthropic-managed VMs, where a device-deployed file is not present.
* Sessions on [third-party providers](/docs/en/server-managed-settings#platform-availability) such as Bedrock, Vertex AI, Foundry, and [Claude Platform on AWS](/docs/en/claude-platform-on-aws) do not receive server-managed settings, so deliver the allowlist through MDM or managed settings files there.
* Server-managed delivery also requires the session to authenticate with an organization login or a directly configured API key. Fleets that generate keys only through an [`apiKeyHelper`](/docs/en/settings#available-settings) script should deliver the allowlist through MDM or managed settings files.
* The Desktop Code tab also hosts [SSH sessions](/docs/en/desktop#ssh-sessions), which read the managed settings file from the remote host they run on. See [Desktop managed settings](/docs/en/desktop#managed-settings).
* The model pickers on claude.ai and in the Desktop app hide or grey out models excluded by your organization’s allowlist. The picker state is a convenience for users; enforcement happens in the session.

### [​](#default-model-behavior) Default model behavior

The Default option in the model picker is not affected by `availableModels` unless [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) is also set. On its own, `availableModels` leaves Default available, resolving to the system’s runtime default [based on the user’s subscription tier](#default-model-setting). If the tier default is a model you intend to restrict, set `enforceAvailableModels` as well.
An empty `availableModels` array never engages the Default-model enforcement: with `availableModels: []`, named model selections are blocked but the Default model for the account type remains usable regardless of `enforceAvailableModels`.

### [​](#enforce-the-allowlist-for-the-default-model) Enforce the allowlist for the Default model

Set `enforceAvailableModels: true` alongside a non-empty `availableModels` in managed settings to extend the allowlist to the Default option. This requires Claude Code v2.1.175 or later.

```
{
  "availableModels": ["sonnet", "haiku"],
  "enforceAvailableModels": true
}
```

When the default model for the user’s account type is not in the allowlist, the Default option instead resolves to the first `availableModels` entry that names an allowed, available model, and the `/model` picker’s Default row shows that model. This applies everywhere the default is reached: session startup, selecting Default in `/model`, the `"default"` keyword in [fallback model chains](#fallback-model-chains), and the fallback used when an excluded selection is dropped.
`enforceAvailableModels` has no effect when `availableModels` is unset or empty: with `availableModels: []`, the Default model for the account type remains usable, so the setting cannot lock users out of every model. When `availableModels` is non-empty but no entry resolves to an allowed and available model, enforcement is skipped and Default resolves to the account-type default, with a warning visible only under `--debug`. Keep at least one guaranteed-available entry in the list to avoid this.
Deploy both keys in the [highest-precedence managed source](/docs/en/settings#settings-precedence): admin-deployed managed sources do not merge, so a pair placed in a managed settings file is ignored when the admin console delivers any settings.

### [​](#control-the-model-users-run-on) Control the model users run on

The `model` setting is an initial selection, not enforcement. It sets which model is active when a session starts, but users can still open `/model` and pick Default, which resolves to the system default for their tier regardless of what `model` is set to, unless [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) redirects it.
To fully control the model experience, combine these settings:

* **`availableModels`**: restricts which named models users can switch to
* **`enforceAvailableModels`**: extends the `availableModels` allowlist to the Default option, so Default cannot resolve to a model outside the list
* **`model`**: sets the initial model selection when a session starts
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`** / **`ANTHROPIC_DEFAULT_FABLE_MODEL`**: control what the Default option and the `sonnet`, `opus`, `haiku`, and `fable` aliases resolve to

This example starts users on Sonnet 4.5, limits the picker to Sonnet and Haiku, and ensures Default resolves to a model on the allowlist rather than the tier default:

```
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "enforceAvailableModels": true,
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Without `enforceAvailableModels` or the `env` block, a user who selects Default in the picker would get the latest release for their tier, bypassing the version pin in `model` and `availableModels`. The two settings cover different scopes: `enforceAvailableModels` makes Default obey the allowlist, while the `env` block pins which version a permitted alias such as `sonnet` resolves to. Use `enforceAvailableModels` alone when restricting model families is enough; add the `env` block when you also need to pin a specific version.

### [​](#merge-behavior) Merge behavior

When the [highest-precedence managed settings source](/docs/en/server-managed-settings#settings-precedence) defines `availableModels`, that list alone applies: entries in user, project, or local settings cannot extend it, and admin-deployed managed sources do not merge with each other, so a list deployed in a managed settings file is ignored when server-managed settings deliver any keys. Otherwise, lists from user, project, and local settings are [concatenated and deduplicated](/docs/en/settings#settings-precedence) like other array settings. As of Claude Code v2.1.175, the managed list replaces lower-precedence entries; earlier versions merge them.
Within the effective list, an entry naming a specific model in a family, whether a version prefix or a full model ID, disables that family’s wildcard entry: `["sonnet", "claude-sonnet-4-5"]` allows only Sonnet 4.5 versions, not every Sonnet model.

### [​](#mantle-model-ids) Mantle model IDs

When the [Bedrock Mantle endpoint](/docs/en/amazon-bedrock#use-the-mantle-endpoint) is enabled, entries in `availableModels` that start with `anthropic.` are added to the `/model` picker as custom options and routed to the Mantle endpoint. This is an exception to the alias matching described in [Pin models for third-party deployments](#pin-models-for-third-party-deployments). The setting still restricts the picker to listed entries, and a Mantle ID embeds a family name, so it counts as a specific entry and disables that family’s wildcard: alongside any Mantle IDs, list the version prefixes or full IDs you want to keep selectable. See [Merge behavior](#merge-behavior).

### [​](#organization-model-restrictions) Organization model restrictions

Organization admins restrict which models members can run by disabling individual models in the Claude Console. Use this Console toggle instead of `availableModels` when your members authenticate through the Anthropic API and you want one org-wide switch without deploying settings files. This restriction is delivered with the account’s entitlements when Claude Code authenticates, separate from any `availableModels` list in settings, and the server enforces the same restriction independently when a session is created. Requires Claude Code v2.1.187 or later.
A restricted model is hidden from the `/model` picker. Selecting it by name with `--model`, the `ANTHROPIC_MODEL` environment variable, or the `model` setting shows the notice `Model "<name>" is restricted by your organization's settings. Using <model> instead.` and the session starts on an allowed model. Typing `/model <name>` for a restricted model is rejected with `Model '<name>' is restricted by your organization's settings. Run /model to choose a different model.` and the session keeps its current model.
Both restrictions apply together: a model is selectable only when it is permitted by `availableModels` and not restricted by the organization. Organization restrictions are delivered to sessions on the Anthropic API and [LLM gateway](/docs/en/llm-gateway) deployments. Sessions on Bedrock, Vertex AI, Foundry, and Claude Platform on AWS do not receive them, so use `availableModels` on those providers instead.

## [​](#special-model-behavior) Special model behavior

### [​](#default-model-setting) `default` model setting

The behavior of `default` depends on your account type:

* **Max, Team Premium, Enterprise pay-as-you-go, and Anthropic API**: defaults to Opus 4.8
* **Claude Platform on AWS**: defaults to Opus 4.7
* **Pro, Team Standard, and Enterprise subscription seats**: defaults to Sonnet 4.6
* **Bedrock, Vertex, and Foundry**: defaults to Sonnet 4.5

Enterprise pay-as-you-go means an Enterprise organization billed by usage rather than by subscription seat.
When managed settings [enforce the allowlist for the Default model](#enforce-the-allowlist-for-the-default-model) and the account-type default is not in `availableModels`, `default` resolves to the enforced Default instead of the account-type default above.
Fable 5 is not the default model on any account type. Sessions use Fable 5 only after you choose it, with `/model fable`, a `model` setting, or the `best` alias where Fable 5 is available. Choosing it with `/model` saves it as the selected model in your user settings, so later sessions start on Fable 5 until you change models.

### [​](#opusplan-model-setting) `opusplan` model setting

The `opusplan` model alias provides an automated hybrid approach:

* **In plan mode**: uses `opus` for complex reasoning and architecture decisions
* **In execution mode**: automatically switches to `sonnet` for code generation and implementation

This pairs Opus’s reasoning for planning with Sonnet’s efficiency for execution.
The plan-mode Opus phase uses the same context window as the `opus` model setting. On subscription tiers where Opus is [automatically upgraded to 1M context](#extended-context), `opusplan` receives the upgrade in plan mode as well. To force 1M context for both phases when you are not on an auto-upgrade tier, set the model to `opusplan[1m]`.
When [`availableModels`](#restrict-model-selection) excludes Opus, `opusplan` stays on Sonnet in plan mode instead of switching. Similarly, a Haiku session that would normally upgrade to Sonnet in plan mode stays on Haiku when Sonnet is excluded.
For a hybrid approach where Claude decides mid-task when to consult a second model rather than switching at the plan boundary, see the [advisor tool](/docs/en/advisor).

### [​](#fallback-model-chains) Fallback model chains

When the primary model is overloaded, unavailable, or returns another non-retryable server error, Claude Code can switch to a fallback model instead of failing the request. Authentication, billing, rate-limit, request-size, and transport errors never trigger a switch; those follow their normal retry and error handling.
Configure one or more fallback models and Claude Code tries them in order, showing a notice when it switches. The switch lasts for the current turn only, so your next message tries the primary model first again. Chains are capped at three models after duplicate removal, and extra entries are ignored.
Set a chain for one session with the `--fallback-model` flag, which accepts a comma-separated list:

```
claude --fallback-model sonnet,haiku
```

To persist a chain across sessions, set `fallbackModel` in [settings](/docs/en/settings) as an array:

```
{
  "fallbackModel": ["claude-sonnet-4-6", "claude-haiku-4-5"]
}
```

The `--fallback-model` flag takes precedence over the `fallbackModel` setting. Each element accepts a model name or alias, and `"default"` expands to the default model.
Two cases cause an element to be skipped:

* **Unavailable model**: a model that can’t be reached, such as a retired model pinned in settings, is skipped and Claude Code continues to the next element.
* **Outside the allowlist**: an element not permitted by [`availableModels`](#restrict-model-selection) is dropped when the chain is read and never tried.

### [​](#automatic-model-fallback) Automatic model fallback

This section covers content-based fallback from Fable 5. For availability-based fallback when a model is overloaded or unavailable, see [Fallback model chains](#fallback-model-chains).
Fable 5 runs with safety classifiers for cybersecurity and biology content. When a classifier flags a request, Claude Code re-runs that request on the default Opus model and shows a notice in the transcript: Opus 4.8 on the Anthropic API and [LLM gateway](/docs/en/llm-gateway) deployments, or Opus 4.7 on [Claude Platform on AWS](/docs/en/claude-platform-on-aws).
The session then continues on that Opus model. To return to Fable 5, run `/model fable`.
The fallback target is checked against [`availableModels`](#restrict-model-selection). When it is blocked, no fallback occurs. The refusal is shown as a normal error and the session’s model is unchanged.

#### [​](#check-what-triggered-fallback) Check what triggered fallback

Fallback can trigger on the first request of a session, before you send anything unusual, because the first request carries workspace context such as your CLAUDE.md content and git status. A repository that contains security or biology material can trip the classifier on that context alone.
To check whether customizations are the trigger, start a session with `claude --safe-mode`, which disables customizations such as CLAUDE.md, skills, MCP servers, and hooks. Git status and directory names are not customizations and are still included.

#### [​](#ask-before-switching) Ask before switching

To decide what happens each time a request is flagged, rather than switching automatically, run `/config` and turn off “switch models when a message is flagged”. A flagged request then pauses the session with two options: switch to the Opus model, or edit the prompt and retry on Fable 5.
Some cases behave differently:

* If both models flag the same request, you can edit the prompt and retry, or start a new session.
* On mobile [Claude Code on the web](/docs/en/claude-code-on-the-web) sessions, editing and retrying is not supported. Switch models, or continue the session from a desktop browser or the desktop app.
* In [non-interactive mode](/docs/en/cli-reference#cli-flags) and SDK integrations that can’t show the prompt, a flagged request ends the turn with a refusal instead.
* When the fallback target is blocked by [`availableModels`](#restrict-model-selection), the prompt is not shown. The flagged request ends with the refusal, the same as automatic fallback when the target is blocked.

#### [​](#enable-fallback-on-bedrock-vertex-ai-and-foundry) Enable fallback on Bedrock, Vertex AI, and Foundry

On [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Vertex AI](/docs/en/google-vertex-ai), and [Microsoft Foundry](/docs/en/microsoft-foundry), model IDs are provider-specific, so automatic fallback only operates when Claude Code can identify both models involved:

* Claude Code must recognize the current model as Fable 5: the model ID contains `claude-fable-5`, matches the value of `ANTHROPIC_DEFAULT_FABLE_MODEL`, or is mapped with [`modelOverrides`](#override-model-ids-per-version).
* The fallback target must resolve to an Opus model: the value of `ANTHROPIC_DEFAULT_OPUS_MODEL` if set, otherwise an Opus 4.8 entry in the provider’s model list.

If either model can’t be identified, Claude Code does not switch automatically. The flagged request ends with a refusal message, and you can switch models with [`/model`](#setting-your-model) and retry. To enable automatic fallback on these providers, set `ANTHROPIC_DEFAULT_FABLE_MODEL` to your Fable 5 model ID and `ANTHROPIC_DEFAULT_OPUS_MODEL` to your Opus 4.8 model ID.

#### [​](#security-research-and-biology-workloads) Security research and biology workloads

Workloads in offensive security or biology, including penetration testing, Capture the Flag (CTF) exercises, and biology-adjacent codebases, trigger fallback frequently, often on the first request. For substantive biology work, expect nearly all requests to reroute.
This is expected routing for these domains, not an account flag. If your organization needs Fable-class capability for this work, ask your Anthropic account team about trusted access programs.

### [​](#adjust-effort-level) Adjust effort level

[Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort) control adaptive reasoning, which lets the model decide whether and how much to think on each step based on task complexity. Lower effort is faster and cheaper for straightforward tasks, while higher effort provides deeper reasoning for complex problems.
The available effort levels depend on the model. Models not listed here do not support effort:

| Model | Levels |
| --- | --- |
| Fable 5 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.8 and Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 and Sonnet 4.6 | `low`, `medium`, `high`, `max` |

If you set a level the active model does not support, Claude Code falls back to the highest supported level at or below the one you set. For example, `xhigh` runs as `high` on Opus 4.6.
The default effort is `high` on Fable 5, Opus 4.8, Opus 4.6, and Sonnet 4.6, and `xhigh` on Opus 4.7.
When you first run Fable 5, Opus 4.8, or Opus 4.7, Claude Code applies that model’s default effort even if you previously set a different level for another model: `high` on Fable 5 and Opus 4.8, and `xhigh` on Opus 4.7. Run `/effort` again to choose a different level after switching.
`low`, `medium`, `high`, and `xhigh` persist across sessions. `max` provides the deepest reasoning with no constraint on token spending and applies to the current session only, except when set through the `CLAUDE_CODE_EFFORT_LEVEL` environment variable.
The `/effort` menu also offers `ultracode`. Ultracode is a Claude Code setting rather than a model effort level: it sends `xhigh` to the model and additionally has Claude orchestrate [dynamic workflows](/docs/en/workflows) for substantive tasks. It applies to the current session only. Set it through `/effort`, or pass `"ultracode": true` via `--settings` or an Agent SDK control request. It is not part of the `effortLevel` setting, the `--effort` flag, or `CLAUDE_CODE_EFFORT_LEVEL`.

#### [​](#choose-an-effort-level) Choose an effort level

Each level trades token spend against capability. The default suits most coding tasks; adjust when you want a different balance.

| Level | When to use it |
| --- | --- |
| `low` | Reserve for short, scoped, latency-sensitive tasks that are not intelligence-sensitive |
| `medium` | Reduces token usage for cost-sensitive work that can trade off some intelligence |
| `high` | Balances token usage and intelligence. Default on Fable 5, Opus 4.8, Opus 4.6, and Sonnet 4.6 |
| `xhigh` | Deeper reasoning at higher token spend. Default on Opus 4.7 |
| `max` | Can improve performance on demanding tasks but may show diminishing returns and is prone to overthinking. Test before adopting broadly |
| `ultracode` | A Claude Code setting that plans a [dynamic workflow](/docs/en/workflows) for each substantive task with `xhigh` per-message reasoning. Session-only |

The effort scale is calibrated per model, so the same level name does not represent the same underlying value across models.

#### [​](#use-ultrathink-for-one-off-deep-reasoning) Use ultrathink for one-off deep reasoning

Include `ultrathink` anywhere in your prompt to request deeper reasoning on that turn without changing your session effort setting. Claude Code recognizes the keyword and adds an in-context instruction. The effort level sent to the API is unchanged. Other phrases such as “think”, “think hard”, and “think more” are passed through as ordinary prompt text and are not recognized as keywords.

#### [​](#set-the-effort-level) Set the effort level

You can change effort through any of the following:

* **`/effort`**: run `/effort` with no arguments to open an interactive slider, `/effort` followed by a level name to set it directly, or `/effort auto` to reset to the model default
* **In `/model`**: use left/right arrow keys to adjust the effort slider when selecting a model
* **`--effort` flag**: pass a level name to set it for a single session when launching Claude Code
* **Environment variable**: set `CLAUDE_CODE_EFFORT_LEVEL` to a level name or `auto`
* **Settings**: set `effortLevel` to `low`, `medium`, `high`, or `xhigh` in your settings file. `max` and `ultracode` are [session-only](#adjust-effort-level) and are not accepted here
* **Skill and subagent frontmatter**: set `effort` in a [skill](/docs/en/skills#frontmatter-reference) or [subagent](/docs/en/sub-agents#supported-frontmatter-fields) markdown file to override the effort level when that skill or subagent runs

The environment variable takes precedence over all other methods, then your configured level, then the model default. Frontmatter effort applies when that skill or subagent is active, overriding the session level but not the environment variable.
The effort slider appears in `/model` when a supported model is selected. The current effort level is also displayed next to the logo and spinner, for example “with low effort”, so you can confirm which setting is active without opening `/model`.

#### [​](#adaptive-reasoning-and-fixed-thinking-budgets) Adaptive reasoning and fixed thinking budgets

Adaptive reasoning makes thinking optional on each step, so Claude can respond faster to routine prompts and reserve deeper thinking for steps that benefit from it. If you want Claude to think more or less often than the current level produces, you can say so directly in your prompt or in `CLAUDE.md`; the model responds to that guidance within its effort setting.
Opus 4.7 and later always use adaptive reasoning, as does Fable 5. The fixed thinking budget mode and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` do not apply to them.
On Opus 4.6 and Sonnet 4.6, you can set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`. See [environment variables](/docs/en/env-vars).

### [​](#extended-thinking) Extended thinking

Extended thinking is the reasoning Claude emits before responding. On models that support [adaptive reasoning](#adjust-effort-level), the effort level is the primary control for how much thinking happens; the settings below turn thinking on or off and control how it displays.

| Control | How to set it |
| --- | --- |
| Toggle for the current session | Press `Option+T` on macOS or `Alt+T` on Windows and Linux |
| Set the global default | Run `/config` and toggle thinking mode. Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json` |
| Disable regardless of effort | Set [`MAX_THINKING_TOKENS=0`](/docs/en/env-vars), which turns thinking off on the Anthropic API except on Fable 5. On [third-party providers](/docs/en/third-party-integrations) this omits the `thinking` parameter instead, and adaptive-reasoning models may still think. Other values apply only with a [fixed thinking budget](#adaptive-reasoning-and-fixed-thinking-budgets) |

Thinking cannot be turned off on Fable 5. The session toggle, `alwaysThinkingEnabled`, and `MAX_THINKING_TOKENS=0` have no effect there, and Fable 5 decides per step how much to think based on the effort level.
Thinking output is collapsed by default. Press `Ctrl+O` to toggle verbose mode and see the reasoning as gray italic text. Interactive sessions on the Anthropic API receive redacted thinking blocks by default, so set `showThinkingSummaries: true` in [settings](/docs/en/settings) if you want the full summaries available when you expand. You are charged for all thinking tokens generated, even when collapsed or redacted.

### [​](#extended-context) Extended context

Fable 5, Opus 4.6 and later, and Sonnet 4.6 support a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) for long sessions with large codebases.
Availability varies by model and plan. On Max, Team, and Enterprise plans, Opus is automatically upgraded to 1M context with no additional configuration. This applies to both Team Standard and Team Premium seats. On the Anthropic API, Fable 5, Opus 4.8, and Opus 4.7 always run with the 1M window. Sonnet with 1M context is not part of the automatic upgrade and requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) on every subscription plan, including Max.

| Plan | Opus with 1M context | Sonnet with 1M context |
| --- | --- | --- |
| Max, Team, and Enterprise | Included with subscription | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API and pay-as-you-go | Full access | Full access |

To disable 1M context entirely, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. This removes 1M model variants from the model picker. See [environment variables](/docs/en/env-vars).
The 1M context window uses standard model pricing with no premium for tokens beyond 200K. For plans where extended context is included with your subscription, usage remains covered by your subscription. For plans that access extended context through usage credits, tokens are billed to usage credits.
If your account supports 1M context, the option appears in the `/model` picker in the latest versions of Claude Code. If you don’t see it, try restarting your session.
You can also use the `[1m]` suffix with model aliases or full model names:

```