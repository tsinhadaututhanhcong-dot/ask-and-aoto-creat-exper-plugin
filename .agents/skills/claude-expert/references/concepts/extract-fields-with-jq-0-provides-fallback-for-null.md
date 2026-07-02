---
title: Extract fields with jq, "// 0" provides fallback for null
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Extract fields with jq, "// 0" provides fallback for null
MODEL=$(echo "$input" | jq -r '.model.display_name')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)