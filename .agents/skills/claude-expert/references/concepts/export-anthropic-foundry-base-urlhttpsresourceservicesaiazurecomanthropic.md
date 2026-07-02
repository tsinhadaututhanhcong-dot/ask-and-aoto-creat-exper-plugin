---
title: export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### [​](#4-pin-model-versions) 4. Pin model versions

Pin specific model versions for every deployment. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code’s built-in default for Foundry, which can lag the newest release and may not yet be available in your account. Foundry has no startup model check, so requests fail when the default is unavailable. When you create Azure deployments, select a specific model version rather than “auto-update to latest.”

Set the model variables to match the deployment names you created in step 1.
Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Foundry resolves to Opus 4.6. Set it to the Opus 4.8 ID to use the latest model:

```
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Foundry, Claude Code defaults this to the primary model because not every account has a Haiku deployment. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a Haiku deployment that is available in your account, as shown above.
For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](/docs/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.
[Prompt caching](/docs/en/prompt-caching) is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set the following variable; cache writes with a 1-hour TTL are billed at a higher rate:

```
export ENABLE_PROMPT_CACHING_1H=1
```

### [​](#5-run-claude-code) 5. Run Claude Code

With the environment variables set, start Claude Code from your project directory:

```
claude
```

Claude Code reads `CLAUDE_CODE_USE_FOUNDRY` and the other Foundry variables from the environment and connects to your Azure resource on the first prompt. Unlike Bedrock and Vertex AI, Foundry has no interactive setup wizard, so the environment variables in steps 3 and 4 are the only configuration path.

## [​](#azure-rbac-configuration) Azure RBAC configuration

The `Azure AI User` and `Cognitive Services User` default roles include all required permissions for invoking Claude models.
For more restrictive permissions, create a custom role with the following:

```
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

For details, see [Microsoft Foundry RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## [​](#troubleshooting) Troubleshooting

If you receive an error “Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed”:

* Configure Entra ID on the environment, or set `ANTHROPIC_FOUNDRY_API_KEY`.

## [​](#additional-resources) Additional resources

* [Microsoft Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry models](https://ai.azure.com/explore/models)
* [Microsoft Foundry pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)

Was this page helpful?

YesNo

[Google Vertex AI](/docs/en/google-vertex-ai)[Network configuration](/docs/en/network-config)

⌘I

---