---
type: Reference
title: Enterprise network configuration - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Enterprise network configuration - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/network-config](https://code.claude.com/docs/en/network-config)

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities (CA), and authenticating with mutual Transport Layer Security (mTLS) certificates for enhanced security.

All environment variables shown on this page can also be configured in [`settings.json`](/docs/en/settings).

## [​](#proxy-configuration) Proxy configuration

### [​](#environment-variables) Environment variables

Claude Code respects standard proxy environment variables:

```