---
title: For Amazon Bedrock:
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: integration
---

# For Amazon Bedrock:
- AWS_ROLE_TO_ASSUME
- AWS_REGION
```

Use the Amazon Bedrock job example above to exchange the GitLab job token for temporary AWS credentials at runtime.

### [​](#prerequisites-2) Prerequisites

Before setting up Claude Code with Google Vertex AI, you need:

1. A Google Cloud project with:
   * Vertex AI API enabled
   * Workload Identity Federation configured to trust GitLab OIDC
2. A dedicated service account with only the required Vertex AI roles
3. GitLab CI/CD variables for WIF:
   * `GCP_WORKLOAD_IDENTITY_PROVIDER` (full resource name)
   * `GCP_SERVICE_ACCOUNT` (service account email)

### [​](#setup-instructions-2) Setup instructions

Configure Google Cloud to allow GitLab CI jobs to impersonate a service account via Workload Identity Federation.**Required setup:**

1. Enable IAM Credentials API, STS API, and Vertex AI API
2. Create a Workload Identity Pool and provider for GitLab OIDC
3. Create a dedicated service account with Vertex AI roles
4. Grant the WIF principal permission to impersonate the service account

**Required values to store in CI/CD variables:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`
* `GCP_SERVICE_ACCOUNT`

Add variables in Settings → CI/CD → Variables:

```