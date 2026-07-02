---
title: Monitoring - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Monitoring - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)

Track Claude Code usage, costs, and tool activity across your organization by exporting telemetry data through OpenTelemetry (OTel). Claude Code exports metrics as time series data via the standard metrics protocol, events via the logs/events protocol, and optionally distributed traces via the [traces protocol](#traces-beta). Configure your metrics, logs, and traces backends to match your monitoring requirements.

## [​](#quick-start) Quick start

Configure OpenTelemetry using environment variables:

```