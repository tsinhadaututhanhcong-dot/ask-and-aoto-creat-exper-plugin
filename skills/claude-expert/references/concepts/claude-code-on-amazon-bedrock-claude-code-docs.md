---
title: Claude Code on Amazon Bedrock - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Claude Code on Amazon Bedrock - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/amazon-bedrock](https://code.claude.com/docs/en/amazon-bedrock)

## [​](#prerequisites) Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

* An AWS account with Bedrock access enabled
* Access to desired Claude models (for example, Claude Sonnet 4.6) in Bedrock
* AWS CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)
* Appropriate IAM permissions

To sign in with your own Bedrock credentials, follow [Sign in with Bedrock](#sign-in-with-bedrock) below. To deploy Claude Code across a team, use the [manual setup](#set-up-manually) steps and [pin your model versions](#4-pin-model-versions) before rolling out.

## [​](#sign-in-with-bedrock) Sign in with Bedrock

If you have AWS credentials and want to start using Claude Code through Bedrock, the login wizard walks you through it. You complete the AWS-side prerequisites once per account; the wizard handles the Claude Code side.

1

Enable Anthropic models in your AWS account

In the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), open the Model catalog, select an Anthropic model, and submit the use case form. Access is granted immediately after submission. See [Submit use case details](#1-submit-use-case-details) for AWS Organizations and [IAM configuration](#iam-configuration) for the permissions your role needs.

2

Start Claude Code and choose Bedrock

Run `claude`. At the login prompt, select **3rd-party platform**, then **Amazon Bedrock**.

3

Follow the wizard prompts

Choose how you authenticate to AWS: an AWS profile detected from your `~/.aws` directory, a Bedrock API key, an access key and secret, or credentials already in your environment. The wizard picks up your region, verifies which Claude models your account can invoke, and lets you pin them. It saves the result to the `env` block of your [user settings file](/docs/en/settings), so you don’t need to export environment variables yourself.

After you’ve signed in, run `/setup-bedrock` any time to reopen the wizard and change your credentials, region, or model pins.

## [​](#set-up-manually) Set up manually

To configure Bedrock through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### [​](#1-submit-use-case-details) 1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per AWS account.

1. Ensure you have the right IAM permissions described below
2. Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
3. Select an Anthropic model from the **Model catalog**
4. Complete the use case form. Access is granted immediately after submission.

If you use AWS Organizations, you can submit the form once from the management account using the [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). This call requires the `bedrock:PutUseCaseForModelAccess` IAM permission. Approval extends to child accounts automatically.

### [​](#2-configure-aws-credentials) 2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:
**Option A: AWS CLI configuration**

```
aws configure
```

**Option B: Environment variables (access key)**

```
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C: Environment variables (SSO profile)**

```
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D: AWS Management Console credentials**

```
aws login
```

[Learn more](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) about `aws login`.
**Option E: Bedrock API keys**

```
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API keys provide a simpler authentication method without needing full AWS credentials. [Learn more about Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### [​](#advanced-credential-configuration) Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file (see [Settings](/docs/en/settings) for file locations).
These two settings have different trigger conditions:

* **`awsAuthRefresh`**: runs only when Claude Code detects that your AWS credentials are expired, either locally based on their timestamp or when Bedrock returns a credential error, then retries the request with refreshed credentials.
* **`awsCredentialExport`**: runs at session start and on each credential reload, even when the credentials in your AWS default credential provider chain are still valid. Use this when your Bedrock account requires cross-account credentials that differ from the ones the default provider chain would resolve.

##### Example configuration

```
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configuration settings explained

**`awsAuthRefresh`**: Use this for commands that modify the `.aws` directory, such as updating credentials, SSO cache, or config files. The command’s output is displayed to the user, but interactive input isn’t supported. This works well for browser-based SSO flows where the CLI displays a URL or code and you complete authentication in the browser.
**`awsCredentialExport`**: Only use this if you can’t modify `.aws` and must directly return credentials. This command runs whenever credentials need to be refreshed, not only when credentials are expired. Output is captured silently and not shown to the user. The command must output JSON in this format:

```
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value",
    "Expiration": "2026-01-01T00:00:00Z"
  }
}
```

As of Claude Code v2.1.181, the flat output from `aws configure export-credentials --format process` is also accepted, with the same keys at the top level instead of nested under `Credentials`.
`Expiration` is optional. As of Claude Code v2.1.176, when the command returns a valid ISO 8601 `Expiration`, Claude Code caches the credentials until five minutes before that time. Without it, or on earlier versions, credentials are cached for one hour.

### [​](#3-configure-claude-code) 3. Configure Claude Code

Set the following environment variables to enable Bedrock:

```