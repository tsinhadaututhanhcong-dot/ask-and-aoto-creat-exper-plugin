---
type: Reference
title: Client SDK: You implement the tool loop
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Client SDK: You implement the tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)