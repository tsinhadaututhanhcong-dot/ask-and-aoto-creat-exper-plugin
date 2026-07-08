---
type: Reference
title: 5. For debugging: reduce export intervals
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# 5. For debugging: reduce export intervals
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)