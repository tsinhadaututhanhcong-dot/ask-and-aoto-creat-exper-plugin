---
type: Reference
title: Connect Claude Code to tools via MCP - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Connect Claude Code to tools via MCP - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)

Claude Code can connect to hundreds of external tools and data sources through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.
Connect a server when you find yourself copying data into chat from another tool, like an issue tracker or a monitoring dashboard. Once connected, Claude can read and act on that system directly instead of working from what you paste.
If you’re connecting your first server, start with the [MCP quickstart](/docs/en/mcp-quickstart) for a step-by-step walkthrough. This page is the full reference.

## [​](#what-you-can-do-with-mcp) What you can do with MCP

With MCP servers connected, you can ask Claude Code to:

* **Implement features from issue trackers**: “Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub.”
* **Analyze monitoring data**: “Check Sentry and Statsig to check the usage of the feature described in ENG-4521.”
* **Query databases**: “Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database.”
* **Integrate designs**: “Update our standard email template based on the new Figma designs that were posted in Slack”
* **Automate workflows**: “Create Gmail drafts inviting these 10 users to a feedback session about the new feature.”
* **React to external events**: an MCP server can also act as a [channel](/docs/en/channels) that pushes messages into your session, so Claude reacts to Telegram messages, Discord chats, or webhook events while you’re away.

## [​](#find-and-build-mcp-servers) Find and build MCP servers

Browse reviewed connectors in the [Anthropic Directory](https://claude.ai/directory). Directory connectors use the same MCP infrastructure as Claude Code, so you can add any remote server listed there with `claude mcp add`.

Verify you trust each server before connecting it. Servers that fetch external content can expose you to [prompt injection risk](/docs/en/security#protect-against-prompt-injection).

To build your own server, see the [MCP server guide](https://modelcontextprotocol.io/docs/develop/build-server) for protocol fundamentals and the [Claude connector building docs](https://claude.com/docs/connectors/building) for authentication, testing, and Directory submission.
You can also have Claude scaffold a server for you with the official [`mcp-server-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev).

1

Install the plugin

In a Claude Code session, run:

```
/plugin install mcp-server-dev@claude-plugins-official
```

If Claude Code reports that the marketplace is not found, run `/plugin marketplace add anthropics/claude-plugins-official` first, then retry the install. Once installed, run `/reload-plugins` to activate it in the current session.

2

Run the build skill

```
/mcp-server-dev:build-mcp-server
```

Claude asks about your use case and scaffolds a remote HTTP or local stdio server.

## [​](#installing-mcp-servers) Installing MCP servers

MCP servers can be configured in several ways depending on your needs:

### [​](#option-1-add-a-remote-http-server) Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers. This is the most widely supported transport for cloud-based services.

```