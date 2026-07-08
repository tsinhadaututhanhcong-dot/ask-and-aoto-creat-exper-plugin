---
type: Reference
title: Only run tests for source files
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi