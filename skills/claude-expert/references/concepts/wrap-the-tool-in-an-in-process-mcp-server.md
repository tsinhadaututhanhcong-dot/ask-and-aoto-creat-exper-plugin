---
type: Reference
title: Wrap the tool in an in-process MCP server
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Wrap the tool in an in-process MCP server
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature],
)
```

See the [`tool()`](/docs/en/agent-sdk/typescript#tool) TypeScript reference or the [`@tool`](/docs/en/agent-sdk/python#tool) Python reference for full parameter details, including JSON Schema input formats and return value structure.

To make a parameter optional: in TypeScript, add `.default()` to the Zod field. In Python, the dict schema treats every key as required, so leave the parameter out of the schema, mention it in the description string, and read it with `args.get()` in the handler. The [`get_precipitation_chance` tool below](#add-more-tools) shows both patterns.

### [​](#call-a-custom-tool) Call a custom tool

Pass the MCP server you created to `query` via the `mcpServers` option. The key in `mcpServers` becomes the `{server_name}` segment in each tool’s fully qualified name: `mcp__{server_name}__{tool_name}`. List that name in `allowedTools` so the tool runs without a permission prompt.
These snippets reuse the `weatherServer` from the [example above](#weather-tool-example) to ask Claude what the weather is in a specific location.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_temperature"],
    )

    async for message in query(
        prompt="What's the temperature in San Francisco?",
        options=options,
    ):
        # ResultMessage is the final message after all tool calls complete
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

### [​](#add-more-tools) Add more tools

A server holds as many tools as you list in its `tools` array. With more than one tool on a server, you can list each one in `allowedTools` individually or use the wildcard `mcp__weather__*` to cover every tool the server exposes.
The example below adds a second tool, `get_precipitation_chance`, to the `weatherServer` from the [weather tool example](#weather-tool-example) and rebuilds it with both tools in the array.

Python

TypeScript

```