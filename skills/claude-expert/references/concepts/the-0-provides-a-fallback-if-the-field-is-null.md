---
title: The "// 0" provides a fallback if the field is null
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# The "// 0" provides a fallback if the field is null
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)