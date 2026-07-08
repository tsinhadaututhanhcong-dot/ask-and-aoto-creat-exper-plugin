---
type: Reference
title: export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

When enabling Bedrock for Claude Code, keep the following in mind:

* As of v2.1.172, you only need to set `AWS_REGION` to override your AWS profile’s region or when your profile has no region. Claude Code resolves the region in this order:
  + `AWS_REGION`
  + `AWS_DEFAULT_REGION`
  + the `region` set on your active AWS profile, read from the AWS shared credentials file first and then the shared config file, matching AWS SDK precedence
  + `us-east-1`The active profile is `AWS_PROFILE` if set, otherwise `default`. Set `AWS_SHARED_CREDENTIALS_FILE` or `AWS_CONFIG_FILE` to point at non-default file paths. Run `/status` to see the resolved region. When the region came from your AWS config files or the default fallback, `/status` also notes the source. On v2.1.171 and earlier, Claude Code does not read the AWS config files, so set `AWS_REGION` explicitly.
* When using Bedrock, the `/logout` command is unavailable since authentication is handled through AWS credentials.
* The WebSearch tool is not available on Bedrock. See [WebSearch tool behavior](/docs/en/tools-reference#websearch-tool-behavior).
* You can use settings files for environment variables like `AWS_PROFILE` that you don’t want to leak to other processes. See [Settings](/docs/en/settings) for more information.

### [​](#4-pin-model-versions) 4. Pin model versions

Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code’s built-in default for Bedrock, which can lag the newest release and may not yet be available in your account. Claude Code [falls back](#startup-model-checks) to the previous version at startup when the default is unavailable, but pinning lets you control when your users move to a new model.

Set these environment variables to specific Bedrock model IDs.
Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Bedrock resolves to Opus 4.6. Set it to the Opus 4.8 ID to use the latest model:

```
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

These variables use cross-region inference profile IDs (with the `us.` prefix). If you use a different region prefix or application inference profiles, adjust accordingly. In AWS GovCloud regions, use the `us-gov.` prefix. For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](/docs/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.
Claude Code uses these default models when no pinning variables are set:

| Model type | Default value |
| --- | --- |
| Primary model | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Small/fast model | Same as primary model |

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Bedrock, Claude Code defaults this to the primary model because Haiku may not be enabled in every account or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID that is available in your account.
To customize models further, use one of these methods:

```