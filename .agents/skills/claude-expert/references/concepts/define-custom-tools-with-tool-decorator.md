---
title: Define custom tools with @tool decorator
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Define custom tools with @tool decorator
@tool("calculate", "Perform mathematical calculations", {"expression": str})
async def calculate(args: dict[str, Any]) -> dict[str, Any]:
    try:
        result = eval(args["expression"], {"__builtins__": {}})
        return {"content": [{"type": "text", "text": f"Result: {result}"}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "is_error": True,
        }


@tool("get_time", "Get current time", {})
async def get_time(args: dict[str, Any]) -> dict[str, Any]:
    from datetime import datetime

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"content": [{"type": "text", "text": f"Current time: {current_time}"}]}


async def main():
    # Create SDK MCP server with custom tools
    my_server = create_sdk_mcp_server(
        name="utilities", version="1.0.0", tools=[calculate, get_time]
    )

    # Configure options with the server
    options = ClaudeAgentOptions(
        mcp_servers={"utils": my_server},
        allowed_tools=["mcp__utils__calculate", "mcp__utils__get_time"],
    )

    # Use ClaudeSDKClient for interactive tool usage
    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's 123 * 456?")

        # Process calculation response
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Calculation: {block.text}")

        # Follow up with time query
        await client.query("What time is it now?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Time: {block.text}")


asyncio.run(main())
```

## [​](#sandbox-configuration) Sandbox Configuration

### [​](#sandboxsettings) `SandboxSettings`

Configuration for sandbox behavior. Use this to enable command sandboxing and configure network restrictions programmatically.

```
class SandboxSettings(TypedDict, total=False):
    enabled: bool
    autoAllowBashIfSandboxed: bool
    excludedCommands: list[str]
    allowUnsandboxedCommands: bool
    network: SandboxNetworkConfig
    ignoreViolations: SandboxIgnoreViolations
    enableWeakerNestedSandbox: bool
```

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `bool` | `False` | Enable sandbox mode for command execution |
| `autoAllowBashIfSandboxed` | `bool` | `True` | Auto-approve bash commands when sandbox is enabled |
| `excludedCommands` | `list[str]` | `[]` | Commands that always bypass sandbox restrictions (e.g., `["docker"]`). These run unsandboxed automatically without model involvement |
| `allowUnsandboxedCommands` | `bool` | `True` | Allow the model to request running commands outside the sandbox. When `True`, the model can set `dangerouslyDisableSandbox` in tool input, which falls back to the [permissions system](#permissions-fallback-for-unsandboxed-commands) |
| `network` | [`SandboxNetworkConfig`](#sandboxnetworkconfig) | `None` | Network-specific sandbox configuration |
| `ignoreViolations` | [`SandboxIgnoreViolations`](#sandboxignoreviolations) | `None` | Configure which sandbox violations to ignore |
| `enableWeakerNestedSandbox` | `bool` | `False` | Enable a weaker nested sandbox for compatibility |

The sandbox depends on platform support and, on Linux, tools like `bubblewrap` and `socat`. By default, when `enabled` is `True` but the sandbox can’t start, commands run unsandboxed with a warning on stderr. This default differs from the TypeScript SDK, where `failIfUnavailable` defaults to `true`.Set `"failIfUnavailable": True` in your sandbox settings to stop instead. The key isn’t declared on `SandboxSettings` yet, but the SDK forwards it to Claude Code, which honors it. `query()` then reports a `ResultMessage` with `subtype="error_during_execution"` and the reason in `errors`. Watch for that subtype rather than expecting `query()` to raise before yielding messages.

#### [​](#example-usage-2) Example usage

```
from claude_agent_sdk import query, ClaudeAgentOptions, SandboxSettings

sandbox_settings: SandboxSettings = {
    "enabled": True,
    "autoAllowBashIfSandboxed": True,
    "network": {"allowLocalBinding": True},
}

async for message in query(
    prompt="Build and test my project",
    options=ClaudeAgentOptions(sandbox=sandbox_settings),
):
    print(message)
```

**Unix socket security**: The `allowUnixSockets` option can grant access to powerful system services. For example, allowing `/var/run/docker.sock` effectively grants full host system access through the Docker API, bypassing sandbox isolation. Only allow Unix sockets that are strictly necessary and understand the security implications of each.

### [​](#sandboxnetworkconfig) `SandboxNetworkConfig`

Network-specific configuration for sandbox mode. These settings apply to sandboxed Bash commands when `enabled` is `True` in the parent [`SandboxSettings`](#sandboxsettings). They do not restrict the WebFetch tool, which uses [permission rules](/docs/en/permissions#webfetch) instead.

```
class SandboxNetworkConfig(TypedDict, total=False):
    allowedDomains: list[str]
    deniedDomains: list[str]
    allowManagedDomainsOnly: bool
    allowUnixSockets: list[str]
    allowAllUnixSockets: bool
    allowLocalBinding: bool
    allowMachLookup: list[str]
    httpProxyPort: int
    socksProxyPort: int
```

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `allowedDomains` | `list[str]` | `[]` | Domain names that sandboxed processes can access |
| `deniedDomains` | `list[str]` | `[]` | Domain names that sandboxed processes cannot access. Takes precedence over `allowedDomains` |
| `allowManagedDomainsOnly` | `bool` | `False` | Managed-settings only: when set in managed settings, ignore `allowedDomains` from non-managed settings sources. Has no effect when set via SDK options |
| `allowUnixSockets` | `list[str]` | `[]` | Unix socket paths that processes can access (e.g., Docker socket) |
| `allowAllUnixSockets` | `bool` | `False` | Allow access to all Unix sockets |
| `allowLocalBinding` | `bool` | `False` | Allow processes to bind to local ports (e.g., for dev servers) |
| `allowMachLookup` | `list[str]` | `[]` | macOS only: XPC/Mach service names to allow. Supports a trailing wildcard |
| `httpProxyPort` | `int` | `None` | HTTP proxy port for network requests |
| `socksProxyPort` | `int` | `None` | SOCKS proxy port for network requests |

The built-in sandbox proxy enforces the network allowlist based on the requested hostname and does not terminate or inspect TLS traffic, so techniques such as [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) can potentially bypass it. See [Sandboxing security limitations](/docs/en/sandboxing#security-limitations) for details and [Secure deployment](/docs/en/agent-sdk/secure-deployment#traffic-forwarding) for configuring a TLS-terminating proxy.

### [​](#sandboxignoreviolations) `SandboxIgnoreViolations`

Configuration for ignoring specific sandbox violations.

```
class SandboxIgnoreViolations(TypedDict, total=False):
    file: list[str]
    network: list[str]
```

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `file` | `list[str]` | `[]` | File path patterns to ignore violations for |
| `network` | `list[str]` | `[]` | Network patterns to ignore violations for |

### [​](#permissions-fallback-for-unsandboxed-commands) Permissions Fallback for Unsandboxed Commands

When `allowUnsandboxedCommands` is enabled, the model can request to run commands outside the sandbox by setting `dangerouslyDisableSandbox: True` in the tool input. These requests fall back to the existing permissions system, meaning your `can_use_tool` handler will be invoked, allowing you to implement custom authorization logic.

**`excludedCommands` vs `allowUnsandboxedCommands`:**

* `excludedCommands`: A static list of commands that always bypass the sandbox automatically (e.g., `["docker"]`). The model has no control over this.
* `allowUnsandboxedCommands`: Lets the model decide at runtime whether to request unsandboxed execution by setting `dangerouslyDisableSandbox: True` in the tool input.

```
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


async def can_use_tool(
    tool: str, input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Check if the model is requesting to bypass the sandbox
    if tool == "Bash" and input.get("dangerouslyDisableSandbox"):
        # The model is requesting to run this command outside the sandbox
        print(f"Unsandboxed command requested: {input.get('command')}")

        if is_command_authorized(input.get("command")):
            return PermissionResultAllow()
        return PermissionResultDeny(
            message="Command not authorized for unsandboxed execution"
        )
    return PermissionResultAllow()