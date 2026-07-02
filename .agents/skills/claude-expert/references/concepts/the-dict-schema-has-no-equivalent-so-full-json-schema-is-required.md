---
title: The dict schema has no equivalent, so full JSON Schema is required.
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# The dict schema has no equivalent, so full JSON Schema is required.
@tool(
    "convert_units",
    "Convert a value from one unit to another",
    {
        "type": "object",
        "properties": {
            "unit_type": {
                "type": "string",
                "enum": ["length", "temperature", "weight"],
                "description": "Category of unit",
            },
            "from_unit": {
                "type": "string",
                "description": "Unit to convert from, e.g. kilometers, fahrenheit, pounds",
            },
            "to_unit": {"type": "string", "description": "Unit to convert to"},
            "value": {"type": "number", "description": "Value to convert"},
        },
        "required": ["unit_type", "from_unit", "to_unit", "value"],
    },
)
async def convert_units(args: dict[str, Any]) -> dict[str, Any]:
    conversions = {
        "length": {
            "kilometers_to_miles": lambda v: v * 0.621371,
            "miles_to_kilometers": lambda v: v * 1.60934,
            "meters_to_feet": lambda v: v * 3.28084,
            "feet_to_meters": lambda v: v * 0.3048,
        },
        "temperature": {
            "celsius_to_fahrenheit": lambda v: (v * 9) / 5 + 32,
            "fahrenheit_to_celsius": lambda v: (v - 32) * 5 / 9,
            "celsius_to_kelvin": lambda v: v + 273.15,
            "kelvin_to_celsius": lambda v: v - 273.15,
        },
        "weight": {
            "kilograms_to_pounds": lambda v: v * 2.20462,
            "pounds_to_kilograms": lambda v: v * 0.453592,
            "grams_to_ounces": lambda v: v * 0.035274,
            "ounces_to_grams": lambda v: v * 28.3495,
        },
    }

    key = f"{args['from_unit']}_to_{args['to_unit']}"
    fn = conversions.get(args["unit_type"], {}).get(key)

    if not fn:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Unsupported conversion: {args['from_unit']} to {args['to_unit']}",
                }
            ],
            "is_error": True,
        }

    result = fn(args["value"])
    return {
        "content": [
            {
                "type": "text",
                "text": f"{args['value']} {args['from_unit']} = {result:.4f} {args['to_unit']}",
            }
        ]
    }


converter_server = create_sdk_mcp_server(
    name="converter",
    version="1.0.0",
    tools=[convert_units],
)
```

Once the server is defined, pass it to `query` the same way as the weather example. This example sends three different prompts in a loop to show the same tool handling different unit types. For each response, it inspects `AssistantMessage` objects (which contain the tool calls Claude made during that turn) and prints each `ToolUseBlock` before printing the final `ResultMessage` text. This lets you see when Claude is using the tool versus answering from its own knowledge.

Python

TypeScript

```
import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    ResultMessage,
    AssistantMessage,
    ToolUseBlock,
)


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"converter": converter_server},
        allowed_tools=["mcp__converter__convert_units"],
    )

    prompts = [
        "Convert 100 kilometers to miles.",
        "What is 72°F in Celsius?",
        "How many pounds is 5 kilograms?",
    ]

    for prompt in prompts:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        print(f"[tool call] {block.name}({block.input})")
            elif isinstance(message, ResultMessage) and message.subtype == "success":
                print(f"Q: {prompt}\nA: {message.result}\n")


asyncio.run(main())
```

## [​](#next-steps) Next steps

Custom tools wrap async functions in a standard interface. You can mix the patterns on this page in the same server: a single server can hold a database tool, an API gateway tool, and an image renderer alongside each other.
From here:

* If your server grows to dozens of tools, see [tool search](/docs/en/agent-sdk/tool-search) to defer loading them until Claude needs them.
* To connect to external MCP servers (filesystem, GitHub, Slack) instead of building your own, see [Connect MCP servers](/docs/en/agent-sdk/mcp).
* To control which tools run automatically versus requiring approval, see [Configure permissions](/docs/en/agent-sdk/permissions).

## [​](#related-documentation) Related documentation

* [TypeScript SDK Reference](/docs/en/agent-sdk/typescript)
* [Python SDK Reference](/docs/en/agent-sdk/python)
* [MCP Documentation](https://modelcontextprotocol.io)
* [SDK Overview](/docs/en/agent-sdk/overview)

Was this page helpful?

YesNo

[Get structured output from agents](/docs/en/agent-sdk/structured-outputs)[Connect to external tools with MCP](/docs/en/agent-sdk/mcp)

⌘I

---