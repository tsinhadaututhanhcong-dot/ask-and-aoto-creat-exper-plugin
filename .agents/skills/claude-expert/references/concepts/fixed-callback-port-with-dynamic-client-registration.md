---
title: Fixed callback port with dynamic client registration
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Fixed callback port with dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### [​](#use-pre-configured-oauth-credentials) Use pre-configured OAuth credentials

Some MCP servers don’t support automatic OAuth setup via Dynamic Client Registration. If you see an error like “Incompatible auth server: does not support dynamic client registration,” the server requires pre-configured credentials. Claude Code also supports servers that use a Client ID Metadata Document (CIMD) instead of Dynamic Client Registration, and discovers these automatically. If automatic discovery fails, register an OAuth app through the server’s developer portal first, then provide the credentials when adding the server.

1

Register an OAuth app with the server

Create an app through the server’s developer portal and note your client ID and client secret.Many servers also require a redirect URI. If so, choose a port and register a redirect URI in the format `http://localhost:PORT/callback`. Use that same port with `--callback-port` in the next step.

2

Add the server with your credentials

Choose one of the following methods. The port used for `--callback-port` can be any available port. It needs to match the redirect URI you registered in the previous step.

* claude mcp add
* claude mcp add-json
* claude mcp add-json (callback port only)
* CI / env var

Use `--client-id` to pass your app’s client ID. The `--client-secret` flag prompts for the secret with masked input:

```
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

Include the `oauth` object in the JSON config and pass `--client-secret` as a separate flag:

```
claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
  --client-secret
```

Use `--callback-port` without a client ID to fix the port while using dynamic client registration:

```
claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
```

Set the secret via environment variable to skip the interactive prompt:

```
MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

3

Authenticate in Claude Code

Run `/mcp` in Claude Code and follow the browser login flow.

Tips:

* The client secret is stored securely in your system keychain (macOS) or a credentials file, not in your config
* If the server uses a public OAuth client with no secret, use only `--client-id` without `--client-secret`
* `--callback-port` can be used with or without `--client-id`
* These flags only apply to HTTP and SSE transports. They have no effect on stdio servers
* Use `claude mcp get <name>` to verify that OAuth credentials are configured for a server

### [​](#override-oauth-metadata-discovery) Override OAuth metadata discovery

Point Claude Code at a specific OAuth authorization server metadata URL to bypass the default discovery chain. Set `authServerMetadataUrl` when the MCP server’s standard endpoints error, or when you want to route discovery through an internal proxy. By default, Claude Code first checks RFC 9728 Protected Resource Metadata at `/.well-known/oauth-protected-resource`, then falls back to RFC 8414 authorization server metadata at `/.well-known/oauth-authorization-server`.
Set `authServerMetadataUrl` in the `oauth` object of your server’s config in `.mcp.json`:

```
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

The URL must use `https://`. `authServerMetadataUrl` requires Claude Code v2.1.64 or later. The metadata URL’s `scopes_supported` overrides the scopes the upstream server advertises.

### [​](#restrict-oauth-scopes) Restrict OAuth scopes

Set `oauth.scopes` to pin the scopes Claude Code requests during the authorization flow. This is the supported way to restrict an MCP server to a security-team-approved subset when the upstream authorization server advertises more scopes than you want to grant. The value is a single space-separated string, matching the `scope` parameter format in RFC 6749 §3.3.

```
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` takes precedence over both `authServerMetadataUrl` and the scopes the server discovers at `/.well-known`. Leave it unset to let the MCP server determine the requested scope set.
If the authorization server advertises `offline_access` in `scopes_supported`, Claude Code appends it to the pinned scopes so the access token can be refreshed without a new browser sign-in.
If the server later returns a 403 `insufficient_scope` for a tool call, Claude Code re-authenticates with the same pinned scopes. Widen `oauth.scopes` when a tool you need requires a scope outside the pinned set.

### [​](#use-dynamic-headers-for-custom-authentication) Use dynamic headers for custom authentication

If your MCP server uses an authentication scheme other than OAuth, such as Kerberos, short-lived tokens, or an internal SSO, use `headersHelper` to generate request headers at connection time. Claude Code runs the command and merges its output into the connection headers.

```
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

The command can also be inline:

```
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Requirements:**

* The command must write a JSON object of string key-value pairs to stdout
* The command runs in a shell with a 10-second timeout
* Dynamic headers override any static `headers` with the same name

The helper runs fresh on each connection, at session start and on reconnect. There is no caching, so your script is responsible for any token reuse.
Claude Code sets these environment variables when executing the helper:

| Variable | Value |
| --- | --- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | the name of the MCP server |
| `CLAUDE_CODE_MCP_SERVER_URL` | the URL of the MCP server |

Use these to write a single helper script that serves multiple MCP servers.

`headersHelper` executes arbitrary shell commands. When defined at project or local scope, it only runs after you accept the workspace trust dialog.

## [​](#add-mcp-servers-from-json-configuration) Add MCP servers from JSON configuration

If you have a JSON configuration for an MCP server, you can add it directly:

1

Add an MCP server from JSON

```