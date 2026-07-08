---
type: Reference
title: Or append [1m] to a full model name
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Or append [1m] to a full model name
/model claude-opus-4-8[1m]
```

## [​](#checking-your-current-model) Checking your current model

You can see which model you’re currently using in two places:

* In the [status line](/docs/en/statusline), if you have one configured
* In `/status`, which also displays your account information

## [​](#add-a-custom-model-option) Add a custom model option

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` to add a single custom entry to the `/model` picker without replacing the built-in aliases. This is useful for testing model IDs that Claude Code does not list by default. For LLM gateway deployments, Claude Code can populate the picker from the gateway’s `/v1/models` endpoint when `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` is set, so this variable is needed only when discovery is disabled or does not return the model you want. See [gateway model discovery](/docs/en/llm-gateway-protocol#model-discovery).
This example sets all three variables to make a gateway-routed Opus deployment selectable:

```
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-8"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

The custom entry appears at the bottom of the `/model` picker. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` and `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` are optional. If omitted, the model ID is used as the name and the description defaults to `Custom model (<model-id>)`.
Claude Code skips validation for the model ID set in `ANTHROPIC_CUSTOM_MODEL_OPTION`, so you can use any string your API endpoint accepts. When [`availableModels`](#restrict-model-selection) is set, include the custom model ID in the allowlist as well: the custom entry is filtered from the picker and a `--model` selection of it is rejected like any other excluded model. A custom ID that embeds a family name, such as `my-gateway/claude-opus-4-8`, counts as a specific entry for that family and disables its wildcard, so also list the versions you intend to keep selectable. See [Merge behavior](#merge-behavior).

## [​](#environment-variables) Environment variables

You can use the following environment variables to control the model names that the aliases map to. Each value must be a full model name, or the equivalent identifier for your API provider.

| Environment variable | Description |
| --- | --- |
| `ANTHROPIC_DEFAULT_FABLE_MODEL` | The model to use for `fable`, and the model ID Claude Code recognizes as Fable 5 for [automatic model fallback](#automatic-model-fallback) on third-party providers |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | The model to use for `opus`, or for `opusplan` when Plan Mode is active. |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | The model to use for `sonnet`, or for `opusplan` when Plan Mode is not active. |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | The model to use for `haiku`, or [background functionality](/docs/en/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | The model to use for all [subagents](/docs/en/sub-agents#choose-a-model) and [agent teams](/docs/en/agent-teams). Overrides the per-invocation `model` parameter and the subagent definition’s `model` frontmatter. Set to `inherit` to use normal model resolution instead |

Note: `ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of
`ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### [​](#pin-models-for-third-party-deployments) Pin models for third-party deployments

When deploying Claude Code through [Bedrock](/docs/en/amazon-bedrock), [Vertex AI](/docs/en/google-vertex-ai), [Foundry](/docs/en/microsoft-foundry), or [Claude Platform on AWS](/docs/en/claude-platform-on-aws), pin model versions before rolling out to users.
Without pinning, Claude Code uses model aliases such as `fable`, `opus`, `sonnet`, and `haiku` that resolve to a built-in default model ID for each provider. That default can lag the newest Anthropic release, and the model it points to may not yet be enabled in a user’s account. When the default is unavailable, Bedrock and Vertex AI users see a notice and fall back to the previous version for that session, while Foundry users see errors because Foundry has no equivalent startup check.

Set the model environment variables to specific version IDs as part of your initial setup. Pinning lets you control when your users move to a new model.

Use the following environment variables with version-specific model IDs for your provider:

| Provider | Example |
| --- | --- |
| Bedrock | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-8'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'` |
| Foundry | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'` |

Apply the same pattern for `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`. For current and legacy model IDs across all providers, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). To upgrade users to a new model version, update these environment variables and redeploy.
To enable [extended context](#extended-context) for a pinned model, append `[1m]` to the model ID in `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8[1m]'
```

The `[1m]` suffix applies the 1M context window to all usage of the `opus` and `sonnet` aliases, including the plan-mode Opus phase of [`opusplan`](#opusplan-model-setting).

* Claude Code strips the suffix before sending the model ID to your provider.
* Only append `[1m]` when the underlying model [supports 1M context](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window).
* The suffix is read per variable, not per model. On Bedrock, Vertex, and Foundry, a model ID without `[1m]` in one variable uses 200K context even if another variable sets the same model with the suffix.

An `availableModels` allowlist delivered through [MDM or a managed settings file](/docs/en/settings#settings-files) still applies when using third-party providers; [server-managed settings are not delivered there](/docs/en/server-managed-settings#platform-availability). Filtering matches on a model alias such as `opus`, a version prefix such as `claude-opus-4-8`, or the full provider-form model ID. Provider-specific prefixes such as `us.anthropic.` are not stripped, so to allow a specific model, list the same provider-form ID the picker shows, or map it through [`modelOverrides`](#override-model-ids-per-version). Any `[1m]` suffix is stripped from both the allowlist entry and the requested model before matching.

### [​](#customize-pinned-model-display-and-capabilities) Customize pinned model display and capabilities

When you pin a model on a third-party provider, the provider-specific ID appears as-is in the `/model` picker and Claude Code may not recognize which features the model supports. You can override the display name and declare capabilities with companion environment variables for each pinned model.
These variables take effect on third-party providers such as Bedrock, Vertex AI, and Foundry. The `_NAME` and `_DESCRIPTION` variables also take effect when `ANTHROPIC_BASE_URL` points to an [LLM gateway](/docs/en/llm-gateway). They have no effect when connecting directly to `api.anthropic.com`.

| Environment variable | Description |
| --- | --- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME` | Display name for the pinned Opus model in the `/model` picker. Defaults to the model ID when not set |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION` | Display description for the pinned Opus model in the `/model` picker. Defaults to `Custom Opus model` when not set |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Comma-separated list of capabilities the pinned Opus model supports |

The same `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` suffixes are available for `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_FABLE_MODEL`, and `ANTHROPIC_CUSTOM_MODEL_OPTION`.
Claude Code enables features like [effort levels](#adjust-effort-level) and [extended thinking](#extended-thinking) by matching the model ID against known patterns. Provider-specific IDs such as Bedrock ARNs or custom deployment names often don’t match these patterns, leaving supported features disabled. Set `_SUPPORTED_CAPABILITIES` to tell Claude Code which features the model actually supports:

| Capability value | Enables |
| --- | --- |
| `effort` | [Effort levels](#adjust-effort-level) and the `/effort` command |
| `xhigh_effort` | The `xhigh` effort level |
| `max_effort` | The `max` effort level |
| `thinking` | [Extended thinking](#extended-thinking) |
| `adaptive_thinking` | Adaptive reasoning that dynamically allocates thinking based on task complexity |
| `interleaved_thinking` | Thinking between tool calls |

When `_SUPPORTED_CAPABILITIES` is set, listed capabilities are enabled and unlisted capabilities are disabled for the matching pinned model. When the variable is unset, Claude Code falls back to built-in detection based on the model ID.
This example pins Opus to a Bedrock custom model ARN, sets a friendly name, and declares its capabilities:

```
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### [​](#override-model-ids-per-version) Override model IDs per version

The family-level environment variables above configure one model ID per family alias. If you need to map several versions within the same family to distinct provider IDs, use the `modelOverrides` setting instead.
`modelOverrides` maps individual Anthropic model IDs to the provider-specific strings that Claude Code sends to your provider’s API. When a user selects a mapped model in the `/model` picker, Claude Code uses your configured value instead of the built-in default.
This lets enterprise administrators route each model version to a specific Bedrock inference profile ARN, Vertex AI version name, or Foundry deployment name for governance, cost allocation, or regional routing.
Set `modelOverrides` in your [settings file](/docs/en/settings#settings-files):

```
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Keys must be Anthropic model IDs as listed in the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). For dated model IDs, include the date suffix exactly as it appears there. Unknown keys are ignored.
Overrides replace the built-in model IDs that back each entry in the `/model` picker. On Bedrock, overrides take precedence over any inference profiles that Claude Code discovers automatically at startup. Values you supply directly through `ANTHROPIC_MODEL`, `--model`, or the `ANTHROPIC_DEFAULT_*_MODEL` environment variables are passed to the provider as-is and are not transformed by `modelOverrides`.
`modelOverrides` works alongside `availableModels`. The allowlist is evaluated against the Anthropic model ID, not the override value, so an entry like `"opus"` in `availableModels` continues to match even when Opus versions are mapped to ARNs. When `enforceAvailableModels` is set in managed settings, the enforced Default resolves through `modelOverrides` from the [highest-precedence managed source](/docs/en/server-managed-settings#settings-precedence) only. An admin’s mapping, such as a version pinned to an inference profile ARN, is honored in the enforced Default. Overrides from user or project settings do not affect it.

### [​](#prompt-caching-configuration) Prompt caching configuration

Claude Code automatically uses [prompt caching](/docs/en/prompt-caching) to optimize performance and reduce costs. You can disable prompt caching globally or for specific model tiers:

| Environment variable | Description |
| --- | --- |
| `DISABLE_PROMPT_CACHING` | Set to `1` to disable prompt caching for all models. Takes precedence over the per-model settings |
| `DISABLE_PROMPT_CACHING_HAIKU` | Set to `1` to disable prompt caching for Haiku models only |
| `DISABLE_PROMPT_CACHING_SONNET` | Set to `1` to disable prompt caching for Sonnet models only |
| `DISABLE_PROMPT_CACHING_OPUS` | Set to `1` to disable prompt caching for Opus models only |
| `DISABLE_PROMPT_CACHING_FABLE` | Set to `1` to disable prompt caching for Fable models only |

To change the cache TTL or learn what triggers a cache miss, see [How Claude Code uses prompt caching](/docs/en/prompt-caching).

Was this page helpful?

YesNo

[Bash sandbox](/docs/en/sandboxing)[Speed up responses with fast mode](/docs/en/fast-mode)

⌘I

---