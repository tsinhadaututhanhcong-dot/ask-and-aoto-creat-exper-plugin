---
type: Reference
title: Required: dummy hook keeps the stream open for can_use_tool
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Required: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}


async def prompt_stream():
    yield {
        "type": "user",
        "message": {"role": "user", "content": "Deploy my application"},
    }


async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            sandbox={
                "enabled": True,
                "allowUnsandboxedCommands": True,  # Model can request unsandboxed execution
            },
            permission_mode="default",
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        print(message)
```

This pattern enables you to:

* **Audit model requests**: Log when the model requests unsandboxed execution
* **Implement allowlists**: Only permit specific commands to run unsandboxed
* **Add approval workflows**: Require explicit authorization for privileged operations

Commands running with `dangerouslyDisableSandbox: True` have full system access. Ensure your `can_use_tool` handler validates these requests carefully.If `permission_mode` is set to `bypassPermissions` and `allow_unsandboxed_commands` is enabled, the model can autonomously execute commands outside the sandbox without approval prompts (an explicit [`ask` rule](/docs/en/agent-sdk/permissions#how-permissions-are-evaluated) still forces one). This combination effectively allows the model to escape sandbox isolation silently.

## [​](#see-also) See also

* [SDK overview](/docs/en/agent-sdk/overview) - General SDK concepts
* [TypeScript SDK reference](/docs/en/agent-sdk/typescript) - TypeScript SDK documentation
* [CLI reference](/docs/en/cli-reference) - Command-line interface
* [Common workflows](/docs/en/common-workflows) - Step-by-step guides

Was this page helpful?

YesNo

[TypeScript V2 (removed)](/docs/en/agent-sdk/typescript-v2-preview)[Migration Guide](/docs/en/agent-sdk/migration-guide)

⌘I

---