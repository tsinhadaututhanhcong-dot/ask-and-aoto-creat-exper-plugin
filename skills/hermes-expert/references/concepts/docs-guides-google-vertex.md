# Google Vertex AI | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/guides/google-vertex](https://hermes-agent.nousresearch.com/docs/guides/google-vertex)

On this page

Hermes Agent supports **Gemini models on Google Cloud Vertex AI** through Vertex's OpenAI-compatible endpoint. Unlike the [Google AI Studio provider](/docs/guides/google-gemini) (which uses a static API key against `generativelanguage.googleapis.com`), Vertex gives you **enterprise-grade rate limits and GCP billing/credits**, and is the right choice when you want Gemini usage to draw on your Google Cloud account rather than an AI Studio key.

Vertex authenticates with OAuth2, not an API key

Vertex has **no static API key** for the standard endpoint. Every request needs a short-lived **OAuth2 access token** (≈1 hour TTL) minted from either a service-account JSON or Application Default Credentials (ADC). Hermes mints and **auto-refreshes** these tokens for you — you never paste a token by hand. This is why pasting a temporary token into a custom provider's `api_key` field does not work: it expires mid-session.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* **A Google Cloud project** with the **Vertex AI API enabled** and billing active.
* **Credentials**, one of:
  + a **service-account JSON** key file with the `roles/aiplatform.user` role, or
  + **Application Default Credentials** via `gcloud auth application-default login` (or the metadata server when running on a GCP VM).
* **`google-auth`** — installed automatically the first time you select Vertex (lazy install), or explicitly with `pip install 'hermes-agent[vertex]'`.

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
# Option A — service account JSON (recommended for servers / gateways)  
echo "VERTEX_CREDENTIALS_PATH=/path/to/service-account.json" >> ~/.hermes/.env  
  
# Option B — Application Default Credentials (good for local dev)  
gcloud auth application-default login  
  
# Select Vertex as your provider  
hermes model  
# → Choose "More providers..." → "Google Vertex AI"  
# → Enter your GCP project ID (or leave blank to use the one in your credentials)  
# → Choose a region (default: global)  
# → Select a Gemini model  
  
# Start chatting  
hermes chat
```

## Configuration[​](#configuration "Direct link to Configuration")

Vertex splits its settings by sensitivity:

* The **credential path** is a pointer to a secret and lives in `~/.hermes/.env`.
* **Project ID and region** are non-secret routing settings and live in `~/.hermes/config.yaml`.

`~/.hermes/.env`:

```
# One of these (checked in this order); omit both to use ADC:  
VERTEX_CREDENTIALS_PATH=/path/to/service-account.json  
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

`~/.hermes/config.yaml`:

```
model:  
  default: google/gemini-3-flash-preview  
  provider: vertex  
  
vertex:  
  project_id: my-gcp-project   # blank → use the project embedded in the credentials  
  region: global               # "global" is required for the Gemini 3.x previews
```

Environment variables win over config.yaml

`VERTEX_PROJECT_ID` and `VERTEX_REGION` override the `vertex.project_id` / `vertex.region` values in `config.yaml`. Use them for per-shell overrides; keep the durable settings in `config.yaml`.

### How authentication works[​](#how-authentication-works "Direct link to How authentication works")

1. Hermes resolves credentials in this order: `VERTEX_CREDENTIALS_PATH` → `GOOGLE_APPLICATION_CREDENTIALS` → ADC.
2. It mints an OAuth2 access token (`cloud-platform` scope) and caches it, refreshing when the token is within 5 minutes of expiry.
3. The token is handed to a standard OpenAI client pointed at the Vertex endpoint:

   ```
   https://aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{region}/endpoints/openapi
   ```

   Regional locations use a `{region}-aiplatform.googleapis.com` host instead.
4. If a session runs longer than the token lifetime and a request returns `401`, Hermes re-mints the token and retries automatically. On a long-running gateway, if ADC's refresh token has itself expired, Hermes falls back to the service-account JSON when one is configured.

## Available Models[​](#available-models "Direct link to Available Models")

Vertex requires the `google/` vendor prefix on model IDs. The `hermes model` picker offers:

| Model | ID |
| --- | --- |
| Gemini 3.1 Pro Preview | `google/gemini-3.1-pro-preview` |
| Gemini 3 Pro Preview | `google/gemini-3-pro-preview` |
| Gemini 3 Flash Preview | `google/gemini-3-flash-preview` |
| Gemini 3.1 Flash Lite Preview | `google/gemini-3.1-flash-lite-preview` |
| Gemini 2.5 Pro | `google/gemini-2.5-pro` |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` |

`global` region for Gemini 3.x

The Gemini 3.x preview models are served through the `global` endpoint. Regional endpoints (`us-central1`, etc.) may 404 them. Leave `region: global` unless you have a specific reason to pin a region.

## Switching Models Mid-Session[​](#switching-models-mid-session "Direct link to Switching Models Mid-Session")

```
/model google/gemini-3-pro-preview  
/model google/gemini-3-flash-preview
```

`/model` switches among already-configured providers and models; it does not collect new credentials. Configure Vertex with `hermes model` first.

## Reasoning / Thinking[​](#reasoning--thinking "Direct link to Reasoning / Thinking")

Vertex exposes Gemini's thinking budget through the OpenAI-compatible surface. Hermes maps its reasoning-effort setting onto `extra_body.google.thinking_config` automatically, so `reasoning_effort` works the same way it does on other Gemini surfaces.

## Diagnostics[​](#diagnostics "Direct link to Diagnostics")

```
hermes doctor
```

The doctor reports whether Vertex credentials can be resolved (service-account path or ADC) and whether the provider is configured.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

### "Vertex AI credentials could not be resolved"[​](#vertex-ai-credentials-could-not-be-resolved "Direct link to \"Vertex AI credentials could not be resolved\"")

Hermes found neither a service-account JSON nor working ADC. Either set `VERTEX_CREDENTIALS_PATH` in `~/.hermes/.env`, or run `gcloud auth application-default login`. If your project isn't embedded in the credentials, set `vertex.project_id` in `config.yaml`.

### `google-auth` not installed[​](#google-auth-not-installed "Direct link to google-auth-not-installed")

Install the extra: `pip install 'hermes-agent[vertex]'`. Hermes also lazy-installs it the first time you select the Vertex provider.

### 404 on Gemini 3.x models[​](#404-on-gemini-3x-models "Direct link to 404 on Gemini 3.x models")

You are probably on a regional endpoint. Set `region: global` in the `vertex:` section of `config.yaml` (or unset `VERTEX_REGION`).

### 403 / permission denied[​](#403--permission-denied "Direct link to 403 / permission denied")

The service account (or your ADC identity) needs the `roles/aiplatform.user` role on the project, and the Vertex AI API must be enabled for that project.

## Related[​](#related "Direct link to Related")

* [Google Gemini (AI Studio)](/docs/guides/google-gemini) — static-API-key Gemini without GCP
* [AWS Bedrock](/docs/guides/aws-bedrock) — another native cloud-provider integration
* [AI Providers](/docs/integrations/providers)
* [Configuration](/docs/user-guide/configuration)

* [Prerequisites](#prerequisites)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
  + [How authentication works](#how-authentication-works)
* [Available Models](#available-models)
* [Switching Models Mid-Session](#switching-models-mid-session)
* [Reasoning / Thinking](#reasoning--thinking)
* [Diagnostics](#diagnostics)
* [Troubleshooting](#troubleshooting)
  + ["Vertex AI credentials could not be resolved"](#vertex-ai-credentials-could-not-be-resolved)
  + [`google-auth` not installed](#google-auth-not-installed)
  + [404 on Gemini 3.x models](#404-on-gemini-3x-models)
  + [403 / permission denied](#403--permission-denied)
* [Related](#related)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/guides/aws-bedrock](./docs-guides-aws-bedrock.md)
- [https://hermes-agent.nousresearch.com/docs/guides/google-gemini](./docs-guides-google-gemini.md)
- [https://hermes-agent.nousresearch.com/docs/integrations/providers](./docs-integrations-providers.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/configuration](./docs-user-guide-configuration.md)
