---
title: Enable Vertex AI API
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### [​](#2-request-model-access) 2. Request model access

Request access to Claude models in Vertex AI:

1. Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Search for “Claude” models
3. Request access to desired Claude models (for example, Claude Sonnet 4.6)
4. Wait for approval (may take 24-48 hours)

### [​](#3-configure-gcp-credentials) 3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.
For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).
Claude Code v2.1.121 or later supports [X.509 certificate-based Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) through the same Application Default Credentials chain. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credential configuration file.

Claude Code uses `ANTHROPIC_VERTEX_PROJECT_ID` as the project ID for Vertex AI requests. The `GCLOUD_PROJECT` and `GOOGLE_CLOUD_PROJECT` environment variables and the credential file referenced by `GOOGLE_APPLICATION_CREDENTIALS` take precedence over it. If none of these are set, the project ID is resolved from your `gcloud` configuration or the attached service account.

#### [​](#advanced-credential-configuration) Advanced credential configuration

Claude Code supports automatic credential refresh for GCP through the `gcpAuthRefresh` setting. When Claude Code detects that your GCP credentials are expired or cannot be loaded, it runs the configured command to obtain new credentials before retrying the request.

```
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

The command’s output is displayed to the user, but interactive input isn’t supported. This works well for browser-based authentication flows where the CLI shows a URL and you complete authentication in the browser. The refresh command times out after three minutes if authentication does not complete. If you set `gcpAuthRefresh` in project settings such as `.claude/settings.json`, the command runs only after you accept the workspace trust prompt.

### [​](#4-configure-claude-code) 4. Configure Claude Code

Set the following environment variables:

```