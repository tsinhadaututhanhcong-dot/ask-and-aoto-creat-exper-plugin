---
type: Reference
title: Models
date_created: 2026-07-01
source_url: https://antigravity.google/docs/models
description: Supported LLM classes (Pro, Flash, etc.).
tags: [concept, llms-txt, js-rendered]
platform: shared
---

* side\_navigation
* Antigravity 2.0
>* Models

# Models[link](#models)

## Reasoning Model[link](#reasoning-model)

For the core reasoning model, Antigravity offers leading frontier models. Availability depends on your plan:

| Model | Standard | Google AI Pro | Google AI Ultra | Enterprise |
| --- | --- | --- | --- | --- |
| Gemini 3.5 Flash | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.1 Pro | ✅ | ✅ | ✅ | ✅ |
| Claude Sonnet 4.6 (thinking) | ❌ | ❌ | ✅ | ❌ |
| Claude Opus 4.6 (thinking) | ❌ | ❌ | ✅ | ❌ |
| GPT-OSS-120b | ❌ | ❌ | ✅ | ❌ |

Users can select which reasoning model they want to use within the model selector drop-down under the conversation prompt box:

![Model Selector Drop Down](/assets/image/docs/model-selector.png)

The choice of reasoning model is sticky between user messages within a conversation, so if you change the reasoning model while the Agent is running, it will continue to use the previously selected reasoning model until it has completed its steps for that user turn (or until you cancel the current execution).

Learn more about reasoning model rate limits in [our plans page](/docs/plans).

## Additional Models[link](#additional-models)

Antigravity uses a number of other models for various parts of the stack that are not customizable:

* **Nano Banana 2**: Used by the generative image tool when the Agent wants

to produce a UI mockup, needs images to populate a web page or application, generate system or architecture diagrams, or other generative image tasks.

On this Page