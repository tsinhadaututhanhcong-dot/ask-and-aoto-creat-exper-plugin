---
title: Define a tool that fetches an image from a URL and returns it to Claude
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Define a tool that fetches an image from a URL and returns it to Claude
@tool("fetch_image", "Fetch an image from a URL and return it to Claude", {"url": str})
async def fetch_image(args):
    async with httpx.AsyncClient() as client:  # Fetch the image bytes
        response = await client.get(args["url"])

    return {
        "content": [
            {
                "type": "image",
                "data": base64.b64encode(response.content).decode(
                    "ascii"
                ),  # Base64-encode the raw bytes
                "mimeType": response.headers.get(
                    "content-type", "image/png"
                ),  # Read MIME type from the response
            }
        ]
    }
```

### [​](#resources) Resources

A resource block embeds a piece of content identified by a URI. The URI is a label for Claude to reference; the actual content rides in the block’s `text` or `blob` field. Use this when your tool produces something that makes sense to address by name later, such as a generated file or a record from an external system.

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `"resource"` |  |
| `resource.uri` | `string` | Identifier for the content. Any URI scheme |
| `resource.text` | `string` | The content, if it’s text. Provide this or `blob`, not both |
| `resource.blob` | `string` | The content base64-encoded, if it’s binary |
| `resource.mimeType` | `string` | Optional |

This example shows a resource block returned from inside a tool handler. The URI `file:///tmp/report.md` is a label that Claude can reference later; the SDK does not read from that path.

TypeScript

Python

```
return {
  content: [
    {
      type: "resource",
      resource: {
        uri: "file:///tmp/report.md", // Label for Claude to reference, not a path the SDK reads
        mimeType: "text/markdown",
        text: "# Report\n..." // The actual content, inline
      }
    }
  ]
};
```

These block shapes come from the MCP `CallToolResult` type. See the [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool-result) for the full definition.

## [​](#return-structured-data) Return structured data

`structuredContent` is an optional JSON object on the result, separate from the `content` array. Use it to return raw values that Claude can read as exact fields instead of parsing them out of a text string or image.
When `structuredContent` is set, Claude receives the JSON plus any image or resource blocks from `content`. Text blocks in `content` are not forwarded, since they are assumed to duplicate the structured data. The example below renders a chart as an image block and returns the data points behind it in `structuredContent` from the same handler.

TypeScript

```
return {
  content: [
    {
      type: "image",
      data: chartPngBuffer.toString("base64"),
      mimeType: "image/png"
    }
  ],
  structuredContent: {
    series: "temperature_2m",
    unit: "fahrenheit",
    points: [62.1, 63.4, 65.0, 64.2]
  }
};
```

The Python `@tool` decorator forwards only `content` and `is_error` from the handler’s return dict. To return `structuredContent` from Python, run a [standalone MCP server](/docs/en/agent-sdk/mcp) instead of an in-process SDK server.

## [​](#example-unit-converter) Example: unit converter

This tool converts values between units of length, temperature, and weight. A user can ask “convert 100 kilometers to miles” or “what is 72°F in Celsius,” and Claude picks the right unit type and units from the request.
It demonstrates two patterns:

* **Enum schemas:** `unit_type` is constrained to a fixed set of values. In TypeScript, use `z.enum()`. In Python, the dict schema doesn’t support enums, so the full JSON Schema dict is required.
* **Unsupported input handling:** when a conversion pair isn’t found, the handler returns `isError: true` so Claude can tell the user what went wrong rather than treating a failure as a normal result.

Python

TypeScript

```
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server