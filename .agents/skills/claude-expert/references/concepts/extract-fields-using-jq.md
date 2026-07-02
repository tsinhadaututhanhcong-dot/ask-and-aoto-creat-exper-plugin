---
title: Extract fields using jq
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Extract fields using jq
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')