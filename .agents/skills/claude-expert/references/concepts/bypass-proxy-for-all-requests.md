---
type: Reference
title: Bypass proxy for all requests
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Bypass proxy for all requests
export NO_PROXY="*"
```

Claude Code does not support SOCKS proxies.

### [​](#basic-authentication) Basic authentication

If your proxy requires basic authentication, include credentials in the proxy URL:

```
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

Avoid hardcoding passwords in scripts. Use environment variables or secure credential storage instead.

For proxies requiring advanced authentication (NTLM, Kerberos, etc.), consider using an LLM Gateway service that supports your authentication method.

## [​](#ca-certificate-store) CA certificate store

By default, Claude Code trusts both its bundled Mozilla CA certificates and your operating system’s certificate store. Enterprise TLS-inspection proxies such as CrowdStrike Falcon and Zscaler work without additional configuration when their root certificate is installed in the OS trust store.
`CLAUDE_CODE_CERT_STORE` accepts a comma-separated list of sources. Recognized values are `bundled` for the Mozilla CA set shipped with Claude Code and `system` for the operating system trust store. The default is `bundled,system`.
To trust only the bundled Mozilla CA set:

```
export CLAUDE_CODE_CERT_STORE=bundled
```

To trust only the OS certificate store:

```
export CLAUDE_CODE_CERT_STORE=system
```

`CLAUDE_CODE_CERT_STORE` has no dedicated `settings.json` schema key. Set it via the `env` block in `~/.claude/settings.json` or directly in the process environment.

## [​](#custom-ca-certificates) Custom CA certificates

If your enterprise environment uses a custom CA, configure Claude Code to trust it directly:

```
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## [​](#mtls-authentication) mTLS authentication

For enterprise environments requiring client certificate authentication:

```