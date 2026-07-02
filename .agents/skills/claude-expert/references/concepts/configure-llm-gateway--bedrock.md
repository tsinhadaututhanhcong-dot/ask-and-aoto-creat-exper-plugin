---
title: Configure LLM gateway (Amazon Bedrock)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Configure LLM gateway (Amazon Bedrock)
```bash
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configure LLM gateway
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
```
