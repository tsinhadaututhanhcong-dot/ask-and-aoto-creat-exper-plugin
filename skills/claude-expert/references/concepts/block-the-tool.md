---
title: Block the tool
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Block the tool
return PermissionResultDeny(message="User rejected this action")
```

Beyond allowing or denying, you can modify the tool’s input or provide context that helps Claude adjust its approach:

* **Approve**: let the tool execute as Claude requested
* **Approve with changes**: modify the input before execution (e.g., sanitize paths, add constraints)
* **Approve and remember**: echo a suggested permission rule back so matching calls skip the prompt next time
* **Reject**: block the tool and tell Claude why
* **Suggest alternative**: block but guide Claude toward what the user wants instead
* **Redirect entirely**: use [streaming input](/docs/en/agent-sdk/streaming-vs-single-mode) to send Claude a completely new instruction

* Approve
* Approve with changes
* Approve and remember
* Reject
* Suggest alternative
* Redirect entirely

The user approves the action as-is. Pass through the `input` from your callback unchanged and the tool executes exactly as Claude requested.

Python

TypeScript

```
async def can_use_tool(tool_name, input_data, context):
    print(f"Claude wants to use {tool_name}")
    approved = await ask_user("Allow this action?")

    if approved:
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User declined")
```

The user approves but wants to modify the request first. You can change the input before the tool executes. Claude sees the result but isn’t told you changed anything. Useful for sanitizing parameters, adding constraints, or scoping access.

Python

TypeScript

```
async def can_use_tool(tool_name, input_data, context):
    if tool_name == "Bash":
        # User approved, but scope all commands to sandbox
        sandboxed_input = {**input_data}
        sandboxed_input["command"] = input_data["command"].replace(
            "/tmp", "/tmp/sandbox"
        )
        return PermissionResultAllow(updated_input=sandboxed_input)
    return PermissionResultAllow(updated_input=input_data)
```

The user approves and doesn’t want to be asked again for this kind of call. The third callback argument carries `suggestions`, an array of ready-made [`PermissionUpdate`](/docs/en/agent-sdk/typescript#permissionupdate) entries. Echo one back in `updatedPermissions` to apply it. A suggestion with the `localSettings` destination writes the rule to `.claude/settings.local.json` so future sessions skip the prompt for matching calls.The Python example requires `claude-agent-sdk` 0.1.80 or later.

Python

TypeScript

```
async def can_use_tool(tool_name, input_data, context):
    choice = await ask_user(f"Allow {tool_name}?", ["once", "always", "no"])

    if choice == "always":
        persist = [
            s for s in context.suggestions if s.destination == "localSettings"
        ]
        return PermissionResultAllow(
            updated_input=input_data, updated_permissions=persist
        )
    if choice == "once":
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User declined")
```

The user doesn’t want this action to happen. Block the tool and provide a message explaining why. Claude sees this message and may try a different approach.

Python

TypeScript

```
async def can_use_tool(tool_name, input_data, context):
    approved = await ask_user(f"Allow {tool_name}?")

    if not approved:
        return PermissionResultDeny(message="User rejected this action")
    return PermissionResultAllow(updated_input=input_data)
```

The user doesn’t want this specific action, but has a different idea. Block the tool and include guidance in your message. Claude will read this and decide how to proceed based on your feedback.

Python

TypeScript

```
async def can_use_tool(tool_name, input_data, context):
    if tool_name == "Bash" and "rm" in input_data.get("command", ""):
        # User doesn't want to delete, suggest archiving instead
        return PermissionResultDeny(
            message="User doesn't want to delete files. They asked if you could compress them into an archive instead."
        )
    return PermissionResultAllow(updated_input=input_data)
```

For a complete change of direction (not just a nudge), use [streaming input](/docs/en/agent-sdk/streaming-vs-single-mode) to send Claude a new instruction directly. This bypasses the current tool request and gives Claude entirely new instructions to follow.

## [​](#handle-clarifying-questions) Handle clarifying questions

When Claude needs more direction on a task with multiple valid approaches, it calls the `AskUserQuestion` tool. This triggers your `canUseTool` callback with `toolName` set to `AskUserQuestion`. The input contains Claude’s questions as multiple-choice options, which you display to the user and return their selections.

Clarifying questions are especially common in [`plan` mode](/docs/en/agent-sdk/permissions#plan-mode-plan), where Claude explores the codebase and asks questions before proposing a plan. This makes plan mode ideal for interactive workflows where you want Claude to gather requirements before making changes.

The following steps show how to handle clarifying questions:

1

Pass a canUseTool callback

Pass a `canUseTool` callback in your query options. By default, `AskUserQuestion` is available. If you specify a `tools` array to restrict Claude’s capabilities (for example, a read-only agent with only `Read`, `Glob`, and `Grep`), include `AskUserQuestion` in that array. Otherwise, Claude won’t be able to ask clarifying questions:

Python

TypeScript

```
async for message in query(
    prompt="Analyze this codebase",
    options=ClaudeAgentOptions(
        # Include AskUserQuestion in your tools list
        tools=["Read", "Glob", "Grep", "AskUserQuestion"],
        can_use_tool=can_use_tool,
    ),
):
    print(message)
```

2

Detect AskUserQuestion

In your callback, check if `toolName` equals `AskUserQuestion` to handle it differently from other tools:

Python

TypeScript

```
async def can_use_tool(tool_name: str, input_data: dict, context):
    if tool_name == "AskUserQuestion":
        # Your implementation to collect answers from the user
        return await handle_clarifying_questions(input_data)
    # Handle other tools normally
    return await prompt_for_approval(tool_name, input_data)
```

3

Parse the question input

The input contains Claude’s questions in a `questions` array. Each question has a `question` (the text to display), `options` (the choices), and `multiSelect` (whether multiple selections are allowed):

```
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview" },
        { "label": "Detailed", "description": "Full explanation" }
      ],
      "multiSelect": false
    },
    {
      "question": "Which sections should I include?",
      "header": "Sections",
      "options": [
        { "label": "Introduction", "description": "Opening context" },
        { "label": "Conclusion", "description": "Final summary" }
      ],
      "multiSelect": true
    }
  ]
}
```

See [Question format](#question-format) for full field descriptions.

4

Collect answers from the user

Present the questions to the user and collect their selections. How you do this depends on your application: a terminal prompt, a web form, a mobile dialog, etc.

5

Return answers to Claude

Build the `answers` object as a record where each key is the `question` text and each value is the selected option’s `label`:

| From the question object | Use as |
| --- | --- |
| `question` field (e.g., `"How should I format the output?"`) | Key |
| Selected option’s `label` field (e.g., `"Summary"`) | Value |

For multi-select questions, pass an array of labels or join them with `", "`. If you [support free-text input](#support-free-text-input), use the user’s custom text as the value.

Python

TypeScript

```
return PermissionResultAllow(
    updated_input={
        "questions": input_data.get("questions", []),
        "answers": {
            "How should I format the output?": "Summary",
            "Which sections should I include?": ["Introduction", "Conclusion"],
        },
    }
)
```

### [​](#question-format) Question format

The input contains Claude’s generated questions in a `questions` array. Each question has these fields:

| Field | Description |
| --- | --- |
| `question` | The full question text to display |
| `header` | Short label for the question (max 12 characters) |
| `options` | Array of 2-4 choices, each with `label` and `description`. TypeScript: optionally `preview` (see [below](#option-previews-typescript)) |
| `multiSelect` | If `true`, users can select multiple options |

The structure your callback receives:

```
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview of key points" },
        { "label": "Detailed", "description": "Full explanation with examples" }
      ],
      "multiSelect": false
    }
  ]
}
```

#### [​](#option-previews-typescript) Option previews (TypeScript)

`toolConfig.askUserQuestion.previewFormat` adds a `preview` field to each option so your app can show a visual mockup alongside the label. Without this setting, Claude does not generate previews and the field is absent.

| `previewFormat` | `preview` contains |
| --- | --- |
| unset (default) | Field is absent. Claude does not generate previews. |
| `"markdown"` | ASCII art and fenced code blocks |
| `"html"` | A styled `<div>` fragment (the SDK rejects `<script>`, `<style>`, and `<!DOCTYPE>` before your callback runs) |

The format applies to all questions in the session. Claude includes `preview` on options where a visual comparison helps (layout choices, color schemes) and omits it where one wouldn’t (yes/no confirmations, text-only choices). Check for `undefined` before rendering.

```
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Help me choose a card layout",
  options: {
    toolConfig: {
      askUserQuestion: { previewFormat: "html" }
    },
    canUseTool: async (toolName, input) => {
      // input.questions[].options[].preview is an HTML string or undefined
      return { behavior: "allow", updatedInput: input };
    }
  }
})) {
  // ...
}
```

An option with an HTML preview:

```
{
  "label": "Compact",
  "description": "Title and metric value only",
  "preview": "<div style=\"padding:12px;border:1px solid #ddd;border-radius:8px\"><div style=\"font-size:12px;color:#666\">Active users</div><div style=\"font-size:28px;font-weight:600\">1,284</div></div>"
}
```

### [​](#response-format) Response format

Return an `answers` object mapping each question’s `question` field to the selected option’s `label`:

| Field | Description |
| --- | --- |
| `questions` | Pass through the original questions array (required for tool processing) |
| `answers` | Object where keys are question text and values are selected labels |
| `response` | Optional freeform reply the user typed instead of answering the structured questions |

For multi-select questions, pass an array of labels or join them with `", "`. For per-question free text such as an “Other” option, put the user’s text in `answers[question]` as shown in [Support free-text input](#support-free-text-input). Set `response` only when your UI lets the user dismiss the question card and type a general reply that isn’t an answer to any specific question. When `response` is set, Claude receives “The user responded: …” instead of the per-question answer list.

```
{
  "questions": [
    // ...
  ],
  "answers": {
    "How should I format the output?": "Summary",
    "Which sections should I include?": ["Introduction", "Conclusion"]
  }
}
```

#### [​](#support-free-text-input) Support free-text input

Claude’s predefined options won’t always cover what users want. To let users type their own answer:

* Display an additional “Other” choice after Claude’s options that accepts text input
* Use the user’s custom text as the answer value (not the word “Other”)

See the [complete example](#complete-example) below for a full implementation.

### [​](#complete-example) Complete example

Claude asks clarifying questions when it needs user input to proceed. For example, when asked to help decide on a tech stack for a mobile app, Claude might ask about cross-platform vs native, backend preferences, or target platforms. These questions help Claude make decisions that match the user’s preferences rather than guessing.
This example handles those questions in a terminal application. Here’s what happens at each step:

1. **Route the request**: The `canUseTool` callback checks if the tool name is `"AskUserQuestion"` and routes to a dedicated handler
2. **Display questions**: The handler loops through the `questions` array and prints each question with numbered options
3. **Collect input**: The user can enter a number to select an option, or type free text directly (e.g., “jquery”, “i don’t know”)
4. **Map answers**: The code checks if input is numeric (uses the option’s label) or free text (uses the text directly)
5. **Return to Claude**: The response includes both the original `questions` array and the `answers` mapping

Python

TypeScript

```
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from claude_agent_sdk.types import HookMatcher, PermissionResultAllow


def parse_response(response: str, options: list) -> str:
    """Parse user input as option number(s) or free text."""
    try:
        indices = [int(s.strip()) - 1 for s in response.split(",")]
        labels = [options[i]["label"] for i in indices if 0 <= i < len(options)]
        return ", ".join(labels) if labels else response
    except ValueError:
        return response


async def handle_ask_user_question(input_data: dict) -> PermissionResultAllow:
    """Display Claude's questions and collect user answers."""
    answers = {}

    for q in input_data.get("questions", []):
        print(f"\n{q['header']}: {q['question']}")

        options = q["options"]
        for i, opt in enumerate(options):
            print(f"  {i + 1}. {opt['label']} - {opt['description']}")
        if q.get("multiSelect"):
            print("  (Enter numbers separated by commas, or type your own answer)")
        else:
            print("  (Enter a number, or type your own answer)")

        response = input("Your choice: ").strip()
        answers[q["question"]] = parse_response(response, options)

    return PermissionResultAllow(
        updated_input={
            "questions": input_data.get("questions", []),
            "answers": answers,
        }
    )


async def can_use_tool(
    tool_name: str, input_data: dict, context
) -> PermissionResultAllow:
    # Route AskUserQuestion to our question handler
    if tool_name == "AskUserQuestion":
        return await handle_ask_user_question(input_data)
    # Auto-approve other tools for this example
    return PermissionResultAllow(updated_input=input_data)


async def prompt_stream():
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Help me decide on the tech stack for a new mobile app",
        },
    }