---
title: Claude Code on Google Vertex AI - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Claude Code on Google Vertex AI - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/google-vertex-ai](https://code.claude.com/docs/en/google-vertex-ai)

## [​](#prerequisites) Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

* A Google Cloud Platform (GCP) account with billing enabled
* A GCP project with Vertex AI API enabled
* Access to desired Claude models (for example, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installed and configured
* Quota allocated in desired GCP region

To sign in with your own Vertex AI credentials, follow [Sign in with Vertex AI](#sign-in-with-vertex-ai) below. To deploy Claude Code across a team, use the [manual setup](#set-up-manually) steps and [pin your model versions](#5-pin-model-versions) before rolling out.

## [​](#sign-in-with-vertex-ai) Sign in with Vertex AI

If you have Google Cloud credentials and want to start using Claude Code through Vertex AI, the login wizard walks you through it. You complete the GCP-side prerequisites once per project; the wizard handles the Claude Code side.

The Vertex AI setup wizard requires Claude Code v2.1.98 or later. Run `claude --version` to check.

1

Enable Claude models in your GCP project

[Enable the Vertex AI API](#1-enable-vertex-ai-api) for your project, then request access to the Claude models you want in the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). See [IAM configuration](#iam-configuration) for the permissions your account needs.

2

Start Claude Code and choose Vertex AI

Run `claude`. At the login prompt, select **3rd-party platform**, then **Google Vertex AI**.

3

Follow the wizard prompts

Choose how you authenticate to Google Cloud: Application Default Credentials from `gcloud`, a service account key file, or credentials already in your environment. The wizard detects your project and region, verifies which Claude models your project can invoke, and lets you pin them. It saves the result to the `env` block of your [user settings file](/docs/en/settings), so you don’t need to export environment variables yourself.

After you’ve signed in, run `/setup-vertex` any time to reopen the wizard and change your credentials, project, region, or model pins.

## [​](#region-configuration) Region configuration

Claude Code supports Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-region, and regional endpoints. Set `CLOUD_ML_REGION` to `global`, a multi-region location such as `eu` or `us`, or a specific region such as `us-east5`. Claude Code selects the correct Vertex AI hostname for each form, including the `aiplatform.eu.rep.googleapis.com` and `aiplatform.us.rep.googleapis.com` hosts for multi-region locations.

Vertex AI may not support the Claude Code default models on every endpoint type. Model availability varies across [specific regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), multi-region locations, and [global endpoints](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). You may need to switch to a supported location or specify a supported model.

## [​](#set-up-manually) Set up manually

To configure Vertex AI through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### [​](#1-enable-vertex-ai-api) 1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

```