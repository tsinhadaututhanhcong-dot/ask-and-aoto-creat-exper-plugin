---
title: Enable Microsoft Foundry (corporate proxy tab)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Enable Microsoft Foundry (corporate proxy tab)
```bash
# Enable Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'
```
