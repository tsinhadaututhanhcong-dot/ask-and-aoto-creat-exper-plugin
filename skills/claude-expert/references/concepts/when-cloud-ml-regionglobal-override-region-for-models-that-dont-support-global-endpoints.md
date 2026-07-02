---
title: When CLOUD_ML_REGION=global, override region for models that don't support global endpoints
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# When CLOUD_ML_REGION=global, override region for models that don't support global endpoints
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Most model versions have a corresponding `VERTEX_REGION_CLAUDE_*` variable. See the [Environment variables reference](/docs/en/env-vars) for the full list. Check [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) to determine which models support global endpoints versus regional only.
[Prompt caching](/docs/en/prompt-caching) is enabled automatically. To disable it, set `DISABLE_PROMPT_CACHING=1`. To request a 1-hour cache TTL instead of the 5-minute default, set `ENABLE_PROMPT_CACHING_1H=1`; cache writes with a 1-hour TTL are billed at a higher rate. For heightened rate limits, contact Google Cloud support. When using Vertex AI, the `/logout` command is unavailable since authentication is handled through Google Cloud credentials.
Claude Code disables [MCP tool search](/docs/en/mcp#scale-with-mcp-tool-search) by default on Vertex AI, so MCP tool definitions load upfront. Vertex AI supports tool search for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later. Set `ENABLE_TOOL_SEARCH=true` to enable it on those models. Earlier models on Vertex AI do not accept the required beta header, and requests fail if you enable tool search with them.

### [​](#5-pin-model-versions) 5. Pin model versions

Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code’s built-in default for Vertex AI, which can lag the newest release and may not yet be enabled in your project. Claude Code [falls back](#startup-model-checks) to the previous version at startup when the default is unavailable, but pinning lets you control when your users move to a new model.

Set these environment variables to specific Vertex AI model IDs.
Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Vertex resolves to Opus 4.6. Set it to the Opus 4.8 ID to use the latest model:

```
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](/docs/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.
Claude Code uses these default models when no pinning variables are set:

| Model type | Default value |
| --- | --- |
| Primary model | `claude-sonnet-4-5@20250929` |
| Small/fast model | Same as primary model |

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Vertex AI, Claude Code defaults this to the primary model because Haiku may not be enabled in every project or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID that is available in your project.
To customize models further:

```
export ANTHROPIC_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## [​](#startup-model-checks) Startup model checks

When Claude Code starts with Vertex AI configured, it verifies that the models it intends to use are accessible in your project. This check requires Claude Code v2.1.98 or later.
If you have pinned a model version that is older than the current Claude Code default, and your project can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your [user settings file](/docs/en/settings) and restarts Claude Code. Declining is remembered until the next default version change.
If you have not pinned a model and the current default is unavailable in your project, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) or [pin a version](#5-pin-model-versions) to make the choice permanent.

## [​](#iam-configuration) IAM configuration

Assign the required IAM permissions:
The `roles/aiplatform.user` role includes the required permissions:

* `aiplatform.endpoints.predict` - Required for model invocation and token counting

For more restrictive permissions, create a custom role with only the permissions above.
For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

Create a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## [​](#1m-token-context-window) 1M token context window

Claude Opus 4.6 and later, and Sonnet 4.6, support the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) on Vertex AI. Claude Code automatically enables the extended context window when you select a 1M model variant.
The [setup wizard](#sign-in-with-vertex-ai) offers a 1M context option when it pins models. To enable it for a manually pinned model instead, append `[1m]` to the model ID. See [Pin models for third-party deployments](/docs/en/model-config#pin-models-for-third-party-deployments) for details.

## [​](#troubleshooting) Troubleshooting

If you encounter “Could not load the default credentials” errors:

* Run `gcloud auth application-default login` to set up Application Default Credentials
* Set `GOOGLE_APPLICATION_CREDENTIALS` to a service account key file path
* See [Configure GCP credentials](#3-configure-gcp-credentials) for all options

If you encounter quota issues:

* Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter “model not found” 404 errors:

* Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verify the model is available in the location you specified. Some models are offered only on `global` or multi-region locations such as `eu` and `us`, not in specific regions
* If using `CLOUD_ML_REGION=global`, check that your models support global endpoints in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) under “Supported features”. For models that don’t support global endpoints, either:
  + Specify a supported model via `ANTHROPIC_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL`, or
  + Set a region or multi-region location using `VERTEX_REGION_<MODEL_NAME>` environment variables

If you encounter 429 errors:

* For regional endpoints, ensure the primary model and small/fast model are supported in your selected region
* Consider switching to `CLOUD_ML_REGION=global` for better availability

## [​](#additional-resources) Additional resources

* [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)

Was this page helpful?

YesNo

[Claude Platform on AWS](/docs/en/claude-platform-on-aws)[Microsoft Foundry](/docs/en/microsoft-foundry)

⌘I

---