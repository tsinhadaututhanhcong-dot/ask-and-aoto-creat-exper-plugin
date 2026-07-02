---
title: For Google Vertex AI:
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: integration
---

# For Google Vertex AI:
- GCP_WORKLOAD_IDENTITY_PROVIDER
- GCP_SERVICE_ACCOUNT
- CLOUD_ML_REGION (for example, us-east5)
```

Use the Google Vertex AI job example above to authenticate without storing keys.

## [​](#configuration-examples) Configuration examples

Below are ready-to-use snippets you can adapt to your pipeline.

### [​](#basic-gitlab-ci-yml-claude-api) Basic .gitlab-ci.yml (Claude API)

```
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
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
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code will use ANTHROPIC_API_KEY from CI/CD variables
```

### [​](#amazon-bedrock-job-example-oidc) Amazon Bedrock job example (OIDC)

**Prerequisites:**

* Amazon Bedrock enabled with access to your chosen Claude model(s)
* GitLab OIDC configured in AWS with a role that trusts your GitLab project and refs
* IAM role with Bedrock permissions (least privilege recommended)

**Required CI/CD variables:**

* `AWS_ROLE_TO_ASSUME`: ARN of the IAM role for Bedrock access
* `AWS_REGION`: Bedrock region (for example, `us-west-2`)

```
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Exchange GitLab OIDC token for AWS credentials
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

Model IDs for Bedrock include region-specific prefixes (for example, `us.anthropic.claude-sonnet-4-6`). Pass the desired model via your job configuration or prompt if your workflow supports it.

### [​](#google-vertex-ai-job-example-workload-identity-federation) Google Vertex AI job example (Workload Identity Federation)

**Prerequisites:**

* Vertex AI API enabled in your GCP project
* Workload Identity Federation configured to trust GitLab OIDC
* A service account with Vertex AI permissions

**Required CI/CD variables:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Full provider resource name
* `GCP_SERVICE_ACCOUNT`: Service account email
* `CLOUD_ML_REGION`: Vertex region (for example, `us-east5`)

```
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git && apt-get clean
    - curl -fsSL https://claude.ai/install.sh | bash
    # Authenticate to Google Cloud via WIF (no downloaded keys)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Review and update code as requested'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

With Workload Identity Federation, you do not need to store service account keys. Use repository-specific trust conditions and least-privilege service accounts.

## [​](#best-practices) Best practices

### [​](#claude-md-configuration) CLAUDE.md configuration

Create a `CLAUDE.md` file at the repository root to define coding standards, review criteria, and project-specific rules. Claude reads this file during runs and follows your conventions when proposing changes.

### [​](#security-considerations) Security considerations

**Never commit API keys or cloud credentials to your repository**. Always use GitLab CI/CD variables:

* Add `ANTHROPIC_API_KEY` as a masked variable (and protect it if needed)
* Use provider-specific OIDC where possible (no long-lived keys)
* Limit job permissions and network egress
* Review Claude’s MRs like any other contributor

### [​](#optimizing-performance) Optimizing performance

* Keep `CLAUDE.md` focused and concise
* Provide clear issue/MR descriptions to reduce iterations
* Configure sensible job timeouts to avoid runaway runs
* Cache npm and package installs in runners where possible

### [​](#ci-costs) CI costs

When using Claude Code with GitLab CI/CD, be aware of associated costs:

* **GitLab Runner time**:
  + Claude runs on your GitLab runners and consumes compute minutes
  + See your GitLab plan’s runner billing for details
* **API costs**:
  + Each Claude interaction consumes tokens based on prompt and response size
  + Token usage varies by task complexity and codebase size
  + See [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) for details
* **Cost optimization tips**:
  + Use specific `@claude` commands to reduce unnecessary turns
  + Set appropriate `max_turns` and job timeout values
  + Limit concurrency to control parallel runs

## [​](#security-and-governance) Security and governance

* Each job runs in an isolated container with restricted network access
* Claude’s changes flow through MRs so reviewers see every diff
* Branch protection and approval rules apply to AI-generated code
* Claude Code uses workspace-scoped permissions to constrain writes
* Costs remain under your control because you bring your own provider credentials

## [​](#troubleshooting) Troubleshooting

### [​](#claude-not-responding-to-@claude-commands) Claude not responding to @claude commands

* Verify your pipeline is being triggered (manually, MR event, or via a note event listener/webhook)
* Ensure CI/CD variables (`ANTHROPIC_API_KEY` or cloud provider settings) are present and unmasked
* Check that the comment contains `@claude` (not `/claude`) and that your mention trigger is configured

### [​](#job-can’t-write-comments-or-open-mrs) Job can’t write comments or open MRs

* Ensure `CI_JOB_TOKEN` has sufficient permissions for the project, or use a Project Access Token with `api` scope
* Check the `mcp__gitlab` tool is enabled in `--allowedTools`
* Confirm the job runs in the context of the MR or has enough context via `AI_FLOW_*` variables

### [​](#authentication-errors) Authentication errors

* **For Claude API**: Confirm `ANTHROPIC_API_KEY` is valid and unexpired
* **For Bedrock/Vertex**: Verify OIDC/WIF configuration, role impersonation, and secret names; confirm region and model availability

## [​](#advanced-configuration) Advanced configuration

### [​](#common-parameters-and-variables) Common parameters and variables

Claude Code supports these commonly used inputs:

* `prompt` / `prompt_file`: Provide instructions inline (`-p`) or via a file
* `max_turns`: Limit the number of back-and-forth iterations
* `timeout_minutes`: Limit total execution time
* `ANTHROPIC_API_KEY`: Required for the Claude API (not used for Bedrock/Vertex)
* Provider-specific environment: `AWS_REGION`, project/region vars for Vertex

Exact flags and parameters may vary by version of `@anthropic-ai/claude-code`. Run `claude --help` in your job to see supported options.

### [​](#customizing-claude’s-behavior) Customizing Claude’s behavior

You can guide Claude in two primary ways:

1. **CLAUDE.md**: Define coding standards, security requirements, and project conventions. Claude reads this during runs and follows your rules.
2. **Custom prompts**: Pass task-specific instructions via `prompt`/`prompt_file` in the job. Use different prompts for different jobs (for example, review, implement, refactor).

Was this page helpful?

YesNo

[GitHub Enterprise Server](/docs/en/github-enterprise-server)[Claude Code in Slack](/docs/en/slack)

⌘I

---