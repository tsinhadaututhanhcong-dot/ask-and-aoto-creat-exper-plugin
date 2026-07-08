---
type: Reference
title: Claude Code on Microsoft Foundry - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Claude Code on Microsoft Foundry - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/microsoft-foundry](https://code.claude.com/docs/en/microsoft-foundry)

## [​](#prerequisites) Prerequisites

Before configuring Claude Code with Microsoft Foundry, ensure you have:

* An Azure subscription with access to Microsoft Foundry
* RBAC permissions to create Microsoft Foundry resources and deployments
* Azure CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)

If you are deploying Claude Code to multiple users, [pin your model versions](#4-pin-model-versions) before rolling out.

## [​](#setup) Setup

### [​](#1-provision-microsoft-foundry-resource) 1. Provision Microsoft Foundry resource

First, create a Claude resource in Azure:

1. Navigate to the [Microsoft Foundry portal](https://ai.azure.com/)
2. Create a new resource, noting your resource name
3. Create deployments for the Claude models:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### [​](#2-configure-azure-credentials) 2. Configure Azure credentials

Claude Code supports two authentication methods for Microsoft Foundry. Choose the method that best fits your security requirements.
**Option A: API key authentication**

1. Navigate to your resource in the Microsoft Foundry portal
2. Go to the **Endpoints and keys** section
3. Copy **API Key**
4. Set the environment variable:

```
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Option B: Microsoft Entra ID authentication**
When `ANTHROPIC_FOUNDRY_API_KEY` is not set, Claude Code automatically uses the Azure SDK [default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
This supports a variety of methods for authenticating local and remote workloads.
On local environments, you commonly may use the Azure CLI:

```
az login
```

When using Microsoft Foundry, the `/logout` command is unavailable since authentication is handled through Azure credentials.

### [​](#3-configure-claude-code) 3. Configure Claude Code

Set the following environment variables to enable Microsoft Foundry:

```