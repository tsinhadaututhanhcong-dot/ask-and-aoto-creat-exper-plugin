---
type: Reference
title: Add a user server
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Add a user server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### [​](#scope-hierarchy-and-precedence) Scope hierarchy and precedence

When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source. The entire server entry from that source is used; fields are not merged across scopes.

1. Local scope
2. Project scope
3. User scope
4. [Plugin-provided servers](/docs/en/plugins)
5. [claude.ai connectors](#use-mcp-servers-from-claude-ai)

The three scopes match duplicates by name. Plugins and connectors match by endpoint, so one that points at the same URL or command as a server above is treated as a duplicate.

### [​](#environment-variable-expansion-in-mcp-json) Environment variable expansion in `.mcp.json`

Claude Code supports environment variable expansion in `.mcp.json` files, allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys.
**Supported syntax:**

* `${VAR}`: expands to the value of environment variable `VAR`
* `${VAR:-default}`: expands to `VAR` if set, otherwise uses `default`

**Expansion locations:**
Environment variables can be expanded in:

* `command`: the server executable path
* `args`: command-line arguments
* `env`: environment variables passed to the server
* `url`: for HTTP server types
* `headers`: for HTTP server authentication

**Example with variable expansion:**

```
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

If a required environment variable isn’t set and has no default value, Claude Code fails to parse the config.

## [​](#practical-examples) Practical examples

### [​](#example-monitor-errors-with-sentry) Example: Monitor errors with Sentry

```
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Authenticate with your Sentry account:

```
/mcp
```

Then debug production issues:

```
What are the most common errors in the last 24 hours?
```

```
Show me the stack trace for error ID abc123
```

```
Which deployment introduced these new errors?
```

### [​](#example-connect-to-github-for-code-reviews) Example: Connect to GitHub for code reviews

GitHub’s remote MCP server authenticates with a GitHub personal access token passed as a header. To get one, open your [GitHub token settings](https://github.com/settings/personal-access-tokens), generate a new fine-grained token with access to the repositories you want Claude to work with, then add the server:

```
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Then work with GitHub:

```
Review PR #456 and suggest improvements
```

```
Create a new issue for the bug we just found
```

```
Show me all open PRs assigned to me
```

### [​](#example-query-your-postgresql-database) Example: Query your PostgreSQL database

```
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Then query your database naturally:

```
What's our total revenue this month?
```

```
Show me the schema for the orders table
```

```
Find customers who haven't made a purchase in 90 days
```

## [​](#authenticate-with-remote-mcp-servers) Authenticate with remote MCP servers

Many cloud-based MCP servers require authentication. Claude Code supports OAuth 2.0 for secure connections.
Claude Code marks a remote server as needing authentication when the server responds with `401 Unauthorized` or `403 Forbidden`. Either status code flags the server in `/mcp` so you can complete the OAuth flow. A custom server that returns a `WWW-Authenticate` header pointing to its authorization server gets the same automatic discovery as any other remote server.
If you configured `headers.Authorization` for the server and the server rejects that header, Claude Code reports the connection as failed instead of falling back to OAuth. Check that the token is valid for the MCP endpoint, or remove the header to use the OAuth flow.

1

Add the server that requires authentication

For example:

```
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

2

Use the /mcp command within Claude Code

In Claude Code, use the command:

```
/mcp
```

Then follow the steps in your browser to log in.

Tips:

* Authentication tokens are stored securely and refreshed automatically
* Use “Clear authentication” in the `/mcp` menu to revoke access
* If your browser doesn’t open automatically, copy the provided URL and open it manually
* If the browser redirect fails with a connection error after authenticating, paste the full callback URL from your browser’s address bar into the URL prompt that appears in Claude Code
* OAuth authentication works with HTTP servers

### [​](#authenticate-from-the-command-line) Authenticate from the command line

From v2.1.186, `claude mcp login <name>` runs a configured server’s OAuth flow directly from your shell, so you don’t need to open the `/mcp` panel inside a session.

```
claude mcp login sentry
```

To clear stored credentials later, run `claude mcp logout <name>`.
As of v2.1.191, the command detects when no local browser is available, such as during an SSH session or on Linux without a display server, and prints the authorization URL instead of trying to open a browser. Open the URL on your local machine, then paste the full redirect URL from your browser’s address bar back at the prompt. The command needs an interactive terminal for the paste step, so connect with `ssh -t`. Pass `--no-browser` to force the URL prompt even when a local browser is detected.

```
claude mcp login sentry --no-browser
```

### [​](#use-a-fixed-oauth-callback-port) Use a fixed OAuth callback port

Some MCP servers require a specific redirect URI registered in advance. By default, Claude Code picks a random available port for the OAuth callback. Use `--callback-port` to fix the port so it matches a pre-registered redirect URI of the form `http://localhost:PORT/callback`.
You can use `--callback-port` on its own (with dynamic client registration) or together with `--client-id` (with pre-configured credentials).

```