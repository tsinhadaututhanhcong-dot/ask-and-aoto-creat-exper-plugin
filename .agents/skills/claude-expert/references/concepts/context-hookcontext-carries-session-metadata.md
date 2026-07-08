---
type: Reference
title: context: HookContext, carries session metadata
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

#   context: HookContext, carries session metadata
async def audit_bash(input_data, tool_use_id, context):
    command = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf" in command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Destructive command blocked",
            }
        }
    return {}  # Empty dict: allow the tool to proceed