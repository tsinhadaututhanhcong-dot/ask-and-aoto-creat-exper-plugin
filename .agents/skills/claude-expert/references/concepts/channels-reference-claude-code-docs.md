---
title: Channels reference - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Channels reference - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/channels-reference](https://code.claude.com/docs/en/channels-reference)

Channels are in [research preview](/docs/en/channels#research-preview) and require Claude Code v2.1.80 or later. Team and Enterprise organizations must [explicitly enable them](/docs/en/channels#enterprise-controls).

A channel is an MCP server that pushes events into a Claude Code session so Claude can react to things happening outside the terminal.
You can build a one-way or two-way channel. One-way channels forward alerts, webhooks, or monitoring events for Claude to act on. Two-way channels like chat bridges also [expose a reply tool](#expose-a-reply-tool) so Claude can send messages back. A channel with a trusted sender path can also opt in to [relay permission prompts](#relay-permission-prompts) so you can approve or deny tool use remotely.
This page covers:

* [Overview](#overview): how channels work
* [What you need](#what-you-need): requirements and general steps
* [Example: build a webhook receiver](#example-build-a-webhook-receiver): a minimal one-way walkthrough
* [Server options](#server-options): the constructor fields
* [Notification format](#notification-format): the event payload and delivery behavior
* [Expose a reply tool](#expose-a-reply-tool): let Claude send messages back
* [Gate inbound messages](#gate-inbound-messages): sender checks to prevent prompt injection
* [Relay permission prompts](#relay-permission-prompts): forward tool approval prompts to remote channels

To use an existing channel instead of building one, see [Channels](/docs/en/channels). Telegram, Discord, iMessage, and fakechat are included in the research preview.

## [​](#overview) Overview

A channel is an [MCP](https://modelcontextprotocol.io) server that runs on the same machine as Claude Code. Claude Code spawns it as a subprocess and communicates over stdio. Your channel server is the bridge between external systems and the Claude Code session:

* **Chat platforms** (Telegram, Discord): your plugin runs locally and polls the platform’s API for new messages. When someone DMs your bot, the plugin receives the message and forwards it to Claude. No URL to expose.
* **Webhooks** (CI, monitoring): your server listens on a local HTTP port. External systems POST to that port, and your server pushes the payload to Claude.

![Architecture diagram showing external systems connecting to your local channel server, which communicates with Claude Code over stdio](https://mintcdn.com/claude-code/zbUxPYi8065L3Y_P/en/images/channel-architecture.svg?fit=max&auto=format&n=zbUxPYi8065L3Y_P&q=85&s=fd6b6b949eab38264043d2a96285a57c)

## [​](#what-you-need) What you need

The only hard requirement is the [`@modelcontextprotocol/sdk`](https://www.npmjs.com/package/@modelcontextprotocol/sdk) package and a Node.js-compatible runtime. [Bun](https://bun.sh), [Node](https://nodejs.org), and [Deno](https://deno.com) all work. The pre-built plugins in the research preview use Bun, but your channel doesn’t have to.
Your server needs to:

1. Declare the `claude/channel` capability so Claude Code registers a notification listener
2. Emit `notifications/claude/channel` events when something happens
3. Connect over [stdio transport](https://modelcontextprotocol.io/docs/concepts/transports#standard-io) (Claude Code spawns your server as a subprocess)

The [Server options](#server-options) and [Notification format](#notification-format) sections cover each of these in detail. See [Example: build a webhook receiver](#example-build-a-webhook-receiver) for a full walkthrough.
During the research preview, custom channels aren’t on the [approved allowlist](/docs/en/channels#supported-channels). Use `--dangerously-load-development-channels` to test locally. See [Test during the research preview](#test-during-the-research-preview) for details.

## [​](#example-build-a-webhook-receiver) Example: build a webhook receiver

This walkthrough builds a single-file server that listens for HTTP requests and forwards them into your Claude Code session. By the end, anything that can send an HTTP POST, like a CI pipeline, a monitoring alert, or a `curl` command, can push events to Claude.
This example uses [Bun](https://bun.sh) as the runtime for its built-in HTTP server and TypeScript support. You can use [Node](https://nodejs.org) or [Deno](https://deno.com) instead; the only requirement is the [MCP SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk).

1

Create the project

Create a new directory and install the MCP SDK:

```
mkdir webhook-channel && cd webhook-channel
bun add @modelcontextprotocol/sdk
```

2

Write the channel server

Create a file called `webhook.ts`. This is your entire channel server: it connects to Claude Code over stdio, and it listens for HTTP POSTs on port 8788. When a request arrives, it pushes the body to Claude as a channel event.

webhook.ts

```
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

// Create the MCP server and declare it as a channel
const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    // this key is what makes it a channel — Claude Code registers a listener for it
    capabilities: { experimental: { 'claude/channel': {} } },
    // added to Claude's system prompt so it knows how to handle these events
    instructions: 'Events from the webhook channel arrive as <channel source="webhook" ...>. They are one-way: read them and act, no reply expected.',
  },
)

// Connect to Claude Code over stdio (Claude Code spawns this process)
await mcp.connect(new StdioServerTransport())

// Start an HTTP server that forwards every POST to Claude
Bun.serve({
  port: 8788,  // any open port works
  // localhost-only: nothing outside this machine can POST
  hostname: '127.0.0.1',
  async fetch(req) {
    const body = await req.text()
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: {
        content: body,  // becomes the body of the <channel> tag
        // each key becomes a tag attribute, e.g. <channel path="/" method="POST">
        meta: { path: new URL(req.url).pathname, method: req.method },
      },
    })
    return new Response('ok')
  },
})
```

The file does three things in order:

* **Server configuration**: creates the MCP server with `claude/channel` in its capabilities, which is what tells Claude Code this is a channel. The [`instructions`](#server-options) string goes into Claude’s system prompt: tell Claude what events to expect, whether to reply, and how to route replies if it should.
* **Stdio connection**: connects to Claude Code over stdin/stdout. This is standard for any [MCP server](https://modelcontextprotocol.io/docs/concepts/transports#standard-io): Claude Code spawns it as a subprocess.
* **HTTP listener**: starts a local web server on port 8788. Every POST body gets forwarded to Claude as a channel event via `mcp.notification()`. The `content` becomes the event body, and each `meta` entry becomes an attribute on the `<channel>` tag. The listener needs access to the `mcp` instance, so it runs in the same process. You could split it into separate modules for a larger project.

3

Register your server with Claude Code

Add the server to your MCP config so Claude Code knows how to start it. For a project-level `.mcp.json` in the same directory, use a relative path. For user-level config in `~/.claude.json`, use the full absolute path so the server can be found from any project:

.mcp.json

```
{
  "mcpServers": {
    "webhook": { "command": "bun", "args": ["./webhook.ts"] }
  }
}
```

Claude Code reads your MCP config at startup and spawns each server as a subprocess.

4

Test it

During the research preview, custom channels aren’t on the allowlist, so start Claude Code with the development flag:

```
claude --dangerously-load-development-channels server:webhook
```

The first time you start a session in this project, Claude Code asks for consent before using the new server from `.mcp.json`. The dialog reports “New MCP server found in this project: webhook”. Select **Use this MCP server** to continue.When Claude Code starts, it reads your MCP config, spawns your `webhook.ts` as a subprocess, and the HTTP listener starts automatically on the port you configured (8788 in this example). You don’t need to run the server yourself.A dim notice below the startup banner confirms the channel is registered: `Channels (experimental) messages from server:webhook inject directly in this session · restart without --dangerously-load-development-channels to stop`.If you see “blocked by org policy,” your organization admin needs to [enable channels](/docs/en/channels#enterprise-controls) first.In a separate terminal, simulate a webhook by sending an HTTP POST with a message to your server. This example sends a CI failure alert to port 8788 (or whichever port you configured):

```
curl -X POST localhost:8788 -d "build failed on main: https://ci.example.com/run/1234"
```

The payload arrives in your Claude Code session as a `<channel>` tag:

```
<channel source="webhook" path="/" method="POST">build failed on main: https://ci.example.com/run/1234</channel>
```

In your Claude Code terminal, you’ll see Claude receive the message and start responding: reading files, running commands, or whatever the message calls for. This is a one-way channel, so Claude acts in your session but doesn’t send anything back through the webhook. To add replies, see [Expose a reply tool](#expose-a-reply-tool).If the event doesn’t arrive, the diagnosis depends on what `curl` returned:

* **`curl` succeeds but nothing reaches Claude**: run `/mcp` in your session to check the server’s status. “Failed to connect” usually means a dependency or import error in your server file; check the debug log at `~/.claude/debug/<session-id>.txt` for the stderr trace.
* **`curl` fails with “connection refused”**: the port is either not bound yet or a stale process from an earlier run is holding it. `lsof -i :<port>` shows what’s listening; `kill` the stale process before restarting your session.

The [fakechat server](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat) extends this pattern with a web UI, file attachments, and a reply tool for two-way chat.

## [​](#test-during-the-research-preview) Test during the research preview

During the research preview, every channel must be on the [approved allowlist](/docs/en/channels#research-preview) to register. The development flag bypasses the allowlist for specific entries after a confirmation prompt. This example shows both entry types:

```