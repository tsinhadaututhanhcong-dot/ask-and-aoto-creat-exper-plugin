---
type: Reference
title: Enterprise deployment overview - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Enterprise deployment overview - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/third-party-integrations](https://code.claude.com/docs/en/third-party-integrations)

Organizations can deploy Claude Code through Anthropic directly or through a cloud provider. This page helps you choose the right configuration.


## [​](#compare-deployment-options) Compare deployment options

For most organizations, Claude for Teams or Claude for Enterprise provides the best experience. Team members get access to both Claude Code and Claude on the web with a single subscription, centralized billing, and no infrastructure setup required.
**Claude for Teams** is self-service and includes collaboration features, admin tools, and billing management. Best for smaller teams that need to get started quickly.
**Claude for Enterprise** adds SSO and domain capture, role-based permissions, compliance API access, and managed policy settings for deploying organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.
Learn more about [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) and [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).
If your organization has specific infrastructure requirements, compare the options below:

| Feature | Claude for Teams/Enterprise | Anthropic Console | Amazon Bedrock | Claude Platform on AWS | Google Vertex AI | Microsoft Foundry |
| --- | --- | --- | --- | --- | --- | --- |
| Best for | Most organizations (recommended) | Individual developers | AWS-native deployments | AWS Marketplace billing with Claude API features | GCP-native deployments | Azure-native deployments |
| Billing | **Teams:** $150/seat (Premium) with PAYG available **Enterprise:** [Contact Sales](https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise) | PAYG | PAYG through AWS | PAYG through AWS Marketplace | PAYG through GCP | PAYG through Azure |
| Regions | Supported [countries](https://www.anthropic.com/supported-countries) | Supported [countries](https://www.anthropic.com/supported-countries) | Multiple AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) | Multiple AWS regions | Multiple GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) | Multiple Azure [regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) |
| Prompt caching | Enabled by default | Enabled by default | Enabled by default | Enabled by default | Enabled by default | Enabled by default |
| Authentication | Claude.ai SSO or email | API key | API key or AWS credentials | API key or AWS credentials | GCP credentials | API key or Microsoft Entra ID |
| Cost tracking | Usage dashboard | Usage dashboard | AWS Cost Explorer | AWS Cost Explorer | GCP Billing | Azure Cost Management |
| Includes Claude on web | Yes | No | No | No | No | No |
| Enterprise features | Team management, SSO, usage monitoring | None | IAM policies, CloudTrail | IAM policies, CloudTrail | IAM roles, Cloud Audit Logs | RBAC policies, Azure Monitor |

For a feature-by-feature breakdown of what’s available on each option, see [Feature availability](/docs/en/feature-availability).
Select a deployment option to view setup instructions:

* [Claude for Teams or Enterprise](/docs/en/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/docs/en/authentication#claude-console-authentication)
* [Amazon Bedrock](/docs/en/amazon-bedrock)
* [Claude Platform on AWS](/docs/en/claude-platform-on-aws)
* [Google Vertex AI](/docs/en/google-vertex-ai)
* [Microsoft Foundry](/docs/en/microsoft-foundry)

## [​](#configure-proxies-and-gateways) Configure proxies and gateways

Most organizations can use a cloud provider directly without additional configuration. However, you may need to configure a corporate proxy or LLM gateway if your organization has specific network or management requirements. These are different configurations that can be used together:

* **Corporate proxy**: Routes traffic through an HTTP/HTTPS proxy. Use this if your organization requires all outbound traffic to pass through a proxy server for security monitoring, compliance, or network policy enforcement. Configure with the `HTTPS_PROXY` or `HTTP_PROXY` environment variables. Learn more in [Enterprise network configuration](/docs/en/network-config).
* **LLM Gateway**: A service that sits between Claude Code and the cloud provider to handle authentication and routing. Use this if you need centralized usage tracking across teams, custom rate limiting or budgets, or centralized authentication management. Configure with the `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, `ANTHROPIC_AWS_BASE_URL`, or `ANTHROPIC_VERTEX_BASE_URL` environment variables. Learn more in [LLM gateways](/docs/en/llm-gateway).

The following examples show the environment variables to set in your shell or shell profile (`.bashrc`, `.zshrc`). See [Settings](/docs/en/settings) for other configuration methods.

### [​](#amazon-bedrock) Amazon Bedrock

* Corporate proxy
* LLM Gateway

Route Bedrock traffic through your corporate proxy by setting the following [environment variables](/docs/en/env-vars):

```