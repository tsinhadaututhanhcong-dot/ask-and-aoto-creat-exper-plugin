---
type: Reference
title: Optional: Passphrase for encrypted private key
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Optional: Passphrase for encrypted private key
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## [​](#network-access-requirements) Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments.

| URL | Required for |
| --- | --- |
| `api.anthropic.com` | Claude API requests |
| `claude.ai` | claude.ai account authentication |
| `platform.claude.com` | Anthropic Console account authentication |
| `downloads.claude.ai` | Plugin executable downloads; native installer and native auto-updater |
| `storage.googleapis.com` | Native installer and native auto-updater on versions prior to 2.1.116 |
| `bridge.claudeusercontent.com` | [Claude in Chrome](/docs/en/chrome) extension WebSocket bridge |
| `*.claudeusercontent.com` | Viewing [artifacts](/docs/en/artifacts) on claude.ai. The viewer loads each artifact’s content from a sandboxed subdomain of this origin. Required in the viewer’s browser, not by the CLI itself |
| `raw.githubusercontent.com` | Changelog feed for [`/release-notes`](/docs/en/commands) and the release notes shown after updating; plugin marketplace install counts |

If you install Claude Code through npm or manage your own binary distribution, end users may not need access to `downloads.claude.ai` or `storage.googleapis.com`.
Claude Code also sends optional operational telemetry by default, which you can disable with environment variables. See [Telemetry services](/docs/en/data-usage#telemetry-services) for how to disable it before finalizing your allowlist.
When using [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Vertex AI](/docs/en/google-vertex-ai), or [Microsoft Foundry](/docs/en/microsoft-foundry), model traffic and authentication go to your provider instead of `api.anthropic.com`, `claude.ai`, or `platform.claude.com`. The WebFetch tool still calls `api.anthropic.com` for its [domain safety check](/docs/en/data-usage#webfetch-domain-safety-check) unless you set `skipWebFetchPreflight: true` in [settings](/docs/en/settings).
[Claude Code on the web](/docs/en/claude-code-on-the-web) and [Code Review](/docs/en/code-review) connect to your repositories from Anthropic-managed infrastructure. If your GitHub Enterprise Cloud organization restricts access by IP address, enable [IP allow list inheritance for installed GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). The Claude GitHub App registers its IP ranges, so enabling this setting allows access without manual configuration. To [add the ranges to your allow list manually](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) instead, or to configure other firewalls, see the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).
For self-hosted [GitHub Enterprise Server](/docs/en/github-enterprise-server) instances behind a firewall, allowlist the same [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses) so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments.

## [​](#additional-resources) Additional resources

* [Claude Code settings](/docs/en/settings)
* [Environment variables reference](/docs/en/env-vars)
* [Troubleshooting guide](/docs/en/troubleshooting)

Was this page helpful?

YesNo

[Microsoft Foundry](/docs/en/microsoft-foundry)[Development containers](/docs/en/devcontainer)

⌘I

---