---
title: Give Claude custom tools - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Give Claude custom tools - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/custom-tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)

Custom tools extend the Agent SDK by letting you define your own functions that Claude can call during a conversation. Using the SDK’s in-process MCP server, you can give Claude access to databases, external APIs, domain-specific logic, or any other capability your application needs.
This guide covers how to define tools with input schemas and handlers, bundle them into an MCP server, pass them to `query`, and control which tools Claude can access. It also covers error handling, tool annotations, and returning non-text content like images.

## [​](#quick-reference) Quick reference

| If you want to… | Do this |
| --- | --- |
| Define a tool | Use [`@tool`](/docs/en/agent-sdk/python#tool) (Python) or [`tool()`](/docs/en/agent-sdk/typescript#tool) (TypeScript) with a name, description, schema, and handler. See [Create a custom tool](#create-a-custom-tool). |
| Register a tool with Claude | Wrap in `create_sdk_mcp_server` / `createSdkMcpServer` and pass to `mcpServers` in `query()`. See [Call a custom tool](#call-a-custom-tool). |
| Pre-approve a tool | Add to your allowed tools. See [Configure allowed tools](#configure-allowed-tools). |
| Remove a built-in tool from Claude’s context | Pass a `tools` array listing only the built-ins you want. See [Configure allowed tools](#configure-allowed-tools). |
| Let Claude call tools in parallel | Set `readOnlyHint: true` on tools with no side effects. See [Add tool annotations](#add-tool-annotations). |
| Handle errors without stopping the loop | Return `isError: true` instead of throwing. See [Handle errors](#handle-errors). |
| Return images or files | Use `image` or `resource` blocks in the content array. See [Return images and resources](#return-images-and-resources). |
| Return a machine-readable JSON result | Set `structuredContent` on the result. See [Return structured data](#return-structured-data). |
| Scale to many tools | Use [tool search](/docs/en/agent-sdk/tool-search) to load tools on demand. |

## [​](#create-a-custom-tool) Create a custom tool

A tool is defined by four parts, passed as arguments to the [`tool()`](/docs/en/agent-sdk/typescript#tool) helper in TypeScript or the [`@tool`](/docs/en/agent-sdk/python#tool) decorator in Python:

* **Name:** a unique identifier Claude uses to call the tool.
* **Description:** what the tool does. Claude reads this to decide when to call it.
* **Input schema:** the arguments Claude must provide. In TypeScript this is always a [Zod schema](https://zod.dev/), and the handler’s `args` are typed from it automatically. In Python this is a dict mapping names to types, like `{"latitude": float}`, which the SDK converts to JSON Schema for you. The Python decorator also accepts a full [JSON Schema](https://json-schema.org/understanding-json-schema/about) dict directly when you need enums, ranges, optional fields, or nested objects.
* **Handler:** the async function that runs when Claude calls the tool. It receives the validated arguments and must return an object with:
  + `content` (required): an array of result blocks, each with a `type` of `"text"`, `"image"`, `"audio"`, `"resource"`, or `"resource_link"`. See [Return images and resources](#return-images-and-resources) for non-text blocks.
  + `structuredContent` (optional): a JSON object holding the result as machine-readable data, returned alongside `content`. See [Return structured data](#return-structured-data).
  + `isError` (optional): set to `true` to signal a tool failure so Claude can react to it. See [Handle errors](#handle-errors).

After defining a tool, wrap it in a server with [`createSdkMcpServer`](/docs/en/agent-sdk/typescript#createsdkmcpserver) (TypeScript) or [`create_sdk_mcp_server`](/docs/en/agent-sdk/python#create_sdk_mcp_server) (Python). The server runs in-process inside your application, not as a separate process.

### [​](#weather-tool-example) Weather tool example

This example defines a `get_temperature` tool and wraps it in an MCP server. It only sets up the tool; to pass it to `query` and run it, see [Call a custom tool](#call-a-custom-tool) below.

Python

TypeScript

```
from typing import Any
import httpx
from claude_agent_sdk import tool, create_sdk_mcp_server