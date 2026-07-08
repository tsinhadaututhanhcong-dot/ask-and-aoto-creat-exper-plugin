---
type: Reference
title: Migrate to Claude Agent SDK - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Migrate to Claude Agent SDK - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/agent-sdk/migration-guide](https://code.claude.com/docs/en/agent-sdk/migration-guide)

## [​](#overview) Overview

The Claude Code SDK has been renamed to the **Claude Agent SDK** and its documentation has been reorganized. This change reflects the SDK’s broader capabilities for building AI agents beyond just coding tasks.

## [​](#what’s-changed) What’s Changed

| Aspect | Old | New |
| --- | --- | --- |
| **Package Name (TS/JS)** | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| **Python Package** | `claude-code-sdk` | `claude-agent-sdk` |
| **Documentation Location** | Claude Code docs | API Guide → Agent SDK section |

**Documentation Changes:** The Agent SDK documentation has moved from the Claude Code docs to the API Guide under a dedicated [Agent SDK](/docs/en/agent-sdk/overview) section. The Claude Code docs now focus on the CLI tool and automation features.

## [​](#migration-steps) Migration Steps

### [​](#for-typescript/javascript-projects) For TypeScript/JavaScript Projects

**1. Uninstall the old package:**

```
npm uninstall @anthropic-ai/claude-code
```

**2. Install the new package:**

```
npm install @anthropic-ai/claude-agent-sdk
```

**3. Update your imports:**
Change all imports from `@anthropic-ai/claude-code` to `@anthropic-ai/claude-agent-sdk`:

```
// Before
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";

// After
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
```

**4. Update package.json dependencies:**
If you have the package listed in your `package.json`, update it:
Before:

```
{
  "dependencies": {
    "@anthropic-ai/claude-code": "^0.0.42"
  }
}
```

After:

```
{
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.2.0"
  }
}
```

**5. Review [breaking changes](#breaking-changes)**
Make any code changes needed to complete the migration.

### [​](#for-python-projects) For Python Projects

**1. Uninstall the old package:**

```
pip uninstall claude-code-sdk
```

**2. Install the new package:**

```
pip install claude-agent-sdk
```

**3. Update your imports:**
Change all imports from `claude_code_sdk` to `claude_agent_sdk`:

```