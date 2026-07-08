---
type: Reference
title: Claude Code GitLab CI/CD - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: integration
---

# Claude Code GitLab CI/CD - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/gitlab-ci-cd](https://code.claude.com/docs/en/gitlab-ci-cd)

Claude Code for GitLab CI/CD is currently in beta. Features and functionality may evolve as we refine the experience.This integration is maintained by GitLab. For support, see the following [GitLab issue](https://gitlab.com/gitlab-org/gitlab/-/issues/573776).

This integration is built on top of the [Claude Code CLI and Agent SDK](/docs/en/agent-sdk/overview), enabling programmatic use of Claude in your CI/CD jobs and custom automation workflows.

## [​](#why-use-claude-code-with-gitlab) Why use Claude Code with GitLab?

* **Instant MR creation**: Describe what you need, and Claude proposes a complete MR with changes and explanation
* **Automated implementation**: Turn issues into working code with a single command or mention
* **Project-aware**: Claude follows your `CLAUDE.md` guidelines and existing code patterns
* **Simple setup**: Add one job to `.gitlab-ci.yml` and a masked CI/CD variable
* **Enterprise-ready**: Choose Claude API, Amazon Bedrock, or Google Vertex AI to meet data residency and procurement needs
* **Secure by default**: Runs in your GitLab runners with your branch protection and approvals

## [​](#how-it-works) How it works

Claude Code uses GitLab CI/CD to run AI tasks in isolated jobs and commit results back via MRs:

1. **Event-driven orchestration**: GitLab listens for your chosen triggers (for example, a comment that mentions `@claude` in an issue, MR, or review thread). The job collects context from the thread and repository, builds prompts from that input, and runs Claude Code.
2. **Provider abstraction**: Use the provider that fits your environment:
   * Claude API (SaaS)
   * Amazon Bedrock (IAM-based access, cross-region options)
   * Google Vertex AI (GCP-native, Workload Identity Federation)
3. **Sandboxed execution**: Each interaction runs in a container with strict network and filesystem rules. Claude Code enforces workspace-scoped permissions to constrain writes. Every change flows through an MR so reviewers see the diff and approvals still apply.

Pick regional endpoints to reduce latency and meet data-sovereignty requirements while using existing cloud agreements.

## [​](#what-can-claude-do) What can Claude do?

Claude Code enables powerful CI/CD workflows that transform how you work with code:

* Create and update MRs from issue descriptions or comments
* Analyze performance regressions and propose optimizations
* Implement features directly in a branch, then open an MR
* Fix bugs and regressions identified by tests or comments
* Respond to follow-up comments to iterate on requested changes

## [​](#setup) Setup

### [​](#quick-setup) Quick setup

The fastest way to get started is to add a minimal job to your `.gitlab-ci.yml` and set your API key as a masked variable.

1. **Add a masked CI/CD variable**
   * Go to **Settings** → **CI/CD** → **Variables**
   * Add `ANTHROPIC_API_KEY` (masked, protected as needed)
2. **Add a Claude job to `.gitlab-ci.yml`**

```
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Adjust rules to fit how you want to trigger the job:
  # - manual runs
  # - merge request events
  # - web/API triggers when a comment contains '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    # Optional: start a GitLab MCP server if your setup provides one
    - /bin/gitlab-mcp-server || true
    # Use AI_FLOW_* variables when invoking via web/API triggers with context payloads
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

After adding the job and your `ANTHROPIC_API_KEY` variable, test by running the job manually from **CI/CD** → **Pipelines**, or trigger it from an MR to let Claude propose updates in a branch and open an MR if needed.

To run on Amazon Bedrock or Google Vertex AI instead of the Claude API, see the [Using with Amazon Bedrock & Google Vertex AI](#using-with-amazon-bedrock-%26-google-vertex-ai) section below for authentication and environment setup.

### [​](#manual-setup-recommended-for-production) Manual setup (recommended for production)

If you prefer a more controlled setup or need enterprise providers:

1. **Configure provider access**:
   * **Claude API**: Create and store `ANTHROPIC_API_KEY` as a masked CI/CD variable
   * **Amazon Bedrock**: **Configure GitLab** → **AWS OIDC** and create an IAM role for Bedrock
   * **Google Vertex AI**: **Configure Workload Identity Federation for GitLab** → **GCP**
2. **Add project credentials for GitLab API operations**:
   * Use `CI_JOB_TOKEN` by default, or create a Project Access Token with `api` scope
   * Store as `GITLAB_ACCESS_TOKEN` (masked) if using a PAT
3. **Add the Claude job to `.gitlab-ci.yml`** (see examples below)
4. **(Optional) Enable mention-driven triggers**:
   * Add a project webhook for “Comments (notes)” to your event listener (if you use one)
   * Have the listener call the pipeline trigger API with variables like `AI_FLOW_INPUT` and `AI_FLOW_CONTEXT` when a comment contains `@claude`

## [​](#example-use-cases) Example use cases

### [​](#turn-issues-into-mrs) Turn issues into MRs

In an issue comment:

```
@claude implement this feature based on the issue description
```

Claude analyzes the issue and codebase, writes changes in a branch, and opens an MR for review.

### [​](#get-implementation-help) Get implementation help

In an MR discussion:

```
@claude suggest a concrete approach to cache the results of this API call
```

Claude proposes changes, adds code with appropriate caching, and updates the MR.

### [​](#fix-bugs-quickly) Fix bugs quickly

In an issue or MR comment:

```
@claude fix the TypeError in the user dashboard component
```

Claude locates the bug, implements a fix, and updates the branch or opens a new MR.

## [​](#using-with-amazon-bedrock-&-google-vertex-ai) Using with Amazon Bedrock & Google Vertex AI

For enterprise environments, you can run Claude Code entirely on your cloud infrastructure with the same developer experience.

* Amazon Bedrock
* Google Vertex AI

### [​](#prerequisites) Prerequisites

Before setting up Claude Code with Amazon Bedrock, you need:

1. An AWS account with Amazon Bedrock access to the desired Claude models
2. GitLab configured as an OIDC identity provider in AWS IAM
3. An IAM role with Bedrock permissions and a trust policy restricted to your GitLab project/refs
4. GitLab CI/CD variables for role assumption:
   * `AWS_ROLE_TO_ASSUME` (role ARN)
   * `AWS_REGION` (Bedrock region)

### [​](#setup-instructions) Setup instructions

Configure AWS to allow GitLab CI jobs to assume an IAM role via OIDC (no static keys).**Required setup:**

1. Enable Amazon Bedrock and request access to your target Claude models
2. Create an IAM OIDC provider for GitLab if not already present
3. Create an IAM role trusted by the GitLab OIDC provider, restricted to your project and protected refs
4. Attach least-privilege permissions for Bedrock invoke APIs

**Required values to store in CI/CD variables:**

* `AWS_ROLE_TO_ASSUME`
* `AWS_REGION`

Add variables in Settings → CI/CD → Variables:

```