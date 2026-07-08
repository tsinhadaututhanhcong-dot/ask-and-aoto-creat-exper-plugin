---
type: Reference
title: Example: Multiple headers
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Example: Multiple headers
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

If the helper fails or prints output that doesn’t meet these requirements, Claude Code reports the error in:

* `/doctor` output
* The debug log, when running with [`--debug`](/docs/en/cli-reference#cli-flags) or after running `/debug` in the session
* stderr, in non-interactive sessions started with `-p`

#### [​](#refresh-behavior) Refresh behavior

The headers helper script runs at startup and periodically thereafter to support token refresh. By default, the script runs every 29 minutes. Customize the interval with the `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` environment variable.

### [​](#multi-team-organization-support) Multi-team organization support

Organizations with multiple teams or departments can add custom attributes to distinguish between different groups using the `OTEL_RESOURCE_ATTRIBUTES` environment variable:

```