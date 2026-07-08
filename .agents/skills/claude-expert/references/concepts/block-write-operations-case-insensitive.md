---
type: Reference
title: Block write operations (case-insensitive)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

On macOS and Linux, make the script executable:

```
chmod +x ./scripts/validate-readonly-query.sh
```

On Windows, write the validation script in PowerShell and add `shell: powershell` to the hook entry. See [running hooks in PowerShell](/docs/en/hooks#windows-powershell-tool).
The hook receives JSON via stdin with the Bash command in `tool_input.command`. Exit code 2 blocks the operation and feeds the error message back to Claude. See [Hooks](/docs/en/hooks#exit-code-output) for details on exit codes and [Hook input](/docs/en/hooks#pretooluse-input) for the complete input schema.

## [​](#next-steps) Next steps

Now that you understand subagents, explore these related features:

* [Distribute subagents with plugins](/docs/en/plugins) to share subagents across teams or projects
* [Run Claude Code programmatically](/docs/en/headless) with the Agent SDK for CI/CD and automation
* [Use MCP servers](/docs/en/mcp) to give subagents access to external tools and data

Was this page helpful?

YesNo

[Overview](/docs/en/agents)[Agent view](/docs/en/agent-view)

⌘I

---