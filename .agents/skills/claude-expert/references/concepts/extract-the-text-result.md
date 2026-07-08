---
type: Reference
title: Extract the text result
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Extract the text result
claude -p "Summarize this project" --output-format json | jq -r '.result'