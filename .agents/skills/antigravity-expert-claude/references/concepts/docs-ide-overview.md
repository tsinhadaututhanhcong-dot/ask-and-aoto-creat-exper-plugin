---
type: Reference
title: IDE Overview
date_created: 2026-07-01
source_url: https://antigravity.google/docs/ide/overview
description: Editor integrations and features.
tags: [concept, llms-txt, js-rendered]
platform: ide
---

* side\_navigation
* Antigravity IDE
>* Overview

# Antigravity IDE[link](#antigravity-ide)

warning

**Note**: Antigravity IDE is not supported for enterprise customers. To use Antigravity with enterprise configurations, use Antigravity 2.0 or Antigravity CLI.

[Enterprise Setup](/docs/enterprise)

Antigravity IDE is an agentic development environment, evolving anyone to build in the agent-first era. It integrates agents directly into your development workspace, providing them the tools needed to autonomously operate across the editor, terminal, and browser—emphasizing verification and higher-level communication via tasks and artifacts. This capability enables agents to plan and execute more complex, end-to-end software tasks, elevating all aspects of development, from building features, UI iteration, and fixing bugs to research and generating reports.

Main Features

automatic\_cluster

AI-powered IDE keyboard\_arrow\_right

An AI-powered IDE with all of the AI features that developers have come to rely on such as Agent and Tab.automatic\_cluster

Asynchronous Agents keyboard\_arrow\_right

Asynchronous, local agents that can work in parallel on all of your workspaces.automatic\_cluster

Browser Agent keyboard\_arrow\_right

Agent that can actuate the browser for you and to accomplish dev tasks like dashboard reads, SCM actions, UI testing, etc. in the Browser.

## Core Surfaces[link](#core-surfaces)

automatic\_cluster

Editor keyboard\_arrow\_right

A fully-functional AI-powered IDE that maps to a single workspace.automatic\_cluster

Browser keyboard\_arrow\_right

Browser-use agent capabilities to read & actuate on more surfaces beyond just the IDE.

## Key Terms[link](#key-terms)

* **Agent**: The primary AI modality within Antigravity. While the user can work tightly with an Agent within the Editor, they can also have multiple agents working across multiple codebases.
* **Tab**: The other AI modality within Antigravity, specifically within the text editor part of the editor surface. Tab is a more powerful autocomplete helper.
* **Artifacts**: We define an artifact as anything that the agent creates to allow it to get its work done or communicate its accomplishments to the human user. These include rich markdown files, diff views, architecture diagrams, images, browser recordings, etc.

On this Page