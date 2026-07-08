# Google Gemini | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/guides/google-gemini](https://hermes-agent.nousresearch.com/docs/guides/google-gemini)

On this page

Hermes Agent supports Google Gemini as a native provider using the **Google AI Studio / Gemini API** — not the OpenAI-compatible endpoint. This lets Hermes translate its internal OpenAI-shaped message and tool loop into Gemini's native `generateContent` API while preserving tool calling, streaming, multimodal inputs, and Gemini-specific response metadata.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* **Google AI Studio API key** — create one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
* **Billing-enabled Google Cloud project** — recommended for agent use. Gemini's free tier is too small for long-running agent sessions because Hermes may make several model calls per user turn.
* **Hermes installed** — no extra Python package is required for the native Gemini provider.

API key path

Set `GOOGLE_API_KEY` or `GEMINI_API_KEY`. Hermes checks both names for the `gemini` provider.

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
# Add your Gemini API key  
echo "GOOGLE_API_KEY=..." >> ~/.hermes/.env  
  
# Select Gemini as your provider  
hermes model  
# → Choose "More providers..." → "Google AI Studio"  
# → Hermes checks your key tier and shows Gemini models  
# → Select a model  
  
# Start chatting  
hermes chat
```

If you prefer direct config editing, use the native Gemini API base URL:

```
model:  
  default: gemini-3-flash-preview  
  provider: gemini  
  base_url: https://generativelanguage.googleapis.com/v1beta
```

## Configuration[​](#configuration "Direct link to Configuration")

After running `hermes model`, your `~/.hermes/config.yaml` will contain:

```
model:  
  default: gemini-3-flash-preview  
  provider: gemini  
  base_url: https://generativelanguage.googleapis.com/v1beta
```

And in `~/.hermes/.env`:

```
GOOGLE_API_KEY=...
```

### Native Gemini API[​](#native-gemini-api "Direct link to Native Gemini API")

The recommended endpoint is:

```
https://generativelanguage.googleapis.com/v1beta
```

Hermes detects this endpoint and creates its native Gemini adapter. Internally, Hermes still keeps the agent loop in OpenAI-shaped messages, then translates each request to Gemini's native schema:

* `messages[]` → Gemini `contents[]`
* system prompts → Gemini `systemInstruction`
* tool schemas → Gemini `functionDeclarations`
* tool results → Gemini `functionResponse` parts
* streaming responses → OpenAI-shaped stream chunks for the Hermes loop

Gemini 3 thought signatures

For Gemini 3 tool use, Hermes preserves the `thoughtSignature` values attached to function-call parts and replays them on the next tool turn. That covers the validation-critical path for multi-step agent workflows.

Gemini 3 may also attach thought signatures to other response parts. Hermes' native adapter is optimized for agent tool loops today, so it does not yet replay every non-tool-call signature with full part-level fidelity.

### Prefer the Native Endpoint[​](#prefer-the-native-endpoint "Direct link to Prefer the Native Endpoint")

Google also exposes an OpenAI-compatible endpoint:

```
https://generativelanguage.googleapis.com/v1beta/openai/
```

For Hermes agent sessions, prefer the native Gemini endpoint above. Hermes includes a native Gemini adapter so it can map multi-turn tool use, tool-call results, streaming, multimodal inputs, and Gemini response metadata directly onto Gemini's `generateContent` API. The OpenAI-compatible endpoint is still useful when you specifically need OpenAI API compatibility.

If you previously set `GEMINI_BASE_URL` to the `/openai` URL, remove it or change it:

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

## Available Models[​](#available-models "Direct link to Available Models")

The `hermes model` picker shows Gemini models maintained in Hermes' provider registry. Common choices include:

| Model | ID | Notes |
| --- | --- | --- |
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | Most capable preview model when available |
| Gemini 3 Pro Preview | `gemini-3-pro-preview` | Strong reasoning and coding model |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | Recommended default balance of speed and capability |
| Gemini 3.1 Flash Lite Preview | `gemini-3.1-flash-lite-preview` | Fastest / lowest-cost option when available |

Model availability changes over time. If a model disappears or is not enabled for your key, run `hermes model` again and pick one from the current list.

Model IDs

Use Gemini's native model IDs such as `gemini-3-flash-preview`, not OpenRouter-style IDs like `google/gemini-3-flash-preview`, when `provider: gemini`.

### Latest Aliases[​](#latest-aliases "Direct link to Latest Aliases")

Google publishes moving aliases for the Pro and Flash Gemini families. `gemini-pro-latest` and `gemini-flash-latest` are useful when you want Google to advance the model automatically without changing your Hermes config.

| Alias | Currently tracks | Notes |
| --- | --- | --- |
| `gemini-pro-latest` | Latest Gemini Pro model | Best when you want Google's current Pro default |
| `gemini-flash-latest` | Latest Gemini Flash model | Best when you want Google's current Flash default |

```
model:  
  default: gemini-pro-latest  
  provider: gemini  
  base_url: https://generativelanguage.googleapis.com/v1beta
```

If you need strict reproducibility, prefer explicit model IDs such as `gemini-3.1-pro-preview` or `gemini-3-flash-preview`.

### Gemma via the Gemini API[​](#gemma-via-the-gemini-api "Direct link to Gemma via the Gemini API")

Google also exposes Gemma models through the Gemini API. Hermes recognizes these as Google models, but hides very low-throughput Gemma entries from the default model picker so new users do not accidentally select an evaluation-tier model for a long-running agent session.

Useful evaluation IDs include:

| Model | ID | Notes |
| --- | --- | --- |
| Gemma 4 31B IT | `gemma-4-31b-it` | Larger Gemma model; useful for compatibility and quality evaluation |
| Gemma 4 26B A4B IT | `gemma-4-26b-a4b-it` | Smaller active-parameter variant when available |

These models are best treated as evaluation options on Gemini API keys. Google's Gemma API pricing is free-tier-only and the usage caps are low compared with production Gemini models, so sustained Hermes agent use should normally move to a paid Gemini model, a self-hosted deployment, or another provider with appropriate quota.

To use a Gemma model that is hidden from the picker, set it directly:

```
model:  
  default: gemma-4-31b-it  
  provider: gemini  
  base_url: https://generativelanguage.googleapis.com/v1beta
```

## Switching Models Mid-Session[​](#switching-models-mid-session "Direct link to Switching Models Mid-Session")

Use the `/model` command during a conversation:

```
/model gemini-3-flash-preview  
/model gemini-flash-latest  
/model gemini-3-pro-preview  
/model gemini-pro-latest  
/model gemma-4-31b-it  
/model gemini-3.1-flash-lite-preview
```

If you have not configured Gemini yet, exit the session and run `hermes model` first. `/model` switches among already-configured providers and models; it does not collect new API keys.

## Diagnostics[​](#diagnostics "Direct link to Diagnostics")

```
hermes doctor
```

The doctor checks:

* Whether `GOOGLE_API_KEY` or `GEMINI_API_KEY` is available
* Whether configured provider credentials can be resolved

## Gateway (Messaging Platforms)[​](#gateway-messaging-platforms "Direct link to Gateway (Messaging Platforms)")

Gemini works with all Hermes gateway platforms (Telegram, Discord, Slack, WhatsApp, LINE, Feishu, etc.). Configure Gemini as your provider, then start the gateway normally:

```
hermes gateway setup  
hermes gateway start
```

The gateway reads `config.yaml` and uses the same Gemini provider configuration.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

### "Gemini native client requires an API key"[​](#gemini-native-client-requires-an-api-key "Direct link to \"Gemini native client requires an API key\"")

Hermes could not find a usable API key. Add one of these to `~/.hermes/.env`:

```
GOOGLE_API_KEY=...  
# or  
GEMINI_API_KEY=...
```

Then run `hermes model` again.

### "This Google API key is on the free tier"[​](#this-google-api-key-is-on-the-free-tier "Direct link to \"This Google API key is on the free tier\"")

Hermes probes Gemini API keys during setup. Free-tier quotas can be exhausted after a handful of agent turns because tool use, retries, compression, and auxiliary tasks may require multiple model calls.

Enable billing on the Google Cloud project attached to your key, regenerate the key if needed, then run:

```
hermes model
```

### "404 model not found"[​](#404-model-not-found "Direct link to \"404 model not found\"")

The selected model is not available for your account, region, or key. Run `hermes model` again and pick another Gemini model from the current list.

### Gemma model is not shown in `hermes model`[​](#gemma-model-is-not-shown-in-hermes-model "Direct link to gemma-model-is-not-shown-in-hermes-model")

Hermes may hide low-throughput Gemma models from the picker by default. If you intentionally want to evaluate one, set the model ID directly in `~/.hermes/config.yaml`.

### "429 quota exceeded" on Gemma[​](#429-quota-exceeded-on-gemma "Direct link to \"429 quota exceeded\" on Gemma")

Gemma models exposed through the Gemini API are useful for evaluation, but their Gemini API free-tier caps are low. Use them for compatibility testing, then switch to a paid Gemini model or another provider for sustained agent sessions.

### OpenAI-compatible endpoint is configured[​](#openai-compatible-endpoint-is-configured "Direct link to OpenAI-compatible endpoint is configured")

Check `~/.hermes/.env` for:

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Change it to the native endpoint or remove the override:

```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

### Tool calling fails with schema errors[​](#tool-calling-fails-with-schema-errors "Direct link to Tool calling fails with schema errors")

Upgrade Hermes and rerun `hermes model`. The native Gemini adapter sanitizes tool schemas for Gemini's stricter function-declaration format; older builds or custom endpoints may not.

## Related[​](#related "Direct link to Related")

* [AI Providers](/docs/integrations/providers)
* [Configuration](/docs/user-guide/configuration)
* [Fallback Providers](/docs/user-guide/features/fallback-providers)
* [AWS Bedrock](/docs/guides/aws-bedrock) — native cloud-provider integration using AWS credentials

* [Prerequisites](#prerequisites)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
  + [Native Gemini API](#native-gemini-api)
  + [Prefer the Native Endpoint](#prefer-the-native-endpoint)
* [Available Models](#available-models)
  + [Latest Aliases](#latest-aliases)
  + [Gemma via the Gemini API](#gemma-via-the-gemini-api)
* [Switching Models Mid-Session](#switching-models-mid-session)
* [Diagnostics](#diagnostics)
* [Gateway (Messaging Platforms)](#gateway-messaging-platforms)
* [Troubleshooting](#troubleshooting)
  + ["Gemini native client requires an API key"](#gemini-native-client-requires-an-api-key)
  + ["This Google API key is on the free tier"](#this-google-api-key-is-on-the-free-tier)
  + ["404 model not found"](#404-model-not-found)
  + [Gemma model is not shown in `hermes model`](#gemma-model-is-not-shown-in-hermes-model)
  + ["429 quota exceeded" on Gemma](#429-quota-exceeded-on-gemma)
  + [OpenAI-compatible endpoint is configured](#openai-compatible-endpoint-is-configured)
  + [Tool calling fails with schema errors](#tool-calling-fails-with-schema-errors)
* [Related](#related)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock](./docs-guides-aws-bedrock.md)
- [https://hermes-agent.nousresearch.com/docs/integrations/providers](./docs-integrations-providers.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/configuration](./docs-user-guide-configuration.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers](./docs-user-guide-features-fallback-providers.md)
