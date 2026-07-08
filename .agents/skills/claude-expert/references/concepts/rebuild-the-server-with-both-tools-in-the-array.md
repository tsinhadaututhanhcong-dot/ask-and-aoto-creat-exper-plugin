---
type: Reference
title: Rebuild the server with both tools in the array
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Rebuild the server with both tools in the array
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature, get_precipitation_chance],
)
```

Every tool in this array consumes context window space on every turn. If you’re defining dozens of tools, see [tool search](/docs/en/agent-sdk/tool-search) to load them on demand instead.

### [​](#add-tool-annotations) Add tool annotations

[Tool annotations](https://modelcontextprotocol.io/docs/concepts/tools#tool-annotations) are optional metadata describing how a tool behaves. Pass them as the fifth argument to `tool()` helper in TypeScript or via the `annotations` keyword argument for the `@tool` decorator in Python. All hint fields are Booleans.

| Field | Default | Meaning |
| --- | --- | --- |
| `readOnlyHint` | `false` | Tool does not modify its environment. Controls whether the tool can be called in parallel with other read-only tools. |
| `destructiveHint` | `true` | Tool may perform destructive updates. Informational only. |
| `idempotentHint` | `false` | Repeated calls with the same arguments have no additional effect. Informational only. |
| `openWorldHint` | `true` | Tool reaches systems outside your process. Informational only. |

Annotations are metadata, not enforcement. A tool marked `readOnlyHint: true` can still write to disk if that’s what the handler does. Keep the annotation accurate to the handler.
This example adds `readOnlyHint` to the `get_temperature` tool from the [weather tool example](#weather-tool-example).

Python

TypeScript

```
from claude_agent_sdk import tool, ToolAnnotations


@tool(
    "get_temperature",
    "Get the current temperature at a location",
    {"latitude": float, "longitude": float},
    annotations=ToolAnnotations(
        readOnlyHint=True
    ),  # Lets Claude batch this with other read-only calls
)
async def get_temperature(args):
    return {"content": [{"type": "text", "text": "..."}]}
```

See `ToolAnnotations` in the [TypeScript](/docs/en/agent-sdk/typescript#toolannotations) or [Python](/docs/en/agent-sdk/python#toolannotations) reference.

## [​](#control-tool-access) Control tool access

The [weather tool example](#weather-tool-example) registered a server and listed tools in `allowedTools`. This section covers how tool names are constructed and how to scope access when you have multiple tools or want to restrict built-ins.

### [​](#tool-name-format) Tool name format

When MCP tools are exposed to Claude, their names follow a specific format:

* Pattern: `mcp__{server_name}__{tool_name}`
* Example: A tool named `get_temperature` in server `weather` becomes `mcp__weather__get_temperature`

### [​](#configure-allowed-tools) Configure allowed tools

The `tools` option and the allowed/disallowed lists affect two layers: availability, which controls whether a tool appears in Claude’s context, and permission, which controls whether a call is approved once Claude attempts it. `tools` and bare-name `disallowedTools` entries change availability. `allowedTools` and scoped `disallowedTools` rules change permission only.

| Option | Layer | Effect |
| --- | --- | --- |
| `tools: ["Read", "Grep"]` | Availability | Only the listed built-ins are in Claude’s context. Unlisted built-ins are removed. MCP tools are unaffected. |
| `tools: []` | Availability | All built-ins are removed. Claude can only use your MCP tools. |
| allowed tools | Permission | Listed tools run without a permission prompt. Unlisted tools remain available; calls go through the [permission flow](/docs/en/agent-sdk/permissions). |
| disallowed tools | Both | A bare tool name such as `"Bash"` removes the tool from Claude’s context, the same as omitting it from `tools`. A scoped rule such as `"Bash(rm *)"` leaves the tool in context and denies only matching calls. |

To remove a built-in entirely, omit it from `tools` or list its bare name in `disallowedTools` (Python: `disallowed_tools`); both keep the tool out of context so Claude never attempts it. A scoped `disallowedTools` rule blocks matching calls but leaves the tool visible, so Claude may waste a turn trying it. See [Configure permissions](/docs/en/agent-sdk/permissions) for the full evaluation order.

## [​](#handle-errors) Handle errors

How your handler reports errors determines whether the agent loop continues or stops:

| What happens | Result |
| --- | --- |
| Handler throws an uncaught exception | Agent loop stops. Claude never sees the error, and the `query` call fails. |
| Handler catches the error and returns `isError: true` (TS) / `"is_error": True` (Python) | Agent loop continues. Claude sees the error as data and can retry, try a different tool, or explain the failure. |

The example below catches two kinds of failures inside the handler instead of letting them throw. A non-200 HTTP status is caught from the response and returned as an error result. A network error or invalid JSON is caught by the surrounding `try/except` (Python) or `try/catch` (TypeScript) and also returned as an error result. In both cases the handler returns normally and the agent loop continues.

Python

TypeScript

```
import json
import httpx
from typing import Any


@tool(
    "fetch_data",
    "Fetch data from an API",
    {"endpoint": str},  # Simple schema
)
async def fetch_data(args: dict[str, Any]) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(args["endpoint"])
            if response.status_code != 200:
                # Return the failure as a tool result so Claude can react to it.
                # is_error marks this as a failed call rather than odd-looking data.
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"API error: {response.status_code} {response.reason_phrase}",
                        }
                    ],
                    "is_error": True,
                }

            data = response.json()
            return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
    except Exception as e:
        # Catching here keeps the agent loop alive. An uncaught exception
        # would end the whole query() call.
        return {
            "content": [{"type": "text", "text": f"Failed to fetch data: {str(e)}"}],
            "is_error": True,
        }
```

## [​](#return-images-and-resources) Return images and resources

The `content` array in a tool result accepts `text`, `image`, `audio`, `resource`, and `resource_link` blocks. You can mix them in the same response. Audio blocks are saved to disk and Claude receives a text block with the saved file path. Resource link blocks are converted to a text block containing the link’s name, URI, and description.

### [​](#images) Images

An image block carries the image bytes inline, encoded as base64. There is no URL field. To return an image that lives at a URL, fetch it in the handler, read the response bytes, and base64-encode them before returning. The result is processed as visual input.

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `"image"` |  |
| `data` | `string` | Base64-encoded bytes. Raw base64 only, no `data:image/...;base64,` prefix |
| `mimeType` | `string` | Required. For example `image/png`, `image/jpeg`, `image/webp`, `image/gif` |

Python

TypeScript

```
import base64
import httpx