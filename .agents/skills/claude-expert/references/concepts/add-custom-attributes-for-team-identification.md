---
title: Add custom attributes for team identification
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Add custom attributes for team identification
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

These custom attributes are included in all metrics and events, allowing you to:

* Filter metrics by team or department
* Track costs per cost center
* Create team-specific dashboards
* Set up alerts for specific teams

Claude Code attaches these values as attributes on every metric datapoint and event record, in addition to sending them in the OTLP resource block. Because most metrics backends expose datapoint attributes as queryable labels, you can group and filter metrics by your custom keys directly. Custom keys never override the [standard attributes](#standard-attributes) such as `user.id` or `session.id`: when a key collides, Claude Code keeps the built-in value.
Each custom key becomes a label on every metric series, so high-cardinality values increase storage cost in your metrics backend. To send custom attributes in the resource block only and omit them from datapoint labels, set `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES=false`. See [Metrics cardinality control](#metrics-cardinality-control).

The `OTEL_RESOURCE_ATTRIBUTES` environment variable uses comma-separated key=value pairs with strict formatting requirements:

* **No spaces allowed**: values can’t contain spaces. For example, `user.organizationName=My Company` is invalid
* **Format**: must be comma-separated key=value pairs: `key1=value1,key2=value2`
* **Allowed characters**: only US-ASCII characters excluding control characters, whitespace, double quotes, commas, semicolons, and backslashes
* **Special characters**: characters outside the allowed range must be percent-encoded

For a value that would need a space, use underscores or camelCase instead. The following examples set `org.name` with each form:

```
export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"
```

You can percent-encode any character, not only the excluded ones. This example encodes both the space and the apostrophe:

```
export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
```

Wrapping values in quotes doesn’t escape spaces. For example, `org.name="My Company"` results in the literal value `"My Company"` with the quotes included, not `My Company`.

### [​](#example-configurations) Example configurations

Set these environment variables before running `claude`. Each block shows a complete configuration for a different exporter or deployment scenario:

```