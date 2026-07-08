---
type: Reference
title: Required workaround: dummy hook keeps the stream open for can_use_tool
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Required workaround: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}


async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

## [​](#limitations) Limitations

* **Subagents**: `AskUserQuestion` is not currently available in subagents spawned via the Agent tool
* **Question limits**: each `AskUserQuestion` call supports 1-4 questions with 2-4 options each

## [​](#other-ways-to-get-user-input) Other ways to get user input

The `canUseTool` callback and `AskUserQuestion` tool cover most approval and clarification scenarios, but the SDK offers other ways to get input from users:

### [​](#streaming-input) Streaming input

Use [streaming input](/docs/en/agent-sdk/streaming-vs-single-mode) when you need to:

* **Interrupt the agent mid-task**: send a cancel signal or change direction while Claude is working
* **Provide additional context**: add information Claude needs without waiting for it to ask
* **Build chat interfaces**: let users send follow-up messages during long-running operations

Streaming input is ideal for conversational UIs where users interact with the agent throughout execution, not just at approval checkpoints.

### [​](#custom-tools) Custom tools

Use [custom tools](/docs/en/agent-sdk/custom-tools) when you need to:

* **Collect structured input**: build forms, wizards, or multi-step workflows that go beyond `AskUserQuestion`’s multiple-choice format
* **Integrate external approval systems**: connect to existing ticketing, workflow, or approval platforms
* **Implement domain-specific interactions**: create tools tailored to your application’s needs, like code review interfaces or deployment checklists

Custom tools give you full control over the interaction, but require more implementation work than using the built-in `canUseTool` callback.

## [​](#related-resources) Related resources

* [Configure permissions](/docs/en/agent-sdk/permissions): set up permission modes and rules
* [Control execution with hooks](/docs/en/agent-sdk/hooks): run custom code at key points in the agent lifecycle
* [TypeScript SDK reference](/docs/en/agent-sdk/typescript#canusetool): full canUseTool API documentation

Was this page helpful?

YesNo

[Streaming Input](/docs/en/agent-sdk/streaming-vs-single-mode)[Stream responses in real-time](/docs/en/agent-sdk/streaming-output)

⌘I

---