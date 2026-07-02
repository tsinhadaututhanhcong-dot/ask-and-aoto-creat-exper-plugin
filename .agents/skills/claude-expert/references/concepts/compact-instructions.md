---
title: Compact instructions
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Compact instructions

When you are using compact, please focus on test output and code changes
```

### [​](#choose-the-right-model) Choose the right model

Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. Use `/model` to switch models mid-session, or set a default in `/config`. For simple subagent tasks, specify `model: haiku` in your [subagent configuration](/docs/en/sub-agents#choose-a-model).

### [​](#reduce-mcp-server-overhead) Reduce MCP server overhead

MCP tool definitions are [deferred by default](/docs/en/mcp#scale-with-mcp-tool-search), so only tool names enter context until Claude uses a specific tool. Run `/context` to see what’s consuming space.

* **Prefer CLI tools when available**: Tools like `gh`, `aws`, `gcloud`, and `sentry-cli` are still more context-efficient than MCP servers because they don’t add any per-tool listing. Claude can run CLI commands directly.
* **Disable unused servers**: Run `/mcp` to see configured servers and disable any you’re not actively using.

### [​](#install-code-intelligence-plugins-for-typed-languages) Install code intelligence plugins for typed languages

[Code intelligence plugins](/docs/en/discover-plugins#code-intelligence) give Claude precise symbol navigation instead of text-based search, reducing unnecessary file reads when exploring unfamiliar code. A single “go to definition” call replaces what might otherwise be a grep followed by reading multiple candidate files. Installed language servers also report type errors automatically after edits, so Claude catches mistakes without running a compiler.

### [​](#offload-processing-to-hooks-and-skills) Offload processing to hooks and skills

Custom [hooks](/docs/en/hooks) can preprocess data before Claude sees it. Instead of Claude reading a 10,000-line log file to find errors, a hook can grep for `ERROR` and return only matching lines, reducing context from tens of thousands of tokens to hundreds.
A [skill](/docs/en/skills) can give Claude domain knowledge so it doesn’t have to explore. For example, a “codebase-overview” skill could describe your project’s architecture, key directories, and naming conventions. When Claude invokes the skill, it gets this context immediately instead of spending tokens reading multiple files to understand the structure.
For example, this PreToolUse hook filters test output to show only failures:

* settings.json
* filter-test-output.sh

Add this to your [settings.json](/docs/en/settings#settings-files) to run the hook before every Bash command:

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/filter-test-output.sh"
          }
        ]
      }
    ]
  }
}
```

The hook calls this script, which checks if the command is a test runner and modifies it to show only failures:

```
#!/bin/bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')