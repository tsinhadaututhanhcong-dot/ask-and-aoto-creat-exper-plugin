---
type: Reference
title: Artifact Review
date_created: 2026-07-01
source_url: https://antigravity.google/docs/artifact-review
description: Interface for approving agent plans and tasks.
tags: [concept, llms-txt, js-rendered]
platform: antigravity-2.0
---

* side\_navigation
* Antigravity 2.0
>* Settings
>* Artifact Review

# Artifact Review[link](#artifact-review)

When starting a new Agent conversation, you can choose between two primary execution modes that determine how changes are proposed and reviewed:

* **Planning Mode**: The agent plans thoroughly before executing tasks. In this mode, the agent organizes its work in [task groups](/docs/task-groups), produces structured implementation plans called [Artifacts](/docs/artifacts), and thoroughly researches the codebase for optimal quality.
* **Fast Mode**: The agent executes tasks directly without a dedicated planning phase. Use this for simple, highly localized tasks that can be completed quickly, such as variable renaming, running a specific bash command, or small refactors.

When working in **Planning Mode**, the Artifact Review Policy controls how you interact with and approve these plans before changes are made to your codebase.

## Artifact Review Policy[link](#artifact-review-policy)

You can customize the review workflow in the **Agent** tab of the Settings pane. Choose between two policies:

### 1. Request Review (Recommended)[link](#1-request-review-recommended)

The agent always halts and requests your explicit approval before proceeding with proposed changes.

* When the agent generates an implementation plan or code diff, it will pause execution and notify you.
* This allows you to thoroughly review the proposed changes, add inline comments, and verify the plan in your workspace.
* Once you are satisfied, you can approve the plan to let the agent proceed.
![Settings Review Policy Manual](assets/image/docs/agent/settings-review-policy-manual.png)

### 2. Always Proceed[link](#2-always-proceed)

The agent never halts for manual review and immediately proceeds with executing its plans.

* When the agent decides to request a review, it will immediately bypass the pause and continue with the implementation.
* Use this if you want a fully autonomous workflow and do not need to manually verify plans before code is modified.
![Settings Review Policy Proceed](assets/image/docs/agent/settings-review-policy-proceed.png)

On this Page