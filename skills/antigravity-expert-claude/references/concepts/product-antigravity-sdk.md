---
type: Reference
title: Antigravity SDK
date_created: 2026-07-01
source_url: https://antigravity.google/product/antigravity-sdk
description: Python SDK to program custom agents, tools, MCP integrations, and tasks.
tags: [concept, llms-txt, js-rendered]
platform: sdk
---

# Antigravity SDK

Build AI agents that autonomously read files, run commands, edit code, and more. The Agent SDK gives you the same tools, agent loop, and context management that power Google Antigravity, programmable in Python.

[Download](https://github.com/google-antigravity/antigravity-sdk-python)

bash

content\_copy

```
            pip install google-antigravity
```

## Important

The Google Antigravity SDK relies on a compiled runtime binary that is included in the platform-specific wheels published to [PyPI](https://pypi.org/project/google-antigravity/). Cloning this repository alone is not sufficient to run the SDK. Always install from PyPI with pip install google-antigravity to obtain the binary.

## Unified Tool Experience

Layer custom Python callables, Model Context Protocol (MCP) servers, and reusable agent skills over our built-in filesystem and terminal tools under a single pipeline.

## Focus on Customizing

The SDK abstracts away the complex machinery of running an AI agent—including state management, tool execution, and backend communication—allowing developers to focus on the agent's behavior rather than infrastructure.

## Multimodal Ingestion

Pass rich multimedia file attachments (images, videos, audio, and documents) to the agent alongside textual instruction prompt lists. You can attach assets directly using content classes (perfect for in-memory bytes) or conveniently from a filesystem path (which automatically resolves types and guesses MIME formats).