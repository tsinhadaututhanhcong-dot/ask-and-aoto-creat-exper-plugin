---
title: Configure LLM gateway (Google Vertex AI)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: enterprise-provider
---

# Configure LLM gateway (Google Vertex AI)
```bash
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configure LLM gateway
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLOUD_ML_REGION=us-east5
```
